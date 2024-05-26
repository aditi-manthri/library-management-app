import { createApp } from 'vue'
import App from './App.vue'
import router from './router';
import axios from 'axios';


const app = createApp(App);

axios.defaults.baseURL = 'http://127.0.0.1:8000';
const axiosInstance = axios.create({
    baseURL: 'http://127.0.0.1:8000',
})

app.config.globalProperties.$axios = axiosInstance;
app.use(router);
app.mount('#app');