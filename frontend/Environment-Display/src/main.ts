import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// import './assets/main.css'

// import './assets/mvp.css'
import './assets/custom.css'

import Vuetify from "@/plugins/vuetify";
import 'vuetify/dist/vuetify.min.css'


const app = createApp(App)

app.use(Vuetify)
app.use(createPinia())
app.use(router)

app.mount('#app')
