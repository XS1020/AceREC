<template>
  <div @click="jumpToIndex">
    text
    <strong>Fuck</strong>
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

</style>