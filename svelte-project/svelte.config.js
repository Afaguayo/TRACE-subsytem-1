import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/kit/vite';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  kit: {
    adapter: adapter() // ✅ Use as a function, not a string
  },
  preprocess: vitePreprocess()
};

export default config;