import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'font-awesome/css/font-awesome.css'
import '@/assets/style.css'
import request from "./request"

Vue.config.productionTip = false
Vue.prototype.$http = request
import NavBar from "@/components/NavBar";
new Vue({
  router,
  store,
  components: {
    NavBar
  },
  render: h => h(App)
}).$mount('#app')
