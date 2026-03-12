import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import { setupInterceptors } from './services/api'
import { useAuthStore } from './stores/auth'
import './assets/main.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Wire up API interceptors with auth store (avoids circular import)
setupInterceptors(() => useAuthStore())

app.mount('#app')
