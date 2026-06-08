import { createApp } from "vue";
import { createPinia } from "pinia";
import { Quasar } from "quasar";
import "@quasar/extras/material-icons/material-icons.css";
import "quasar/dist/quasar.prod.css";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import App from "./App.vue";
import router from "./router"; // 👈 Importem el router des del fitxer extern

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

const app = createApp(App);
app.use(createPinia());
app.use(router);
app.use(Quasar);
app.mount("#app");
