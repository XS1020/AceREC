<template>
  <div style="border-right: 2px solid #e7e7e7" v-clickoutside="closeMenu">
    <span class="browse-cate-title" @click="openMenu">
      <span> Browse Category </span>
      <i class="fa fa-chevron-down"/>
      <BrowseMenu :show="showMenu"/>
    </span>

  </div>
</template>

<script>
import BrowseMenu from "@/components/Navbar/BrowseMenu";
import clickoutside from "@/utils/clickOutside";
export default {
  name: "BrowseCategories",
  directives: {clickoutside},
  data () {
    return {
      showMenu: false
    }
  },
  methods: {
    closeMenu () {
      this.showMenu = false;
    },
    openMenu () {
      this.showMenu = true
    }
  },
  components: {BrowseMenu}
}
</script>

<style scoped>
</style>