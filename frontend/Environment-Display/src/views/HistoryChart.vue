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
const fetchedData = reactive([])
// const fakeData = [{timestamp: '2016-12-25', temperature: 20}, {timestamp: '2016-12-26', temperature: 10}, {timestamp: '2016-12-27', temperature: 15}]
// const fakeData = [{x: 1, y: 20}, {x: 2, y: 0.5}, {x: 3, y: 4}, {x: 4, y: 10}]
const fakeData = [{"temperature": 70.8, "humidity": 36.9, "timestamp": "2023-04-24T10:09:52"}, {
  "temperature": 70.8,
  "humidity": 36.8,
  "timestamp": "2023-04-24T10:10:05"
}, {"temperature": 70.8, "humidity": 36.8, "timestamp": "2023-04-24T10:10:16"}, {
  "temperature": 70.8,
  "humidity": 36.8,
  "timestamp": "2023-04-24T10:10:26"
}, {"temperature": 70.9, "humidity": 36.7, "timestamp": "2023-04-24T10:10:59"}, {
  "temperature": 70.9,
  "humidity": 36.7,
  "timestamp": "2023-04-24T10:11:10"
}, {"temperature": 70.9, "humidity": 36.6, "timestamp": "2023-04-24T10:11:20"}, {
  "temperature": 70.9,
  "humidity": 36.6,
  "timestamp": "2023-04-24T10:11:31"
}, {"temperature": 70.9, "humidity": 36.6, "timestamp": "2023-04-24T10:11:41"}, {
  "temperature": 71.0,
  "humidity": 36.6,
  "timestamp": "2023-04-24T10:11:51"
}]

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

// const historyChart = reactive({
//   labels: fetchedData.map((dataPoint: any) => dataPoint.timestamp),
//   datasets: [
//     {
//       label: 'Temperature',
//       backgroundColor: '#21c965',
//       color: '#ffffff',
//       // xAxisKey: '',
//       // yAxisKey: 'temperature',
//       // xAxisType: 'time',
//       data: fetchedData.map((dataPoint: any) => dataPoint.temperature)
//     }
//   ]
// })

const historyChart = computed(() => {
  return {
    labels: fetchedData.map((dataPoint: any) => dataPoint.timestamp),
    datasets:
        [
          {
            label: 'Temperature',
            backgroundColor: '#21c965',
            color: '#ffffff',
            // xAxisKey: '',
            // yAxisKey: 'temperature',
            // xAxisType: 'time',
            data: fetchedData.map((dataPoint: any) => dataPoint.temperature)
          }
        ]
  }

})

const exampleChart = {
  // labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
  labels: fakeData.map((dataPoint: any) => dataPoint.timestamp),
  datasets: [
    {
      label: 'Data One',
      backgroundColor: '#f87979',
      data: fakeData.map((dataPoint: any) => dataPoint.temperature)
    }
  ]
}

const chartOptions = {
  responsive: false,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: false,
    }
  },
  // options: {
  //   parsing: {
  //     xAxisKey: "timestamp",
  //     yAxisKey: "temperature"
  //   }
  // }
}


function getHistoricData(room: string, days: number) {
  loadingData.value = true
  fetch(`${window.location.protocol + "//" + window.location.hostname}:8085/history/${room}/${days}`)
      .then(res => res.json())
      .then(res => Object.assign(fetchedData, res))
      // .then(() => buildChart())
      .then(() => loadingData.value = false)
      .then(() => console.log(fetchedData))
}


const route = useRoute()
watch(() => route.params.room, () => {
      // Reload chart data when the route (room) changes
      getHistoricData(route.params.room.toString(), 1)
    },
    {immediate: true})


</script>

<script lang="ts">
export default {
  name: 'HistoryChart'
}
</script>
