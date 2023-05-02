<template>
  <div class="charts-div">
    <!--    <h1>Charts!</h1>-->
    <div class="d-flex flex-row flex-wrap align-center">
      <h3 class="py-2">History Chart of Past</h3>
      <!--      <v-text-field class="mx-2" style="max-width: 50px" variant="underlined" type="number" v-model="days"-->
      <!--                    @change="reloadChart"></v-text-field>-->
      <!--      The Vuetify number input raises an exception when changing the number, so we'll use the uglier default one -->
      <input min="1" class="mx-2" style="max-width: 50px" type="number" v-model="data.timeCount" @change="reloadChart"/>
      <!--      Allow selecting days or hours -->
      <v-select variant="plain" class="mx-2" style="max-width: 70px" v-model="data.timeUnitSelection"
                :items="dynamicTimeOptions" @update:modelValue="reloadChart"/>
      <!--      <h3 class="py-2">{{ data.timeCount !== 1 ? "Days" : "Day" }}-->
      <h3 class="py-2">for
        {{ store.getDataForRoom(data.roomName)?.friendly_name || `"${data.roomName}"` }}</h3>

      <span class="ml-auto">
          Resolution
        <input min="0" step="100" class="mx-2" style="max-width: 75px" type="number" v-model="data.resolution"
               @change="reloadChart"/>
        <v-btn class="pa-2 ma-2" icon="mdi-refresh" @click="reloadChart"/>
      </span>

    </div>

    <div v-if="data.loadingData" class="d-flex justify-center align-center">
      <v-progress-circular class="ma-4" indeterminate size="64"/>
      <h2>Loading</h2>
    </div>
    <Line v-else :data="historyChart" :options="chartOptions"/>
    <div v-if="!data.loadingData" class="d-flex flex-row align-center">
      <v-checkbox v-model="data.autoScale" label="Auto Scale" class="mt-2"/>
      <p>Showing {{ data.fetchedData.length }} data points.</p>
    </div>
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

const timeUnits = {
  "singular": ["Day", "Hour"],
  "plural": ["Days", "Hours"]
}

const data = reactive({
  loadingData: false,
  fetchedData: [],
  autoScale: true,
  roomName: '',
  timeCount: 1,
  timeUnit: timeUnits.singular[0],  // Always singular and lowercase
  timeUnitSelection: timeUnits.singular[0], // May be singular or plural and capitalized
  resolution: 1000,
})

const store = useEnvironmentDataStore()

const dynamicTimeOptions = computed(() => {
  return data.timeCount > 1 ? timeUnits.plural : timeUnits.singular
})


function updateTimeUnit() {
  // Runs when the user changes the time count

  // Update the front end display of the time unit
  const isPlural = data.timeCount > 1
  const selectedTimeUnit = data.timeUnitSelection
  let selectedTimeUnitIndex = timeUnits.singular.indexOf(selectedTimeUnit)
  if (selectedTimeUnitIndex === -1) {
    selectedTimeUnitIndex = timeUnits.plural.indexOf(selectedTimeUnit)
  }

  if (isPlural) {
    data.timeUnitSelection = timeUnits.plural[selectedTimeUnitIndex]
  } else {
    data.timeUnitSelection = timeUnits.singular[selectedTimeUnitIndex]
  }

  // Update the time unit on the backend to be the singular form of the selected time unit
  data.timeUnit = timeUnits.singular[selectedTimeUnitIndex].toLowerCase()
}


watch(() => data.timeCount, updateTimeUnit)

const historyChart = computed(() => {
  return {
    labels: data.fetchedData.map((dataPoint: any) => dataPoint.timestamp),
    datasets:
        [
          {
            label: 'Temperature (°F)',
            backgroundColor: '#21c965',
            data: data.fetchedData.map((dataPoint: any) => dataPoint.temperature)
          },
          {
            label: 'Relative Humidity (%)',
            backgroundColor: '#2f8bb0',
            data: data.fetchedData.map((dataPoint: any) => dataPoint.humidity)
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
        beginAtZero: !data.autoScale
      },
      x: {
        type: 'time',
        time: {
          unit: data.timeUnit === "day" ? 'day' : 'hour',
        }
      }
    },
    animation: {
      duration: 0
    }
  }
})

function getHistoricData(room: string, hours: number, resolution: number) {
  data.loadingData = true
  fetch(`${window.location.protocol + "//" + window.location.hostname}:8085/history/${room}/${hours}/${resolution}`)
      .then(res => res.json())
      .then(newData => data.fetchedData = newData)
      .then(() => data.loadingData = false)
}

function reloadChart() {
  updateTimeUnit()
  const hours = data.timeUnit === "day" ? data.timeCount * 24 : data.timeCount
  getHistoricData(data.roomName, hours, data.resolution)
}


const route = useRoute()
watch(() => route.params.room, () => {
      if (route.params.room != undefined) {
        // Reload chart data when the route (room) changes
        data.roomName = route.params.room.toString()
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
