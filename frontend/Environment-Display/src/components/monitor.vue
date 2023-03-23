<template>
  <article>
    <aside>
      <h1>{{ store.friendlyNamesMap[name] || "Unknown friendly room name" }}</h1>

      <template v-if="store.getDataForRoom(name) != null">
        <h1>{{ store.environmentData[name].temperature.current }}
          <span v-html="store.environmentData[name].temperature.units"></span></h1>
        <h1>{{ store.environmentData[name].humidity.current }}%</h1>
      </template>
      <template v-else>
        <h1>Waiting for sensor data...</h1>
      </template>

    </aside>
  </article>
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