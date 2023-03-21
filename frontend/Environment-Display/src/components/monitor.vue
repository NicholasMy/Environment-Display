<template>
  <article>
    <aside>
      <h1>{{ name }}</h1>
      <h1>{{ store.environmentData[props.name].current }} {{ store.environmentData[props.name].units }}</h1>
    </aside>
  </article>
</template>

<script>
export default {
  name: "monitor"
}
</script>
<script setup>
import {useEnvironmentDataStore} from "@/stores/environmentData";
import {reactive} from "vue";

const props = defineProps({
  name: String,
})
const store = useEnvironmentDataStore()

</script>

<style scoped>

</style>