// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  build: {
    assets: '_assets',
    inlineStylesheets: 'never',
    format: 'file'
  },
  outDir: './dist',
  publicDir: './public',
  base: '/',
  trailingSlash: 'always'
});
