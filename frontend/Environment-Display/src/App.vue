<script setup lang="ts">
import {RouterLink, RouterView} from 'vue-router'
import {computed, reactive, ref} from "vue";
import {useEnvironmentDataStore} from "@/stores/environmentData"
// import HelloWorld from './components/HelloWorld.vue'

const environmentDataStore = useEnvironmentDataStore()

function formatDate(dateString: string | undefined) {
  if (dateString === undefined) return "..."
  const date = new Date(Date.parse(dateString))
  return date.toLocaleString('en-US')
}

const now = ref(new Date())
setInterval(() => {
  now.value = new Date()
}, 100)

const timeSinceUpdate = computed(() => {
  // Return the time since the last data update in milliseconds
  const dataTime = new Date(Date.parse(environmentDataStore.environmentData.time))
  return now.value.getTime() - dataTime.getTime()
})

const dataIsStale = computed(() => {
  return timeSinceUpdate.value > 15_000 || environmentDataStore.environmentData.time === undefined
})

// Represent the time since the last update in a human-readable format
const timeSinceUpdateString = computed(() => {
  if (environmentDataStore.environmentData.time === undefined) {
    return "never"
  }
  const seconds = Math.floor(timeSinceUpdate.value / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)
  if (days > 0) {
    return `${days} day${days > 1 ? "s" : ""} ago`
  } else if (hours > 0) {
    return `${hours} hour${hours > 1 ? "s" : ""} ago`
  } else if (minutes > 0) {
    return `${minutes} minute${minutes > 1 ? "s" : ""} ago`
  } else if (seconds > 0) {
    return `${seconds} second${seconds > 1 ? "s" : ""} ago`
  } else {
    return "just now"
  }
})
</script>

<template>

  <v-app>

    <v-app-bar color="primary" flat absolute>

      <v-tabs hide-slider>
        <v-tab class="rounded-0" :to="{name: 'home'}">
          Environment Display
        </v-tab>

        <v-tab class="rounded-0" :to="{name: 'room', params: {room: room.name}}"
               v-for="room in environmentDataStore.rooms" :key="room.name">
          {{ room.friendly_name }}
        </v-tab>
      </v-tabs>
    </v-app-bar>
    <v-main>

      <div class="d-flex align-center flex-column" v-if="!environmentDataStore.websocketConnected">
        <v-card class="pa-8 ma-4">
          <h1>Connecting to WebSocket...</h1>
          <p>If this takes too long, ensure the backend API is running.</p>
          <v-progress-linear class="mt-4" height="10" rounded rounded-bar indeterminate color="primary"/>
        </v-card>
      </div>
      <RouterView/>
    </v-main>
    <v-footer style="max-height: 200px;" class="mt-8 pa-4">
      <div class="d-flex justify-center w-100">
        <template v-if="dataIsStale">
          <v-alert title="Data is outdated!" color="red" icon="mdi-clock-alert" max-width="700"
                   prominent>
            Last updated at {{ formatDate(environmentDataStore.environmentData.time) }} ({{ timeSinceUpdateString }})
          </v-alert>
        </template>
        <template v-else>
          <v-alert title="Up to date!" color="green" icon="mdi-clock-check" variant="outlined" max-width="700"
                   prominent>
            Last updated at {{ formatDate(environmentDataStore.environmentData.time) }} ({{ timeSinceUpdateString }})
          </v-alert>
        </template>
      </div>
    </v-footer>

  </v-app>

</template>

<style scoped>
.v-tab--selected {
  background-color: #00438c;
}
</style>

<style>
/* Remove default uppercase text from Material Design */
* {
  text-transform: none;
}
</style>
