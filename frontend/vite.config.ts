import { fileURLToPath, URL } from 'node:url';

import vue from '@vitejs/plugin-vue';
import { NaiveUiResolver } from "unplugin-vue-components/resolvers"; // also from Naive-UI
import Components from 'unplugin-vue-components/vite';
import { defineConfig } from 'vite';
import vueDevTools from 'vite-plugin-vue-devtools';

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    //vueDevTools(),
    Components({ resolvers: [NaiveUiResolver()] })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
