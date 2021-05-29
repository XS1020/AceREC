<template>
  <div class="image-not-loaded">
    <img src="../assets/warning-fill.svg" alt="">
    Preview Not Available
  </div>
</template>

<script>
export default {
  name: "ImageNotLoaded"
}
</script>

<style lang="less">
.image-not-loaded {
  background-color: #e7e7e7;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 8px;
  img {
    width: 20%;
  }
}
</style>