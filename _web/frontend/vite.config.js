import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// /api istekleri FastAPI'ye yonlendiriliyor. Boylece arayuz kodunda mutlak
// adres yok: gelistirmede de uretimde de "/api/soru" yaziyoruz.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // 8001: port 8000'i baska bir yerel FastAPI projesi tutuyor.
    proxy: { '/api': { target: 'http://127.0.0.1:8001', changeOrigin: true } },
  },
})
