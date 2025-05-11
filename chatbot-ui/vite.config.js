import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Allows access from LAN/mobile devices
    port: 3000,       // Optional: Customize if needed
  },
})
