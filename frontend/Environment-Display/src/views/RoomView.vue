<template>

  <div class="mb-8 d-flex flex-column flex-lg-row justify-center align-center align-lg-start w-100">
    <Monitor :name="$route.params.room" class="flex-shrink-0">
      <MonitorExtendedAttributes :room="$route.params.room"/>
    </Monitor>
    <HistoryChart  class="flex-shrink-1" />
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
import HistoryChart from "@/views/HistoryChart.vue";

const store = useEnvironmentDataStore()
</script>

<script>
import Monitor from "@/components/Monitor.vue";

export default {
  name: "RoomView",
  components: {Monitor}
}
</script>

