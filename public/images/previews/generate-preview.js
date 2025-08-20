const { createCanvas } = require('canvas');
const fs = require('fs');
const path = require('path');

// Create canvas
const canvas = createCanvas(800, 400);
const ctx = canvas.getContext('2d');

// Draw preview
ctx.fillStyle = '#87CEEB'; // Sky blue background
ctx.fillRect(0, 0, canvas.width, canvas.height);

// Draw Earth circle
ctx.fillStyle = '#4CAF50';
ctx.beginPath();
ctx.arc(400, 200, 150, 0, Math.PI * 2);
ctx.fill();

// Draw Sun
ctx.fillStyle = '#FFD700';
ctx.beginPath();
ctx.arc(600, 100, 30, 0, Math.PI * 2);
ctx.fill();

// Add glow around sun
const gradient = ctx.createRadialGradient(600, 100, 30, 600, 100, 60);
gradient.addColorStop(0, 'rgba(255, 215, 0, 0.3)');
gradient.addColorStop(1, 'rgba(255, 215, 0, 0)');
ctx.fillStyle = gradient;
ctx.beginPath();
ctx.arc(600, 100, 60, 0, Math.PI * 2);
ctx.fill();

// Add text
ctx.font = 'bold 24px Arial';
ctx.fillStyle = '#000';
ctx.textAlign = 'center';
ctx.fillText('For Flat Earthers', 400, 350);

// Save to file
const buffer = canvas.toBuffer('image/png');
fs.writeFileSync('flat-earth-preview.png', buffer);
