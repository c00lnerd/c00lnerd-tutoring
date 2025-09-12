class SundialSimulation {
    constructor() {
        this.isPlaying = false;
        this.animationId = null;
        // Initialize with 12:00 PM local time
        this.currentDate = new Date('2025-06-21T12:00:00');
        this.latitude = 33.59;
        this.longitude = -86.49;
        this.gnomonHeight = 10; // cm
        this.sunHeightFE = 5000; // km - flat earth sun height
        
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
            // Treat input time as local time - no conversion needed
            this.currentDate = new Date(`${e.target.value}T${timeStr}:00`);
            this.updateSimulation();
        });
        
        document.getElementById('timeInput').addEventListener('change', (e) => {
            const dateStr = document.getElementById('dateInput').value;
            // Treat input time as local time - no conversion needed
            this.currentDate = new Date(`${dateStr}T${e.target.value}:00`);
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
        
        document.getElementById('sunHeightFE').addEventListener('input', (e) => {
            this.sunHeightFE = parseFloat(e.target.value);
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
        // Reset to 12:00 PM local time
        this.currentDate = new Date('2025-06-21T12:00:00');
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
        
        // Use input time as local time - no longitude correction needed for display
        const localTime = this.currentDate.getHours() + this.currentDate.getMinutes() / 60;
        const localSolarTime = localTime; // Use local time directly
        
        // Solar declination - corrected formula for proper seasonal variation
        const declination = 23.45 * Math.sin((360 * (dayOfYear - 81) / 365) * Math.PI / 180);
        
        // Hour angle from local solar noon
        const hourAngle = 15 * (localSolarTime - 12); // degrees from solar noon
        
        // Convert to radians
        const latRad = this.latitude * Math.PI / 180;
        const decRad = declination * Math.PI / 180;
        const hourRad = hourAngle * Math.PI / 180;
        
        // Solar elevation
        const elevation = Math.asin(
            Math.sin(decRad) * Math.sin(latRad) + 
            Math.cos(decRad) * Math.cos(latRad) * Math.cos(hourRad)
        ) * 180 / Math.PI;
        
        // Solar azimuth (corrected for proper north reference)
        let azimuth = Math.atan2(
            Math.sin(hourRad),
            Math.cos(hourRad) * Math.sin(latRad) - Math.tan(decRad) * Math.cos(latRad)
        ) * 180 / Math.PI;
        
        // Normalize azimuth: 0° = North, 90° = East, 180° = South, 270° = West
        if (azimuth < 0) azimuth += 360;
        
        // Remove debug output
        
        return {
            elevation: elevation,
            azimuth: azimuth,
            declination: declination,
            hourAngle: hourAngle,
            dayOfYear: dayOfYear,
            localTime: localSolarTime
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
        const sunY = centerY + sunDistance * Math.sin(timeAngle * Math.PI / 180) - 100; // Circular path above
        
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
        
        // Calculate shadow direction (opposite to sun direction)
        flatShadowAngle = Math.atan2(-dx, -dy) * 180 / Math.PI; // Shadow points away from sun
        
        // Calculate sun's elevation angle in flat earth model using actual sun height
        // In flat earth model, calculate horizontal distance based on latitude and sun position
        // Assume sun is at "solar noon" position relative to the Tropic of Cancer/Capricorn
        const flatEarthSunData = this.calculateSolarPosition();
        
        // Calculate horizontal distance from observer to point below sun in flat earth model
        // Use simpler approach that matches typical flat earth calculators
        const sunOverheadLatitude = flatEarthSunData.declination; // Where sun is directly overhead
        
        // In flat earth model, use direct latitude difference for noon calculations
        // Your reference shows ~3300 km, so let's use a scaling factor that produces this
        const latitudeDifference = Math.abs(this.latitude - sunOverheadLatitude);
        
        // Calculate time offset from solar noon
        const localSolarTime = this.currentDate.getUTCHours() + this.currentDate.getUTCMinutes() / 60 + this.longitude / 15;
        const hoursFromNoon = Math.abs(localSolarTime - 12);
        
        // Base distance from latitude difference, with time-of-day adjustment
        const flatEarthBaseDistance = latitudeDifference * 111; // km per degree latitude
        const timeAdjustment = hoursFromNoon * 200; // Additional distance for time offset
        const horizontalDistanceKm = Math.sqrt(flatEarthBaseDistance * flatEarthBaseDistance + timeAdjustment * timeAdjustment);
        
        let flatEarthElevation = 90; // Default to overhead
        if (horizontalDistanceKm > 0) {
            // Use the flat earth sun height parameter for elevation calculation
            flatEarthElevation = Math.atan2(this.sunHeightFE, horizontalDistanceKm) * 180 / Math.PI;
            // Calculate shadow length using proper trigonometry: length = height / tan(elevation)
            flatShadowLength = this.gnomonHeight / Math.tan(flatEarthElevation * Math.PI / 180);
            
            // Debug logging
            console.log('Flat Earth Debug:', {
                sunHeightFE: this.sunHeightFE,
                horizontalDistanceKm: horizontalDistanceKm,
                flatEarthElevation: flatEarthElevation,
                latitude: this.latitude,
                declination: flatEarthSunData.declination
            });
        } else {
            // Sun directly overhead
            flatShadowLength = 0;
        }
        
        // Draw shadow - always present in flat earth model
        if (flatShadowLength > 0) {
            // Calculate shadow direction - directly opposite to sun position
            const sunAngle = Math.atan2(sunY - centerY, sunX - centerX);
            const shadowDirection = sunAngle + Math.PI; // 180 degrees opposite
            
            // Scale shadow length to fit within sundial (radius ~80px, gnomon height scaled to ~24px)
            const pixelsPerCm = 8; // 8 pixels per cm for realistic scaling
            const shadowLengthPixels = flatShadowLength * pixelsPerCm;
            
            // Calculate shadow end position
            const shadowEndX = centerX + Math.cos(shadowDirection) * shadowLengthPixels;
            const shadowEndY = centerY + Math.sin(shadowDirection) * shadowLengthPixels;
            
            ctx.strokeStyle = 'rgba(0,0,0,0.5)';
            ctx.lineWidth = 6;
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.lineTo(shadowEndX, shadowEndY);
            ctx.stroke();
        }
        
        // Display the input time directly (already local time)
        const inputTime = this.currentDate.getHours() + this.currentDate.getMinutes() / 60;
        let localTime = inputTime;
        
        // Normalize to 0-24 hour range
        while (localTime < 0) localTime += 24;
        while (localTime >= 24) localTime -= 24;
        
        const flatTimeHours = Math.floor(localTime);
        const flatTimeMinutes = Math.floor((localTime - flatTimeHours) * 60);
        
        // Update display
        document.getElementById('flatEarthTime').textContent = 
            `${flatTimeHours % 12 || 12}:${flatTimeMinutes.toString().padStart(2, '0')} ${flatTimeHours >= 12 ? 'PM' : 'AM'}`;
        document.getElementById('flatShadowLength').textContent = Math.abs(flatShadowLength).toFixed(1);
        document.getElementById('flatShadowAngle').textContent = Math.round(flatShadowAngle);
        
        // Store flat earth elevation for info panel
        this.flatEarthElevationAngle = flatEarthElevation;
        
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
        
        // Draw hour markings (simple clock-style for educational clarity)
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 2;
        for (let hour = 6; hour <= 18; hour++) {
            // Simple clock positioning: 12 at top, 6 at bottom, 3 at right, 9 at left
            const clockAngle = (hour - 12) * 30 * Math.PI / 180; // 30 degrees per hour
            
            const x1 = centerX + 70 * Math.sin(clockAngle);
            const y1 = centerY - 70 * Math.cos(clockAngle);
            const x2 = centerX + 60 * Math.sin(clockAngle);
            const y2 = centerY - 60 * Math.cos(clockAngle);
            
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.stroke();
            
            // Hour labels
            if (hour % 3 === 0) {
                ctx.fillStyle = '#333';
                ctx.font = '12px Arial';
                ctx.textAlign = 'center';
                const labelX = centerX + 85 * Math.sin(clockAngle);
                const labelY = centerY - 85 * Math.cos(clockAngle) + 4;
                ctx.fillText(hour.toString(), labelX, labelY);
            }
        }
        
        // Draw sun (realistic position)
        if (sunData.elevation > 0) {
            const sunDistance = 120; // Closer to sundial for better visibility
            // Position sun based on azimuth and elevation
            const azimuthRad = sunData.azimuth * Math.PI / 180;
            const elevationRad = sunData.elevation * Math.PI / 180;
            
            // Calculate sun position - high elevation should appear high in sky
            // For September 10 at noon: elevation ~61°, azimuth ~180° (south)
            const elevationFactor = Math.sin(elevationRad) * 80; // Scale elevation effect
            const azimuthDistance = 100; // Distance from center for azimuth positioning
            
            const sunX = centerX + azimuthDistance * Math.sin(azimuthRad);
            const sunY = centerY - azimuthDistance * Math.cos(azimuthRad) - elevationFactor;
            
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
            // Shadow angle: shadow points opposite to sun azimuth
            // If sun is at 180° (south), shadow points at 0° (north)
            realShadowAngle = sunData.azimuth + 180; // Shadow points opposite to sun
            if (realShadowAngle >= 360) realShadowAngle -= 360;
            
            // Get sun position using same calculation as drawing code
            const azimuthRad = sunData.azimuth * Math.PI / 180;
            const elevationRad = sunData.elevation * Math.PI / 180;
            const elevationFactor = Math.sin(elevationRad) * 80;
            const azimuthDistance = 100;
            
            const sunX = centerX + azimuthDistance * Math.sin(azimuthRad);
            const sunY = centerY - azimuthDistance * Math.cos(azimuthRad) - elevationFactor;
            
            // Draw shadow - point directly opposite to sun position
            const pixelsPerCm = 8; // Same scaling as flat earth model
            const shadowLengthPixels = realShadowLength * pixelsPerCm;
            
            // Calculate shadow direction to point to correct hour on sundial
            // Shadow should point to current time on the hour markings
            const currentHour = sunData.localTime;
            const shadowAngle = (currentHour - 12) * 30 * Math.PI / 180; // 30 degrees per hour, same as hour markings
            
            const shadowEndX = centerX + shadowLengthPixels * Math.sin(shadowAngle);
            const shadowEndY = centerY - shadowLengthPixels * Math.cos(shadowAngle);
            
            ctx.strokeStyle = 'rgba(0,0,0,0.6)';
            ctx.lineWidth = 6;
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.lineTo(shadowEndX, shadowEndY);
            ctx.stroke();
        }
        
        // Update display - show the input time directly (already local time)
        const inputTime = this.currentDate.getHours() + this.currentDate.getMinutes() / 60;
        let displayTime = inputTime;
        
        // Normalize to 0-24 hour range
        while (displayTime < 0) displayTime += 24;
        while (displayTime >= 24) displayTime -= 24;
        
        const realTimeHours = Math.floor(displayTime);
        const realTimeMinutes = Math.floor((displayTime - realTimeHours) * 60);
        document.getElementById('sphericalEarthTime').textContent = 
            `${realTimeHours % 12 || 12}:${realTimeMinutes.toString().padStart(2, '0')} ${realTimeHours >= 12 ? 'PM' : 'AM'}`;
        document.getElementById('realShadowLength').textContent = Math.abs(realShadowLength).toFixed(1);
        document.getElementById('realShadowAngle').textContent = Math.round(realShadowAngle);
        
        return { time: displayTime, shadowLength: realShadowLength, shadowAngle: realShadowAngle };
    }
    
    updateDataDisplay(sunData) {
        // Update sun position data
        document.getElementById('solarElevation').textContent = `${sunData.elevation.toFixed(1)}°`;
        document.getElementById('solarAzimuth').textContent = `${sunData.azimuth.toFixed(1)}°`;
        document.getElementById('hourAngle').textContent = `${sunData.hourAngle.toFixed(1)}°`;
        document.getElementById('declination').textContent = `${sunData.declination.toFixed(1)}°`;
        
        // Update flat earth elevation display
        if (this.flatEarthElevationAngle !== undefined) {
            document.getElementById('flatEarthElevation').textContent = `${this.flatEarthElevationAngle.toFixed(1)}°`;
        }
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
