<template>
  <div class="image-not-loaded" ref="this-wrap">
    <img src="../assets/warning-fill.svg" alt="">
    Preview Not Available
  </div>
</template>

<script>
export default {
  name: "ImageNotLoaded",
  mounted() {
    this.adjustSize()
  },
  methods: {
    adjustSize () {
      const ref = this.$refs["this-wrap"]
      if (ref.offsetWidth < 100) {
        ref.style.fontSize = "12px"
        ref.style.minHeight = '130px'
      }
    }
  }
}
</script>

<style lang="less">
.image-not-loaded {
  background-color: #e7e7e7;
  display: flex;
  min-height: 200px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  border-radius: 8px;
  img {
    width: 20%;
  }
}
</style>