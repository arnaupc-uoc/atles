import { createApp } from "vue";
import { createPinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import App from "./App.vue";

// Corregir el path dels icons per defecte de Leaflet, ja que no es poden carregar correctament quan s'utilitza amb Vite
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png",
  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png",
});

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
