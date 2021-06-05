<template>
  <div class="all-genres-container clearfix">
    <PaperDisplay v-for="paper in papers" :src-path="paper"
    />
  </div>
</template>

<script>
import PaperDisplay from "@/components/Home/PaperDisplay";
export default {
  name: "AllGenres",
  components: {PaperDisplay},
  created () {
    this.$http({
      url: "/api/mainpage",
      params: {
        local_id: this.$store.state.localId
      }
    }).then(res => {
      const jsRes = res.data
      this.papers = jsRes.Rec
      this.submitViewRec()
    })
  },
  data () {
    return {
      papers: []
    }
  },
  methods: {
    submitViewRec () {
      let param = new URLSearchParams()
      param.append('local_id', this.$store.state.localId)
      param.append('paper_id', this.papers)
      this.$http({
        method: "post",
        url: "/api/viewrecord",
        data: param
      }).then(res => {})
    }
  }
}
</script>

<style scoped>
.all-genres-container {
  width: 100%;
  margin: 50px 0;
  padding: 40px 40px;
}
.all-genres-container > div {
  float: left;
  width: 50%;
  box-sizing: border-box;
  /*display: flex;*/
  /*justify-content: center;*/
  /*align-items: center;*/
  padding: 40px;

}
</style>