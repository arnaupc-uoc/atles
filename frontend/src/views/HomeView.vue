<template>
  <l-map :zoom="13" :center="[41.3874, 2.1686]">
    <l-tile-layer
      url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
      layer-type="base"
      name="CartoDB Voyager"
      :options="tileOptions"
    />
  </l-map>
</template>

<script setup>
import { LMap, LTileLayer } from "@vue-leaflet/vue-leaflet";

// Definim les opcions de la capa indicant el crossOrigin
const tileOptions = {
  crossOrigin: true // Això afegeix la capçalera CORS anònima automàticament
};
</script>

<style scoped>
.l-map {
  /* Ara el v-main ja li dona l'espai, 100% d'altura del contenidor */
  height: calc(100vh - 48px - 44px); /* Alçada restant de la barra i el footer */
  width: 100%;
}
</style>
