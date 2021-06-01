<template>
  <div class="right-container user-info" v-if="$store.state.login"
  @click="showThePanel" v-clickoutside="() => {showPanel = false}">
    <div>
      <img v-if="$store.state.login" src="../../assets/logo.png"
      class="avatar" alt=""/>
      <UserPanel :show="showPanel"/>
    </div>
    <span class="user-name"> {{$store.state.userName}} </span>

  </div>
  <div class="right-container sign-in" v-else>
    <span @click="signIn"> Sign In </span>
    <div>
      <button @click="jumpToSignUp"> Sign Up </button>
    </div>
  </div>
</template>

<script>
import SignUp from "@/components/Navbar/UserInfo/SignUp";
import clickoutside from "@/utils/clickOutside";
import BrowseCategories from "@/components/Navbar/BrowseCategories";
import UserPanel from "@/components/Navbar/UserInfo/UserPanel";
export default {
  name: "UserInfo",
  directives: {clickoutside},
  data () {
    return {
      showForm: false,
      showPanel: false
    }
  },
  methods: {
    signIn () {
      this.$router.push("/signin")
    },
    showThePanel () {
      console.log("hhh");
      this.showPanel = true
    },
    jumpToSignUp () {
      this.$router.push("/signup")
    }
  },
  components: {BrowseCategories, SignUp, UserPanel}
}
</script>

<style scoped>

</style>