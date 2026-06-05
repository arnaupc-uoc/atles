<template>
  <v-app>
    <v-app-bar color="primary" density="compact">
      <v-app-bar-title>Atles</v-app-bar-title>
    </v-app-bar>

    <v-main>
      <l-map :zoom="13" :center="[41.3874, 2.1686]">
        <l-tile-layer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          layer-type="base"
          name="OpenStreetMap"
        />
      </l-map>
    </v-main>

    <v-footer app color="grey-lighten-1" density="compact">
      <v-row justify="center" no-gutters>
        <v-btn variant="text" class="mx-2">About</v-btn>
        <v-btn variant="text" class="mx-2">Contacte</v-btn>
      </v-row>
    </v-footer>
  </v-app>
</template>

<script setup>
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer } from "@vue-leaflet/vue-leaflet";
</script>

<style scoped>
.l-map {
  height: calc(100vh - 112px);
  width: 100%;
}
</style>
