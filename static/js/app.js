import Vue from 'vue'
import App from '../vue/App.vue'

import VueResource from 'vue-resource';
Vue.use(VueResource);

new Vue({
  el: '#app',
  render: h => h(App)
})