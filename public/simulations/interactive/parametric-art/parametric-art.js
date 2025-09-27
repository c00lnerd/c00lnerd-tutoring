// Parametric Mathematical Art Simulation
// Based on the beautiful mathematical art code provided

class ParametricArt {
    constructor() {
        this.canvas = document.getElementById('artCanvas');
        this.ctx = this.canvas.getContext('2d');
        
        // Animation parameters
        this.t = 0;
        this.isAnimating = true;
        this.animationId = null;
        
        // Drawing parameters
        this.points = [];
        this.maxPoints = 100;
        this.centerX = this.canvas.width / 2;
        this.centerY = this.canvas.height / 2;
        
        // Mathematical parameters (matching the original code structure)
        this.params = {
            a: 1.0,
            b: 1.0, 
            c: 1.0,
            d: 1.0,
            speed: 1.0,
            scale: 100,
            trailLength: 100
        };
        
        // Color cycling
        this.colorPhase = 0;
        
        this.initializeControls();
        this.setupCanvas();
        this.startAnimation();
    }
    
    initializeControls() {
        // Parameter sliders
        const sliders = ['a', 'b', 'c', 'd', 'speed', 'scale', 'trailLength'];
        
        sliders.forEach(param => {
            const slider = document.getElementById(param + 'Slider');
            const display = document.getElementById(param + 'Value');
            
            if (slider && display) {
                slider.addEventListener('input', (e) => {
                    const value = parseFloat(e.target.value);
                    this.params[param === 'trailLength' ? 'trailLength' : param] = value;
                    display.textContent = param === 'trailLength' ? value.toString() : value.toFixed(1);
                    
                    if (param === 'trailLength') {
                        this.maxPoints = value;
                    }
                });
                
                // Initialize display
                const initialValue = param === 'trailLength' ? this.params.trailLength : this.params[param];
                display.textContent = param === 'trailLength' ? initialValue.toString() : initialValue.toFixed(1);
            }
        });
    }
    
    setupCanvas() {
        // Set up canvas with high DPI support
        const rect = this.canvas.getBoundingClientRect();
        const dpr = window.devicePixelRatio || 1;
        
        this.canvas.width = rect.width * dpr;
        this.canvas.height = rect.height * dpr;
        
        this.ctx.scale(dpr, dpr);
        this.canvas.style.width = rect.width + 'px';
        this.canvas.style.height = rect.height + 'px';
        
        this.centerX = rect.width / 2;
        this.centerY = rect.height / 2;
        
        // Set initial canvas properties
        this.ctx.lineCap = 'round';
        this.ctx.lineJoin = 'round';
        this.ctx.globalCompositeOperation = 'lighter';
    }
    
    // Core parametric equation calculation (based on the original code)
    calculatePoint(t) {
        const { a, b, c, d, scale } = this.params;
        
        // Original equations from the provided code:
        // x = a * sin(b * t + c) * cos(d * t)
        // y = a * cos(b * t + c) * sin(d * t)
        
        const x = a * Math.sin(b * t + c) * Math.cos(d * t) * scale + this.centerX;
        const y = a * Math.cos(b * t + c) * Math.sin(d * t) * scale + this.centerY;
        
        return { x, y };
    }
    
    // Enhanced version with more complex patterns
    calculateComplexPoint(t) {
        const { a, b, c, d, scale } = this.params;
        
        // More complex parametric equations for varied patterns
        const freq1 = b * t;
        const freq2 = d * t;
        const phase = c;
        
        const x = a * (Math.sin(freq1 + phase) * Math.cos(freq2) + 
                      0.3 * Math.sin(3 * freq1) * Math.cos(freq2 / 2)) * scale + this.centerX;
        const y = a * (Math.cos(freq1 + phase) * Math.sin(freq2) + 
                      0.3 * Math.cos(3 * freq1) * Math.sin(freq2 / 2)) * scale + this.centerY;
        
        return { x, y };
    }
    
    updateAnimation() {
        if (!this.isAnimating) return;
        
        // Calculate new point
        const point = this.calculatePoint(this.t);
        
        // Add color information
        this.colorPhase += 0.02;
        const hue = (this.colorPhase * 180 + this.t * 50) % 360;
        point.color = `hsl(${hue}, 80%, 60%)`;
        point.alpha = 1.0;
        
        // Add to points array
        this.points.push(point);
        
        // Limit points array length
        if (this.points.length > this.maxPoints) {
            this.points.shift();
        }
        
        // Update time parameter
        this.t += 0.02 * this.params.speed;
        
        this.draw();
        this.animationId = requestAnimationFrame(() => this.updateAnimation());
    }
    
