import { useState, useEffect, useRef, useCallback } from "react";

const STEPS = 16;
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

function createAudioCtx() {
  return new (window.AudioContext || window.webkitAudioContext)();
}

function playKick(ctx, t) {
  const o = ctx.createOscillator(), g = ctx.createGain();
  o.connect(g); g.connect(ctx.destination);
  o.frequency.setValueAtTime(150, t);
  o.frequency.exponentialRampToValueAtTime(0.001, t + 0.5);
  g.gain.setValueAtTime(1, t);
  g.gain.exponentialRampToValueAtTime(0.001, t + 0.5);
  o.start(t); o.stop(t + 0.5);
}

function playSnare(ctx, t) {
  const buf = ctx.createBuffer(1, ctx.sampleRate * 0.2, ctx.sampleRate);
  const d = buf.getChannelData(0);
  for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
  const src = ctx.createBufferSource(), g = ctx.createGain();
  const f = ctx.createBiquadFilter();
  f.type = "highpass"; f.frequency.value = 1000;
  src.buffer = buf; src.connect(f); f.connect(g); g.connect(ctx.destination);
  g.gain.setValueAtTime(0.8, t);
  g.gain.exponentialRampToValueAtTime(0.001, t + 0.2);
  src.start(t); src.stop(t + 0.2);
}

function playHihat(ctx, t, open = false) {
  const buf = ctx.createBuffer(1, ctx.sampleRate * (open ? 0.3 : 0.08), ctx.sampleRate);
  const d = buf.getChannelData(0);
  for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
  const src = ctx.createBufferSource(), g = ctx.createGain();
  const f = ctx.createBiquadFilter();
  f.type = "highpass"; f.frequency.value = 7000;
  src.buffer = buf; src.connect(f); f.connect(g); g.connect(ctx.destination);
  g.gain.setValueAtTime(0.4, t);
  g.gain.exponentialRampToValueAtTime(0.001, t + (open ? 0.3 : 0.08));
  src.start(t); src.stop(t + (open ? 0.3 : 0.08));
}

function playBass(ctx, t) {
  const o = ctx.createOscillator(), g = ctx.createGain();
  o.type = "sawtooth"; o.connect(g); g.connect(ctx.destination);
  o.frequency.setValueAtTime(80, t);
  g.gain.setValueAtTime(0.5, t);
  g.gain.exponentialRampToValueAtTime(0.001, t + 0.3);
  o.start(t); o.stop(t + 0.3);
}

function playClap(ctx, t) {
  const buf = ctx.createBuffer(1, ctx.sampleRate * 0.1, ctx.sampleRate);
  const d = buf.getChannelData(0);
  for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
  const src = ctx.createBufferSource(), g = ctx.createGain();
  const f = ctx.createBiquadFilter();
  f.type = "bandpass"; f.frequency.value = 1200; f.Q.value = 0.5;
  src.buffer = buf; src.connect(f); f.connect(g); g.connect(ctx.destination);
  g.gain.setValueAtTime(0.7, t);
  g.gain.exponentialRampToValueAtTime(0.001, t + 0.1);
  src.start(t); src.stop(t + 0.1);
}

function triggerSound(ctx, type, t) {
  try {
    if (type === "kick") playKick(ctx, t);
    else if (type === "snare") playSnare(ctx, t);
    else if (type === "hihat") playHihat(ctx, t, false);
    else if (type === "openhat") playHihat(ctx, t, true);
    else if (type === "bass") playBass(ctx, t);
    else if (type === "clap") playClap(ctx, t);
  } catch(e) {}
}

