<template>
  <div id="app">
    <nav-bar></nav-bar>
    <div id="main-wrap">
      <router-view @showExportOptions="showExportOptions"/>
    </div>
    <div class="pop-up-window">
      <ExportOptions/>
    </div>
  </div>
</template>
<script>
import NavBar from "./components/NavBar";
export default {
  name: "App",
  components: {
    NavBar,
    ExportOptions: () => import("./components/Home/ExportOptions")
  },
  methods: {
    showExportOptions () {
    }
  }
}
</script>
<style lang="less">
@import "assets/css/baseStyle.less";
#main-wrap {
  margin-top: 80px;
}
#app {
  width: 1440px;
}
.pop-up-window {
 position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.1);
  display: flex;
  justify-content: center;
  align-items: center;
  & > div {
    .display-card();
    padding: 40px;
  }
}
</style>
