# 📚 Updating Python Course on Thumb Drive

## 🎯 What This Update Fixes
- ✅ **Navigation links** - No more broken .html links
- ✅ **Course structure** - Now shows "12 Lessons" instead of "8 Lessons"  
- ✅ **Progress bars** - Correct lesson counts (1 of 12, 2 of 12, etc.)
- ✅ **All 12 lessons** - Including new lessons 9-12 (Math Art, N-Body Physics, Gravitational Destroyer, Parametric Art)

## 🚀 Quick Update (Recommended)

### Method 1: Use the Batch File
1. **Connect the thumb drive** to the other computer
2. **Copy the project folder** to the other computer (or pull latest from git)
3. **Double-click `update_thumb_drive.bat`**
4. **Wait for completion** - it will automatically find the thumb drive and update it

### Method 2: Manual Update
1. **Open Command Prompt** in the project folder
2. **Run:** `npm run build`
3. **Find your thumb drive** (usually D:, E:, F:, etc.)
4. **Run:** `robocopy "dist" "X:\Python_Course" /E /PURGE` (replace X: with your drive letter)

## 📋 Verification Steps
After updating, check that the thumb drive has:
- ✅ `Python_Course` folder with updated files
- ✅ `programming/python/lesson1.html` through `lesson12.html`
- ✅ `programming/python-fundamentals.html` shows "12 Lessons"
- ✅ Navigation links work without .html extensions

## 🔧 Troubleshooting
- **"Could not find thumb drive"** - Make sure it's connected and has a `Python_Course` folder
- **"Build failed"** - Run `npm install` first, then try again
- **"Copy failed"** - Check that thumb drive isn't write-protected

## 📁 What Gets Updated
```
Python_Course/
├── index.html (main page)
├── programming/
│   ├── index.html
│   ├── python-fundamentals.html (updated course info)
│   └── python/
│       ├── lesson1.html (fixed navigation)
│       ├── lesson2.html (fixed navigation)
│       ├── ...
│       ├── lesson11.html (Gravitational Destroyer)
│       ├── lesson12.html (Parametric Art)
│       └── setup.html
└── [all other website files]
```

## ✨ After Update
The portable Python learning environment will have:
- 🎮 **12 complete lessons** from Mystery Numbers to Advanced Mathematical Art
- 🔗 **Working navigation** between all lessons
- 📊 **Correct progress tracking** 
- 🖥️ **Offline functionality** on any Windows computer
