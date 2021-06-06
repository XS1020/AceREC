<template>
  <div @click="jumpToIndex">
    Ace
    <strong> REC </strong>
  </div>
</template>

<script>
export default {
  name: "NavBarLogo",
  methods: {
    jumpToIndex () {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
* {
  font-size: 18px;
}
strong {
  color: rebeccapurple;
}
</style>