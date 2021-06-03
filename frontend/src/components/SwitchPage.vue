<template>
  <ul class="swich-page">
    <li v-for="index in range1"
        :class="{'active': index == curIndex}"
        @click="switchTo(index)"> {{index}} </li>
  </ul>
</template>

<script>
export default {
  name: "SwitchPage",
  props: ['totalPages', 'curIndex'],
  data () {
    return {
    }
  },
  computed: {
    range1 () {
      const list = []
      for (let i = Math.max(1, parseInt(this.curIndex) - 5); i <= Math.min(parseInt(this.curIndex) + 5, this.totalPages); i++)
        list.push(i)
      return list
    }
  },
  methods: {
    switchTo (index) {
      if (index !== this.curIndex)
        this.$emit('switchPage', index)
    }
  }
}
</script>

<style lang="less">
@import "../assets/css/baseStyle";
.swich-page {
  display: flex;
  width: 100%;
  justify-content: center;
  list-style: none;
  padding: 0;
  li {
    margin: 5px;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid @font-medium-grey;
    color: @font-medium-grey;
    cursor: pointer;
    transition: all 0.3s;
  }
  li:hover, li.active {
    color: white;
    background-color: mediumpurple;
  }
}
</style>