import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import {
	faMoon,
	faCloudMoon,
	faUtensils,
	faBottleWater,
	faBaby,
	faPuzzlePiece,
	faNoteSticky,
} from "@fortawesome/free-solid-svg-icons";

import App from './App.vue'
import router from './router'

import './styles.css'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css' 

library.add(faMoon, faCloudMoon, faUtensils, faBottleWater, faBaby, faPuzzlePiece, faNoteSticky);
const app = createApp(App)
app.component('font-awesome-icon', FontAwesomeIcon)

app.use(createPinia())
app.use(router)

app.use(Toast)
app.mount('#app')
