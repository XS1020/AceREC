<template>
  <div class="sign-up-form">
    <div class="form-wrapper">
      <h2> Sign Up </h2>
      <i class="fa fa-percent"/>
      <CleverInputBox :text="'Username'" :type="'text'" :hint="'No more than 16 letters'"></CleverInputBox>
      <i class="fa fa-percent"/>
      <CleverInputBox :text="'E-mail'" :type="'text'"></CleverInputBox>
      <i class="fa fa-percent"/>
      <CleverInputBox :text="'Password'" :type="'password'" :hint="'8~20 letters'"></CleverInputBox>
      <i class="fa fa-percent"/>
      <CleverInputBox :text="'Confirm Password'" :type="'password'"></CleverInputBox>
      <button>Create Account </button>
    </div>
  </div>
</template>

<script>
import CleverInputBox from "@/components/Navbar/UserInfo/CleverInputBox";
export default {
  name: "SignUp",
  components: {CleverInputBox}
}
</script>

<style scoped>
.sign-up-form .form-wrapper {
  height: 0;
  overflow: hidden;
}
.show-form .form-wrapper {
  height: auto;
}
</style>