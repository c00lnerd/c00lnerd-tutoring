/**
 * 3D Parametric Mathematical Art - JavaScript Implementation
 * Interactive exploration of 3D mathematical beauty through parametric equations
 */

class ParametricArt3D {
    constructor() {
        this.canvas = document.getElementById('artCanvas');
        this.ctx = this.canvas.getContext('2d');
        
        // Animation state
        this.time = 0;
        this.isPlaying = true;
        this.animationId = null;
        
        // 3D transformation parameters
        this.rotationX = 0;
        this.rotationY = 0;
        this.panX = 0;
        this.panY = 0;
        this.zoom = 1.0;
        this.focalLength = 400;
        this.zOffset = -300;
        
        // Pattern parameters
        this.pattern = 1;
        this.speed = 1.0;
        this.trailMode = 'fading';
        this.maxTrailLength = 500;
        
        // Trail storage - array of arrays, one for each trail
        this.trails = [];
        for (let i = 0; i < 12; i++) {
            this.trails.push([]);
        }
        
        // Colors for different trails
        this.colors = [
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD',
            '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9', '#F8C471', '#82E0AA'
        ];
        
        // Mouse interaction
        this.mouseDown = false;
        this.lastMouseX = 0;
        this.lastMouseY = 0;
        this.shiftPressed = false;
        
        this.initializeControls();
        this.setupEventListeners();
        this.animate();
    }
    
    // ===== 3D MATHEMATICS =====
    
    rotate3DPoint(x, y, z) {
        // Invert rotation angles for object rotation (not camera rotation)
        const rotY = -this.rotationY;
        const rotX = -this.rotationX;
        
        // Rotate around Y-axis first (horizontal mouse movement)
        const xRot = x * Math.cos(rotY) - z * Math.sin(rotY);
        const zRot = x * Math.sin(rotY) + z * Math.cos(rotY);
        
        // Then rotate around X-axis (vertical mouse movement)
        const yRot = y * Math.cos(rotX) - zRot * Math.sin(rotX);
        const zFinal = y * Math.sin(rotX) + zRot * Math.cos(rotX);
        
        return [xRot, yRot, zFinal];
    }
    
    projectTo2D(x, y, z) {
        // Perspective projection
        if (z > -50) z = -50; // Prevent division by zero
        
        const screenX = 450 + (x * this.focalLength * this.zoom) / (-z) + this.panX;
        const screenY = 300 + (y * this.focalLength * this.zoom) / (-z) + this.panY;
        
        return [screenX, screenY, z];
    }
    
    // ===== PARAMETRIC PATTERNS =====
    
    flowerPattern3D(t) {
        const points = [];
        
        // Object 1: True 3D Rose using spherical coordinates
        const theta1 = t * 2;
        const phi1 = t * 1.5;
        const a1 = 80, m1 = 4, n1 = 3, k1 = 2;
        const rho1 = a1 * Math.cos(m1 * theta1) * Math.pow(Math.abs(Math.cos(n1 * phi1)), k1);
        const x1 = rho1 * Math.cos(theta1) * Math.cos(phi1);
        const y1 = rho1 * Math.sin(theta1) * Math.cos(phi1);
        const z1 = this.zOffset + rho1 * Math.sin(phi1);
        points.push([x1, y1, z1, 0]);
        
        // Object 2: 3D Lissajous curve
        const x2 = 100 * Math.sin(t * 2.1);
        const y2 = 80 * Math.sin(t * 3.2);
        const z2 = this.zOffset + 60 * Math.sin(t * 1.7);
        points.push([x2, y2, z2, 1]);
        
        // Object 3: 3D Spiral
        const r3 = 80 + 20 * Math.sin(t * 0.5);
        const x3 = r3 * Math.cos(t * 1.5);
        const y3 = r3 * Math.sin(t * 1.5);
        const z3 = this.zOffset + t * 3;
        points.push([x3, y3, z3, 2]);
        
        // Object 4: Figure-8 with Z variation
        const scale4 = 90;
        const x4 = scale4 * Math.sin(t * 1.8);
        const y4 = scale4 * Math.sin(t * 1.8) * Math.cos(t * 1.8);
        const z4 = this.zOffset + 50 * Math.sin(t * 2.3);
        points.push([x4, y4, z4, 3]);
        
        // Object 5: 3D Epicycloid
        const R5 = 60, r5 = 20;
        const x5 = (R5 + r5) * Math.cos(t * 0.9) - r5 * Math.cos((R5 + r5) / r5 * t * 0.9);
        const y5 = (R5 + r5) * Math.sin(t * 0.9) - r5 * Math.sin((R5 + r5) / r5 * t * 0.9);
        const z5 = this.zOffset + 40 * Math.sin(t * 1.1);
        points.push([x5, y5, z5, 4]);
        
        // Object 6: 3D Butterfly curve
        const eT = Math.exp(Math.cos(t * 1.3)) - 2 * Math.cos(4 * t * 1.3) - Math.pow(Math.sin(t * 1.3 / 12), 5);
        const x6 = 30 * Math.sin(t * 1.3) * eT;
        const y6 = 30 * Math.cos(t * 1.3) * eT;
        const z6 = this.zOffset + 30 * Math.sin(t * 2.1);
        points.push([x6, y6, z6, 5]);
        
        return points;
    }
    
