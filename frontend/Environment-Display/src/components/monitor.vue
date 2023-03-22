<template>
  <article>
    <aside>
      <h1>{{ store.friendlyNamesMap.data }}</h1>
      <!--      TODO get the friendly room name to show-->

      <template v-if="store.getDataForRoom(name) != null">
        <h1>{{ store.environmentData[props.name].current }}
          {{ store.environmentData[props.name].units }}</h1>


      </template>

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