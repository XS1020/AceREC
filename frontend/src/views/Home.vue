<template>
  <div class="home">
    <Carousel/>
    <div class="clearfix">
      <div class="sidebar-content">
        <div class="featured-author">
          <h2> Author of the week </h2>
          <AuthorInfo/>
          <AuthorInfo/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Home',
  components: {
    AuthorInfo: () => import("@/components/Home/AuthorInfo"),
    Carousel: () =>  import("@/components/Home/Carousel"),
  }
}
</script>
<style scoped>
.sidebar-content {
  width: 25%;
  float: left;
  padding: 40px;
}
.sidebar-content h2 {
  font-size: 22px;
  color: #767676;
  font-weight: 500;
  margin-left: 10px;
}
.main-content {
  width: 75%;
  float: left;
}
</style>
