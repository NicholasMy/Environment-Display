<template>
  <div>
    <h1>Charts!</h1>
    <Line v-if="!loadingData" :data="historyChart" :options="chartOptions"/>
    <p>Loading? {{ loadingData }}</p>
    {{ fetchedData }}
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
  Legend,
} from 'chart.js';
import {useRoute} from "vue-router";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

const loadingData = ref(false)
const fetchedData = reactive({})
// const fakeData = [{timestamp: '2016-12-25', temperature: 20}, {timestamp: '2016-12-26', temperature: 10}, {timestamp: '2016-12-27', temperature: 15}]
const fakeData = [{x: 1, y: 20}, {x: 2, y: 0.5}, {x: 3, y: 4}, {x: 4, y: 10}]

// function buildChart() {
//   let newChartData = {
//     datasets: [
//       {
//         label: 'Temperature',
//         backgroundColor: '#21c965',
//         color: '#ffffff',
//         xAxisKey: 'x',
//         // yAxisKey: 'temperature',
//         // xAxisType: 'time',
//         data: fakeData
//       }
//     ]
//   }
//   Object.assign(historyChart, newChartData)
// }

const historyChart = reactive({
  datasets: [
    {
      label: 'Temperature',
      backgroundColor: '#21c965',
      color: '#ffffff',
      // xAxisKey: '',
      // yAxisKey: 'temperature',
      // xAxisType: 'time',
      data: fetchedData
    }
  ]
})

const chartOptions = {
  responsive: false,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: false,
      min: 0,
      max: 100
    }
  },
  options: {
    parsing: {
      xAxisKey: "x",
      yAxisKey: "y"
    }
  }
}


function getHistoricData(room: string, days: number) {
  loadingData.value = true
  fetch(`${window.location.protocol + "//" + window.location.hostname}:8085/history/${room}/${days}`)
      .then(res => res.json())
      .then(res => Object.assign(fetchedData, fakeData))
      // .then(() => buildChart())
      .then(() => loadingData.value = false)
      .then(() => console.log(fetchedData))
}


const route = useRoute()
watch(() => route.params.room, () => {
      getHistoricData("davis339c", 1)
    },
    {immediate: true})


</script>

<script lang="ts">
export default {
  name: 'HistoryChart'
}
</script>
