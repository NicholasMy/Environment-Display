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
    .then(json => {
      Object.assign(environmentDataStore.rooms, json.rooms)
    })
// That was the major bug! We can't directly reassign to a reactive, or we lose the reactivity.

</script>

<template>

  <v-app>

    <v-app-bar color="#005bbb" flat>

      <v-tabs hide-slider>
        <v-tab :to="{name: 'home'}">
            Environment Display
        </v-tab>
      </v-tabs>

      <v-spacer/>

      <v-tabs hide-slider>
        <v-tab :to="{name: 'room', params: {room: room.name}}" v-for="room in environmentDataStore.rooms" :key="room.name">
          {{ room.friendly_name }}
        </v-tab>
      </v-tabs>


      <!--      <v-tabs>-->
      <!--        <v-tab>-->
      <!--          <RouterLink :to="{name: 'home'}">Home</RouterLink>-->
      <!--        </v-tab>-->
      <!--        <v-tab v-for="room in environmentDataStore.rooms" :key="room.name">-->
      <!--          <RouterLink :to="{name: 'room', params: {room: room.name}}">{{ room.friendly_name }}</RouterLink>-->
      <!--        </v-tab>-->


      <!--      </v-tabs>-->


      <!--                  <ul>-->
      <!--                    <li>-->
      <!--                      <RouterLink :to="{name: 'home'}">Home</RouterLink>-->
      <!--                    </li>-->

      <!--                    <li v-for="room in environmentDataStore.rooms" :key="room.name">-->
      <!--                      <RouterLink :to="{name: 'room', params: {room: room.name}}">{{ room.friendly_name }}</RouterLink>-->
      <!--                    </li>-->

      <!--                  </ul>-->
    </v-app-bar>
    <v-main>

      <div v-if="!environmentDataStore.websocketConnected">
        <h1>Connecting to WebSocket...</h1>
        <p>If this takes too long, ensure the backend API is running.</p>
      </div>
      <RouterView v-else/>
    </v-main>

  </v-app>

</template>

<style scoped>

</style>
