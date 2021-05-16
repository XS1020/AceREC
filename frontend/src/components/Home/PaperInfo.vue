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
  name: "PaperInfo"
}
</script>

<style scoped>

</style>