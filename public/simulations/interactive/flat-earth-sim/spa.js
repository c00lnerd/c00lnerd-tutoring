/**
 * Flat Earth Solar Position Calculator
 * Based on a simple geometric model with the sun moving in a circular path at constant height
 */
class SolarPositionAlgorithm {
    constructor() {
        this.debugEl = document.getElementById('debugLog');
        this.rad = Math.PI / 180;  // Degree to radian conversion
        this.deg = 180 / Math.PI;  // Radian to degree conversion
        this.earthRadius = 6371;   // Earth radius in km for distance calculations
    }

    /**
     * Calculate sun position for given date and location
     * @param {Date} date - JavaScript Date object
     * @param {number} latitude - Observer latitude in degrees
     * @param {number} longitude - Observer longitude in degrees
     * @returns {Object} Solar position parameters
     */
    calculateSolarPosition(date, latitude, longitude, sunHeight) {
        // Clear debug log at start of calculation
        if (this.debugEl) this.debugEl.textContent = '';
        // Calculate day of year
        const startOfYear = new Date(date.getFullYear(), 0, 0);
        const dayOfYear = Math.floor((date - startOfYear) / (1000 * 60 * 60 * 24));

        // Calculate sun's declination (latitude of subsolar point)
        // On June 21 (day 172), declination should be +23.44° (sun over Tropic of Cancer)
        // On December 21 (day 355), declination should be -23.44° (sun over Tropic of Capricorn)
        const declination = -23.44 * Math.cos(2 * Math.PI * (dayOfYear + 10) / 365);

        // Calculate sun's hour angle based on UTC time
        const utcHour = date.getUTCHours() + date.getUTCMinutes() / 60;
        const hoursSinceNoon = utcHour - 12;
        // Sun moves 15° per hour eastward in standard coordinates
        // For Gleason map with 0° at 3 o'clock, positive angle = clockwise
        const solarHourAngle = hoursSinceNoon * 15;
        // This makes the sun move East to West (counterclockwise)
        // At noon: sun at 0° (prime meridian)
        // Morning: sun is East (positive degrees)
        // Afternoon: sun is West (negative degrees)

        // Convert to radians for calculations
        const latRad = latitude * this.rad;
        const declinationRad = declination * this.rad;
        const hourAngleRad = solarHourAngle * this.rad;

        // Calculate azimuth using spherical astronomy formulas
        // This gives correct sun path for all latitudes and seasons
        // Formula: arctan2(sin(H), cos(H)sin(φ) - tan(δ)cos(φ))
        let azimuth = Math.atan2(
            Math.sin(hourAngleRad),
            Math.cos(hourAngleRad) * Math.sin(latRad) - 
            Math.tan(declinationRad) * Math.cos(latRad)
        ) * this.deg;

        // Convert to -180 to +180 range, measured from north
        // Positive = east of north
        // Negative = west of north
        if (azimuth > 180) azimuth -= 360;
        if (azimuth <= -180) azimuth += 360;

        // Calculate distances from center on flat earth
        // Using Earth's actual radius at equator: 6378 km
        // This gives us 111 km per degree of latitude
        const kmPerDegree = 111.32; // Exact Earth equatorial circumference / 360°
        const flatEarthRadius = 90 * kmPerDegree; // 9990 km total radius
        
        // Convert latitude to radius (distance from center)
        // At 90°N (center), r = 0
        // At 0° (equator), r = flatEarthRadius * 0.5
        // At 90°S (edge), r = flatEarthRadius
        const obsR = (90 - latitude) * kmPerDegree;
        const sunR = (90 - declination) * kmPerDegree;

        
        // Calculate ground distance on flat earth
        // Convert lat/lon to radial coordinates from center
        // Distance from center for observer and sun
        const obsRadius = (90 - latitude) * kmPerDegree;
        const sunRadius = (90 - declination) * kmPerDegree;
        
        // Convert standard longitude to Gleason map angle (clockwise from 3 o'clock)
        // Standard: -180 to +180, positive is East
        // Gleason: 0° at prime meridian (3 o'clock), clockwise
        const obsAngle = -longitude * this.rad;
        // For sun angle, we want counterclockwise motion (East to West)
        const sunAngle = solarHourAngle * this.rad;
        
        // Calculate x,y coordinates
        const obsX = obsRadius * Math.cos(obsAngle);
        const obsY = obsRadius * Math.sin(obsAngle);
        const sunX = sunRadius * Math.cos(sunAngle);
        const sunY = sunRadius * Math.sin(sunAngle);
        
        // Direct distance between points
        const distance = Math.sqrt(
            Math.pow(obsX - sunX, 2) + 
            Math.pow(obsY - sunY, 2)
        );


        // Calculate 3D distance including sun height
        let distance3D = Math.sqrt(
            Math.pow(distance, 2) + Math.pow(sunHeight, 2)
        );

        // Calculate elevation using pure geometry
        // elevation = arctan(height/distance)
        const elevation = Math.atan2(sunHeight, distance) * this.deg;

        // Calculate azimuth (angle from north, clockwise)
        // Get vector from observer to sun
        const dx = sunX - obsX;
        const dy = sunY - obsY;
        
        // When observer is south of sun's declination, the sun appears to move clockwise
        // When north of declination, it moves counterclockwise
        const isSouthOfSun = latitude < declination;
        
        // Convert to angle from north
        let baseAzimuth;
        if (isSouthOfSun) {
            // When south of sun, invert the x-coordinate to make path symmetric around north
            baseAzimuth = Math.atan2(-dx, -dy) * this.deg;
        } else {
            baseAzimuth = Math.atan2(dx, -dy) * this.deg;
        }
        
        // Convert to 0-360 range
        let finalAzimuth = baseAzimuth < 0 ? baseAzimuth + 360 : baseAzimuth;

        // Calculate sun diameter that would subtend 0.5° at sun height
        // Using formula: angle = 2 * arctan(diameter/(2*distance))
        // For 0.5° angle at sun height: 0.5 = 2 * arctan(diameter/(2*height))
        // Therefore: diameter = 2 * height * tan(0.25°)
        const quarterDegRad = 0.25 * this.rad; // 0.25 degrees in radians
        const sunDiameter = 2 * sunHeight * Math.tan(quarterDegRad);
        
        // Calculate angular size based on current 3D distance
        // Using the same formula: angle = 2 * arctan(diameter/(2*distance))
        const angularSize = 2 * Math.atan(sunDiameter/(2*distance3D)) * this.deg;


        // At solar noon (solarHourAngle = 0):
        // - If observer is north of sun's declination -> sun is due south (180°)
        // - If observer is south of sun's declination -> sun is due north (0°)
        // - If observer is at sun's declination -> sun is directly overhead
        if (Math.abs(solarHourAngle) < 0.00001) {
            finalAzimuth = (latitude > declination) ? 180 : 0;
        }

        return {
            azimuth: finalAzimuth,
            elevation: elevation,
            groundDistance: distance,
            groundDistance3D: distance3D,
            subsolarLat: declination,
            subsolarLon: -solarHourAngle, // Negative because sun moves westward
            angularSize: angularSize,
            sunDiameter: sunDiameter
        };
    }

    /**
     * Set the sun height
     * @param {number} height - Height in kilometers
     */
    setSunHeight(height) {
        this.sunHeight = height;
    }
}
