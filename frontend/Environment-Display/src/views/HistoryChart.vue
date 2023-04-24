<template>
  <div>
    <h1>Charts!</h1>
    <Line v-if="!loadingData" :data="historyChart" :options="chartOptions"/>
    <p>Loading? {{ loadingData }}</p>
    {{fetchedData}}
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

const historyChart = {
    datasets: [
      {
        label: 'Temperature',
        backgroundColor: '#21c965',
        color: '#ffffff',
        xAxisKey: 'timestamp',
        yAxisKey: 'temperature',
        data: fetchedData
      }
    ]
  }

const chartOptions = reactive({
  responsive: false,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: false
    }
  }
})


function getHistoricData(room: string, days: number) {
  loadingData.value = true
  fetch(`${window.location.protocol + "//" + window.location.hostname}:8085/history/${room}/${days}`)
      .then(res => res.json())
      .then(res => Object.assign(fetchedData, res))
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
