// @ts-check
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

// https://astro.build/config
export default defineConfig({
  integrations: [tailwind()],
  output: 'static',
  build: {
    format: 'file',
    inlineStylesheets: 'always'
  },
  // Enable relative paths for offline use (comment out for dev server)
  // base: './',
  trailingSlash: 'never'
});
