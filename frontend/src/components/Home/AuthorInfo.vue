<template>
  <div class="author-info-wrapper"
       @mouseenter="loaded = true; showDetail=true"
       @mouseleave="showDetail = false">
    <img src="../../assets/avatar.webp" alt=""/>
    <span> Hori Miona </span>
    <AuthorDetail v-show="showDetail" v-if="loaded" :detail-type="'author'"/>
  </div>
</template>

<script>
export default {
  name: "AuthorInfo",
  components: {
    AuthorDetail: () => import("./ItemDetail"),
  },
  data () {
    return {
      showDetail: false,
      loaded: false
    }
  },
  methods: {
  }
}
</script>

<style scoped>
.author-info-wrapper {
  display: flex;
  justify-content: left;
  align-items: center;
  margin: 20px 0;
  box-sizing: border-box;
  padding: 5px 0;
}
.author-info-wrapper>img {
  border-radius: 50%;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.4);
  height: 50px;
  width: 50px;
}
.author-info-wrapper>span {
  font-weight: 600;
  margin-left: 20px;
  color: #767676;
}

.view-home-page {
  border-top: 1px solid #e7e7e7;
}
</style>