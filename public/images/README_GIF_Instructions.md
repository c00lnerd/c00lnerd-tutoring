# Screen Capture Video Instructions for Lesson 14

## Required MP4 Videos

The following MP4 videos should be created using screen capture software:

### Required Files:
1. **6.4.mp4** - Ultrasonic ranging with RGB LED feedback demonstration
2. **6.5.mp4** - Ultrasonic following behavior demonstration

### Creation Steps:
1. Set up your miniAuto robot with ultrasonic sensor
2. Upload the Section 6.4 Arduino code
3. Use screen capture software to record the demonstration
4. Save as `6.4.mp4` in this directory
5. Upload the Section 6.5 Arduino code  
6. Record the following behavior demonstration
7. Save as `6.5.mp4` in this directory

### What to Demonstrate:

**6.4.mp4 - Ultrasonic Ranging:**
- Show RGB LEDs changing colors based on distance
- Red breathing when very close (<80mm)
- Color transitions: Red → Blue → Green as distance increases
- Real-time response to moving objects

**6.5.mp4 - Ultrasonic Following:**
- Robot moving backward when object too close (<200mm)
- Robot stopping in optimal zone (200-300mm)
- Robot following forward when object moves away (300-700mm)
- Robot stopping when object too far (>700mm)

### File Locations:
- Place videos here: `public/images/6.4.mp4` and `public/images/6.5.mp4`
- Lesson file: `src/pages/programming/lessons32/lesson14.astro`
- Videos will auto-load with HTML5 controls when present

### Benefits:
- Better quality than GIFs
- Smaller file sizes
- Student playback controls
- No external dependencies
- Your own hardware setup demonstration
