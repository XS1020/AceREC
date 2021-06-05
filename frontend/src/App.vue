<template>
  <div id="app">
    <nav-bar></nav-bar>
    <div id="main-wrap">
      <router-view @showExportOptions="showExportOptions"/>
    </div>
    <div class="pop-up-window" v-if="exportOptions">
      <ExportOptions  @closePopup="exportOptions = false" :id="paperId"/>
    </div>
    <BrowseHistory v-if="this.$store.state.login"/>
  </div>
</template>
<script>
import NavBar from "./components/NavBar";
import BrowseHistory from "@/components/BrowseHistory";
export default {
  name: "App",
  components: {
    BrowseHistory,
    NavBar,
    ExportOptions: () => import("./components/Home/ExportOptions")
  },
  mounted() {
  },
  data () {
    return {
      exportOptions: false,
      paperId: ""
    }
  },
  methods: {
    showExportOptions(id) {
      this.paperId = id
      this.exportOptions = true
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
  z-index: 1;
  position: fixed;
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
