// Organic Parametric Art - Based on the user's original complex mathematical art code
// Creates flowing, plant-like patterns similar to the provided image

class OrganicParametricArt {
    constructor() {
        this.canvas = document.getElementById('artCanvas');
        this.ctx = this.canvas.getContext('2d');
        
        // Animation parameters
        this.t = 0;
        this.isAnimating = true;
        this.animationId = null;
        
        // Drawing parameters
        this.centerX = this.canvas.width / 2;
        this.centerY = this.canvas.height / 2;
        
        // Mathematical parameters (based on the original code structure)
        this.params = {
            a: 1.0,        // amplitude
            k: 4.0,        // main frequency
            phase: 0.0,    // phase shift
            complexity: 3.0, // complexity factor
            speed: 1.0,    // animation speed
            scale: 80,     // overall scale (smaller for creature)
            branches: 6    // number of branches
        };
        
        // Creature movement parameters
        this.creature = {
            x: this.centerX,
            y: this.centerY,
            vx: 0,
            vy: 0,
            direction: 0,
            wanderAngle: 0
        };
        
        // Color and visual parameters
        this.colorPhase = 0;
        this.points = [];
        
        this.initializeControls();
        this.setupCanvas();
        
        // Draw initial test pattern
        this.drawTestPattern();
        
        this.startAnimation();
    }
    
    initializeControls() {
        const sliders = ['a', 'k', 'phase', 'complexity', 'speed', 'scale', 'branches'];
        
        sliders.forEach(param => {
            const slider = document.getElementById(param + 'Slider');
            const display = document.getElementById(param + 'Value');
            
            if (slider && display) {
                slider.addEventListener('input', (e) => {
                    const value = parseFloat(e.target.value);
                    this.params[param] = value;
                    display.textContent = param === 'branches' ? value.toString() : value.toFixed(1);
                });
                
                // Initialize display
                const initialValue = this.params[param];
                display.textContent = param === 'branches' ? initialValue.toString() : initialValue.toFixed(1);
            }
        });
    }
    
    setupCanvas() {
        const rect = this.canvas.getBoundingClientRect();
        const dpr = window.devicePixelRatio || 1;
        
        this.canvas.width = rect.width * dpr;
        this.canvas.height = rect.height * dpr;
        
        this.ctx.scale(dpr, dpr);
        this.canvas.style.width = rect.width + 'px';
        this.canvas.style.height = rect.height + 'px';
        
        this.centerX = rect.width / 2;
        this.centerY = rect.height / 2;
        
        // Set canvas properties for organic look
        this.ctx.lineCap = 'round';
        this.ctx.lineJoin = 'round';
        this.ctx.globalCompositeOperation = 'source-over'; // Normal blending
    }
    
    drawTestPattern() {
        // Draw a simple test pattern to verify canvas is working
        this.ctx.strokeStyle = '#00ff88';
        this.ctx.lineWidth = 3;
        
        // Draw cross in center
        this.ctx.beginPath();
        this.ctx.moveTo(this.centerX - 50, this.centerY);
        this.ctx.lineTo(this.centerX + 50, this.centerY);
        this.ctx.moveTo(this.centerX, this.centerY - 50);
        this.ctx.lineTo(this.centerX, this.centerY + 50);
        this.ctx.stroke();
        
        console.log('Test pattern drawn at center:', this.centerX, this.centerY);
    }
    
    // Recreate the exact swimming creature from your Python code
    calculateCreaturePoint(t, armIndex = 0) {
        const { a, k, phase, complexity, scale } = this.params;
        
        // Based on your original Python code structure:
        // a=(x,y,d=mag(k=(4+sin(y*2-t)*3)*cos(x/29),e=y/8-13))=>point((q=3*sin(k*2)+.3/k+sin(y/25)*k*(9+4*sin(e*9-d*3+t*2)))+30*cos(e=d+200,q*sin(c)+d*39-220)
        
        // Multiple arms radiating from creature center
        const armAngle = (armIndex * Math.PI * 2 / this.params.branches) + this.creature.direction;
        
        // Arm length parameter (t represents distance along the arm)
        const armT = t;
        
        // Complex oscillations based on your original equations
        const y = armT * 10; // Scale factor for arm length
        const x = armAngle * 10; // Use angle as x component
        
        // Your original complex mathematical relationships
        const k_component = (4 + Math.sin(y * 2 - this.t) * 3) * Math.cos(x / 29);
        const e_component = y / 8 - 13;
        const d_component = Math.sqrt(k_component * k_component + e_component * e_component); // magnitude
        
        // Main arm calculation based on your formula
        const q = 3 * Math.sin(k_component * 2) + 0.3 / (k_component + 0.1) + 
                  Math.sin(y / 25) * k_component * (9 + 4 * Math.sin(e_component * 9 - d_component * 3 + this.t * 2));
        
        // Final position calculation
        const e_final = d_component + 200;
        const c = this.t * 0.5; // time-based oscillation
        
        const armX = q + 30 * Math.cos(e_final);
        const armY = q * Math.sin(c) + d_component * 39 - 220;
        
        // Scale and position relative to creature
        const finalX = this.creature.x + (Math.cos(armAngle) * armX + Math.sin(armAngle) * armY) * scale * 0.01;
        const finalY = this.creature.y + (Math.sin(armAngle) * armX - Math.cos(armAngle) * armY) * scale * 0.01;
        
        return { x: finalX, y: finalY };
    }
    
