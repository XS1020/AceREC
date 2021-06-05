<template>
  <LoadingCpn v-if="loading" class="cited-paper-item"/>
  <div class="cited-paper-item" @click="jumpToPaper" :key="id" v-else>
    <img :src="imgurl" alt="" v-if="imgurl.length">
    <ImageNotLoaded v-else/>
    <div class="paper-item-info">
      <h2> {{title}} </h2>
      <span><i class="fa fa-user-circle-o"/> {{authorList}} </span>
      <span><i class="fa fa-clock-o"/> {{year}} </span>
      <ul class="label-list">
        <li v-for="tag in tags"> {{tag}} </li>
      </ul>
    </div>
  </div>
</template>

<script>
import ImageNotLoaded from '@/components/ImageNotLoaded'
import LoadingCpn from "@/components/LoadingCpn";
export default {
  name: "CitedPaperItem",
  props: ['paperInfo'],
  created() {
    this.id = this.paperInfo.id
    this.click = this.paperInfo.click
    this.$http({
      url: "/api/citecardinfo",
      params: {
        paperid: this.id
      }
    }).then(res => {
      const data = res.data
      this.title = data.title
      this.year = data.year
      this.imgurl = data.imgurl
      this.authorList = JSON.parse(JSON.stringify(data.author_name_list)).slice(0,10).join(", ")
      if (data.author_name_list.length > 10)
        this.authorList = this.authorList + "..."
      this.tags = JSON.parse(JSON.stringify(data.tags))
      this.tags = this.tags.sort((a, b) => a.length - b.length)
      this.tags = this.tags.slice(0,3)
      return new Promise(resolve => resolve())
    }).then(() => {
      this.loading = false
    })
  },
  data () {
    return {
      loading: true,
      id: "",
      click: 0,
      title: "",
      year: 0,
      imgurl: "",
      authorList: "",
      tags: []
    }
  },
  components: {
    LoadingCpn,
    ImageNotLoaded
  },
  methods: {
    jumpToPaper () {
      if (this.click)
        this.$router.push("/paper/" + this.id)
    }
  }
}
</script>

<style lang="less">
@import "../../assets/css/baseStyle";
.cited-paper-container {
  display: flex;
  padding: 10px;
  flex-direction: column;
  justify-content: flex-start;
  & > div {
    width: 100%;
    margin: 5px;
  }
  .cited-paper-item {
    position: relative;
    min-height: 120px;
    display: flex;
    justify-content: flex-start;
    border-radius: 8px;
    padding: 10px;
    transition: all 0.3s;
    &:hover {
      box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    & > img, & > div.image-not-loaded {
      position: relative;
      width: 18%;
    }
    & > img {
      object-fit: contain;
    }
    &:hover {
      &:after, &:before {
        position: absolute;
        top: 20%;
        width: 4px;
        content: "";
        background-color: mediumpurple;
        height: 60%;
      }
      &:before{
        left: 0;
      }
      &:after{
        right: 0;
      }
    }
  }
}
.paper-item-info {
  width: 80%;
  margin-left: 10px;
  h2 {
    font-size: 16px;
    margin-bottom: 5px;
    & ~ span {
      display: block;
      font-size: 14px;
      margin: 5px;
      color: @font-medium-grey;
    }
  }
  ul.label-list {
    margin: 0;
    padding: 0;
    display: flex;
    list-style: none;
    flex-wrap: wrap;
    li {
      margin: 5px;
      font-size: 12px;
      padding: 2px 5px;
      border-radius: 4px;
    }
    .label-list()
  }
}
</style>