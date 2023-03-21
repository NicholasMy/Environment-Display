<template>
  <h1>Welcome to Environment Display!</h1>

  {{ store.rooms }}

  <p v-for="room in store.rooms" :key="room.name">
    hello
  </p>

  <monitor v-for="room in store.rooms" :key="room.name" :name="room.name">
    hello
  </monitor>

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