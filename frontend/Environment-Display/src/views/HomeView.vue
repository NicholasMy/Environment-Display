<template>

  <div class="d-flex align-center flex-column">
    <h1 class="ms-4">Davis Server Room Environmental Monitor</h1>
  </div>


  <div class="d-flex flex-wrap justify-center">
    <monitor v-for="room in store.state.rooms" :key="room.name" :name="room.name"/>

  </div>


</template>
<script setup>
import {useEnvironmentDataStore} from "@/stores/environmentData";

const store = useEnvironmentDataStore();

</script>

<script>
import Monitor from "@/components/Monitor.vue";


export default {
  name: "MainView",
  components: {Monitor}
}
</script>

<style scoped>

</style>