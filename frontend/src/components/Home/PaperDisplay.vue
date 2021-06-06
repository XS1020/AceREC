<template>
  <div>
    <div class="paper-display-container">
        <loading-cpn v-if="!loaded"/>
        <error-cpn v-if="loaded===2"/>
        <div class="paper-display-main clearfix" v-if="loaded===1">
          <ImageNotLoaded v-if="imgSrc.length === 0"/>
          <img :src="imgSrc" alt="" v-else>
          <div>
            <h2 class="paper-display-title">{{title}}</h2>
            <span> by {{author}} </span>
            <ul class="paper-display-star clearfix">
              <li class="active" v-for="i in stars"><i class="fa fa-star"/></li>
              <li v-for="i in 5 - stars"><i class="fa fa-star"/></li>
              <li class="paper-views"> {{cited}} Cited </li>
            </ul>
            <p> {{desc}} </p>
          </div>
          <a class="view-detail" @click="jumpToDetail(srcPath)"> View Detail<i class="fa fa-angle-right"/> </a>
        </div>
<!--        <div class="paper-display-bottom" v-if="loaded">-->
<!--          <ul class="paper-display-viewers clearfix">-->
<!--            <li><img alt="" src="../../assets/avatar.webp"/></li>-->
<!--            <li><img alt="" src="../../assets/avatar.webp"/></li>-->
<!--          </ul>-->
<!--        </div>-->
    </div>
  </div>
</template>

<script>
import LoadingCpn from "@/components/LoadingCpn";
import ErrorCpn from "@/components/ErrorCpn";
import ImageNotLoaded from "@/components/ImageNotLoaded";
export default {
  name: "PaperDisplay",
  components: {ImageNotLoaded, ErrorCpn, LoadingCpn},
  props: ['srcPath'],
  mounted () {
    this.$http({
      url: "/api/CardInfo",
      params: {paperid: this.srcPath}
    }).then(res => {
      const data = res.data
      this.title = data.title
      this.desc = data.abstract
      this.author = data.author_name_list[0]
      this.imgSrc = data.imgurl
      this.loaded = 1
      this.cited = data.citation_count
    }).catch(error => {
      console.log(error)
      this.loaded = 2
    })
  },
  data () {
    return {
      imgSrc: "",
      title: "Act like it",
      author: "Lucy Parker",
      loaded: 0,
      cited: 0,
      desc: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse non odio ac sapien maximus malesuada non a tellus. Integer et tempor orci, vel mollis urna"
    }
  },
  methods: {
    jumpToDetail (paperId) {
      this.$router.push("/paper/" + paperId)
    }
  },
  computed: {
    stars () {
      if (this.cited >= 1000) return 5
      if (this.cited >= 500) return 4
      if (this.cited >= 200) return 3
      if (this.cited >= 100) return 2
      if (this.cited > 0) return 1
      return 0
    }
  }
}
</script>

<style scoped>
.paper-display-container {
  box-shadow: 0 5px 25px rgba(0,0,0,0.1);
  background-color: white;
  position: relative;
  min-height: 253px;
  min-width: 490px;
}
.paper-display-main {
  padding: 10px;
}
.paper-display-main h2 {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}
.paper-display-bottom {
  padding: 0;
}
.paper-display-main > img, .image-not-loaded{
  box-shadow: 0 5px 25px rgba(0,0,0,0.2);
  width: 40% !important;
  min-height: 248px;
  transform: translate(7%, -15%);
  float: left;
}
.paper-display-main > div {
  width: 60%;
  box-sizing: border-box;
  float: left;
  padding:0 30px;
}
.paper-display-main .paper-views {
  font-size: 12px;
  line-height: 23px;
  margin-left: 10px;
}
.paper-display-title {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #565656;
  margin-bottom: 4px;
}
.paper-display-main > div span {
  font-size: 13px;
  color: #989898;
  font-weight: 600;
}
.paper-display-star {
  list-style: none;
  margin: 10px 0;
  padding: 0;
}
.paper-display-star > li {
  color: #989898;
  float: left;
  margin: 2px;
}
.paper-display-star >li.active {
  color: orange;
}
.paper-display-main p {
  font-size: 13px;
  color: #989898;
  line-height: 24px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 4;
}
.paper-display-viewers {
  list-style: none;
  margin: 5px;
  padding: 10px 20px;
}
.paper-display-viewers li {
  float: left;
  margin: -2px;
}
.paper-display-viewers li > img {
  width: 30px;
  height: 30px;
  border-radius: 50%;
}
.paper-display-viewers li:nth-child(n + 1) {
  margin-left: -7px;
}
.paper-display-main .view-detail {
  position: absolute;
  bottom: 10px;
  right: 15px;
  font-size: 12px;
  color: rebeccapurple;
  text-decoration: none;
  cursor: pointer;
}
.view-detail:hover, .view-detail:active {
  text-decoration: underline;
}
.view-detail > i {
  margin-left: 10px;
}
</style>