import { createRouter, createWebHistory } from 'vue-router'
import MainView from "@/views/HomeView.vue";
import RoomView from "@/views/RoomView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      // component: HomeView
      component: MainView
    },
    {
      path: '/room/:room',
      name: 'room',
      component: RoomView
    }
  ]
})

export default router
