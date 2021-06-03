<template>
  <ul class="view-options" :style="{'--selected-option': selectedOption * 120 + 'px'}">
    <router-link v-for="(option, index) in options"
                 @click.native="setOption(index)"
                 :to="option.to" tag="li">
      {{option.text}}
    </router-link>
  </ul>
</template>

<script>
export default {
  name: "ViewOptions",
  props: ['options'],
  data () {
    return {
      selectedOption: 0
    }
  },
  methods: {
    setOption (index) {
      this.selectedOption = index
    }
  }
}
</script>

<style lang="less">
.view-options {
  list-style: none;
  position: absolute;
  right: 20px;
  top: 20px;
  display: flex;
  justify-content: flex-end;
  padding: 0;
  li {
    width: 120px;
    font-weight: 600;
    text-align: center;
    cursor: pointer;
  }
  &:after {
    position: absolute;
    content: "";
    background-color: mediumpurple;
    height: 3px;
    width: 50px;
    bottom: -5px;
    left: 35px;
    transition: all 0.3s;
    transform: translateX(var(--selected-option));
  }
}
</style>