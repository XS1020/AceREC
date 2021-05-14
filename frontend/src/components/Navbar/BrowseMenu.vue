<template>
  <ul class="browse-menu" :class="{'show-menu': show}">
    <li v-for="(item, index) in menu"
        :class="{active: item.active, 'show': show}"
        @click="setActive(index)">
      <i :class="item.iconClass"/>
      {{ item.text }}
    </li>
  </ul>
</template>

<script>
export default {
  name: "BrowseMenu",
  data () {
    return {
      menu: [
        {text: "Paper", active: false, iconClass: "fa fa-star"},
        {text: "Author", active: false, iconClass: "fa fa-star"},
        {text: "Affiliation", active: false, iconClass: "fa fa-star"}
      ],
    }
  },
  props: ['show'],
  computed: {
    selectedMenu () {
      return this.menu.filter(item => item.active).map(item => item.text)
    }
  },
  methods: {
    setActive (index) {
      this.$set(this.menu[index], "active", !this.menu[index].active);
    }
  }
}
</script>

<style scoped>

</style>