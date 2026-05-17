import { useState, useEffect, useRef, useCallback } from "react";

const DEFAULT_BEATS = 4;
const AVAILABLE_BEATS = [4, 8, 16, 32];
const DEFAULT_STEPS = DEFAULT_BEATS * 4;
const DEFAULT_BPM = 90;

const TRACKS = [
  { name: "Kick",    color: "#e74c3c", freq: 60,  type: "kick" },
  { name: "Snare",   color: "#e67e22", freq: 200, type: "snare" },
  { name: "Hi-Hat",  color: "#f1c40f", freq: 800, type: "hihat" },
  { name: "Open HH", color: "#2ecc71", freq: 600, type: "openhat" },
  { name: "Bass",    color: "#3498db", freq: 80,  type: "bass" },
  { name: "Clap",    color: "#9b59b6", freq: 300, type: "clap" },
];

const DEFAULT_PATTERN = [
  [1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0],
  [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0],
  [1,0,1,0, 1,0,1,0, 1,0,1,0, 1,0,1,0],
  [0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0],
  [1,0,0,1, 0,0,1,0, 1,0,0,1, 0,0,1,0],
  [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0],
];

function createEmptyPattern(steps) {
  return TRACKS.map(() => Array(steps).fill(0));
}

function resizeRow(row, steps) {
  if (row.length === steps) return [...row];
  if (row.length > steps) return row.slice(0, steps);
  const out = [];
  for (let i = 0; i < steps; i++) out.push(row[i % row.length] ?? 0);
  return out;
}

function resizePattern(pattern, steps) {
  const base = Array.isArray(pattern) ? pattern : [];
  const out = TRACKS.map((_, i) => resizeRow(base[i] ?? [], steps));
  return out;
}

function clamp01(x) {
  return Math.max(0, Math.min(1, x));
}

function findTrackIndex(type) {
  return TRACKS.findIndex(t => t.type === type);
}

function mean(arr) {
  if (!arr.length) return 0;
  let s = 0;
  for (let i = 0; i < arr.length; i++) s += arr[i];
  return s / arr.length;
}

function std(arr) {
  if (arr.length < 2) return 0;
  const m = mean(arr);
  let v = 0;
  for (let i = 0; i < arr.length; i++) {
    const d = arr[i] - m;
    v += d * d;
  }
  return Math.sqrt(v / (arr.length - 1));
}

function lowpass1Pole(x, a, state) {
  state.v = state.v + a * (x - state.v);
  return state.v;
}

function estimateBpmFromOnsetCurve(onset, sampleRate, hop) {
  // Autocorrelation over onset strength curve.
  const minBpm = 60;
  const maxBpm = 180;
  const minLag = Math.floor((60 * sampleRate) / (maxBpm * hop));
  const maxLag = Math.floor((60 * sampleRate) / (minBpm * hop));
  const n = onset.length;

  // Normalize (zero-mean).
  const m = mean(onset);
  const x = new Float32Array(n);
  for (let i = 0; i < n; i++) x[i] = onset[i] - m;

  let bestLag = 0;
  let bestScore = -Infinity;
  for (let lag = minLag; lag <= maxLag; lag++) {
    let s = 0;
    for (let i = 0; i < n - lag; i++) {
      s += x[i] * x[i + lag];
    }
    if (s > bestScore) {
      bestScore = s;
      bestLag = lag;
    }
  }

  if (!bestLag) return null;
  const bpm = (60 * sampleRate) / (bestLag * hop);
  return bpm;
}

function peakPick(onset, threshold, minDistanceFrames) {
  const peaks = [];
  let lastPeak = -Infinity;
  for (let i = 1; i < onset.length - 1; i++) {
    const v = onset[i];
    if (v < threshold) continue;
    if (v <= onset[i - 1] || v <= onset[i + 1]) continue;
    if (i - lastPeak < minDistanceFrames) continue;
    peaks.push(i);
    lastPeak = i;
  }
  return peaks;
}

async function analyzeAudioFile(file, steps, sensitivity) {
  const arrayBuffer = await file.arrayBuffer();
  const ctx = new (window.AudioContext || window.webkitAudioContext)();
  const audioBuffer = await ctx.decodeAudioData(arrayBuffer);

  const sr = audioBuffer.sampleRate;
  const ch0 = audioBuffer.getChannelData(0);
  const ch1 = audioBuffer.numberOfChannels > 1 ? audioBuffer.getChannelData(1) : null;
  const len = audioBuffer.length;

  // Mix to mono.
  const mono = new Float32Array(len);
  if (ch1) {
    for (let i = 0; i < len; i++) mono[i] = 0.5 * (ch0[i] + ch1[i]);
  } else {
    mono.set(ch0);
  }

  // Frame parameters.
  const frameSize = 1024;
  const hop = 256;
  const frames = Math.floor((len - frameSize) / hop);

  // Band-ish envelopes using simple one-pole filters.
  // These are heuristics; tuned for drum loops.
  const lpState = { v: 0 };
  const hpState = { v: 0 };
  const midLpState = { v: 0 };
  const midHpState = { v: 0 };

  // Filter coefficients (0..1). Smaller = slower cutoff.
  // Derived empirically for ~44.1k; still works decently across SR.
  const aKick = 2 * Math.PI * 140 / sr; // lowpass ~140Hz
  const aHatLp = 2 * Math.PI * 8000 / sr; // lowpass for mid chain
  const aMidHp = 2 * Math.PI * 180 / sr; // highpass ~180Hz
  const aSmooth = 2 * Math.PI * 10 / sr; // envelope smoothing

  const envLow = new Float32Array(frames);
  const envMid = new Float32Array(frames);
  const envHigh = new Float32Array(frames);
  const onset = new Float32Array(frames);

  let prevEnergy = 0;
  let envLowState = { v: 0 };
  let envMidState = { v: 0 };
  let envHighState = { v: 0 };

  for (let f = 0; f < frames; f++) {
    const start = f * hop;
    let eLow = 0, eMid = 0, eHigh = 0;
    for (let i = 0; i < frameSize; i++) {
      const s = mono[start + i] || 0;

      // Low band (kick-ish): lowpass.
      const low = lowpass1Pole(s, aKick, lpState);

      // High band (hat-ish): highpass by subtracting lowpass @ ~8k-ish surrogate.
      const midBase = lowpass1Pole(s, aHatLp, midLpState);
      const high = s - midBase;

      // Mid band (snare-ish): highpass then lowpass-ish.
      const midHp = (midBase - lowpass1Pole(midBase, aMidHp, midHpState));
      const mid = midHp;

      eLow += low * low;
      eMid += mid * mid;
      eHigh += high * high;
    }

    // Simple envelope smoothing.
    const lowEnv = lowpass1Pole(Math.sqrt(eLow / frameSize), aSmooth, envLowState);
    const midEnv = lowpass1Pole(Math.sqrt(eMid / frameSize), aSmooth, envMidState);
    const highEnv = lowpass1Pole(Math.sqrt(eHigh / frameSize), aSmooth, envHighState);

    envLow[f] = lowEnv;
    envMid[f] = midEnv;
    envHigh[f] = highEnv;

    const energy = lowEnv + midEnv + highEnv;
    const diff = Math.max(0, energy - prevEnergy);
    onset[f] = diff;
    prevEnergy = energy;
  }

  // Peak picking.
  const onsetArr = Array.from(onset);
  const thr = mean(onsetArr) + sensitivity * std(onsetArr);
  const minDist = Math.floor((0.06 * sr) / hop); // ~60ms
  const peakFrames = peakPick(onset, thr, minDist);

  // BPM.
  let bpm = estimateBpmFromOnsetCurve(onset, sr, hop);
  if (!bpm || !Number.isFinite(bpm)) bpm = 120;
  // Fold BPM into sane range.
  while (bpm < 60) bpm *= 2;
  while (bpm > 180) bpm /= 2;

  // Convert peaks to times and classify.
  const hits = [];
  for (const pf of peakFrames) {
    const t = (pf * hop) / sr;

    // Energy ratios at that frame.
    const l = envLow[pf] + 1e-8;
    const mE = envMid[pf] + 1e-8;
    const h = envHigh[pf] + 1e-8;
    const total = l + mE + h;
    const rl = l / total;
    const rm = mE / total;
    const rh = h / total;

    let kind = "snare";
    if (rl > 0.55) kind = "kick";
    else if (rh > 0.55) kind = "hihat";
    else if (rm >= rl && rm >= rh) kind = "snare";

    hits.push({ t, kind });
  }

  // Quantize to steps.
  const secondsPerBeat = 60 / bpm;
  const secondsPerStep = secondsPerBeat / 4;
  const startTime = hits.length ? hits[0].t : 0;

  const kickSteps = new Set();
  const snareSteps = new Set();
  const hatSteps = new Set();
  for (const h of hits) {
    const rel = h.t - startTime;
    const step = ((Math.round(rel / secondsPerStep) % steps) + steps) % steps;
    if (h.kind === "kick") kickSteps.add(step);
    else if (h.kind === "hihat") hatSteps.add(step);
    else snareSteps.add(step);
  }

  try { ctx.close(); } catch (e) {}

  return {
    bpm,
    steps,
    kick: Array.from(kickSteps).sort((a,b) => a-b),
    snare: Array.from(snareSteps).sort((a,b) => a-b),
    hihat: Array.from(hatSteps).sort((a,b) => a-b),
    hitCount: hits.length,
  };
}

