<template>

  <div class="d-flex justify-center">
    <Monitor :name="$route.params.room">
      <MonitorExtendedAttributes :room="$route.params.room" />
    </Monitor>
  </div>

  <v-expansion-panels class="pa-4">
    <v-expansion-panel title="View raw data">
      <v-expansion-panel-text>
        {{ store.getDataForRoom($route.params.room) }}
      </v-expansion-panel-text>
    </v-expansion-panel>
  </v-expansion-panels>


</template>

<script setup>
import {useEnvironmentDataStore} from "@/stores/environmentData";
import MonitorExtendedAttributes from "@/components/MonitorExtendedAttributes.vue";

const store = useEnvironmentDataStore()
</script>

<script>
import Monitor from "@/components/Monitor.vue";

export default {
  name: "RoomView",
  components: {Monitor}
}
</script>

<style scoped>

</style>