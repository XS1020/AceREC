<template>
  <div class="paper-info-wrapper"
       @mouseenter="loaded = true; showDetail=true"
       @mouseleave="showDetail = false">
    <img src="../../assets/cover.jpg" alt=""/>
    <div>
      <span> BIG MAGIC: Creative Living Beyond Fear </span>
      <p> by Julie Klassen </p>
    </div>
    <PaperDetail v-show="showDetail" v-if="loaded" :detail-type="'paper'"/>
  </div>
</template>

<script>
export default {
  name: "PaperInfo",
  components: {
    PaperDetail: () => import("./ItemDetail")
  },
  data () {
    return {
      showDetail: false,
      loaded: false
    }
  }
}
</script>

<style scoped>
.paper-info-wrapper {
  display: flex;
  justify-content: left;
  margin: 20px 0;
  box-sizing: border-box;
  padding: 5px 0;
}
.paper-info-wrapper>img {
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.4);
  height: 100px;
  width: 65px;
}
.paper-info-wrapper span {
  font-weight: 600;
  margin-left: 20px;
  color: #767676;
  max-width: 200px;
  line-height: 26px;
  display: block;
}
.paper-info-wrapper p {
  color: #989898;
  font-size: 14px;
  margin-left: 20px;
}
</style>