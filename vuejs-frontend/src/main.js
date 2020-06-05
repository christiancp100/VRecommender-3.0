import Vue from "vue";
import router from "./router";
import {BootstrapVueIcons} from 'bootstrap-vue'
import axios from "axios"
import VueAxios from "vue-axios"

Vue.use(VueAxios, axios)

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import { LayoutPlugin, AlertPlugin, TabsPlugin, FormPlugin, FormCheckboxPlugin, FormDatepickerPlugin, ButtonPlugin,
     FormGroupPlugin, FormInputPlugin, FormSelectPlugin, CardPlugin, ListGroupPlugin, ModalPlugin, SpinnerPlugin } from 'bootstrap-vue'
Vue.use(LayoutPlugin)
Vue.use(AlertPlugin)
Vue.use(TabsPlugin)
Vue.use(FormPlugin)
Vue.use(FormCheckboxPlugin)
Vue.use(FormGroupPlugin)
Vue.use(FormInputPlugin)
Vue.use(FormDatepickerPlugin)
Vue.use(FormSelectPlugin)
Vue.use(CardPlugin)
Vue.use(ListGroupPlugin)
Vue.use(ModalPlugin)
Vue.use(SpinnerPlugin)
Vue.use(ButtonPlugin)

Vue.use(BootstrapVueIcons)

import App from "./App.vue";

Vue.config.productionTip = false;

new Vue({
    router,
    render: (h) => h(App),
}).$mount("#app");