    synchronizedLissajous(t) {
        const points = [];
        for (let i = 0; i < 6; i++) {
            const phase = i * Math.PI / 3;
            const x = 120 * Math.sin(t * 1.5 + phase);
            const y = 100 * Math.sin(t * 2.0 + phase);
            const z = this.zOffset + 80 * Math.sin(t * 1.2 + phase);
            points.push([x, y, z, i]);
        }
        return points;
    }
    
    spiralGalaxy(t) {
        const points = [];
        for (let i = 0; i < 6; i++) {
            const armOffset = i * Math.PI / 3;
            const r = 20 + t * 2 + i * 10;
            const theta = t * 0.8 + armOffset;
            const x = r * Math.cos(theta);
            const y = r * Math.sin(theta);
            const z = this.zOffset + 30 * Math.sin(t * 1.5 + armOffset);
            points.push([x, y, z, i]);
        }
        return points;
    }
    
    dnaHelix(t) {
        const points = [];
        for (let i = 0; i < 2; i++) {
            const phase = i * Math.PI;
            const x = 80 * Math.cos(t * 1.2 + phase);
            const y = 80 * Math.sin(t * 1.2 + phase);
            const z = this.zOffset + t * 4;
            points.push([x, y, z, i]);
        }
        
        // Connecting rungs
        for (let i = 0; i < 4; i++) {
            const phase = i * Math.PI / 2;
            const x = 40 * Math.cos(t * 1.2 + phase);
            const y = 40 * Math.sin(t * 1.2 + phase);
            const z = this.zOffset + t * 4 + i * 20;
            points.push([x, y, z, i + 2]);
        }
        
        return points;
    }
    
    singleLissajous(t) {
        const x = 120 * Math.sin(t * 1.8);
        const y = 100 * Math.sin(t * 2.5);
        const z = this.zOffset + 60 * Math.sin(t * 0.7);
        return [[x, y, z, 0]];
    }
    
    single3DRose(t) {
        // Smooth 3D Rose using spherical coordinates
        const theta = t * 1.2;
        const phi = t * 0.8;
        const a = 100, m = 3, n = 2, k = 0.8;
        
        // Natural cosine function for authentic 3D rose shape
        const rho = a * (0.5 + 0.5 * Math.cos(m * theta)) * Math.pow(0.7 + 0.3 * Math.cos(n * phi), k);
        const x = rho * Math.cos(theta) * Math.cos(phi);
        const y = rho * Math.sin(theta) * Math.cos(phi);
        const z = this.zOffset + rho * Math.sin(phi);
        
        return [[x, y, z, 0]];
    }
    
    getPatternPoints3D(t) {
        switch (this.pattern) {
            case 1: return this.flowerPattern3D(t);
            case 2: return this.synchronizedLissajous(t);
            case 3: return this.spiralGalaxy(t);
            case 4: return this.dnaHelix(t);
            case 5: return this.singleLissajous(t);
            case 6: return this.single3DRose(t);
            default: return this.flowerPattern3D(t);
        }
    }
    
    // ===== RENDERING =====
    
