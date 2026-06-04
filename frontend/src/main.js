import { createApp } from "vue";
import { createPinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";
import App from "./App.vue";

const vuetify = createVuetify({
  components,
  directives,
  icons: { defaultSet: "mdi" },
});

const router = createRouter({
  history: createWebHistory(),
  routes: [],
});

const app = createApp(App);
app.use(createPinia());
app.use(router);
app.use(vuetify);
app.mount("#app");
