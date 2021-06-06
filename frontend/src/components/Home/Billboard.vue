<template>
  <div class="billboard-container clearfix">
    <div class="billboard-col">
      <img :src="data.imgurl" alt="" class="billboard-cover"/>
    </div>
    <div class="billboard-col">
      <h2 class="billboard-title"> {{data.text}} </h2>
      <span class="billboard-author"> {{data.time}} </span>
      <ul class="billboard-star clearfix">
        <li class="active" v-for="count in stars"><i class="fa fa-star"/></li>
        <li v-for="count in 5-stars"><i class="fa fa-star"/></li>
        <li class="views"> {{views}} Views </li>
      </ul>
      <span class="desc" v-for="news in data.desc">
        {{news}}
      </span>
      <button class="see-paper-btn"><a :href="data.originURL" target="_blank"> See This Conference </a></button>
    </div>
  </div>
</template>

<script>
export default {
  name: "Billboard",
  props: ['data'],
  data () {
    return {
      desc: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse non odio ac sapien maximus malesuada non a tellus. Integer et tempor orci, vel mollis urna. Nullam rutrum neque fermentum dui volutpat, a faucibus nulla bibendum.",
      stars: 4,
      views: "1,322",
      author: "Nishino Nanase",
      title: "BIG MAGIC: Creative Living",
      coverSrc: require("../../assets/cover.jpg")
    }
  },
  methods: {
    jumpToSite () {
      this.$router.push(this.data.originURL)
    }
  }
}
</script>

<style scoped>
.billboard-container {
  width: 100%;
  display: block;
}
.billboard-col {
  width: 50%;
  float: left;
  padding-top: 20px;
}

.billboard-title {
  font-size: 22px;
  font-weight: 600;
  color: white;
  margin-bottom: 5px;
  padding: 0 30px;
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
}
.billboard-author {
  color: #e7e7e7;
  font-size: 12px;
  padding: 0 30px;
}
.billboard-col p {
  font-size: 14px;
  color: #f3f3f3;
  padding: 0 30px;
  line-height: 22px;
}
.billboard-star {
  list-style: none;
  margin: 10px 0;
  padding: 0 30px;
}
.billboard-star > li {
  float: left;
  font-size: 13px;
  margin: 0 2px;
  color: white;
}
.billboard-star > li.active {
  color: purple;
}
.billboard-star .views {
  margin-left: 30px;
  color: #f0f0f0;
}
.see-paper-btn {
  background-color: white;
  font-size: 16px;
  padding: 10px 60px;
  border-radius: 20px;
  color: #8A0868;
  font-weight: 600;
  line-height: 20px;
  margin-top: 30px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2);
}
.see-paper-btn a {
  text-decoration: none;
}
.billboard-cover {
  width: 80%;
  height: 432px;
  transform: translate3d(50px, 50px, 100px);
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2);
}
.desc {
  font-size: 16px;
  font-weight: 400;
  display: block;
  color: #e7e7e7;
  margin: 10px;
  padding-left: 20px;
}
</style>