<template>
  <div class="right-container user-info" v-if="$store.state.login"
  @click="showPanel = true" v-clickoutside="() => {showPanel = false}">
    <img v-if="$store.state.login" src="../../assets/logo.png"
    class="avatar" alt=""/>
    <span class="user-name"> {{$store.state.username}} </span>

  </div>
  <div class="right-container sign-in" v-else>
    <span> Sign In </span>
    <div>
      <button @click="showForm = !showForm"> Sign Up </button>
      <SignUp :class="{'show-form': showForm}"/>
    </div>
  </div>
</template>

<script>
import SignUp from "@/components/Navbar/UserInfo/SignUp";
import clickoutside from "@/utils/clickOutside";
export default {
  name: "UserInfo",
  directives: {clickoutside},
  data () {
    return {
      showForm: false,
      showPanel: false
    }
  },
  components: {SignUp}
}
</script>

<style scoped>

</style>