<template>
  <h1>Davis Server Room Environmental Monitor</h1>

  <monitor v-for="room in store.rooms" :key="room.name" :name="room.name" />

</template>
<script setup>
import {useEnvironmentDataStore} from "@/stores/environmentData";

const store = useEnvironmentDataStore();

</script>

<script>
import Monitor from "@/components/monitor.vue";


export default {
  name: "MainView",
  components: {Monitor}
}
</script>

<style scoped>

</style>