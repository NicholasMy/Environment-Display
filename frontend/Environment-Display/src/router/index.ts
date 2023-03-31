import {createRouter, createWebHistory} from 'vue-router'
import MainView from "@/views/HomeView.vue";
import RoomView from "@/views/RoomView.vue";
import TestView from "@/views/TestView.vue";

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
        },
        {
            path: '/test',
            name: 'test',
            component: TestView
        }
    ]
})

export default router
