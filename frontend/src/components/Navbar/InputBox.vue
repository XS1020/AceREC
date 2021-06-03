<template>
  <div class="input-wrapper">
    <i class="fa fa-search"/>
    <input type="text" placeholder="Search for something" class="input-box"
           v-model="queryString"
            @keyup.enter="submit"/>
  </div>
</template>

<script>
export default {
  name: "InputBox",
  data () {
    return {
      queryString: ""
    }
  },
  methods: {
    submit () {
      if (this.queryString.length > 0)
        this.$router.push({
          path: "/search",
          query: {
            queryString: encodeURI(this.queryString),
            mode: 'All'
          }
        })
    }
  }
}
</script>

<style scoped>

</style>