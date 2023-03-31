<template>

  <v-card class="ma-2 pa-2 rounded-lg" style="width: 400px;">
    <v-card-title>
      <h2>{{ store.friendlyNamesMap[name] || "Unknown friendly room name" }}</h2>
    </v-card-title>

    <template v-if="store.getDataForRoom(name) == null">
      <v-card-item>
        <h1>Waiting for sensor data...</h1>
      </v-card-item>
    </template>
    <template v-else-if="!store.getDataForRoom(name).success">
      <v-card-item>
        <h2 class="text-red">Error connecting to sensor.</h2>
        <p>Check the console output for more information.</p>
      </v-card-item>
    </template>

    <template v-else>
      <v-card-item>
        <h2>
          {{ store.environmentData[name].temperature.current.toFixed(1) }}
          <span v-html="store.environmentData[name].temperature.units"></span>
          <template v-if="isUsingFahrenheit()">
            <span class="font-weight-regular text-grey">
              / {{ fahrenheitToCelsius(store.environmentData[name].temperature.current).toFixed(1) }} &deg;C
            </span>
          </template>
        </h2>
        <v-progress-linear :model-value="calculateTemperatureProgress(store.environmentData[name].temperature.current)"
                           :color="calculateBarColor(store.environmentData[name].temperature)"
                           height="20" rounded/>
      </v-card-item>
      <v-card-item>
        <h2>
          {{ store.environmentData[name].humidity.current.toFixed(1) }}%
          <span class="font-weight-regular text-grey" v-if="$vuetify.display.xs">RH</span>
          <span class="font-weight-regular text-grey" v-else>Relative Humidity</span>
        </h2>
        <v-progress-linear :model-value="store.environmentData[name].humidity.current"
                           :color="calculateBarColor(store.environmentData[name].humidity)"
                           height="20" rounded/>

      </v-card-item>
      <v-card-item>
        <slot></slot>
      </v-card-item>

      <v-card-item>
        <MulticolorProgressBar :min="minTemp" :max="maxTemp"
                               :warning="store.environmentData[name].temperature.maxWThresh"
                               :critical="store.environmentData[name].temperature.maxThresh"
                               :value="80"/>
<!--                               :value="store.environmentData[name].temperature.current"/>-->
      </v-card-item>


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
import MulticolorProgressBar from "@/components/MulticolorProgressBar.vue";

const props = defineProps({
  name: String,
})
const store = useEnvironmentDataStore()
const minTemp = 55
const maxTemp = 90

function calculateTemperatureProgress(temperature: number) {
  return (temperature - minTemp) / (maxTemp - minTemp) * 100
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

function isUsingFahrenheit(): boolean {
  return store.environmentData[props.name].temperature.units === "&deg;F"
}

function fahrenheitToCelsius(fahrenheit: number): number {
  return (fahrenheit - 32) * 5 / 9
}

</script>

<style scoped>

</style>