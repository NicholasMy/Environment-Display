<template>

  <v-card class="ma-2 pa-2 rounded-lg" style="width: 400px;">
    <v-card-title>
      <h2>{{ store.friendlyNamesMap[name] || "Unknown friendly room name" }}</h2>
    </v-card-title>

    <template v-if="store.getDataForRoom(name) != null">

      <v-card-item>
        <h2>
          {{ store.environmentData[name].temperature.current }}
          <span v-html="store.environmentData[name].temperature.units"></span>
        </h2>
        <v-progress-linear :model-value="calculateTemperatureProgress(store.environmentData[name].temperature.current)"
                           :color="calculateBarColor(store.environmentData[name].temperature)"
                           height="20" rounded/>
      </v-card-item>
      <v-card-item>
        <h2>
          {{ store.environmentData[name].humidity.current }}%
          <span class="font-weight-regular text-grey" v-if="$vuetify.display.xs">RH</span>
          <span class="font-weight-regular text-grey" v-else>Relative Humidity</span>
        </h2>
        <v-progress-linear :model-value="store.environmentData[name].humidity.current"
                           :color="calculateBarColor(store.environmentData[name].humidity)"
                           height="20" rounded/>

      </v-card-item>
    </template>
    <template v-else>
      <h1>Waiting for sensor data...</h1>
    </template>
  </v-card>

</template>

<script lang="ts">
export default {
  name: "monitor"
}
</script>
<script setup lang="ts">
import {useEnvironmentDataStore} from "@/stores/environmentData";
import {reactive} from "vue";

const props = defineProps({
  name: String,
})
const store = useEnvironmentDataStore()

function calculateTemperatureProgress(temperature: number) {
  const min = 55
  const max = 90
  return (temperature - min) / (max - min) * 100
}

function calculateBarColor(data: Map<string, any>) {
  // data is either the "temperature" or "humidity" map
  const warningLevel = data.maxWThresh
  const criticalLevel = data.maxThresh
  const current = data.current
  if (current >= criticalLevel) {
    return "red"
  } else if (current >= warningLevel) {
    return "yellow"
  } else {
    return "green"
  }
}

</script>

<style scoped>

</style>