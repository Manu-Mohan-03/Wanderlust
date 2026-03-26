import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    include: [
      'deck.gl',
      '@deck.gl/react',
      '@deck.gl/layers',
      '@deck.gl/core',
    ],
  },
  resolve: {
    dedupe: ['deck.gl', '@deck.gl/core']
  }
})
