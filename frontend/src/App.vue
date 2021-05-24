<template>
  <div id="app">
    <nav-bar></nav-bar>
    <div id="main-wrap">
      <router-view/>
    </div>
  </div>
</template>
<script>
import NavBar from "./components/NavBar";
export default {
  name: "App",
  components: {
    NavBar
  }
}
</script>
<style>
#main-wrap {
  margin-top: 80px;
}
#app {
  width: 1440px;
}
</style>
