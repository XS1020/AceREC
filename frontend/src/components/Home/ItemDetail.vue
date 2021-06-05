<template>
  <div class="author-info-detail clearfix" v-if="finishedLoading">
    <div class="avatar-container">
      <img :src="avatar" alt=""
           :class="{'author-avatar': detailType === 'author',
                    'paper-img': detailType ==='paper'}"
      />
      <span v-if="detailType==='author'"> {{title}} </span>
    </div>
    <div class="author-info-container">
      <h2>  {{name}} </h2>
      <span> {{affiliation}} </span>
      <p> {{desc}} </p>
      <span><i class="fa fa-location-arrow"/> {{location}} </span>
    </div>
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
    setTimeout(() => {this.finishedLoading = true}, 100)
  },
  props: ['detailType', 'name', 'affiliation', 'avatar', 'desc'],
  data () {
    return {
      finishedLoading: false,
      title: "Professor",
      institution: "Nogizaka 46",
      location: "China Mainland",
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
  z-index: 2;
  border-radius: 10px;
  transition: all 0.3s;
}
.author-info-detail:before {
  content: "";
  width: 10px;
  height: 10px;
  z-index: 1;
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
.avatar-container > img.author-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin-top: 20px;
  object-fit: contain;
}
.avatar-container > img.paper-img {
  width: 80px;
  height: 120px;
  margin-top: 20px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
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