const STYLE_PRESETS = {
  "Classic Boom Bap": {
    bpm: 92,
    pattern: [
      [1,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0],
      [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0],
      [0,0,1,0, 0,0,1,0, 0,0,1,0, 0,0,1,0],
      [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0],
      [1,0,0,0, 0,0,1,0, 1,0,0,0, 0,0,1,0],
      [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0],
    ],
  },
  "Trap (808 + Hats)": {
    bpm: 140,
    pattern: [
      [1,0,0,0, 0,0,1,0, 1,0,0,0, 0,1,0,0],
      [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0],
      [1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1],
      [0,0,0,0, 0,0,1,0, 0,0,0,0, 0,0,1,0],
      [1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0],
      [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0],
    ],
  },
  "UK Drill": {
    bpm: 145,
    pattern: [
      [1,0,0,0, 0,0,1,0, 0,0,1,0, 0,0,0,1],
      [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0],
      [1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1],
      [0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0],
      [1,0,0,0, 0,1,0,0, 1,0,0,0, 0,1,0,0],
      [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0],
    ],
  },
  "Lo‑Fi Chill": {
    bpm: 78,
    pattern: [
      [1,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0],
      [0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,1,0],
      [1,0,0,1, 1,0,0,1, 1,0,0,1, 1,0,0,1],
      [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0],
      [1,0,0,0, 0,0,1,0, 1,0,0,0, 0,0,1,0],
      [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0],
    ],
  },
  "West Coast Bounce": {
    bpm: 96,
    pattern: [
      [1,0,0,0, 0,0,1,0, 1,0,0,0, 0,0,1,0],
      [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0],
      [0,0,1,0, 0,1,0,0, 0,0,1,0, 0,1,0,0],
      [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0],
      [1,0,0,1, 0,0,1,0, 1,0,0,1, 0,0,1,0],
      [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0],
    ],
  },
  "Reggaeton / Dembow": {
    bpm: 95,
    pattern: [
      [1,0,0,0, 0,0,1,0, 0,0,1,0, 0,1,0,0],
      [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0],
      [0,0,1,0, 0,0,1,0, 0,0,1,0, 0,0,1,0],
      [0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0],
      [1,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0],
      [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0],
    ],
  },
};

const SAVED_BEATS_KEY = "rap_beat_studio_saved_beats_v1";

function safeJsonParse(s) {
  try {
    return JSON.parse(s);
  } catch (e) {
    return null;
  }
}

function loadSavedBeats() {
  if (typeof window === "undefined") return [];
  const raw = window.localStorage.getItem(SAVED_BEATS_KEY);
  const parsed = raw ? safeJsonParse(raw) : null;
  if (!Array.isArray(parsed)) return [];
  return parsed;
}

function persistSavedBeats(items) {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(SAVED_BEATS_KEY, JSON.stringify(items));
}

function createAudioCtx() {
  return new (window.AudioContext || window.webkitAudioContext)();
}

function playKick(ctx, t, out) {
  const o = ctx.createOscillator(), g = ctx.createGain();
  o.connect(g); g.connect(out || ctx.destination);
  o.frequency.setValueAtTime(150, t);
  o.frequency.exponentialRampToValueAtTime(0.001, t + 0.5);
  g.gain.setValueAtTime(1, t);
  g.gain.exponentialRampToValueAtTime(0.001, t + 0.5);
  o.start(t); o.stop(t + 0.5);
}

function playSnare(ctx, t, out) {
  const buf = ctx.createBuffer(1, ctx.sampleRate * 0.2, ctx.sampleRate);
  const d = buf.getChannelData(0);
  for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
  const src = ctx.createBufferSource(), g = ctx.createGain();
  const f = ctx.createBiquadFilter();
  f.type = "highpass"; f.frequency.value = 1000;
  src.buffer = buf; src.connect(f); f.connect(g); g.connect(out || ctx.destination);
  g.gain.setValueAtTime(0.8, t);
  g.gain.exponentialRampToValueAtTime(0.001, t + 0.2);
  src.start(t); src.stop(t + 0.2);
}

function playHihat(ctx, t, open = false, out) {
  const buf = ctx.createBuffer(1, ctx.sampleRate * (open ? 0.3 : 0.08), ctx.sampleRate);
  const d = buf.getChannelData(0);
  for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
  const src = ctx.createBufferSource(), g = ctx.createGain();
  const f = ctx.createBiquadFilter();
  f.type = "highpass"; f.frequency.value = 7000;
  src.buffer = buf; src.connect(f); f.connect(g); g.connect(out || ctx.destination);
  g.gain.setValueAtTime(0.4, t);
  g.gain.exponentialRampToValueAtTime(0.001, t + (open ? 0.3 : 0.08));
  src.start(t); src.stop(t + (open ? 0.3 : 0.08));
}

function playBass(ctx, t, out) {
  const o = ctx.createOscillator(), g = ctx.createGain();
  o.type = "sawtooth"; o.connect(g); g.connect(out || ctx.destination);
  o.frequency.setValueAtTime(80, t);
  g.gain.setValueAtTime(0.5, t);
  g.gain.exponentialRampToValueAtTime(0.001, t + 0.3);
  o.start(t); o.stop(t + 0.3);
}

function playClap(ctx, t, out) {
  const buf = ctx.createBuffer(1, ctx.sampleRate * 0.1, ctx.sampleRate);
  const d = buf.getChannelData(0);
  for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
  const src = ctx.createBufferSource(), g = ctx.createGain();
  const f = ctx.createBiquadFilter();
  f.type = "bandpass"; f.frequency.value = 1200; f.Q.value = 0.5;
  src.buffer = buf; src.connect(f); f.connect(g); g.connect(out || ctx.destination);
  g.gain.setValueAtTime(0.7, t);
  g.gain.exponentialRampToValueAtTime(0.001, t + 0.1);
  src.start(t); src.stop(t + 0.1);
}

function triggerSound(ctx, type, t, out) {
  try {
    if (type === "kick") playKick(ctx, t, out);
    else if (type === "snare") playSnare(ctx, t, out);
    else if (type === "hihat") playHihat(ctx, t, false, out);
    else if (type === "openhat") playHihat(ctx, t, true, out);
    else if (type === "bass") playBass(ctx, t, out);
    else if (type === "clap") playClap(ctx, t, out);
  } catch(e) {}
}

