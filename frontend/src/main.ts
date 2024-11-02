import './assets/main.css'

import { autoAnimatePlugin } from '@formkit/auto-animate/vue'
import { cs } from '@formkit/i18n'
import { defaultConfig, plugin } from '@formkit/vue'
import { createPinia } from 'pinia'
import { createApp } from 'vue'

import App from './App.vue'
import router from './router'

// Ensure naive-ui css is importe before tailwind-css reset
// https://www.naiveui.com/en-US/light/docs/style-conflict
const meta = document.createElement("meta");
meta.name = "naive-ui-style";
document.head.appendChild(meta);

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(plugin, defaultConfig({
    locales: { cs },
    locale: 'cs',
}))
app.use(autoAnimatePlugin)

app.mount('#app')
