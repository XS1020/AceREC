<template>
  <div class="nav-bar">
    <div class="left-container">
      <BrowseCategories></BrowseCategories>
      <InputBox/>
      <NavBarLogo/>
    </div>
    <UserInfo/>
  </div>
</template>

<script>
import BrowseCategories from "@/components/Navbar/BrowseCategories";
import InputBox from "@/components/Navbar/InputBox";
import NavBarLogo from "@/components/Navbar/NavBarLogo";
import UserInfo from "@/components/Navbar/UserInfo";
export default {
  name: "NavBar",
  components: {
    UserInfo,
    InputBox,
    BrowseCategories,
    NavBarLogo
  }
}
</script>

<style scoped>
</style>