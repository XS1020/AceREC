<template>
  <div class="author-info-wrapper"
       @mouseenter="loaded = true; showDetail=true"
       @mouseleave="showDetail = false">
    <img src="../../assets/avatar_default.jpg" alt="" @click="jumpToAuthor(authorId)"/>
    <span> {{name}} </span>
    <AuthorDetail v-show="showDetail" v-if="loaded" :detail-type="'author'"
    :name="name" :affiliation="affiliation" :avatar="imgurl" :desc="desc"/>
  </div>
</template>

<script>
export default {
  name: "AuthorInfo",
  props: ['authorId'],
  created() {
    this.$http({
      url: '/user/user_info',
      params: {
        local_id: this.authorId
      }
    }).then(res => {
      this.name = res.data.pinyin[0].toUpperCase() + " " + res.data.pinyin.slice(1).join('')
      this.imgurl = res.data.avatar_url
      this.affiliation = res.data.affiliation
      this.desc = res.data.research_list.join(', ')
    })
  },
  components: {
    AuthorDetail: () => import("./ItemDetail"),
  },
  data () {
    return {
      name: "",
      imgurl: "",
      affiliation: "",
      desc: "",
      showDetail: false,
      loaded: false
    }
  },
  methods: {
    jumpToAuthor (author) {
      console.log(author)
      this.$router.push('/profile/' + author)
    }
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
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  height: 50px;
  width: 50px;
}
.author-info-wrapper>span {
  font-weight: 600;
  margin-left: 20px;
  color: #767676;
}

</style>