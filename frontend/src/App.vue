<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-toolbar-title>Atles</q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer elevated class="bg-grey-3">
      <div class="row items-center justify-center q-pa-sm">
        <q-btn flat class="mx-sm" label="About" />
        <q-btn flat class="mx-sm" label="Contacte" />
      </div>
    </q-footer>
  </q-layout>
</template>

<script setup>
</script>
