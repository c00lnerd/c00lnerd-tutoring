#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

console.log('🔧 Building offline version for thumbdrive...');

// Step 1: Update astro.config.mjs for offline build
const configPath = 'astro.config.mjs';
let config = fs.readFileSync(configPath, 'utf8');

// Enable offline configuration
config = config.replace('// base: \'.\/\',', 'base: \'./\',');

fs.writeFileSync(configPath, config);
console.log('✅ Updated astro.config.mjs for offline build');

try {
  // Step 2: Build the site
  console.log('🏗️  Building site...');
  execSync('npm run build', { stdio: 'inherit' });
  
  // Step 3: Fix emoji encoding in HTML files
  console.log('🔧 Fixing emoji encoding in HTML files...');
  
  const distDir = './dist';
  
  function fixEmojisInFile(filePath) {
    if (path.extname(filePath) === '.html') {
      let content = fs.readFileSync(filePath, 'utf8');
      let modified = false;
      
      // Fix common HTML entity encodings for emojis
      const emojiReplacements = {
        '&#128218;': '📚',  // Books
        '&#129504;': '🧠',  // Brain
        '&#127916;': '🎬',  // Movie camera
        '&#127760;': '🌐',  // Globe
        '&#127912;': '🎨',  // Artist palette
        '&#128640;': '🚀',  // Rocket
        '&#127775;': '🌟',  // Star
        '&#128279;': '🔗',  // Link
        '&#127919;': '🎯',  // Target
        '&amp;#': '&#',     // Fix double encoding
        'ðŸ"¥': '🔥',       // Fire (common encoding issue)
        'ðŸš€': '🚀',       // Rocket (common encoding issue)
        'ðŸŒŸ': '🌟',       // Star (common encoding issue)
        'ðŸ"š': '📚',       // Books (common encoding issue)
        'ðŸ§ ': '🧠',       // Brain (common encoding issue)
        'ðŸŽ¬': '🎬',       // Movie camera (common encoding issue)
        'ðŸŒ': '🌐',       // Globe (common encoding issue)
        'ðŸŽ¨': '🎨',       // Artist palette (common encoding issue)
      };
      
      for (const [encoded, emoji] of Object.entries(emojiReplacements)) {
        if (content.includes(encoded)) {
          content = content.replaceAll(encoded, emoji);
          modified = true;
        }
      }
      
      if (modified) {
        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`  ✅ Fixed emojis in ${filePath}`);
      }
    }
  }
  
  function processDirectory(dir) {
    const items = fs.readdirSync(dir);
    
    for (const item of items) {
      const fullPath = path.join(dir, item);
      const stat = fs.statSync(fullPath);
      
      if (stat.isDirectory()) {
        processDirectory(fullPath);
      } else {
        fixEmojisInFile(fullPath);
      }
    }
  }
  
  if (fs.existsSync(distDir)) {
    processDirectory(distDir);
  }
  
  console.log('✅ Offline build complete!');
  console.log('📁 Copy the contents of ./dist/ to replace Python_Course folder on thumbdrive');
  
} catch (error) {
  console.error('❌ Build failed:', error.message);
} finally {
  // Step 4: Restore original config
  config = config.replace('base: \'./\',', '// base: \'./\',');
  fs.writeFileSync(configPath, config);
  console.log('✅ Restored astro.config.mjs to online configuration');
}
