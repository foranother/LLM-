// import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import '@mdi/font/css/materialdesignicons.css'

import App from './App.vue'
import router from './router'

import auth from './utils/auth'

import axios from 'axios'


// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { md3 } from 'vuetify/blueprints'

// Init firebase
// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app"
import { getAuth } from "firebase/auth"
import { getFirestore } from 'firebase/firestore'

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDTeGvkYYZZDwBwF4QZCZhBaUChpIq8yTA",
  authDomain: "nurse-project-a5cc9.firebaseapp.com",
  projectId: "nurse-project-a5cc9",
  storageBucket: "nurse-project-a5cc9.appspot.com",
  messagingSenderId: "579541302149",
  appId: "1:579541302149:web:ab87c17fbd91cce28e22ec",
  measurementId: "G-5L34Y05T6T"
}
// Initialize Firebase
const firebaseApp = initializeApp(firebaseConfig)
const db = getFirestore(firebaseApp);

const vuetify = createVuetify({
  components,
  directives,
  blueprint: md3,
  icons: {
    defaultSet: 'mdi'
  }
})
const instance = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_ENDPOINT
})

instance.interceptors.request.use(function (config) {
  if (auth.isLoggedIn()) config.headers.Authorization = `Token ${auth.getToken()}`
  return config
})


const app = createApp(App)
app.config.globalProperties.axios = instance
app.config.globalProperties.firebaseApp = firebaseApp
app.config.globalProperties.db = db


const pinia = createPinia()
pinia.use(({ store }) => {
  store.$axios = instance
  store.$firebaseApp = firebaseApp
  store.$auth = auth
  store.$db = db
})
app.use(pinia)
app.use(router)
app.use(vuetify)

app.mount('#app')
