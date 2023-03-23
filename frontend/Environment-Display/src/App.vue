<script setup lang="ts">
import {RouterLink, RouterView} from 'vue-router'
import {reactive} from "vue";
import {useEnvironmentDataStore} from "@/stores/environmentData"
// import HelloWorld from './components/HelloWorld.vue'

const environmentDataStore = useEnvironmentDataStore()

// Create a GET request to fetch the list of rooms from the backend and populate data.rooms
fetch('http://localhost:8085/rooms')
    .then(res => res.json())
    // .then(json => {environmentDataStore.rooms = json.rooms})
    .then(json => {Object.assign(environmentDataStore.rooms, json.rooms)})
    // That was the major bug! We can't directly reassign to a reactive, or we lose the reactivity.

</script>

<template>
  <!--  <header>-->
  <!--    <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />-->

  <!--    <div class="wrapper">-->
  <!--      <HelloWorld msg="You did it!" />-->

  <!--      <nav>-->
  <!--        <RouterLink to="/">Home</RouterLink>-->
  <!--        <RouterLink to="/about">About</RouterLink>-->
  <!--      </nav>-->
  <!--    </div>-->
  <!--  </header>-->

  <header>
    <nav>
      Environment Display
      <ul>
        <li>
          <RouterLink :to="{name: 'home'}">Home</RouterLink>
        </li>


        <li v-for="room in environmentDataStore.rooms" :key="room.name">
          <RouterLink :to="{name: 'room', params: {room: room.name}}">{{ room.friendly_name }}</RouterLink>
        </li>

      </ul>
    </nav>
  </header>
  <main>
    <RouterView/>
    Environment data store: {{ environmentDataStore.environmentData }}
  </main>

</template>

<style scoped>
/*https://andybrewer.github.io/mvp/#docs*/
/*header {*/
/*  line-height: 1.5;*/
/*  max-height: 100vh;*/
/*}*/

/*.logo {*/
/*  display: block;*/
/*  margin: 0 auto 2rem;*/
/*}*/

/*nav {*/
/*  width: 100%;*/
/*  font-size: 12px;*/
/*  text-align: center;*/
/*  margin-top: 2rem;*/
/*}*/

/*nav a.router-link-exact-active {*/
/*  color: var(--color-text);*/
/*}*/

/*nav a.router-link-exact-active:hover {*/
/*  background-color: transparent;*/
/*}*/

/*nav a {*/
/*  display: inline-block;*/
/*  padding: 0 1rem;*/
/*  border-left: 1px solid var(--color-border);*/
/*}*/

/*nav a:first-of-type {*/
/*  border: 0;*/
/*}*/

/*@media (min-width: 1024px) {*/
/*  header {*/
/*    display: flex;*/
/*    place-items: center;*/
/*    padding-right: calc(var(--section-gap) / 2);*/
/*  }*/

/*  .logo {*/
/*    margin: 0 2rem 0 0;*/
/*  }*/

/*  header .wrapper {*/
/*    display: flex;*/
/*    place-items: flex-start;*/
/*    flex-wrap: wrap;*/
/*  }*/

/*  nav {*/
/*    text-align: left;*/
/*    margin-left: -1rem;*/
/*    font-size: 1rem;*/

/*    padding: 1rem 0;*/
/*    margin-top: 1rem;*/
/*  }*/
/*}*/
</style>
