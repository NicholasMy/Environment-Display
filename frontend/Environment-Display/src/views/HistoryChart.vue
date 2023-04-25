<template>
  <div class="charts-div">
    <!--    <h1>Charts!</h1>-->
    <div class="d-flex flex-row align-center">
      <h3 class="py-2">History Chart of Past</h3>
      <v-text-field class="mx-2" style="max-width: 50px" variant="underlined" type="number" v-model="days"
                    @change="reloadChart"></v-text-field>
      <h3 class="py-2">{{ days != 1 ? "Days" : "Day" }} for
        {{ store.getDataForRoom(roomName)?.friendly_name || `"${roomName}"` }}</h3>
    </div>

    <div v-if="loadingData" class="charts-div d-flex justify-center align-center">
      <v-progress-circular class="ma-4" indeterminate size="64"/>
      <h2>Loading</h2>
    </div>
    <Line v-else :data="historyChart" :options="chartOptions"/>
  </div>
</template>

<script setup lang="ts">
import {Line} from 'vue-chartjs'
import {computed, getCurrentInstance, reactive, ref, watch} from "vue";
// https://vue-chartjs.org/examples/
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend, TimeScale,
} from 'chart.js';
import {useRoute} from "vue-router";
import 'chartjs-adapter-moment'
import {useEnvironmentDataStore} from "@/stores/environmentData";
import {da} from "vuetify/locale";

ChartJS.register(
    CategoryScale,
    LinearScale,
    TimeScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

const loadingData = ref(false)
const fetchedData = reactive([])
const roomName = ref('')
const days = ref(1)
const store = useEnvironmentDataStore()

const historyChart = computed(() => {
  return {
    labels: fetchedData.map((dataPoint: any) => dataPoint.timestamp),
    datasets:
        [
          {
            label: 'Temperature (°F)',
            backgroundColor: '#21c965',
            data: fetchedData.map((dataPoint: any) => dataPoint.temperature)
          },
          {
            label: 'Relative Humidity (%)',
            backgroundColor: '#2f8bb0',
            data: fetchedData.map((dataPoint: any) => dataPoint.humidity)
          }
        ]
  }
})


const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: false,
    },
    x: {
      type: 'time',
      time: {
        unit: 'hour'
      }
    }
  },
  animation: {
    duration: 0
  }
}

function getHistoricData(room: string, days: number) {
  loadingData.value = true
  fetch(`${window.location.protocol + "//" + window.location.hostname}:8085/history/${room}/${days}`)
      .then(res => res.json()
        // Object.assign(fetchedData, [{"temperature": 63.9, "humidity": 52.0, "timestamp": "2023-04-24T10:09:55"}, {"temperature": 63.9, "humidity": 52.0, "timestamp": "2023-04-24T10:10:07"}])
        // Object.assign(fetchedData, js)
        // loadingData.value = false
      )
      .then(data => {
        Object.assign(fetchedData, data)
      })
      .then
      (() => {
        loadingData.value = false
      })
      // TODO: Fix the old data not being removed bug

}

function reloadChart() {
  getHistoricData(roomName.value, days.value)
}


const route = useRoute()
watch(() => route.params.room, () => {
      if (route.params.room != undefined) {
        // Reload chart data when the route (room) changes
        roomName.value = route.params.room.toString()
        reloadChart()
      }
    },
    {immediate: true})


</script>

<script lang="ts">
export default {
  name: 'HistoryChart'
}
</script>

<style scoped>

.charts-div {
  height: 400px;
  max-width: 800px;
  width: 100%;
}

</style>
