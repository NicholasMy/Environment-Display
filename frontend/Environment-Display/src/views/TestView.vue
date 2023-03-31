<template>
  <h1>Test Page</h1>

  <v-card max-width="500px">
    <v-card-item>

      <v-slider label="min" thumb-label="always" v-model="minTemp" class="ma-6 pt-4"></v-slider>
      <v-slider label="warn" thumb-label="always" v-model="warningTemp" class="ma-6"></v-slider>
      <v-slider label="crit" thumb-label="always" v-model="criticalTemp" class="ma-6"></v-slider>
      <v-slider label="max" thumb-label="always" v-model="maxTemp" class="ma-6"></v-slider>
      <v-slider label="value" thumb-label="always" v-model="sliderValue" class="ma-6"></v-slider>

      <MulticolorProgressBar :min="minTemp"
                             :max="maxTemp"
                             :warning="warningTemp"
                             :critical="criticalTemp"
                             :value="sliderValue"/>
    </v-card-item>

    <p>{{ sliderValue }}</p>

  </v-card>


</template>

<script setup lang="ts">

import {ref} from "vue";
import MulticolorProgressBar from "@/components/MulticolorProgressBar.vue";

let minTemp = ref(55)
let warningTemp = ref(78)
let criticalTemp = ref(85)
let maxTemp = ref(90)
let sliderValue = ref(80)

</script>

<style scoped>

</style>