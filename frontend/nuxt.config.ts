// @ts-ignore – JSON import from bench config
// import { webserver_port } from '../../../sites/common_site_config.json'
//  webserver_port = 8000;
// https://nuxt.com/docs/api/configuration/nuxt-config
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
          href: 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
        }
      ]
    }
  },
  runtimeConfig: {
    public: {
      appName: ''
    }
  },
  nitro: {
    devProxy: {
      '/api': {
        target: `http://localhost:8000`,
        changeOrigin: true,
      },
      '/assets': {
        target: `http://localhost:8000`,
        changeOrigin: true,
      },
    },
  },
  vite: {
    server: {
      proxy: {
        '/api': {
          target: `http://localhost:8000`,
          changeOrigin: true,
        },
        '/assets': {
          target: `http://localhost:8000`,
          changeOrigin: true,
        },
      },
    },
  },
})

 