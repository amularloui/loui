import { createApp } from 'vue'
import App from './App.vue'

// ✅ Import Bootstrap CSS and JS
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js' // <-- this line is required!

// Initialize API services
import './services/api'

createApp(App).mount('#app')