export default function BeatStudio() {
  const [steps, setSteps] = useState(DEFAULT_STEPS);
  const [pattern, setPattern] = useState(() => resizePattern(DEFAULT_PATTERN, DEFAULT_STEPS));
  const [bpm, setBpm] = useState(DEFAULT_BPM);
  const [playing, setPlaying] = useState(false);
  const [curStep, setCurStep] = useState(-1);
  const [volumes, setVolumes] = useState(TRACKS.map(() => 0.8));
  const [styleName, setStyleName] = useState("Custom");
  const [endFill, setEndFill] = useState("None");
  const [backingURL, setBackingURL] = useState(null);
  const [backingFile, setBackingFile] = useState(null);
  const [backingVol, setBackingVol] = useState(0.8);
  const [syncBacking, setSyncBacking] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisError, setAnalysisError] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [analysisSensitivity, setAnalysisSensitivity] = useState(1.0);
  const [analysisOverwrite, setAnalysisOverwrite] = useState(true);
  const [savedBeats, setSavedBeats] = useState(() => loadSavedBeats());
  const [saveBeatName, setSaveBeatName] = useState("");
  const [selectedBeatId, setSelectedBeatId] = useState("");
  const [exportJson, setExportJson] = useState("");
  const [importJson, setImportJson] = useState("");
  const [saveBeatError, setSaveBeatError] = useState(null);
  const [recText, setRecText] = useState("");
  const [micRecording, setMicRecording] = useState(false);
  const [audioURL, setAudioURL] = useState(null);
  const [mixRecording, setMixRecording] = useState(false);
  const [mixURL, setMixURL] = useState(null);
  const [syncRecordingWithBeat, setSyncRecordingWithBeat] = useState(true);
  const [tab, setTab] = useState("beats");
  const [mixVolBeat, setMixVolBeat] = useState(0.8);
  const [mixVolVoice, setMixVolVoice] = useState(0.9);
  const [tip, setTip] = useState(0);

  const ctxRef = useRef(null);
  const stepRef = useRef(0);
  const nextTimeRef = useRef(0);
  const loopStartTimeRef = useRef(0);
  const timerRef = useRef(null);
  const patternRef = useRef(pattern);
  const bpmRef = useRef(bpm);
  const volRef = useRef(volumes);
  const stepsRef = useRef(steps);
  const endFillRef = useRef(endFill);
  const playingRef = useRef(false);
  const mediaRecRef = useRef(null);
  const chunksRef = useRef([]);
  const beatGainRef = useRef(null);
  const voiceGainRef = useRef(null);
  const masterGainRef = useRef(null);
  const recordDestRef = useRef(null);
  const backingSourceRef = useRef(null);
  const micStreamRef = useRef(null);
  const micSourceRef = useRef(null);
  const backingAudioRef = useRef(null);
  const gridScrollRef = useRef(null);
  const labelsScrollRef = useRef(null);
  const scrollSyncRef = useRef(false);

  useEffect(() => {
    persistSavedBeats(savedBeats);
  }, [savedBeats]);

  useEffect(() => { patternRef.current = pattern; }, [pattern]);
  useEffect(() => { bpmRef.current = bpm; }, [bpm]);
  useEffect(() => { volRef.current = volumes; }, [volumes]);
  useEffect(() => { stepsRef.current = steps; }, [steps]);
  useEffect(() => { endFillRef.current = endFill; }, [endFill]);

  useEffect(() => {
    const el = backingAudioRef.current;
    if (!el) return;
    el.volume = backingVol;
  }, [backingVol]);

  const getCtx = () => {
    if (!ctxRef.current) {
      const ctx = createAudioCtx();

      // Master mix bus so we can record (and apply mix volumes).
      const master = ctx.createGain();
      master.gain.value = 1;
      master.connect(ctx.destination);

      const recordDest = ctx.createMediaStreamDestination();
      master.connect(recordDest);

      const beat = ctx.createGain();
      beat.gain.value = mixVolBeat;
      beat.connect(master);

      const voice = ctx.createGain();
      voice.gain.value = mixVolVoice;
      voice.connect(master);

      masterGainRef.current = master;
      recordDestRef.current = recordDest;
      beatGainRef.current = beat;
      voiceGainRef.current = voice;

      ctxRef.current = ctx;
    }
    return ctxRef.current;
  };

  useEffect(() => {
    if (beatGainRef.current) beatGainRef.current.gain.value = mixVolBeat;
  }, [mixVolBeat]);

  useEffect(() => {
    if (voiceGainRef.current) voiceGainRef.current.gain.value = mixVolVoice;
  }, [mixVolVoice]);

  useEffect(() => {
    // Route backing audio element through the AudioContext so it can be recorded in the mix.
    const el = backingAudioRef.current;
    if (!el || !backingURL) return;
    const ctx = getCtx();
    try {
      if (!backingSourceRef.current) {
        const src = ctx.createMediaElementSource(el);
        src.connect(beatGainRef.current || ctx.destination);
        backingSourceRef.current = src;
      }
    } catch (e) {}
  }, [backingURL]);

  const schedule = useCallback(() => {
    const ctx = getCtx();
    const secondsPerStep = 60 / bpmRef.current / 4;
    while (nextTimeRef.current < ctx.currentTime + 0.1) {
      const step = stepRef.current;

      const curSteps = stepsRef.current;
      const curEndFill = endFillRef.current;
      const beatsPerLoop = curSteps / 4;
      const fillActive = beatsPerLoop === 32 && curEndFill !== "None";
      const beatIdx = Math.floor(step / 4);
      const subStep = step % 4;
      const isFillStep = fillActive && beatIdx >= 28;

      const fillExtraHit = (trackType) => {
        if (!isFillStep) return false;

        const b = beatIdx;
        const ss = subStep;
        if (curEndFill === "Hat Stutter") {
          if (trackType === "hihat") return true;
          if (trackType === "openhat") return b === 31 && ss === 3;
          return false;
        }

        if (curEndFill === "Snare Roll") {
          if (trackType === "snare") return true;
          if (trackType === "hihat") return !(b === 31 && ss === 3);
          return false;
        }

        if (curEndFill === "Clap Build") {
          if (trackType === "clap") return true;
          if (trackType === "hihat") return (b === 29 || b === 31) && ss === 0;
          return false;
        }

        if (curEndFill === "Kick Drop") {
          if (trackType === "kick") return (b === 28 || b === 30) && ss === 0;
          if (trackType === "snare") return b === 29 && ss === 0;
          if (trackType === "openhat") return b === 31 && ss === 3;
          return false;
        }

        return false;
      };

      TRACKS.forEach((tr, i) => {
        if (patternRef.current[i][step] || fillExtraHit(tr.type)) {
          const g = ctx.createGain();
          g.gain.value = volRef.current[i];
          g.connect(beatGainRef.current || ctx.destination);
          triggerSound(ctx, tr.type, nextTimeRef.current, g);
        }
      });
      stepRef.current = (step + 1) % curSteps;
      nextTimeRef.current += secondsPerStep;
    }
  }, []);

  const startPlay = () => {
    const ctx = getCtx();
    if (ctx.state === "suspended") ctx.resume();
    stepRef.current = 0;
    loopStartTimeRef.current = ctx.currentTime + 0.05;
    nextTimeRef.current = loopStartTimeRef.current;
    playingRef.current = true;
    timerRef.current = setInterval(schedule, 25);
    setPlaying(true);

    if (syncBacking && backingAudioRef.current && backingURL) {
      try {
        backingAudioRef.current.currentTime = 0;
        backingAudioRef.current.play();
      } catch (e) {}
    }
  };

  const stopPlay = () => {
    clearInterval(timerRef.current);
    playingRef.current = false;
    setPlaying(false);
    setCurStep(-1);

    if (syncBacking && backingAudioRef.current) {
      try {
        backingAudioRef.current.pause();
        backingAudioRef.current.currentTime = 0;
      } catch (e) {}
    }
  };

  const togglePlay = () => playing ? stopPlay() : startPlay();

  useEffect(() => {
    if (!playing) return;

    let raf = 0;
    const tick = () => {
      if (!playingRef.current) return;
      const ctx = ctxRef.current;
      if (!ctx) return;

      const curSteps = stepsRef.current;
      const secondsPerStep = 60 / bpmRef.current / 4;
      const elapsed = ctx.currentTime - loopStartTimeRef.current;
      if (elapsed >= 0 && Number.isFinite(elapsed)) {
        const step = ((Math.floor(elapsed / secondsPerStep) % curSteps) + curSteps) % curSteps;
        setCurStep(step);

        const scroller = gridScrollRef.current;
        if (scroller) {
          const el = scroller.querySelector(`[data-track="0"][data-step="${step}"]`);
          if (el) {
            const left = el.offsetLeft;
            const right = left + el.offsetWidth;
            const viewLeft = scroller.scrollLeft;
            const viewRight = viewLeft + scroller.clientWidth;
            if (left < viewLeft + 40 || right > viewRight - 40) {
              const target = left - scroller.clientWidth / 2 + el.offsetWidth / 2;
              scroller.scrollTo({ left: Math.max(0, target), behavior: "smooth" });
              const labels = labelsScrollRef.current;
              if (labels) {
                labels.scrollTo({ left: Math.max(0, target), behavior: "smooth" });
              }
            }
          }
        }
      }

      raf = requestAnimationFrame(tick);
    };

    raf = requestAnimationFrame(tick);
    return () => {
      try { cancelAnimationFrame(raf); } catch (e) {}
    };
  }, [playing]);

  const toggleStep = (track, step) => {
    setPattern(p => {
      const np = p.map(r => [...r]);
      np[track][step] = np[track][step] ? 0 : 1;
      return np;
    });
    setStyleName("Custom");
  };

  const clearPattern = () => {
    setPattern(createEmptyPattern(stepsRef.current));
    setStyleName("Custom");
  };

  const resetPattern = () => {
    setPattern(resizePattern(DEFAULT_PATTERN, stepsRef.current));
    setBpm(DEFAULT_BPM);
    setStyleName("Custom");
  };

  const applyStyle = (name) => {
    if (name === "Custom") {
      setStyleName("Custom");
      return;
    }

    const preset = STYLE_PRESETS[name];
    if (!preset) return;

    setStyleName(name);
    setBpm(preset.bpm);
    setPattern(resizePattern(preset.pattern, stepsRef.current));
  };

  const applySteps = (nextBeats) => {
    const beats = Number(nextBeats);
    if (!AVAILABLE_BEATS.includes(beats)) return;
    const s = beats * 4;
    setSteps(s);
    setPattern((p) => resizePattern(p, s));
    stepRef.current = 0;
    nextTimeRef.current = getCtx().currentTime + 0.05;
    if (beats !== 32) {
      setEndFill("None");
    }
  };

  const onBackingUpload = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const url = URL.createObjectURL(file);
    setBackingURL(url);
    setBackingFile(file);
    setAnalysis(null);
    setAnalysisError(null);
  };

  const makeBeatSnapshot = () => {
    return {
      steps: stepsRef.current,
      bpm: bpmRef.current,
      pattern: resizePattern(patternRef.current, stepsRef.current),
      endFill: endFillRef.current,
      styleName,
    };
  };

  const saveCurrentBeat = () => {
    const name = (saveBeatName || "").trim();
    if (!name) {
      setSaveBeatError("Enter a name to save this beat.");
      return;
    }
    setSaveBeatError(null);
    const id = `beat_${Date.now()}_${Math.floor(Math.random() * 1e9)}`;
    const item = {
      id,
      name,
      createdAt: Date.now(),
      data: makeBeatSnapshot(),
    };
    setSavedBeats(prev => [item, ...prev]);
    setSelectedBeatId(id);
    setSaveBeatName("");
    setExportJson("");
  };

  const loadBeatById = (id) => {
    const item = savedBeats.find(b => b.id === id);
    if (!item) return;
    const d = item.data || {};
    const rawSteps = Number(d.steps);
    const normalizedSteps = Number.isFinite(rawSteps) ? rawSteps : DEFAULT_STEPS;
    const beats = Math.max(4, Math.min(32, Math.round(normalizedSteps / 4)));
    const nextSteps = beats * 4;
    const nextPattern = resizePattern(d.pattern || [], nextSteps);

    stop();
    setSteps(nextSteps);
    stepsRef.current = nextSteps;
    setPattern(nextPattern);
    setBpm(Math.round(d.bpm || DEFAULT_BPM));
    bpmRef.current = Math.round(d.bpm || DEFAULT_BPM);

    setEndFill(d.endFill || "None");
    setStyleName(d.styleName || "Custom");
    setExportJson("");
  };

  const deleteBeatById = (id) => {
    setSavedBeats(prev => prev.filter(b => b.id !== id));
    if (selectedBeatId === id) {
      setSelectedBeatId("");
      setExportJson("");
    }
  };

  const exportSelectedBeat = () => {
    const item = savedBeats.find(b => b.id === selectedBeatId);
    if (!item) return;
    setExportJson(JSON.stringify(item, null, 2));
  };

  const importBeatFromJson = () => {
    const parsed = safeJsonParse(importJson);
    if (!parsed) {
      setSaveBeatError("Invalid JSON.");
      return;
    }

    const asItem = (() => {
      if (parsed && parsed.id && parsed.data) return parsed;
      if (parsed && parsed.steps && parsed.pattern) {
        return {
          id: `beat_${Date.now()}_${Math.floor(Math.random() * 1e9)}`,
          name: parsed.name || `Imported ${new Date().toLocaleString()}`,
          createdAt: Date.now(),
          data: {
            steps: parsed.steps,
            bpm: parsed.bpm,
            pattern: parsed.pattern,
            endFill: parsed.endFill,
            styleName: parsed.styleName,
          }
        };
      }
      return null;
    })();

    if (!asItem) {
      setSaveBeatError("JSON format not recognized.");
      return;
    }
    setSaveBeatError(null);
    setSavedBeats(prev => [asItem, ...prev]);
    setSelectedBeatId(asItem.id);
    setImportJson("");
    setExportJson("");
  };

  const clearBacking = () => {
    if (backingAudioRef.current) {
      try {
        backingAudioRef.current.pause();
        backingAudioRef.current.currentTime = 0;
      } catch (e) {}
    }
    if (backingURL) {
      try {
        URL.revokeObjectURL(backingURL);
      } catch (e) {}
    }
    setBackingURL(null);
    setBackingFile(null);
    setAnalysis(null);
    setAnalysisError(null);
  };

  const runAnalysis = async () => {
    if (!backingFile) return;
    setAnalyzing(true);
    setAnalysisError(null);
    try {
      const res = await analyzeAudioFile(backingFile, stepsRef.current, analysisSensitivity);
      setAnalysis(res);
    } catch (e) {
      setAnalysisError("Analysis failed. Try a shorter/cleaner loop (WAV works best). ");
    } finally {
      setAnalyzing(false);
    }
  };

  const applyAnalysis = () => {
    if (!analysis) return;
    const kickI = findTrackIndex("kick");
    const snareI = findTrackIndex("snare");
    const hatI = findTrackIndex("hihat");
    if (kickI < 0 || snareI < 0 || hatI < 0) return;

    setBpm(Math.round(analysis.bpm));

    setPattern((prev) => {
      const curSteps = stepsRef.current;
      const base = analysisOverwrite ? createEmptyPattern(curSteps) : resizePattern(prev, curSteps);
      const next = base.map(r => [...r]);

      for (const s of analysis.kick) next[kickI][s] = 1;
      for (const s of analysis.snare) next[snareI][s] = 1;
      for (const s of analysis.hihat) next[hatI][s] = 1;

      return next;
    });

    setStyleName("Custom");
  };

  const startMic = async () => {
    try {
      const ctx = getCtx();
      if (ctx.state === "suspended") await ctx.resume();
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const rec = new MediaRecorder(stream);
      chunksRef.current = [];
      rec.ondataavailable = e => chunksRef.current.push(e.data);
      rec.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        setAudioURL(URL.createObjectURL(blob));
      };
      rec.start();
      mediaRecRef.current = rec;
      setMicRecording(true);

      if (syncRecordingWithBeat) {
        // Restart beat/backing so the recorded vocal starts aligned to step 1.
        try { stopPlay(); } catch (e) {}
        setTimeout(() => {
          try { startPlay(); } catch (e) {}
        }, 60);
      }
    } catch(e) {
      alert("Microphone access denied. Please allow mic access to record.");
    }
  };

  const stopMic = () => {
    mediaRecRef.current?.stop();
    setMicRecording(false);
  };

  const ensureMicInMix = async () => {
    if (micStreamRef.current) return;
    const ctx = getCtx();
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    micStreamRef.current = stream;
    try {
      const src = ctx.createMediaStreamSource(stream);
      micSourceRef.current = src;
      src.connect(voiceGainRef.current || ctx.destination);
    } catch (e) {}
  };

  const stopMicInMix = () => {
    if (micStreamRef.current) {
      try {
        micStreamRef.current.getTracks().forEach(t => t.stop());
      } catch (e) {}
    }
    micStreamRef.current = null;
    micSourceRef.current = null;
  };

  const startMixRecord = async () => {
    try {
      const ctx = getCtx();
      if (ctx.state === "suspended") await ctx.resume();
      await ensureMicInMix();

      const dest = recordDestRef.current;
      if (!dest) return;

      const rec = new MediaRecorder(dest.stream);
      chunksRef.current = [];
      rec.ondataavailable = e => chunksRef.current.push(e.data);
      rec.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        setMixURL(URL.createObjectURL(blob));
        stopMicInMix();
      };
      rec.start();
      mediaRecRef.current = rec;
      setMixRecording(true);

      if (syncRecordingWithBeat) {
        try { stopPlay(); } catch (e) {}
        setTimeout(() => {
          try { startPlay(); } catch (e) {}
        }, 60);
      }
    } catch (e) {
      alert("Could not start mix recording. Make sure mic access is allowed.");
    }
  };

  const stopMixRecord = () => {
    mediaRecRef.current?.stop();
    setMixRecording(false);
  };

  const tips = [
    "🎤 Rap tip: Start your bars on beat 1 or beat 3 — they're the strongest hits!",
    "🥁 Beat tip: The kick on beat 1, snare on beat 3 is a classic hip-hop groove.",
    "🎵 Tip: Try muting the hi-hats every 4th step for a 'breathing' feel.",
    "🔥 Flow tip: Write your hook first — it's the catchiest part of your song.",
    "🎚️ Mixing tip: Keep your voice louder than the beat so lyrics cut through.",
    "🎹 Bass tip: The bass and kick should hit together for a punchy low end.",
  ];

  return (
    <div style={{ fontFamily: "'Segoe UI', sans-serif", background: "#0f0f1a", minHeight: "100vh", color: "#fff", padding: "16px" }}>
      {/* Header */}
      <div style={{ textAlign: "center", marginBottom: 20 }}>
        <div style={{ fontSize: 32, fontWeight: 900, background: "linear-gradient(90deg,#e74c3c,#9b59b6,#3498db)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
          🎧 Rap Beat Studio
        </div>
        <div style={{ color: "#aaa", fontSize: 13 }}>Make beats • Record vocals • Mix your track</div>
      </div>

      {/* Tabs */}
      <div style={{ display: "flex", gap: 8, justifyContent: "center", marginBottom: 20 }}>
        {["beats","record","mix","tips"].map(t => (
          <button key={t} onClick={() => setTab(t)} style={{
            padding: "8px 20px", borderRadius: 20, border: "none", cursor: "pointer", fontWeight: 700, fontSize: 13,
            background: tab === t ? "linear-gradient(90deg,#e74c3c,#9b59b6)" : "#1e1e30",
            color: tab === t ? "#fff" : "#aaa"
          }}>{t.charAt(0).toUpperCase()+t.slice(1)}</button>
        ))}
      </div>

      {/* BEATS TAB */}
      {tab === "beats" && (
        <div>
          {/* BPM + Controls */}
          <div style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 16, flexWrap: "wrap", justifyContent: "center" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <span style={{ color: "#aaa", fontSize: 13 }}>Beats</span>
              <select
                value={steps / 4}
                onChange={(e) => applySteps(e.target.value)}
                style={{
                  height: 34,
                  borderRadius: 10,
                  border: "1px solid #333",
                  background: "#0f0f1a",
                  color: "#fff",
                  padding: "0 10px",
                  fontWeight: 700,
                  fontSize: 12,
                }}
              >
                {AVAILABLE_BEATS.map((n) => (
                  <option key={n} value={n}>{n}</option>
                ))}
              </select>
            </div>

            {steps === 128 && (
              <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <span style={{ color: "#aaa", fontSize: 13 }}>End Fill</span>
                <select
                  value={endFill}
                  onChange={(e) => setEndFill(e.target.value)}
                  style={{
                    height: 34,
                    borderRadius: 10,
                    border: "1px solid #333",
                    background: "#0f0f1a",
                    color: "#fff",
                    padding: "0 10px",
                    fontWeight: 700,
                    fontSize: 12,
                  }}
                >
                  {[
                    "None",
                    "Hat Stutter",
                    "Snare Roll",
                    "Clap Build",
                    "Kick Drop",
                  ].map((name) => (
                    <option key={name} value={name}>{name}</option>
                  ))}
                </select>
              </div>
            )}
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <span style={{ color: "#aaa", fontSize: 13 }}>Style</span>
              <select
                value={styleName}
                onChange={(e) => applyStyle(e.target.value)}
                style={{
                  height: 34,
                  borderRadius: 10,
                  border: "1px solid #333",
                  background: "#0f0f1a",
                  color: "#fff",
                  padding: "0 10px",
                  fontWeight: 700,
                  fontSize: 12,
                }}
              >
                <option value="Custom">Custom</option>
                {Object.keys(STYLE_PRESETS).map((name) => (
                  <option key={name} value={name}>{name}</option>
                ))}
              </select>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <span style={{ color: "#aaa", fontSize: 13 }}>BPM</span>
              <input type="range" min="60" max="180" value={bpm} onChange={e => setBpm(+e.target.value)}
                style={{ width: 120, accentColor: "#e74c3c" }} />
              <span style={{ fontWeight: 700, color: "#e74c3c", width: 36 }}>{bpm}</span>
            </div>
            <button onClick={togglePlay} style={{
              padding: "10px 28px", borderRadius: 24, border: "none", cursor: "pointer",
              background: playing ? "#e74c3c" : "linear-gradient(90deg,#2ecc71,#27ae60)",
              color: "#fff", fontWeight: 800, fontSize: 15
            }}>{playing ? "⏹ Stop" : "▶ Play"}</button>
            <button onClick={clearPattern} style={{ padding: "8px 16px", borderRadius: 16, border: "1px solid #555", background: "transparent", color: "#aaa", cursor: "pointer", fontSize: 12 }}>Clear</button>
            <button onClick={resetPattern} style={{ padding: "8px 16px", borderRadius: 16, border: "1px solid #555", background: "transparent", color: "#aaa", cursor: "pointer", fontSize: 12 }}>Reset</button>
          </div>

          {/* Step labels */}
          <div
            ref={labelsScrollRef}
            onScroll={() => {
              if (scrollSyncRef.current) return;
              const labels = labelsScrollRef.current;
              const grid = gridScrollRef.current;
              if (!labels || !grid) return;
              scrollSyncRef.current = true;
              grid.scrollLeft = labels.scrollLeft;
              scrollSyncRef.current = false;
            }}
            style={{ overflowX: "auto", paddingBottom: 6 }}
          >
            <div style={{ display: "grid", gridTemplateColumns: `72px repeat(${steps}, 34px)`, gap: 3, marginBottom: 4, width: "max-content" }}>
              <div />
              {Array.from({length:steps},(_,i) => (
                <div key={i} style={{ textAlign: "center", fontSize: 10, color: i % 4 === 0 ? "#e74c3c" : "#555", fontWeight: i%4===0 ? 700 : 400, width: 34 }}>
                  {i%4===0 ? (i/4+1) : "·"}
                </div>
              ))}
            </div>
          </div>

          {/* Sequencer Grid */}
          <div
            ref={gridScrollRef}
            onScroll={() => {
              if (scrollSyncRef.current) return;
              const labels = labelsScrollRef.current;
              const grid = gridScrollRef.current;
              if (!labels || !grid) return;
              scrollSyncRef.current = true;
              labels.scrollLeft = grid.scrollLeft;
              scrollSyncRef.current = false;
            }}
            style={{ overflowX: "auto", paddingBottom: 10 }}
          >
            <div style={{ width: "max-content" }}>
              {TRACKS.map((tr, ti) => (
                <div key={ti} style={{ display: "grid", gridTemplateColumns: `72px repeat(${steps}, 34px)`, gap: 3, marginBottom: 3 }}>
                  <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", paddingRight: 6 }}>
                    <span style={{ fontSize: 11, color: tr.color, fontWeight: 700 }}>{tr.name}</span>
                  </div>
                  {Array.from({length:steps},(_,si) => (
                    <button key={si} data-step={si} data-track={ti} onClick={() => toggleStep(ti,si)} style={{
                      height: 34, width: 34, borderRadius: 5, border: "none", cursor: "pointer",
                      background: pattern[ti][si]
                        ? (curStep === si ? "#fff" : tr.color)
                        : (curStep === si ? "#2a2a40" : "#1a1a2e"),
                      transition: "background 0.05s",
                      boxShadow: pattern[ti][si] && curStep===si ? `0 0 8px ${tr.color}` : "none"
                    }} />
                  ))}
                </div>
              ))}
            </div>
          </div>

          {/* Backing track */}
          <div style={{ marginTop: 18, background: "#1a1a2e", borderRadius: 16, padding: 16 }}>
            <div style={{ color: "#aaa", fontSize: 12, marginBottom: 10, fontWeight: 700 }}>Backing Track (MP3/WAV)</div>
            <div style={{ display: "flex", gap: 10, flexWrap: "wrap", alignItems: "center" }}>
              <input type="file" accept="audio/*" onChange={onBackingUpload} />
              {backingURL && (
                <button onClick={clearBacking} style={{
                  padding: "8px 16px",
                  borderRadius: 16,
                  border: "1px solid #555",
                  background: "transparent",
                  color: "#aaa",
                  cursor: "pointer",
                  fontSize: 12,
                }}>Remove</button>
              )}
              <label style={{ display: "flex", alignItems: "center", gap: 8, color: "#aaa", fontSize: 12 }}>
                <input type="checkbox" checked={syncBacking} onChange={(e) => setSyncBacking(e.target.checked)} />
                Sync play/stop with sequencer
              </label>
            </div>

            {backingURL && (
              <div style={{ marginTop: 10 }}>
                <audio ref={backingAudioRef} controls src={backingURL} style={{ width: "100%" }} />
                <div style={{ display: "flex", alignItems: "center", gap: 10, marginTop: 8, flexWrap: "wrap" }}>
                  <span style={{ color: "#aaa", fontSize: 12 }}>Volume</span>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.05"
                    value={backingVol}
                    onChange={(e) => setBackingVol(+e.target.value)}
                    style={{ width: 160, accentColor: "#3498db" }}
                  />
                  <span style={{ color: "#3498db", fontWeight: 700, fontSize: 12 }}>{Math.round(backingVol * 100)}%</span>
                </div>
                <div style={{ marginTop: 10, paddingTop: 10, borderTop: "1px solid #232343" }}>
                  <div style={{ display: "flex", gap: 10, flexWrap: "wrap", alignItems: "center" }}>
                    <button
                      onClick={runAnalysis}
                      disabled={!backingFile || analyzing}
                      style={{
                        padding: "10px 16px",
                        borderRadius: 16,
                        border: "none",
                        cursor: analyzing ? "not-allowed" : "pointer",
                        background: analyzing ? "#444" : "linear-gradient(90deg,#3498db,#9b59b6)",
                        color: "#fff",
                        fontWeight: 800,
                        fontSize: 12,
                      }}
                    >
                      {analyzing ? "Analyzing…" : "Analyze Beat"}
                    </button>

                    <label style={{ display: "flex", alignItems: "center", gap: 8, color: "#aaa", fontSize: 12 }}>
                      Sensitivity
                      <input
                        type="range"
                        min="0.5"
                        max="2.0"
                        step="0.1"
                        value={analysisSensitivity}
                        onChange={(e) => setAnalysisSensitivity(+e.target.value)}
                        style={{ width: 140, accentColor: "#9b59b6" }}
                      />
                      <span style={{ color: "#9b59b6", fontWeight: 700 }}>{analysisSensitivity.toFixed(1)}</span>
                    </label>

                    <label style={{ display: "flex", alignItems: "center", gap: 8, color: "#aaa", fontSize: 12 }}>
                      <input type="checkbox" checked={analysisOverwrite} onChange={(e) => setAnalysisOverwrite(e.target.checked)} />
                      Overwrite grid
                    </label>
                  </div>

                  {analysisError && (
                    <div style={{ color: "#ff8080", fontSize: 12, marginTop: 8 }}>
                      {analysisError}
                    </div>
                  )}

                  {analysis && (
                    <div style={{ marginTop: 10 }}>
                      <div style={{ display: "flex", gap: 10, flexWrap: "wrap", alignItems: "center" }}>
                        <div style={{ color: "#aaa", fontSize: 12 }}>
                          Detected BPM: <span style={{ color: "#2ecc71", fontWeight: 800 }}>{Math.round(analysis.bpm)}</span>
                        </div>
                        <div style={{ color: "#555", fontSize: 12 }}>
                          Hits: {analysis.hitCount} · K:{analysis.kick.length} S:{analysis.snare.length} H:{analysis.hihat.length}
                        </div>
                        <button
                          onClick={applyAnalysis}
                          style={{
                            padding: "8px 16px",
                            borderRadius: 16,
                            border: "none",
                            cursor: "pointer",
                            background: "#2ecc71",
                            color: "#0f0f1a",
                            fontWeight: 900,
                            fontSize: 12,
                          }}
                        >
                          Apply to Grid
                        </button>
                      </div>
                    </div>
                  )}
                </div>
                <div style={{ color: "#555", fontSize: 11, marginTop: 6, lineHeight: 1.4 }}>
                  Note: This plays your audio file as a backing track. It does not automatically detect BPM or convert the MP3 into step hits.
                </div>
              </div>
            )}
          </div>

          <div style={{ marginTop: 18, background: "#1a1a2e", borderRadius: 16, padding: 16 }}>
            <div style={{ color: "#aaa", fontSize: 12, marginBottom: 10, fontWeight: 700 }}>Saved Beats</div>
            <div style={{ display: "flex", gap: 10, flexWrap: "wrap", alignItems: "center" }}>
              <input
                value={saveBeatName}
                onChange={(e) => setSaveBeatName(e.target.value)}
                placeholder="Name this beat"
                style={{
                  height: 34,
                  borderRadius: 10,
                  border: "1px solid #333",
                  background: "#0f0f1a",
                  color: "#fff",
                  padding: "0 10px",
                  fontWeight: 700,
                  fontSize: 12,
                  width: 220,
                }}
              />
              <button
                onClick={saveCurrentBeat}
                style={{
                  padding: "10px 16px",
                  borderRadius: 16,
                  border: "none",
                  cursor: "pointer",
                  background: "linear-gradient(90deg,#e74c3c,#9b59b6)",
                  color: "#fff",
                  fontWeight: 900,
                  fontSize: 12,
                }}
              >
                Save
              </button>

              <select
                value={selectedBeatId}
                onChange={(e) => { setSelectedBeatId(e.target.value); setExportJson(""); }}
                style={{
                  height: 34,
                  borderRadius: 10,
                  border: "1px solid #333",
                  background: "#0f0f1a",
                  color: "#fff",
                  padding: "0 10px",
                  fontWeight: 700,
                  fontSize: 12,
                  minWidth: 260,
                }}
              >
                <option value="">Select a saved beat…</option>
                {savedBeats.map((b) => (
                  <option key={b.id} value={b.id}>{b.name}</option>
                ))}
              </select>

              <button
                onClick={() => loadBeatById(selectedBeatId)}
                disabled={!selectedBeatId}
                style={{
                  padding: "10px 16px",
                  borderRadius: 16,
                  border: "none",
                  cursor: selectedBeatId ? "pointer" : "not-allowed",
                  background: selectedBeatId ? "#2ecc71" : "#444",
                  color: "#0f0f1a",
                  fontWeight: 900,
                  fontSize: 12,
                }}
              >
                Load
              </button>

              <button
                onClick={() => deleteBeatById(selectedBeatId)}
                disabled={!selectedBeatId}
                style={{
                  padding: "10px 16px",
                  borderRadius: 16,
                  border: "1px solid #555",
                  cursor: selectedBeatId ? "pointer" : "not-allowed",
                  background: "transparent",
                  color: "#aaa",
                  fontWeight: 800,
                  fontSize: 12,
                }}
              >
                Delete
              </button>

              <button
                onClick={exportSelectedBeat}
                disabled={!selectedBeatId}
                style={{
                  padding: "10px 16px",
                  borderRadius: 16,
                  border: "1px solid #555",
                  cursor: selectedBeatId ? "pointer" : "not-allowed",
                  background: "transparent",
                  color: "#aaa",
                  fontWeight: 800,
                  fontSize: 12,
                }}
              >
                Export
              </button>
            </div>

            {saveBeatError && (
              <div style={{ color: "#ff8080", fontSize: 12, marginTop: 8 }}>
                {saveBeatError}
              </div>
            )}

            <div style={{ marginTop: 10, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
              <div>
                <div style={{ color: "#555", fontSize: 11, marginBottom: 6 }}>Export JSON</div>
                <textarea
                  value={exportJson}
                  readOnly
                  rows={6}
                  style={{
                    width: "100%",
                    borderRadius: 10,
                    border: "1px solid #333",
                    background: "#0f0f1a",
                    color: "#fff",
                    padding: 10,
                    fontSize: 11,
                    resize: "vertical",
                  }}
                />
              </div>
              <div>
                <div style={{ color: "#555", fontSize: 11, marginBottom: 6 }}>Import JSON</div>
                <textarea
                  value={importJson}
                  onChange={(e) => setImportJson(e.target.value)}
                  rows={6}
                  placeholder="Paste beat JSON here"
                  style={{
                    width: "100%",
                    borderRadius: 10,
                    border: "1px solid #333",
                    background: "#0f0f1a",
                    color: "#fff",
                    padding: 10,
                    fontSize: 11,
                    resize: "vertical",
                  }}
                />
                <div style={{ marginTop: 8 }}>
                  <button
                    onClick={importBeatFromJson}
                    disabled={!importJson.trim()}
                    style={{
                      padding: "8px 16px",
                      borderRadius: 16,
                      border: "none",
                      cursor: importJson.trim() ? "pointer" : "not-allowed",
                      background: importJson.trim() ? "#3498db" : "#444",
                      color: "#fff",
                      fontWeight: 900,
                      fontSize: 12,
                    }}
                  >
                    Import
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Volume sliders */}
          <div style={{ marginTop: 16 }}>
            <div style={{ color: "#aaa", fontSize: 12, marginBottom: 8 }}>Track Volumes</div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 8 }}>
              {TRACKS.map((tr, i) => (
                <div key={i} style={{ display: "flex", alignItems: "center", gap: 6 }}>
                  <span style={{ fontSize: 10, color: tr.color, width: 52 }}>{tr.name}</span>
                  <input type="range" min="0" max="1" step="0.05" value={volumes[i]}
                    onChange={e => setVolumes(v => v.map((x,j) => j===i ? +e.target.value : x))}
                    style={{ flex: 1, accentColor: tr.color }} />
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* RECORD TAB */}
      {tab === "record" && (
        <div style={{ maxWidth: 500, margin: "0 auto" }}>
          <div style={{ background: "#1a1a2e", borderRadius: 16, padding: 20, marginBottom: 16 }}>
            <div style={{ color: "#9b59b6", fontWeight: 700, marginBottom: 8 }}>📝 Write Your Lyrics</div>
            <textarea value={recText} onChange={e => setRecText(e.target.value)}
              placeholder={"Write your rap lyrics here...\n\nExample:\nI wake up every morning with a plan in mind\nGonna grind all day and leave the doubt behind..."}
              style={{ width: "100%", height: 160, background: "#0f0f1a", color: "#fff", border: "1px solid #333", borderRadius: 8, padding: 10, fontSize: 13, resize: "vertical", boxSizing: "border-box" }} />
            <div style={{ fontSize: 11, color: "#555", marginTop: 4 }}>
              {recText.split(/\s+/).filter(Boolean).length} words · {recText.split("\n").filter(Boolean).length} lines
            </div>
          </div>

          <div style={{ background: "#1a1a2e", borderRadius: 16, padding: 20 }}>
            <div style={{ color: "#e74c3c", fontWeight: 700, marginBottom: 12 }}>🎤 Record Your Voice</div>
            <p style={{ color: "#aaa", fontSize: 12, marginBottom: 16 }}>
              Hit Play on the Beats tab to hear your beat while recording. Then press Record here to capture your voice!
            </p>
            <div style={{ display: "flex", justifyContent: "center", marginBottom: 12 }}>
              <label style={{ display: "flex", alignItems: "center", gap: 8, color: "#aaa", fontSize: 12 }}>
                <input
                  type="checkbox"
                  checked={syncRecordingWithBeat}
                  onChange={(e) => setSyncRecordingWithBeat(e.target.checked)}
                />
                Sync recording with beat (restart from step 1)
              </label>
            </div>
            <div style={{ display: "flex", gap: 10, justifyContent: "center" }}>
              <button onClick={micRecording ? stopMic : startMic} style={{
                padding: "12px 28px", borderRadius: 24, border: "none", cursor: "pointer",
                background: micRecording ? "#e74c3c" : "linear-gradient(90deg,#9b59b6,#e74c3c)",
                color: "#fff", fontWeight: 800, fontSize: 15
              }}>
                {micRecording ? "⏹ Stop Recording" : "⏺ Record"}
              </button>
            </div>
            {micRecording && (
              <div style={{ textAlign: "center", marginTop: 12, color: "#e74c3c", fontWeight: 700, animation: "pulse 1s infinite" }}>
                🔴 Recording...
              </div>
            )}
            {audioURL && (
              <div style={{ marginTop: 16 }}>
                <div style={{ color: "#2ecc71", fontWeight: 700, marginBottom: 8 }}>✅ Recording saved!</div>
                <audio controls src={audioURL} style={{ width: "100%" }} />
                <a href={audioURL} download="my_vocals.webm" style={{
                  display: "inline-block", marginTop: 8, padding: "6px 16px",
                  background: "#2ecc71", borderRadius: 12, color: "#fff", fontSize: 12, textDecoration: "none", fontWeight: 700
                }}>⬇ Download Vocals</a>
              </div>
            )}

            <div style={{ marginTop: 18, paddingTop: 18, borderTop: "1px solid #232343" }}>
              <div style={{ color: "#3498db", fontWeight: 700, marginBottom: 10 }}>🎚️ Record Full Mix (Voice + Beat)</div>
              <p style={{ color: "#aaa", fontSize: 12, marginBottom: 14 }}>
                This records what you hear: your beat + backing track + your microphone into one downloadable file.
              </p>
              <div style={{ display: "flex", gap: 10, justifyContent: "center", flexWrap: "wrap" }}>
                <button onClick={mixRecording ? stopMixRecord : startMixRecord} style={{
                  padding: "12px 28px", borderRadius: 24, border: "none", cursor: "pointer",
                  background: mixRecording ? "#e74c3c" : "linear-gradient(90deg,#3498db,#2ecc71)",
                  color: "#fff", fontWeight: 800, fontSize: 15
                }}>
                  {mixRecording ? "⏹ Stop Mix" : "⏺ Record Mix"}
                </button>
              </div>
              {mixRecording && (
                <div style={{ textAlign: "center", marginTop: 12, color: "#e74c3c", fontWeight: 700, animation: "pulse 1s infinite" }}>
                  🔴 Recording mix...
                </div>
              )}
              {mixURL && (
                <div style={{ marginTop: 16 }}>
                  <div style={{ color: "#2ecc71", fontWeight: 700, marginBottom: 8 }}>✅ Mix saved!</div>
                  <audio controls src={mixURL} style={{ width: "100%" }} />
                  <a href={mixURL} download="my_mix.webm" style={{
                    display: "inline-block", marginTop: 8, padding: "6px 16px",
                    background: "#2ecc71", borderRadius: 12, color: "#fff", fontSize: 12, textDecoration: "none", fontWeight: 700
                  }}>⬇ Download Mix</a>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* MIX TAB */}
      {tab === "mix" && (
        <div style={{ maxWidth: 500, margin: "0 auto" }}>
          <div style={{ background: "#1a1a2e", borderRadius: 16, padding: 20 }}>
            <div style={{ color: "#3498db", fontWeight: 700, fontSize: 16, marginBottom: 16 }}>🎚️ Mix Your Track</div>

            <div style={{ marginBottom: 20 }}>
              <div style={{ color: "#aaa", fontSize: 12, marginBottom: 8 }}>Beat Volume</div>
              <input type="range" min="0" max="1" step="0.05" value={mixVolBeat}
                onChange={e => setMixVolBeat(+e.target.value)}
                style={{ width: "100%", accentColor: "#e74c3c" }} />
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, color: "#555" }}>
                <span>Quiet</span><span style={{ color: "#e74c3c", fontWeight: 700 }}>{Math.round(mixVolBeat*100)}%</span><span>Loud</span>
              </div>
            </div>

            <div style={{ marginBottom: 20 }}>
              <div style={{ color: "#aaa", fontSize: 12, marginBottom: 8 }}>Voice Volume</div>
              <input type="range" min="0" max="1" step="0.05" value={mixVolVoice}
                onChange={e => setMixVolVoice(+e.target.value)}
                style={{ width: "100%", accentColor: "#9b59b6" }} />
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, color: "#555" }}>
                <span>Quiet</span><span style={{ color: "#9b59b6", fontWeight: 700 }}>{Math.round(mixVolVoice*100)}%</span><span>Loud</span>
              </div>
            </div>

            <div style={{ background: "#0f0f1a", borderRadius: 12, padding: 14, marginBottom: 16 }}>
              <div style={{ color: "#f1c40f", fontWeight: 700, marginBottom: 8 }}>Mix Balance</div>
              <div style={{ display: "flex", height: 20, borderRadius: 10, overflow: "hidden" }}>
                <div style={{ width: `${mixVolBeat/(mixVolBeat+mixVolVoice)*100}%`, background: "#e74c3c", transition: "width 0.2s" }} />
                <div style={{ flex: 1, background: "#9b59b6" }} />
              </div>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, color: "#aaa", marginTop: 4 }}>
                <span>🥁 Beat</span><span>🎤 Voice</span>
              </div>
            </div>

            <div style={{ background: "#0f0f1a", borderRadius: 12, padding: 14 }}>
              <div style={{ color: "#2ecc71", fontWeight: 700, marginBottom: 8 }}>🎛️ Pro Mixing Tips</div>
              {[
                "Voice should be 10-20% louder than the beat",
                "Lower the bass when your kick hits hard",
                "Add reverb to voice for a studio feel",
                "A limiter on the master keeps things from distorting"
              ].map((t,i) => (
                <div key={i} style={{ fontSize: 12, color: "#aaa", marginBottom: 6, paddingLeft: 12, borderLeft: "2px solid #2ecc71" }}>
                  {t}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* TIPS TAB */}
      {tab === "tips" && (
        <div style={{ maxWidth: 500, margin: "0 auto" }}>
          <div style={{ background: "#1a1a2e", borderRadius: 16, padding: 20, marginBottom: 16 }}>
            <div style={{ color: "#f1c40f", fontWeight: 700, fontSize: 16, marginBottom: 12 }}>🔥 Tip of the Moment</div>
            <div style={{ background: "#0f0f1a", borderRadius: 12, padding: 16, fontSize: 15, lineHeight: 1.6, color: "#fff", marginBottom: 12 }}>
              {tips[tip]}
            </div>
            <button onClick={() => setTip(t => (t+1) % tips.length)} style={{
              padding: "8px 20px", borderRadius: 16, border: "none", cursor: "pointer",
              background: "#f1c40f", color: "#000", fontWeight: 700
            }}>Next Tip ➡</button>
          </div>

          <div style={{ background: "#1a1a2e", borderRadius: 16, padding: 20, marginBottom: 16 }}>
            <div style={{ color: "#e74c3c", fontWeight: 700, marginBottom: 12 }}>📚 How to Make a Rap Song</div>
            {[
              ["1️⃣ Make your beat","Go to the Beats tab. Turn steps on/off to build a rhythm. Classic hip-hop: Kick on 1 & 3, Snare on 2 & 4."],
              ["2️⃣ Write your lyrics","Go to the Record tab and write your verses, hook, and bridge."],
              ["3️⃣ Record your voice","Hit Play on your beat, then record yourself rapping in the Record tab."],
              ["4️⃣ Mix it together","Head to the Mix tab and balance your beat and vocals. Vocals slightly louder!"],
              ["5️⃣ Save & share","Download your vocal recording and use free tools like GarageBand or BandLab to layer it on top of your beat."],
            ].map(([title, body], i) => (
              <div key={i} style={{ marginBottom: 14, paddingLeft: 12, borderLeft: "3px solid #e74c3c" }}>
                <div style={{ fontWeight: 700, marginBottom: 4 }}>{title}</div>
                <div style={{ fontSize: 12, color: "#aaa" }}>{body}</div>
              </div>
            ))}
          </div>

          <div style={{ background: "#1a1a2e", borderRadius: 16, padding: 20 }}>
            <div style={{ color: "#9b59b6", fontWeight: 700, marginBottom: 12 }}>🛠️ Level Up — Free Pro Tools</div>
            {[
              ["BandLab (free, online)", "Full DAW in your browser — record, mix, add effects"],
              ["GarageBand (Mac/iOS free)", "Apple's beginner-friendly music studio"],
              ["LMMS (free desktop)", "Similar to FL Studio, fully free"],
              ["Audacity (free desktop)", "Record & edit audio like a pro"],
            ].map(([name, desc], i) => (
              <div key={i} style={{ marginBottom: 10 }}>
                <span style={{ color: "#9b59b6", fontWeight: 700 }}>{name}</span>
                <div style={{ fontSize: 12, color: "#aaa" }}>{desc}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