    blendColor(color1, color2, factor) {
        const hex1 = color1.replace('#', '');
        const hex2 = color2.replace('#', '');
        
        const r1 = parseInt(hex1.substr(0, 2), 16);
        const g1 = parseInt(hex1.substr(2, 2), 16);
        const b1 = parseInt(hex1.substr(4, 2), 16);
        
        const r2 = parseInt(hex2.substr(0, 2), 16);
        const g2 = parseInt(hex2.substr(2, 2), 16);
        const b2 = parseInt(hex2.substr(4, 2), 16);
        
        const r = Math.round(r1 * (1 - factor) + r2 * factor);
        const g = Math.round(g1 * (1 - factor) + g2 * factor);
        const b = Math.round(b1 * (1 - factor) + b2 * factor);
        
        return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
    }
    
    draw() {
        // Clear canvas
        this.ctx.fillStyle = '#000000';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Get current 3D points
        const points3D = this.getPatternPoints3D(this.time);
        
        // Add points to trails
        for (const [x, y, z, trailId] of points3D) {
            this.trails[trailId].push([x, y, z]);
            
            // Limit trail length
            if (this.trails[trailId].length > this.maxTrailLength) {
                this.trails[trailId].shift();
            }
        }
        
        // Draw trails
        for (let trailId = 0; trailId < this.trails.length; trailId++) {
            const trail = this.trails[trailId];
            if (trail.length < 2) continue;
            
            const baseColor = this.colors[trailId % this.colors.length];
            
            // Project trail points with rotation
            const projectedTrail = [];
            const centerX = 0, centerY = 0, centerZ = this.zOffset;
            
            for (const [x3d, y3d, z3d] of trail) {
                // Apply rotation around object center
                const relX = x3d - centerX;
                const relY = y3d - centerY;
                const relZ = z3d - centerZ;
                
                const [xRot, yRot, zRot] = this.rotate3DPoint(relX, relY, relZ);
                
                const finalX = xRot + centerX;
                const finalY = yRot + centerY;
                const finalZ = zRot + centerZ;
                
                const [screenX, screenY, depth] = this.projectTo2D(finalX, finalY, finalZ);
                projectedTrail.push([screenX, screenY, depth]);
            }
            
            // Draw trail segments
            for (let i = 1; i < projectedTrail.length; i++) {
                const [prevX, prevY, prevDepth] = projectedTrail[i - 1];
                const [currX, currY, currDepth] = projectedTrail[i];
                
                // Check for discontinuities (skip long jumps)
                const lineLength = Math.sqrt((currX - prevX) ** 2 + (currY - prevY) ** 2);
                if (lineLength > 150) continue;
                
                // Depth-based sizing
                const avgDepth = (prevDepth + currDepth) / 2;
                const depthFactor = Math.max(0.2, Math.min(1.0, (-avgDepth - 200) / 400));
                
                let lineColor, width;
                
                if (this.trailMode === 'persistent') {
                    lineColor = baseColor;
                    width = Math.max(1, Math.round(2 * depthFactor));
                } else {
                    // Fading trails
                    const alpha = i / projectedTrail.length;
                    if (alpha > 0.9) {
                        lineColor = baseColor;
                        width = Math.round(4 * depthFactor);
                    } else if (alpha > 0.7) {
                        lineColor = this.blendColor(baseColor, '#FFFFFF', 0.3);
                        width = Math.round(3 * depthFactor);
                    } else if (alpha > 0.5) {
                        lineColor = this.blendColor(baseColor, '#888888', 0.5);
                        width = Math.round(2 * depthFactor);
                    } else {
                        lineColor = '#222222';
                        width = 1;
                    }
                }
                
                if (width > 0 && prevX > 0 && currX > 0) {
                    this.ctx.strokeStyle = lineColor;
                    this.ctx.lineWidth = width;
                    this.ctx.lineCap = 'round';
                    this.ctx.beginPath();
                    this.ctx.moveTo(prevX, prevY);
                    this.ctx.lineTo(currX, currY);
                    this.ctx.stroke();
                }
            }
        }
        
        // Draw current points as glowing dots
        for (const [x, y, z, trailId] of points3D) {
            // Apply same rotation as trails
            const centerX = 0, centerY = 0, centerZ = this.zOffset;
            const relX = x - centerX;
            const relY = y - centerY;
            const relZ = z - centerZ;
            
            const [xRot, yRot, zRot] = this.rotate3DPoint(relX, relY, relZ);
            
            const finalX = xRot + centerX;
            const finalY = yRot + centerY;
            const finalZ = zRot + centerZ;
            
            const [screenX, screenY, depth] = this.projectTo2D(finalX, finalY, finalZ);
            const baseColor = this.colors[trailId % this.colors.length];
            
            // Size based on depth
            const depthFactor = Math.max(0.3, Math.min(1.0, (-depth - 200) / 300));
            const radius = Math.round(5 * depthFactor);
            
            if (radius > 0 && screenX > 0 && screenY > 0) {
                // Outer glow
                const glowColor = this.blendColor(baseColor, '#FFFFFF', 0.7);
                this.ctx.fillStyle = glowColor;
                this.ctx.beginPath();
                this.ctx.arc(screenX, screenY, radius + 1, 0, 2 * Math.PI);
                this.ctx.fill();
                
                // Main dot
                this.ctx.fillStyle = baseColor;
                this.ctx.strokeStyle = 'white';
                this.ctx.lineWidth = 1;
                this.ctx.beginPath();
                this.ctx.arc(screenX, screenY, radius, 0, 2 * Math.PI);
                this.ctx.fill();
                this.ctx.stroke();
                
                // Inner highlight
                const highlightRadius = Math.max(1, Math.round(radius / 2));
                this.ctx.fillStyle = 'white';
                this.ctx.beginPath();
                this.ctx.arc(screenX, screenY, highlightRadius, 0, 2 * Math.PI);
                this.ctx.fill();
            }
        }
        
        // Draw 3D axis indicator
        this.draw3DAxisIndicator();
        
        // Draw info text
        this.drawInfoText();
    }
    
