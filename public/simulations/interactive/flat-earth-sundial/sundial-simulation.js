class SundialSimulation {
    constructor() {
        this.isPlaying = false;
        this.animationId = null;
        this.currentDate = new Date('2025-06-21T12:00:00Z');
        this.latitude = 40;
        this.longitude = -74;
        this.gnomonHeight = 10; // cm
        
        this.flatEarthCanvas = document.getElementById('flatEarthCanvas');
        this.sphericalEarthCanvas = document.getElementById('sphericalEarthCanvas');
        this.flatCtx = this.flatEarthCanvas.getContext('2d');
        this.sphericalCtx = this.sphericalEarthCanvas.getContext('2d');
        
        this.setupEventListeners();
        this.updateSimulation();
    }
    
    setupEventListeners() {
        document.getElementById('dateInput').addEventListener('change', (e) => {
            const timeStr = document.getElementById('timeInput').value;
            this.currentDate = new Date(`${e.target.value}T${timeStr}:00Z`);
            this.updateSimulation();
        });
        
        document.getElementById('timeInput').addEventListener('change', (e) => {
            const dateStr = document.getElementById('dateInput').value;
            this.currentDate = new Date(`${dateStr}T${e.target.value}:00Z`);
            this.updateSimulation();
        });
        
        document.getElementById('latInput').addEventListener('input', (e) => {
            this.latitude = parseFloat(e.target.value);
            this.updateSimulation();
        });
        
        document.getElementById('lonInput').addEventListener('input', (e) => {
            this.longitude = parseFloat(e.target.value);
            this.updateSimulation();
        });
        
        document.getElementById('gnomonHeight').addEventListener('input', (e) => {
            this.gnomonHeight = parseFloat(e.target.value);
            this.updateSimulation();
        });
        
        document.getElementById('playButton').addEventListener('click', () => {
            this.toggleAnimation();
        });
        
        document.getElementById('resetButton').addEventListener('click', () => {
            this.resetSimulation();
        });
    }
    
    toggleAnimation() {
        if (this.isPlaying) {
            this.stopAnimation();
        } else {
            this.startAnimation();
        }
    }
    
    startAnimation() {
        this.isPlaying = true;
        document.getElementById('playButton').textContent = 'Pause Animation';
        this.animate();
    }
    
    stopAnimation() {
        this.isPlaying = false;
        document.getElementById('playButton').textContent = 'Play Animation';
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
    }
    
    animate() {
        if (!this.isPlaying) return;
        
        // Advance time by 5 minutes
        this.currentDate.setMinutes(this.currentDate.getMinutes() + 5);
        
        // Update time input
        const timeStr = this.currentDate.toISOString().substr(11, 5);
        document.getElementById('timeInput').value = timeStr;
        
        this.updateSimulation();
        
        this.animationId = requestAnimationFrame(() => {
            setTimeout(() => this.animate(), 200); // 200ms delay between frames
        });
    }
    
    resetSimulation() {
        this.stopAnimation();
        this.currentDate = new Date('2025-06-21T12:00:00Z');
        document.getElementById('dateInput').value = '2025-06-21';
        document.getElementById('timeInput').value = '12:00';
        this.updateSimulation();
    }
    
    updateSimulation() {
        const sunData = this.calculateSolarPosition();
        this.drawFlatEarthSundial(sunData);
        this.drawSphericalEarthSundial(sunData);
        this.updateDataDisplay(sunData);
    }
    
    calculateSolarPosition() {
        const dayOfYear = this.getDayOfYear(this.currentDate);
        const localTime = this.currentDate.getUTCHours() + this.currentDate.getUTCMinutes() / 60;
        
        // Solar declination (simplified)
        const declination = 23.45 * Math.sin(Math.PI * (284 + dayOfYear) / 365 * Math.PI / 180);
        
        // Hour angle from local solar noon
        const hourAngle = 15 * (localTime - 12); // degrees from solar noon
        
        // Convert to radians
        const latRad = this.latitude * Math.PI / 180;
        const decRad = declination * Math.PI / 180;
        const hourRad = hourAngle * Math.PI / 180;
        
        // Solar elevation
        const elevation = Math.asin(
            Math.sin(decRad) * Math.sin(latRad) + 
            Math.cos(decRad) * Math.cos(latRad) * Math.cos(hourRad)
        ) * 180 / Math.PI;
        
        // Solar azimuth
        const azimuth = Math.atan2(
            Math.sin(hourRad),
            Math.cos(hourRad) * Math.sin(latRad) - Math.tan(decRad) * Math.cos(latRad)
        ) * 180 / Math.PI + 180;
        
        return {
            elevation: elevation,
            azimuth: azimuth,
            declination: declination,
            hourAngle: hourAngle,
            dayOfYear: dayOfYear,
            localTime: localTime
        };
    }
    
    getDayOfYear(date) {
        const start = new Date(date.getFullYear(), 0, 0);
        const diff = date - start;
        return Math.floor(diff / (1000 * 60 * 60 * 24));
    }
    
    drawFlatEarthSundial(sunData) {
        const canvas = this.flatEarthCanvas;
        const ctx = this.flatCtx;
        const width = canvas.width;
        const height = canvas.height;
        
        // Clear canvas
        ctx.clearRect(0, 0, width, height);
        
        // Draw background
        ctx.fillStyle = '#e3f2fd';
        ctx.fillRect(0, 0, width, height);
        
        // Draw ground
        ctx.fillStyle = '#8bc34a';
        ctx.fillRect(0, height * 0.7, width, height * 0.3);
        
        // Center point for sundial
        const centerX = width / 2;
        const centerY = height * 0.7;
        
        // Draw sundial base
        ctx.fillStyle = '#795548';
        ctx.beginPath();
        ctx.arc(centerX, centerY, 80, 0, 2 * Math.PI);
        ctx.fill();
        
        // Draw hour markings
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 2;
        for (let hour = 0; hour < 24; hour++) {
            const angle = (hour - 6) * 15 * Math.PI / 180; // 6 AM at bottom
            const x1 = centerX + 70 * Math.cos(angle);
            const y1 = centerY + 70 * Math.sin(angle);
            const x2 = centerX + 60 * Math.cos(angle);
            const y2 = centerY + 60 * Math.sin(angle);
            
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.stroke();
            
            // Hour labels
            if (hour % 3 === 0) {
                ctx.fillStyle = '#333';
                ctx.font = '12px Arial';
                ctx.textAlign = 'center';
                const labelX = centerX + 85 * Math.cos(angle);
                const labelY = centerY + 85 * Math.sin(angle) + 4;
                ctx.fillText(hour.toString(), labelX, labelY);
            }
        }
        
        // Flat Earth sun position calculation
        // Sun moves in a circle above the flat earth plane
        // 0 hours = midnight (north), 6 hours = sunrise (east), 12 hours = noon (south), 18 hours = sunset (west)
        const timeAngle = (sunData.localTime - 6) * 15; // degrees from east (sunrise)
        
        // In flat earth model, sun circles above at constant height
        // Distance from observer: closest at noon (south), farthest at midnight (north)
        const baseDistance = 120;
        const maxDistance = 250;
        
        // Calculate distance based on time - closest at noon, farthest at midnight
        const noonDistance = Math.abs(sunData.localTime - 12); // Hours from noon
        const distanceFromNoon = Math.min(noonDistance, 24 - noonDistance); // Handle wrap-around
        const sunDistance = baseDistance + (maxDistance - baseDistance) * (distanceFromNoon / 12);
        
        // Sun position: East (6AM) -> South (12PM) -> West (6PM) -> North (12AM)
        const sunX = centerX + sunDistance * Math.cos(timeAngle * Math.PI / 180);
        const sunY = centerY - 100 - 20 * Math.cos(distanceFromNoon * Math.PI / 12); // Varying apparent height
        
        // Sun size varies with distance (perspective effect)
        const baseSunSize = 25;
        const sunSize = baseSunSize * (baseDistance / sunDistance);
        
        // Draw sun with variable size
        ctx.fillStyle = '#ffeb3b';
        ctx.beginPath();
        ctx.arc(sunX, sunY, sunSize, 0, 2 * Math.PI);
        ctx.fill();
        
        // Draw sun rays (scaled with sun size)
        ctx.strokeStyle = '#ffeb3b';
        ctx.lineWidth = 2;
        const rayLength = sunSize * 1.5;
        for (let i = 0; i < 8; i++) {
            const rayAngle = i * Math.PI / 4;
            const x1 = sunX + (sunSize + 5) * Math.cos(rayAngle);
            const y1 = sunY + (sunSize + 5) * Math.sin(rayAngle);
            const x2 = sunX + (sunSize + rayLength) * Math.cos(rayAngle);
            const y2 = sunY + (sunSize + rayLength) * Math.sin(rayAngle);
            
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.stroke();
        }
        
        // Draw gnomon (vertical stick)
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(centerX, centerY - this.gnomonHeight * 3); // Scale for display
        ctx.stroke();
        
        // Calculate flat earth shadow - sun is always above horizon in flat earth model
        let flatShadowAngle = 0;
        let flatShadowLength = 0;
        
        const dx = sunX - centerX;
        const dy = sunY - centerY;
        const gnomonDisplayHeight = this.gnomonHeight * 3;
        
        // In flat earth model, calculate shadow based on sun's 3D position
        // Shadow points directly away from sun on the ground plane
        if (Math.abs(dx) > 0.1 || Math.abs(dy) > 0.1) {
            // Calculate shadow direction (opposite to sun direction)
            flatShadowAngle = Math.atan2(-dx, dy) * 180 / Math.PI; // Shadow points away from sun
            
            // Calculate shadow length based on sun's apparent elevation
            const sunElevationAngle = Math.atan2(-(sunY - centerY), Math.sqrt(dx * dx + (sunY - centerY) * (sunY - centerY)));
            if (sunElevationAngle > 0) {
                flatShadowLength = gnomonDisplayHeight / Math.tan(sunElevationAngle);
            } else {
                flatShadowLength = gnomonDisplayHeight * 2; // Long shadow when sun is low
            }
            
            // Draw shadow - always present in flat earth model
            const shadowScale = Math.min(0.8, 50 / flatShadowLength); // Scale for display, max length
            const shadowEndX = centerX - dx * shadowScale;
            const shadowEndY = centerY - dy * shadowScale * 0.3; // Flatten the shadow on ground
            
            ctx.strokeStyle = 'rgba(0,0,0,0.5)';
            ctx.lineWidth = 6;
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.lineTo(shadowEndX, shadowEndY);
            ctx.stroke();
        } else {
            // When sun is directly overhead
            flatShadowLength = 0;
            flatShadowAngle = 0;
        }
        
        // Calculate flat earth time based on sun's apparent position
        // In flat earth model, time is determined by sun's position in its circular path
        // Sun at east = 6 AM, south = 12 PM, west = 6 PM, north = 12 AM
        const sunAngleFromEast = Math.atan2(sunY - centerY, sunX - centerX) * 180 / Math.PI;
        let flatEarthTime = 6 + (sunAngleFromEast / 15); // Convert angle to hours from 6 AM
        
        // Normalize to 0-24 hour range
        while (flatEarthTime < 0) flatEarthTime += 24;
        while (flatEarthTime >= 24) flatEarthTime -= 24;
        
        const flatTimeHours = Math.floor(flatEarthTime);
        const flatTimeMinutes = Math.floor((flatEarthTime - flatTimeHours) * 60);
        
        // Update display
        document.getElementById('flatEarthTime').textContent = 
            `${flatTimeHours % 12 || 12}:${flatTimeMinutes.toString().padStart(2, '0')} ${flatTimeHours >= 12 ? 'PM' : 'AM'}`;
        document.getElementById('flatShadowLength').textContent = Math.abs(flatShadowLength).toFixed(1);
        document.getElementById('flatShadowAngle').textContent = Math.round(flatShadowAngle);
        
        return { time: flatEarthTime, shadowLength: flatShadowLength, shadowAngle: flatShadowAngle };
    }
    
    drawSphericalEarthSundial(sunData) {
        const canvas = this.sphericalEarthCanvas;
        const ctx = this.sphericalCtx;
        const width = canvas.width;
        const height = canvas.height;
        
        // Clear canvas
        ctx.clearRect(0, 0, width, height);
        
        // Draw background
        ctx.fillStyle = '#e8f5e8';
        ctx.fillRect(0, 0, width, height);
        
        // Draw ground
        ctx.fillStyle = '#4caf50';
        ctx.fillRect(0, height * 0.7, width, height * 0.3);
        
        // Center point for sundial
        const centerX = width / 2;
        const centerY = height * 0.7;
        
        // Draw sundial base
        ctx.fillStyle = '#795548';
        ctx.beginPath();
        ctx.arc(centerX, centerY, 80, 0, 2 * Math.PI);
        ctx.fill();
        
        // Draw hour markings (properly calculated for spherical earth)
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 2;
        for (let hour = 6; hour <= 18; hour++) {
            const hourAngle = (hour - 12) * 15; // degrees from solar noon
            const hourAngleRad = hourAngle * Math.PI / 180;
            const latRad = this.latitude * Math.PI / 180;
            const decRad = sunData.declination * Math.PI / 180;
            
            // Calculate proper sundial angle accounting for latitude and declination
            const sundialAngle = Math.atan2(
                Math.sin(hourAngleRad),
                Math.cos(hourAngleRad) * Math.sin(latRad) - Math.tan(decRad) * Math.cos(latRad)
            );
            
            const x1 = centerX + 70 * Math.sin(sundialAngle);
            const y1 = centerY - 70 * Math.cos(sundialAngle);
            const x2 = centerX + 60 * Math.sin(sundialAngle);
            const y2 = centerY - 60 * Math.cos(sundialAngle);
            
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.stroke();
            
            // Hour labels
            if (hour % 3 === 0) {
                ctx.fillStyle = '#333';
                ctx.font = '12px Arial';
                ctx.textAlign = 'center';
                const labelX = centerX + 85 * Math.sin(sundialAngle);
                const labelY = centerY - 85 * Math.cos(sundialAngle) + 4;
                ctx.fillText(hour.toString(), labelX, labelY);
            }
        }
        
        // Draw sun (realistic position)
        if (sunData.elevation > 0) {
            const sunDistance = 150;
            const sunX = centerX + sunDistance * Math.sin(sunData.azimuth * Math.PI / 180);
            const sunY = centerY - sunDistance * Math.cos(sunData.azimuth * Math.PI / 180) - sunData.elevation * 2;
            
            ctx.fillStyle = '#ffeb3b';
            ctx.beginPath();
            ctx.arc(sunX, sunY, 15, 0, 2 * Math.PI);
            ctx.fill();
            
            // Draw sun rays
            ctx.strokeStyle = '#ffeb3b';
            ctx.lineWidth = 2;
            for (let i = 0; i < 8; i++) {
                const rayAngle = i * Math.PI / 4;
                const x1 = sunX + 20 * Math.cos(rayAngle);
                const y1 = sunY + 20 * Math.sin(rayAngle);
                const x2 = sunX + 28 * Math.cos(rayAngle);
                const y2 = sunY + 28 * Math.sin(rayAngle);
                
                ctx.beginPath();
                ctx.moveTo(x1, y1);
                ctx.lineTo(x2, y2);
                ctx.stroke();
            }
        }
        
        // Draw gnomon
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(centerX, centerY - this.gnomonHeight * 3);
        ctx.stroke();
        
        // Calculate real shadow
        let realShadowLength = 0;
        let realShadowAngle = 0;
        let realTime = sunData.hour;
        
        if (sunData.elevation > 0) {
            realShadowLength = this.gnomonHeight / Math.tan(sunData.elevation * Math.PI / 180);
            realShadowAngle = sunData.azimuth + 180; // Shadow points opposite to sun
            if (realShadowAngle >= 360) realShadowAngle -= 360;
            
            // Draw shadow - correct direction calculation
            const shadowEndX = centerX + realShadowLength * 2 * Math.sin(realShadowAngle * Math.PI / 180);
            const shadowEndY = centerY - realShadowLength * 2 * Math.cos(realShadowAngle * Math.PI / 180);
            
            ctx.strokeStyle = 'rgba(0,0,0,0.6)';
            ctx.lineWidth = 6;
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.lineTo(shadowEndX, shadowEndY);
            ctx.stroke();
        }
        
        // Update display - use local time
        const localTime = sunData.localTime;
        const realTimeHours = Math.floor(localTime);
        const realTimeMinutes = Math.floor((localTime - realTimeHours) * 60);
        document.getElementById('sphericalEarthTime').textContent = 
            `${realTimeHours % 12 || 12}:${realTimeMinutes.toString().padStart(2, '0')} ${realTimeHours >= 12 ? 'PM' : 'AM'}`;
        document.getElementById('realShadowLength').textContent = Math.abs(realShadowLength).toFixed(1);
        document.getElementById('realShadowAngle').textContent = Math.round(realShadowAngle);
        
        return { time: localTime, shadowLength: realShadowLength, shadowAngle: realShadowAngle };
    }
    
    updateDataDisplay(sunData) {
        // Update sun position data
        document.getElementById('solarElevation').textContent = `${sunData.elevation.toFixed(1)}°`;
        document.getElementById('solarAzimuth').textContent = `${sunData.azimuth.toFixed(1)}°`;
        document.getElementById('hourAngle').textContent = `${sunData.hourAngle.toFixed(1)}°`;
        document.getElementById('declination').textContent = `${sunData.declination.toFixed(1)}°`;
        
        // Get sundial data
        const flatData = this.getLastFlatEarthData();
        const realData = this.getLastSphericalEarthData();
        
        // Calculate differences
        const timeDiff = Math.abs(flatData.time - realData.time) * 60; // minutes
        const shadowLengthDiff = Math.abs(flatData.shadowLength - realData.shadowLength);
        const shadowAngleDiff = Math.abs(flatData.shadowAngle - realData.shadowAngle);
        const accuracyError = (timeDiff / 60) * 100; // percentage based on hour difference
        
        document.getElementById('timeDifference').textContent = `${timeDiff.toFixed(0)} minutes`;
        document.getElementById('shadowLengthDiff').textContent = `${shadowLengthDiff.toFixed(1)} cm`;
        document.getElementById('shadowAngleDiff').textContent = `${shadowAngleDiff.toFixed(0)}°`;
        document.getElementById('accuracyError').textContent = `${accuracyError.toFixed(1)}%`;
        
        // Update explanation based on conditions
        this.updateExplanation(sunData, timeDiff, accuracyError);
    }
    
    getLastFlatEarthData() {
        // This would normally store the last calculated values
        // For simplicity, we'll recalculate
        const flatEarthSunAngle = (this.currentDate.getUTCHours() + this.currentDate.getUTCMinutes() / 60 - 6) * 15;
        const flatEarthTime = 6 + (flatEarthSunAngle / 15);
        return {
            time: flatEarthTime,
            shadowLength: 5, // simplified
            shadowAngle: flatEarthSunAngle
        };
    }
    
    getLastSphericalEarthData() {
        const hour = this.currentDate.getUTCHours() + this.currentDate.getUTCMinutes() / 60;
        const sunData = this.calculateSolarPosition();
        const shadowLength = sunData.elevation > 0 ? this.gnomonHeight / Math.tan(sunData.elevation * Math.PI / 180) : 0;
        return {
            time: hour,
            shadowLength: shadowLength,
            shadowAngle: sunData.azimuth - 180
        };
    }
    
    updateExplanation(sunData, timeDiff, accuracyError) {
        const explanationBox = document.getElementById('explanationBox');
        
        if (accuracyError > 50) {
            explanationBox.className = 'explanation error';
            explanationBox.innerHTML = `
                <h4>Major Discrepancy Detected!</h4>
                <p>The flat earth sundial is showing a ${accuracyError.toFixed(1)}% error compared to reality. This demonstrates fundamental problems with the flat earth model:</p>
                <ul>
                    <li><strong>Seasonal Effects:</strong> The sun's declination (${sunData.declination.toFixed(1)}°) cannot be properly modeled on a flat earth.</li>
                    <li><strong>Latitude Dependency:</strong> Real sundials must be calibrated for specific latitudes, but flat earth theory suggests uniform behavior.</li>
                    <li><strong>Shadow Geometry:</strong> The shadow patterns don't match what would be expected from a sun moving in a circle above a flat plane.</li>
                </ul>
            `;
        } else if (accuracyError > 20) {
            explanationBox.className = 'explanation warning';
            explanationBox.innerHTML = `
                <h4>Significant Differences Observed</h4>
                <p>The flat earth sundial shows ${accuracyError.toFixed(1)}% error. Key issues include:</p>
                <ul>
                    <li>Incorrect shadow angles due to simplified sun movement model</li>
                    <li>Failure to account for Earth's axial tilt and orbital mechanics</li>
                    <li>Time discrepancy of ${timeDiff.toFixed(0)} minutes shows the model's limitations</li>
                </ul>
            `;
        } else {
            explanationBox.className = 'explanation success';
            explanationBox.innerHTML = `
                <h4>Models Appear Similar (But This Is Misleading)</h4>
                <p>While the current error is only ${accuracyError.toFixed(1)}%, this similarity is temporary and location-dependent:</p>
                <ul>
                    <li>Try different dates, especially solstices and equinoxes</li>
                    <li>Test extreme latitudes (near poles or equator)</li>
                    <li>The flat earth model fails catastrophically in many conditions</li>
                    <li>Real sundials have been accurately predicting time for thousands of years using spherical earth principles</li>
                </ul>
            `;
        }
    }
}

// Initialize simulation when page loads
document.addEventListener('DOMContentLoaded', () => {
    new SundialSimulation();
});
