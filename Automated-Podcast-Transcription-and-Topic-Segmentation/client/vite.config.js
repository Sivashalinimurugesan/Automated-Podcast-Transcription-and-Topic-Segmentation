import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

export default defineConfig({
  plugins: [react()],
  server: {
    fs: {
      // Allow Vite to access node_modules in the parent directory
      allow: [
        resolve(__dirname, '..') 
      ]
    }
  }
})