    draw3DAxisIndicator() {
        const centerX = 850, centerY = 550;
        const axisLength = 40;
        
        // Background circle
        this.ctx.fillStyle = '#000000';
        this.ctx.strokeStyle = '#333333';
        this.ctx.lineWidth = 1;
        this.ctx.beginPath();
        this.ctx.arc(centerX, centerY, 45, 0, 2 * Math.PI);
        this.ctx.fill();
        this.ctx.stroke();
        
        // Axis vectors
        const axes = [
            [axisLength, 0, 0, '#FF4444', 'X'],
            [0, axisLength, 0, '#44FF44', 'Y'],
            [0, 0, axisLength, '#4444FF', 'Z']
        ];
        
        for (const [ax, ay, az, color, label] of axes) {
            const [xRot, yRot, zRot] = this.rotate3DPoint(ax, ay, az);
            
            const endX = centerX + xRot;
            const endY = centerY + yRot;
            
            // Line thickness based on depth
            const depthFactor = Math.max(0.3, (zRot + axisLength) / (2 * axisLength));
            const lineWidth = Math.max(1, Math.round(3 * depthFactor));
            
            // Draw axis line
            this.ctx.strokeStyle = color;
            this.ctx.lineWidth = lineWidth;
            this.ctx.lineCap = 'round';
            this.ctx.beginPath();
            this.ctx.moveTo(centerX, centerY);
            this.ctx.lineTo(endX, endY);
            this.ctx.stroke();
            
            // Draw label if pointing towards viewer
            if (depthFactor > 0.5) {
                this.ctx.fillStyle = color;
                this.ctx.font = 'bold 12px Arial';
                this.ctx.textAlign = 'center';
                this.ctx.fillText(label, endX + 10, endY + 5);
            }
        }
        
        // Center dot
        this.ctx.fillStyle = 'white';
        this.ctx.beginPath();
        this.ctx.arc(centerX, centerY, 2, 0, 2 * Math.PI);
        this.ctx.fill();
    }
    
    drawInfoText() {
        this.ctx.fillStyle = 'cyan';
        this.ctx.font = '14px Arial';
        this.ctx.textAlign = 'center';
        
        const trailModeText = this.trailMode === 'persistent' ? 'Persistent' : 'Fading';
        const zoomText = `${this.zoom.toFixed(1)}x`;
        
        this.ctx.fillText(
            `🖱️ Drag: rotate | ⇧+Drag: pan | 🖱️ Wheel: zoom`,
            450, 25
        );
        
        this.ctx.fillText(
            `Pattern ${this.pattern} | Trail: ${trailModeText} | Speed: ${this.speed.toFixed(1)}x | Zoom: ${zoomText}`,
            450, 580
        );
    }
    
    // ===== ANIMATION =====
    
    animate() {
        if (this.isPlaying) {
            this.time += 0.05 * this.speed;
        }
        
        this.draw();
        
        this.animationId = requestAnimationFrame(() => this.animate());
    }
    
