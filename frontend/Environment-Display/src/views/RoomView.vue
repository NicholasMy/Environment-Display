<template>

  <div class="d-flex justify-center">
    <monitor :name="$route.params.room"/>
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

const store = useEnvironmentDataStore()
</script>

<script>
import Monitor from "@/components/monitor.vue";

export default {
  name: "RoomView",
  components: {Monitor}
}
</script>

<style scoped>

</style>