    draw() {
        // Fade effect instead of complete clear
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        if (this.points.length < 2) return;
        
        // Draw the trail
        for (let i = 1; i < this.points.length; i++) {
            const prev = this.points[i - 1];
            const curr = this.points[i];
            
            // Calculate alpha based on age
            const age = (this.points.length - i) / this.points.length;
            const alpha = Math.pow(age, 0.5);
            
            // Draw line segment
            this.ctx.beginPath();
            this.ctx.moveTo(prev.x, prev.y);
            this.ctx.lineTo(curr.x, curr.y);
            
            // Use gradient for smooth color transitions
            const gradient = this.ctx.createLinearGradient(prev.x, prev.y, curr.x, curr.y);
            gradient.addColorStop(0, prev.color.replace('60%)', `${alpha * 60}%)`));
            gradient.addColorStop(1, curr.color.replace('60%)', `${alpha * 60}%)`));
            
            this.ctx.strokeStyle = gradient;
            this.ctx.lineWidth = alpha * 3 + 0.5;
            this.ctx.stroke();
        }
        
        // Draw current point with glow effect
        if (this.points.length > 0) {
            const current = this.points[this.points.length - 1];
            
            // Outer glow
            this.ctx.beginPath();
            this.ctx.arc(current.x, current.y, 8, 0, Math.PI * 2);
            this.ctx.fillStyle = current.color.replace('60%)', '30%)');
            this.ctx.fill();
            
            // Inner bright point
            this.ctx.beginPath();
            this.ctx.arc(current.x, current.y, 3, 0, Math.PI * 2);
            this.ctx.fillStyle = current.color;
            this.ctx.fill();
        }
    }
    
    startAnimation() {
        if (!this.isAnimating) {
            this.isAnimating = true;
            this.updateAnimation();
        }
    }
    
    stopAnimation() {
        this.isAnimating = false;
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
    }
    
    clear() {
        this.ctx.fillStyle = 'rgba(0, 0, 0, 1)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        this.points = [];
        this.t = 0;
        this.colorPhase = 0;
    }
    
    saveImage() {
        const link = document.createElement('a');
        link.download = `parametric-art-${Date.now()}.png`;
        link.href = this.canvas.toDataURL();
        link.click();
    }
}

// Preset configurations
const presets = {
    flower: { a: 2.0, b: 3.0, c: 1.5, d: 2.0, speed: 0.8, scale: 80 },
    spiral: { a: 1.5, b: 1.0, c: 0.5, d: 4.0, speed: 1.2, scale: 120 },
    butterfly: { a: 2.5, b: 2.0, c: 3.14, d: 1.0, speed: 0.6, scale: 90 },
    heart: { a: 1.8, b: 1.0, c: 1.57, d: 2.0, speed: 0.7, scale: 100 },
    infinity: { a: 1.0, b: 2.0, c: 0, d: 1.0, speed: 1.0, scale: 150 },
    random: null // Will be generated randomly
};

// Global functions
let artInstance;

function initializeArt() {
    artInstance = new ParametricArt();
}

function clearCanvas() {
    if (artInstance) {
        artInstance.clear();
    }
}

function toggleAnimation() {
    if (artInstance) {
        if (artInstance.isAnimating) {
            artInstance.stopAnimation();
        } else {
            artInstance.startAnimation();
        }
    }
}

function saveImage() {
    if (artInstance) {
        artInstance.saveImage();
    }
}

function loadPreset(presetName) {
    if (!artInstance) return;
    
    let preset;
    if (presetName === 'random') {
        preset = {
            a: Math.random() * 3 + 0.5,
            b: Math.random() * 4 + 0.5,
            c: Math.random() * 6.28,
            d: Math.random() * 4 + 0.5,
            speed: Math.random() * 2 + 0.3,
            scale: Math.random() * 100 + 50
        };
    } else {
        preset = presets[presetName];
    }
    
    if (!preset) return;
    
    // Update sliders and parameters
    Object.keys(preset).forEach(param => {
        const slider = document.getElementById(param + 'Slider');
        const display = document.getElementById(param + 'Value');
        
        if (slider && display) {
            slider.value = preset[param];
            artInstance.params[param] = preset[param];
            display.textContent = preset[param].toFixed(1);
        }
    });
    
    // Clear and restart with new parameters
    artInstance.clear();
}

// Handle window resize
function handleResize() {
    if (artInstance) {
        artInstance.setupCanvas();
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', initializeArt);
window.addEventListener('resize', handleResize);

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    switch(e.key.toLowerCase()) {
        case ' ':
            e.preventDefault();
            toggleAnimation();
            break;
        case 'c':
            clearCanvas();
            break;
        case 's':
            if (e.ctrlKey) {
                e.preventDefault();
                saveImage();
            }
            break;
        case 'r':
            loadPreset('random');
            break;
    }
});

// Add mouse interaction for real-time parameter adjustment
document.addEventListener('mousemove', (e) => {
    if (artInstance && e.shiftKey) {
        const rect = artInstance.canvas.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width;
        const y = (e.clientY - rect.top) / rect.height;
        
        // Map mouse position to parameters
        artInstance.params.c = x * 6.28; // 0 to 2π
        artInstance.params.d = y * 5 + 0.1; // 0.1 to 5.1
        
        // Update displays
        document.getElementById('cValue').textContent = artInstance.params.c.toFixed(1);
        document.getElementById('dValue').textContent = artInstance.params.d.toFixed(1);
        document.getElementById('cSlider').value = artInstance.params.c;
        document.getElementById('dSlider').value = artInstance.params.d;
    }
});
