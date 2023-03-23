<script setup lang="ts">
import {RouterLink, RouterView} from 'vue-router'
import {reactive} from "vue";
import {useEnvironmentDataStore} from "@/stores/environmentData"
// import HelloWorld from './components/HelloWorld.vue'

const environmentDataStore = useEnvironmentDataStore()

// Create a GET request to fetch the list of rooms from the backend and populate data.rooms
fetch('http://localhost:8085/rooms')
    .then(res => res.json())
    // .then(json => {environmentDataStore.rooms = json.rooms})
    .then(json => {Object.assign(environmentDataStore.rooms, json.rooms)})
    // That was the major bug! We can't directly reassign to a reactive, or we lose the reactivity.

</script>

<template>
  <header>
    <nav>
      Environment Display
      <ul>
        <li>
          <RouterLink :to="{name: 'home'}">Home</RouterLink>
        </li>

        <li v-for="room in environmentDataStore.rooms" :key="room.name">
          <RouterLink :to="{name: 'room', params: {room: room.name}}">{{ room.friendly_name }}</RouterLink>
        </li>

      </ul>
    </nav>
  </header>
  <main>

    <div v-if="!environmentDataStore.websocketConnected">
      <h1>Connecting to WebSocket...</h1>
      <p>If this takes too long, ensure the backend API is running.</p>
    </div>
    <RouterView v-else/>
  </main>

</template>

<style scoped>

</style>
