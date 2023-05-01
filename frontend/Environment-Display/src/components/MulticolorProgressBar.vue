<template>

  <v-row no-gutters>
    <v-col :style="normalBarStyle">
      <v-progress-linear height="20"
                         :model-value="normalBarPercent"
                         :color="normalBarColor"
                         class="rounded-s-pill"/>
    </v-col>
    <v-col :style="warningBarStyle">
      <v-progress-linear height="20"
                         :model-value="warningBarPercent"
                         :color="warningBarColor"/>
    </v-col>
    <v-col :style="criticalBarStyle">
      <v-progress-linear height="20"
                         :model-value="criticalBarPercent"
                         :color="criticalBarColor"
                         class="rounded-e-pill"/>
    </v-col>
  </v-row>

</template>

<script setup lang="ts">
import {computed} from "vue";

const props = defineProps({
  min: {
    type: Number,
    required: true
  },
  warning: {
    type: Number,
    required: true
  },
  critical: {
    type: Number,
    required: true
  },
  max: {
    type: Number,
    required: true
  },
  value: {
    type: Number,
    required: true
  }
})

const normalBarStyle = computed(() => {
  return {maxWidth: (props.warning - props.min) / (props.max - props.min) * 100 + "%"}
})

const warningBarStyle = computed(() => {
  return {maxWidth: (props.critical - props.warning) / (props.max - props.min) * 100 + "%"}
})

const criticalBarStyle = computed(() => {
  return {maxWidth: (props.max - props.critical) / (props.max - props.min) * 100 + "%"}
})

const normalBarColor = computed(() => {
  if (props.value <= props.min) {
    return "light-blue"
  } else if (props.value < props.warning) {
    return "green"
  } else if (props.value < props.critical) {
    return "yellow-lighten-3"
  } else {
    return "red-lighten-3"
  }
})

const warningBarColor = computed(() => {
  if (props.value <= props.min) {
    return "light-blue"
  } else if (props.value < props.critical) {
    return "yellow-darken-1"
  } else {
    return "red-lighten-2"
  }
})

const criticalBarColor = computed(() => {
  if (props.value <= props.min) {
    return "light-blue"
  } else {
    return "red"
  }
})

const normalBarPercent = computed(() => {
  if (props.value <= props.min) {
    return 100
  }
  return (props.value - props.min) / (props.warning - props.min) * 100
})

const warningBarPercent = computed(() => {
  if (props.value <= props.min) {
    return 100
  }
  return Math.max(props.value - props.warning, 0.0) / (props.critical - props.warning) * 100
})

const criticalBarPercent = computed(() => {
  if (props.value <= props.min) {
    return 100
  }
  return Math.max(props.value - props.critical, 0.0) / (props.max - props.critical) * 100
})


</script>

<style scoped>
:deep(.v-progress-linear__determinate) {
  transition: none !important
}

</style>