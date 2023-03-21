<template>
  This is the view for a particular room: {{ $route.params.room }}

  <monitor :name="$route.params.room" />

</template>

<script>
import Monitor from "@/components/monitor.vue";

export default {
  name: "RoomView",
  components: {Monitor}
}
</script>

<style scoped>

</style>