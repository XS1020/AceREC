<template>
  <div @click="jumpToUser">
    <img :src="imgurl" alt="">
    <div class="scholar-info-container">
      {{name}}
      <span> {{affiliation}} </span>
    </div>
  </div>
</template>

<script>
function nameToUpperCase (str) {
  return str.toLowerCase().replace(/( |^)[a-z]/g, (L) => L.toUpperCase());
}
export default {
  name: "RelatedScholar",
  props: ['userId'],
  created() {
    this.$http({
      url: "/user/user_info",
      params: {
        local_id: this.userId
      }
    }).then(res => {
      const data = res.data
      this.name = JSON.parse(JSON.stringify(data.pinyin))
      this.name = this.name.join(" ")
      this.name = nameToUpperCase(this.name)
      this.imgurl = data.avatar_url
      this.affiliation = data.affiliation
    })
  },
  data () {
    return {
      name: "",
      affiliation: "",
      imgurl: ""
    }
  },
  methods: {
    jumpToUser () {
      this.$router.push('/profile/' + this.userId)
    }
  }
}
</script>

<style scoped>

</style>