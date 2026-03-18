// @ts-ignore – JSON import from bench config
import { webserver_port } from '../../../sites/common_site_config.json'

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  modules: ['@nuxtjs/tailwindcss'],
  devtools: { enabled: true },

  app: {
    head: {
      title: 'MaxEdu | Student ERM',
      link: [
        {
          rel: 'stylesheet',
          href: 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css'
        }
      ]
    }
  },

  runtimeConfig: {
    public: {
      appName: '',
      apiBaseUrl: ''
    }
  },

  nitro: {
    devProxy: {
      '/api': {
        target: `http://localhost:${webserver_port}`,
        changeOrigin: true,
      },
      '/assets': {
        target: `http://localhost:${webserver_port}`,
        changeOrigin: true,
      },
      '/files': {
        target: `http://localhost:${webserver_port}`,
        changeOrigin: true,
      },
    },
  },

  vite: {
    server: {
      proxy: {
        '/api': {
          target: `http://localhost:${webserver_port}`,
          changeOrigin: true,
        },
        '/assets': {
          target: `http://localhost:${webserver_port}`,
          changeOrigin: true,
        },
        '/files': {
          target: `http://localhost:${webserver_port}`,
          changeOrigin: true,
        },
      },
    },
  },
})