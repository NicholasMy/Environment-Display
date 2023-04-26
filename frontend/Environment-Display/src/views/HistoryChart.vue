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

    <div v-if="loadingData" class="d-flex justify-center align-center">
      <v-progress-circular class="ma-4" indeterminate size="64"/>
      <h2>Loading</h2>
    </div>
    <Line v-else :data="historyChart" :options="chartOptions"/>
    <v-checkbox v-model="autoScale" label="Auto Scale" class="mt-2"/>
  </div>
</template>

<script setup lang="ts">
import {Line} from 'vue-chartjs'
import {computed, reactive, ref, watch} from "vue";
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
const autoScale = ref(true)
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


const chartOptions = computed(() => {
  return {
    responsive: true,
    maintainAspectRatio: true,
    scales: {
      y: {
        beginAtZero: !autoScale.value
      },
      x: {
        type: 'time',
        time: {
          unit: days.value > 2 ? 'day' : 'hour',
        }
      }
    },
    animation: {
      duration: 0
    }
  }
})

function getHistoricData(room: string, days: number) {
  loadingData.value = true
  fetch(`${window.location.protocol + "//" + window.location.hostname}:8085/history/${room}/${days}`)
      .then(res => res.json())
      .then(data => {
        Object.assign(fetchedData, data)
        fetchedData.length = data.length
      })
      .then(() => loadingData.value = false)
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
  height: 500px;
  max-width: 800px;
  width: 100%;
}

</style>