    // Update creature movement (wandering behavior)
    updateCreatureMovement() {
        const canvas = this.canvas;
        const margin = 100;
        
        // Wandering behavior - change direction randomly
        this.creature.wanderAngle += (Math.random() - 0.5) * 0.3;
        this.creature.direction += this.creature.wanderAngle * 0.1;
        
        // Calculate desired velocity
        const speed = 0.5;
        this.creature.vx += Math.cos(this.creature.direction) * 0.1;
        this.creature.vy += Math.sin(this.creature.direction) * 0.1;
        
        // Apply some drag
        this.creature.vx *= 0.95;
        this.creature.vy *= 0.95;
        
        // Limit speed
        const vel = Math.sqrt(this.creature.vx ** 2 + this.creature.vy ** 2);
        if (vel > speed) {
            this.creature.vx = (this.creature.vx / vel) * speed;
            this.creature.vy = (this.creature.vy / vel) * speed;
        }
        
        // Update position
        this.creature.x += this.creature.vx;
        this.creature.y += this.creature.vy;
        
        // Bounce off edges
        if (this.creature.x < margin) {
            this.creature.x = margin;
            this.creature.vx = Math.abs(this.creature.vx);
            this.creature.direction = Math.PI - this.creature.direction;
        }
        if (this.creature.x > canvas.width / (window.devicePixelRatio || 1) - margin) {
            this.creature.x = canvas.width / (window.devicePixelRatio || 1) - margin;
            this.creature.vx = -Math.abs(this.creature.vx);
            this.creature.direction = Math.PI - this.creature.direction;
        }
        if (this.creature.y < margin) {
            this.creature.y = margin;
            this.creature.vy = Math.abs(this.creature.vy);
            this.creature.direction = -this.creature.direction;
        }
        if (this.creature.y > canvas.height / (window.devicePixelRatio || 1) - margin) {
            this.creature.y = canvas.height / (window.devicePixelRatio || 1) - margin;
            this.creature.vy = -Math.abs(this.creature.vy);
            this.creature.direction = -this.creature.direction;
        }
    }
    
    // Alternative calculation for more feather-like patterns
    calculateFeatherPattern(t, branchIndex = 0) {
        const { a, k, phase, complexity, scale } = this.params;
        const branchOffset = (branchIndex * Math.PI * 2) / this.params.branches;
        
        // Feather-like parametric equations
        const mainT = k * t + phase + branchOffset;
        const detail = complexity * t;
        
        // Create feather spine and barbs
        const spine = Math.cos(t / 25);
        const barbs = Math.sin(detail) * Math.exp(-Math.abs(t % (Math.PI * 2) - Math.PI) / 2);
        
        const x = a * (Math.sin(mainT) * spine + barbs * 0.3) * scale + this.centerX;
        const y = a * (Math.cos(mainT) * spine + barbs * 0.2) * scale + this.centerY;
        
        return { x, y };
    }
    
    updateAnimation() {
        if (!this.isAnimating) return;
        
        // Clear canvas with black background (fade trail)
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.08)';
        this.ctx.fillRect(0, 0, this.canvas.width / (window.devicePixelRatio || 1), this.canvas.height / (window.devicePixelRatio || 1));
        
        // Update creature movement
        this.updateCreatureMovement();
        
        // Update color phase
        this.colorPhase += 0.01;
        
        // Draw the creature's organic body
        this.drawCreature();
        
        // Update time parameter
        this.t += 0.03 * this.params.speed;
        
