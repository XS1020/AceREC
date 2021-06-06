<template>
  <div class="user-panel" :class="{'user-panel-active': show}">
    <ul>
      <li  @click="jumpToSettings">
        <i class="fa fa-cogs"/>
        Settings
      </li>
      <li @click="signOut">
        <i class="fa fa-sign-out"/>
        Sign Out
      </li>
      <li @click="jumpToUser">
        <i class="fa fa-github"/>
        My Profile
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "UserPanel",
  props: ['show'],
  methods: {
    signOut () {
      this.$store.commit('logout')
      this.$router.push("/signin")
    },
    jumpToSettings () {
      this.$router.push("/settings")
    },
    jumpToUser () {
      if (this.$store.state.remoteId !== -1)
        this.$router.push('/profile/' + this.$store.state.localId)
    }
  }
}
</script>

<style scoped>
.user-panel {
  position: absolute;
  top: 90px;
  background-color: white;
  border-radius: 5px;
  transition: all 0.3s;
  height: 0;
  overflow: hidden;
}
.user-panel-active:before {
  content: "";
  display: block;
  width: 12px;
  height: 12px;
  position: absolute;
  right: 15px;
  top: -6px;
  z-index: -1;
  background-color: white;
  transform: rotate(45deg);
}
.user-panel-active {
  height: auto;
  overflow: visible;
}
.user-panel-active ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.user-panel-active ul > li {
  width: 140px;
  margin: 0;
  color: #989898;
  padding: 10px;
  transition: all 0.3s;
  cursor: pointer;
  font-size: 12px;
}
.user-panel-active ul > li:hover {
  color: rebeccapurple;
}
.user-panel-active ul > li:active {
  color: #f7f7f7;
  background-color: mediumpurple;
}
.user-panel-active ul > li:nth-child(1) {
  border-top-right-radius: 5px;
  border-top-left-radius: 5px;
}
.user-panel-active ul > li:nth-last-child(1) {
  border-bottom-right-radius: 5px;
  border-bottom-left-radius: 5px;
}
.user-panel-active ul > li > i {
  margin-right: 10px;
}
</style>