<template>
  <v-divider/>

  <v-container class="d-flex pa-1 my-3 align-center flex-column">
    <h3 class="text-yellow">
      <v-icon icon="mdi-alert"/>
      Warning at
    </h3>
    <v-row class="pa-4">
      <v-sheet class="bg-yellow rounded-pill py-1 px-3 mx-2">
        {{ store.environmentData[room].temperature.maxWThresh }}
        <span v-html="store.environmentData[room].temperature.units"></span>
      </v-sheet>
      <v-sheet class="bg-yellow rounded-pill py-1 px-3 mx-2">
        {{ store.environmentData[room].humidity.maxWThresh }}% RH
      </v-sheet>
    </v-row>
  </v-container>

  <v-container class="d-flex pa-1 my-3 align-center flex-column">
    <h3 class="text-red">
      <v-icon icon="mdi-fire-alert"/>
      Critical at
    </h3>
    <v-row class="pa-4">
      <v-sheet class="bg-red rounded-pill py-1 px-3 mx-2">
        {{ store.environmentData[room].temperature.maxThresh }}
        <span v-html="store.environmentData[room].temperature.units"></span>
      </v-sheet>
      <v-sheet class="bg-red rounded-pill py-1 px-3 mx-2">
        {{ store.environmentData[room].humidity.maxThresh }}% RH
      </v-sheet>
    </v-row>
  </v-container>


  <v-btn class="mt-4 bg-blue-darken-4" :href="store.environmentData[room].url" target="_blank">Edit settings</v-btn>
</template>

<script setup lang="ts">
import {useEnvironmentDataStore} from "@/stores/environmentData";

const store = useEnvironmentDataStore()
</script>

<script lang="ts">
export default {
  name: "MonitorExtendedAttributes",
  props: {
    room: String
  }
}
</script>

<style scoped>

</style>