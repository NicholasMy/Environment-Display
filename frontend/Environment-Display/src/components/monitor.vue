<template>

      <v-card class="ma-2 pa-2 rounded-lg">
        <v-card-title>{{ store.friendlyNamesMap[name] || "Unknown friendly room name" }}</v-card-title>

        <template v-if="store.getDataForRoom(name) != null">

          <v-card-item>{{ store.environmentData[name].temperature.current }}
            <span v-html="store.environmentData[name].temperature.units"></span></v-card-item>
          <v-card-item>{{ store.environmentData[name].humidity.current }}% RH</v-card-item>
        </template>
        <template v-else>
          <h1>Waiting for sensor data...</h1>
        </template>
      </v-card>

</template>

<script>
export default {
  name: "monitor"
}
</script>
<script setup>
import {useEnvironmentDataStore} from "@/stores/environmentData";
import {reactive} from "vue";

const props = defineProps({
  name: String,
})
const store = useEnvironmentDataStore()

</script>

<style scoped>

</style>