        this.animationId = requestAnimationFrame(() => this.updateAnimation());
    }
    
    drawCreature() {
        // Draw each branch/appendage of the creature
        for (let branch = 0; branch < this.params.branches; branch++) {
            this.drawCreatureBranch(branch);
        }
    }
    
    drawCreatureBranch(armIndex) {
        const numSegments = 40;
        
        // Draw each arm extending outward from the creature center
        for (let i = 0; i < numSegments - 1; i++) {
            // t represents distance along the arm (from 0 outward)
            const t1 = i * 0.3;
            const t2 = (i + 1) * 0.3;
            
            const point1 = this.calculateCreaturePoint(t1, armIndex);
            const point2 = this.calculateCreaturePoint(t2, armIndex);
            
            // Calculate alpha based on distance from creature center
            const distance = Math.sqrt((point1.x - this.creature.x) ** 2 + (point1.y - this.creature.y) ** 2);
            const maxDistance = 100;
            const alpha = Math.max(0.1, 1 - (distance / maxDistance));
            
            // Arm tapering - stronger at base, weaker at tips
            const armAlpha = Math.max(0.2, 1 - (i / numSegments));
            const finalAlpha = alpha * armAlpha;
            
            // Color scheme matching the original - more monochromatic like the image
            const hue = (this.colorPhase * 60 + armIndex * 15) % 360;
            const saturation = 30 + Math.sin(this.t + i * 0.1) * 20; // Lower saturation for more natural look
            const lightness = 80 + Math.sin(this.t * 0.3 + i * 0.05) * 15; // Higher lightness like the original
            
            this.ctx.beginPath();
            this.ctx.moveTo(point1.x, point1.y);
            this.ctx.lineTo(point2.x, point2.y);
            this.ctx.strokeStyle = `hsla(${hue}, ${saturation}%, ${lightness}%, ${finalAlpha})`;
            this.ctx.lineWidth = 0.8; // Thinner lines like the original
            this.ctx.stroke();
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
        this.ctx.fillRect(0, 0, this.canvas.width / (window.devicePixelRatio || 1), this.canvas.height / (window.devicePixelRatio || 1));
        this.t = 0;
        this.colorPhase = 0;
        
        // Draw a test pattern to verify canvas is working
        this.ctx.strokeStyle = '#00ff88';
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.arc(this.centerX, this.centerY, 50, 0, Math.PI * 2);
        this.ctx.stroke();
        console.log('Canvas cleared and test circle drawn');
    }
    
    saveImage() {
        const link = document.createElement('a');
        link.download = `organic-parametric-art-${Date.now()}.png`;
        link.href = this.canvas.toDataURL();
        link.click();
    }
}

// Preset configurations for organic patterns
const organicPresets = {
    fern: { a: 1.2, k: 4.0, phase: 1.57, complexity: 3.0, speed: 0.8, scale: 180, branches: 6 },
    feather: { a: 1.5, k: 6.0, phase: 0, complexity: 4.0, speed: 1.0, scale: 200, branches: 8 },
    coral: { a: 0.8, k: 3.0, phase: 3.14, complexity: 5.0, speed: 0.6, scale: 220, branches: 12 },
    lightning: { a: 2.0, k: 8.0, phase: 0.5, complexity: 2.0, speed: 1.5, scale: 150, branches: 4 },
    tree: { a: 1.0, k: 2.0, phase: 1.0, complexity: 6.0, speed: 0.7, scale: 250, branches: 10 },
    random: null // Will be generated randomly
};

// Global functions
let organicArtInstance;

function initializeOrganicArt() {
    console.log('Initializing Organic Parametric Art...');
    organicArtInstance = new OrganicParametricArt();
    console.log('Organic Art initialized:', organicArtInstance);
}

function clearCanvas() {
    if (organicArtInstance) {
        organicArtInstance.clear();
    }
}

function toggleAnimation() {
    if (organicArtInstance) {
        if (organicArtInstance.isAnimating) {
            organicArtInstance.stopAnimation();
        } else {
            organicArtInstance.startAnimation();
        }
    }
}

function saveImage() {
    if (organicArtInstance) {
        organicArtInstance.saveImage();
    }
}

function loadPreset(presetName) {
    if (!organicArtInstance) return;
    
    let preset;
    if (presetName === 'random') {
        preset = {
            a: Math.random() * 2 + 0.5,
            k: Math.random() * 8 + 2,
            phase: Math.random() * 6.28,
            complexity: Math.random() * 6 + 1,
            speed: Math.random() * 2 + 0.3,
            scale: Math.random() * 150 + 100,
            branches: Math.floor(Math.random() * 10) + 4
        };
    } else {
        preset = organicPresets[presetName];
    }
    
    if (!preset) return;
    
    // Update sliders and parameters
    Object.keys(preset).forEach(param => {
        const slider = document.getElementById(param + 'Slider');
        const display = document.getElementById(param + 'Value');
        
        if (slider && display) {
            slider.value = preset[param];
            organicArtInstance.params[param] = preset[param];
            display.textContent = param === 'branches' ? preset[param].toString() : preset[param].toFixed(1);
        }
    });
    
    // Clear and restart with new parameters
    organicArtInstance.clear();
}

// Handle window resize
function handleResize() {
    if (organicArtInstance) {
        organicArtInstance.setupCanvas();
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', initializeOrganicArt);
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
