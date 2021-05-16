<template>
  <div class="author-info-detail clearfix" v-if="finishedLoading && detailType==='author'">
    <div class="avatar-container">
      <img :src="avatar" alt=""/>
      <span> {{title}} </span>
    </div>
    <div class="author-info-container">
      <h2>  {{name}} </h2>
      <span> {{institution}} </span>
      <p> {{desc}} </p>
      <span><i class="fa fa-location-arrow"/> {{location}} </span>
    </div>
  </div>
  <div class="author-info-detail clearfix" v-else-if="finishedLoading && detailType==='paper'">

  </div>
  <div class="author-info-detail author-info-loading" v-else>
    <LoadingCpn/>
  </div>
</template>

<script>
import LoadingCpn from "@/components/LoadingCpn";
export default {
  name: "AuthorDetail",
  components: {LoadingCpn},
  beforeMount() {
    setTimeout(() => {this.finishedLoading = true}, 1000)
  },
  props: ['detailType'],
  data () {
    return {
      finishedLoading: false,
      name: "Hori Miona",
      title: "Professor",
      institution: "Nogizaka 46",
      desc: "CS undergraduate, KDE user, Vim\\NeoVim, i3, Archlinux beginner",
      avatar: require("../../assets/avatar.webp"),
      location: "Tokyo, Japan",
    }

  }
}
</script>

<style scoped>
.author-info-detail {
  position: absolute;
  background-color: white;
  padding: 0 20px;
  left: 250px;
  border-radius: 10px;
  transition: all 0.3s;
}
.author-info-detail:before {
  content: "";
  width: 10px;
  height: 10px;
  z-index: -1;
  background-color: inherit;
  position: absolute;
  left: -5px;
  top: 50%;
  transform: rotate(45deg);
}
.author-info-detail h2 {
  font-size: 18px;
  font-weight: 500;
  color: #767676;
  margin: 0;
}
.author-info-detail span {
  color: purple;
  font-size: 13px;
}
.avatar-container {
  float: left;
  width: 20%;
  text-align: center;
}
.avatar-container > img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin-top: 20px;
}
.author-info-container {
  float: left;
  width: 80%;
  box-sizing: border-box;
  padding: 20px;
}
.author-info-container > p {
  max-width: 300px;
  font-size: 14px;
  margin: 10px 0 0 0;
  line-height: 20px;
}
.author-info-loading {
  height: 140px;
  width: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>