    // ===== EVENT HANDLERS =====
    
    setupEventListeners() {
        // Mouse events
        this.canvas.addEventListener('mousedown', (e) => this.onMouseDown(e));
        this.canvas.addEventListener('mousemove', (e) => this.onMouseMove(e));
        this.canvas.addEventListener('mouseup', () => this.onMouseUp());
        this.canvas.addEventListener('wheel', (e) => this.onWheel(e));
        
        // Keyboard events
        document.addEventListener('keydown', (e) => {
            this.shiftPressed = e.shiftKey;
        });
        
        document.addEventListener('keyup', (e) => {
            this.shiftPressed = e.shiftKey;
        });
        
        // Prevent context menu
        this.canvas.addEventListener('contextmenu', (e) => e.preventDefault());
    }
    
    onMouseDown(e) {
        this.mouseDown = true;
        this.lastMouseX = e.clientX;
        this.lastMouseY = e.clientY;
    }
    
    onMouseMove(e) {
        if (!this.mouseDown) return;
        
        const dx = e.clientX - this.lastMouseX;
        const dy = e.clientY - this.lastMouseY;
        
        if (this.shiftPressed) {
            // Pan
            this.panX += dx;
            this.panY += dy;
        } else {
            // Rotate
            this.rotationY += dx * 0.01;
            this.rotationX += dy * 0.01;
        }
        
        this.lastMouseX = e.clientX;
        this.lastMouseY = e.clientY;
    }
    
    onMouseUp() {
        this.mouseDown = false;
    }
    
    onWheel(e) {
        e.preventDefault();
        const zoomFactor = e.deltaY > 0 ? 0.9 : 1.1;
        this.zoom = Math.max(0.1, Math.min(5.0, this.zoom * zoomFactor));
        document.getElementById('zoomSlider').value = this.zoom;
        document.getElementById('zoomValue').textContent = `${this.zoom.toFixed(1)}x`;
    }
    
    // ===== UI CONTROLS =====
    
    initializeControls() {
        // Pattern selection
        document.getElementById('patternSelect').addEventListener('change', (e) => {
            this.pattern = parseInt(e.target.value);
            this.updatePatternInfo();
            this.resetTrails();
        });
        
        // Speed control
        document.getElementById('speedSlider').addEventListener('input', (e) => {
            this.speed = parseFloat(e.target.value);
            document.getElementById('speedValue').textContent = `${this.speed.toFixed(1)}x`;
        });
        
        // Trail mode
        document.getElementById('trailMode').addEventListener('change', (e) => {
            this.trailMode = e.target.value;
        });
        
        // Zoom control
        document.getElementById('zoomSlider').addEventListener('input', (e) => {
            this.zoom = parseFloat(e.target.value);
            document.getElementById('zoomValue').textContent = `${this.zoom.toFixed(1)}x`;
        });
        
        // Play/Pause button
        document.getElementById('playPauseBtn').addEventListener('click', () => {
            this.isPlaying = !this.isPlaying;
            document.getElementById('playPauseBtn').textContent = this.isPlaying ? '⏸️ Pause' : '▶️ Play';
        });
        
        // Reset button
        document.getElementById('resetBtn').addEventListener('click', () => {
            this.resetView();
        });
        
        this.updatePatternInfo();
    }
    
    updatePatternInfo() {
        const info = document.getElementById('patternInfo');
        const descriptions = {
            1: 'Six independent mathematical objects creating a complex 3D art display',
            2: 'Synchronized Lissajous curves with phase offsets',
            3: 'Spiral galaxy arms expanding outward in 3D space',
            4: 'DNA double helix with connecting base pairs',
            5: 'Single Lissajous curve - perfect for testing rotation',
            6: 'Pure 3D rose using spherical coordinate mathematics'
        };
        info.textContent = descriptions[this.pattern] || descriptions[1];
    }
    
    resetTrails() {
        for (let i = 0; i < this.trails.length; i++) {
            this.trails[i] = [];
        }
    }
    
    resetView() {
        this.rotationX = 0;
        this.rotationY = 0;
        this.panX = 0;
        this.panY = 0;
        this.zoom = 1.0;
        this.time = 0;
        document.getElementById('zoomSlider').value = 1.0;
        document.getElementById('zoomValue').textContent = '1.0x';
        this.resetTrails();
    }
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new ParametricArt3D();
});