export default function BeatStudio() {
  const [pattern, setPattern] = useState(DEFAULT_PATTERN.map(r => [...r]));
  const [bpm, setBpm] = useState(DEFAULT_BPM);
  const [playing, setPlaying] = useState(false);
  const [curStep, setCurStep] = useState(-1);
  const [volumes, setVolumes] = useState(TRACKS.map(() => 0.8));
  const [recText, setRecText] = useState("");
  const [micRecording, setMicRecording] = useState(false);
  const [audioURL, setAudioURL] = useState(null);
  const [tab, setTab] = useState("beats");
  const [mixVolBeat, setMixVolBeat] = useState(0.8);
  const [mixVolVoice, setMixVolVoice] = useState(0.9);
  const [tip, setTip] = useState(0);

  const ctxRef = useRef(null);
  const stepRef = useRef(0);
  const nextTimeRef = useRef(0);
  const timerRef = useRef(null);
  const patternRef = useRef(pattern);
  const bpmRef = useRef(bpm);
  const volRef = useRef(volumes);
  const playingRef = useRef(false);
  const mediaRecRef = useRef(null);
  const chunksRef = useRef([]);
  const beatGainRef = useRef(null);
  const voiceGainRef = useRef(null);

  useEffect(() => { patternRef.current = pattern; }, [pattern]);
  useEffect(() => { bpmRef.current = bpm; }, [bpm]);
  useEffect(() => { volRef.current = volumes; }, [volumes]);

  const getCtx = () => {
    if (!ctxRef.current) ctxRef.current = createAudioCtx();
    return ctxRef.current;
  };

  const schedule = useCallback(() => {
    const ctx = getCtx();
    const secondsPerStep = 60 / bpmRef.current / 4;
    while (nextTimeRef.current < ctx.currentTime + 0.1) {
      const step = stepRef.current;
      setCurStep(step);
      TRACKS.forEach((tr, i) => {
        if (patternRef.current[i][step]) {
          const g = ctx.createGain();
          g.gain.value = volRef.current[i];
          g.connect(ctx.destination);
          triggerSound(ctx, tr.type, nextTimeRef.current);
        }
      });
      stepRef.current = (step + 1) % STEPS;
      nextTimeRef.current += secondsPerStep;
    }
  }, []);

  const startPlay = () => {
    const ctx = getCtx();
    if (ctx.state === "suspended") ctx.resume();
    stepRef.current = 0;
    nextTimeRef.current = ctx.currentTime + 0.05;
    playingRef.current = true;
    timerRef.current = setInterval(schedule, 25);
    setPlaying(true);
  };

  const stopPlay = () => {
    clearInterval(timerRef.current);
    playingRef.current = false;
    setPlaying(false);
    setCurStep(-1);
  };

  const togglePlay = () => playing ? stopPlay() : startPlay();

  const toggleStep = (track, step) => {
    setPattern(p => {
      const np = p.map(r => [...r]);
      np[track][step] = np[track][step] ? 0 : 1;
      return np;
    });
  };

  const clearPattern = () => setPattern(TRACKS.map(() => Array(STEPS).fill(0)));
  const resetPattern = () => setPattern(DEFAULT_PATTERN.map(r => [...r]));

  const startMic = async () => {
    try {
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
    } catch(e) {
      alert("Microphone access denied. Please allow mic access to record.");
    }
  };

  const stopMic = () => {
    mediaRecRef.current?.stop();
    setMicRecording(false);
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
          <div style={{ display: "grid", gridTemplateColumns: "72px repeat(16, 1fr)", gap: 3, marginBottom: 4 }}>
            <div />
            {Array.from({length:16},(_,i) => (
              <div key={i} style={{ textAlign: "center", fontSize: 10, color: i % 4 === 0 ? "#e74c3c" : "#555", fontWeight: i%4===0 ? 700 : 400 }}>
                {i%4===0 ? (i/4+1) : "·"}
              </div>
            ))}
          </div>

          {/* Sequencer Grid */}
          {TRACKS.map((tr, ti) => (
            <div key={ti} style={{ display: "grid", gridTemplateColumns: "72px repeat(16, 1fr)", gap: 3, marginBottom: 3 }}>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", paddingRight: 6 }}>
                <span style={{ fontSize: 11, color: tr.color, fontWeight: 700 }}>{tr.name}</span>
              </div>
              {Array.from({length:16},(_,si) => (
                <button key={si} onClick={() => toggleStep(ti,si)} style={{
                  height: 34, borderRadius: 5, border: "none", cursor: "pointer",
                  background: pattern[ti][si]
                    ? (curStep === si ? "#fff" : tr.color)
                    : (curStep === si ? "#2a2a40" : "#1a1a2e"),
                  transition: "background 0.05s",
                  boxShadow: pattern[ti][si] && curStep===si ? `0 0 8px ${tr.color}` : "none"
                }} />
              ))}
            </div>
          ))}

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
