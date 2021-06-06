<template>
  <div class="sign-up-wrap">
    <div class="sign-up-card">
      <div class="left-box">
        <h2> Sign In. </h2>
        <span> Sign in with your data provided during registration  </span>
        <div class="data-form">
          <span class="hint"> User Name </span>
          <input type="text" placeholder="email@example.com" v-model="userName">
        </div>
        <div class="data-form">
          <span class="hint"> Your Password </span>
          <input type="password" placeholder="Your Password" v-model="password" :class="{'error': passwordIncorrect}"
          @keyup.enter="signIn">
          <i class="error-message" v-if="passwordIncorrect"> Password Incorrect </i>
        </div>
        <div class="agreement">
          <input type="checkbox" id="agree-checkbox">
          <label for="agree-checkbox"><i class="fa fa-check"/> </label>
          <p class="desc"> Remember me </p>
        </div>
        <button class="confirm-button" @click="signIn"> {{submitting? 'Loading' : 'Sign In'}} </button>
      </div>
      <div class="right-box">
        <img src="../assets/infinite-loop-01.jpg" alt="">
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SignIn",
  data () {
    return {
      userName: "",
      password: "",
      passwordIncorrect: false,
      submitting: false
    }
  },
  methods: {
     signIn () {
       this.submitting = true
       const signInData = new URLSearchParams()
       signInData.append('user_name', this.userName)
       signInData.append('password', this.password)
       this.$http({
         method: "post",
         url: "/user//user_login",
         data: signInData
       }).then(res => {
         const data = res.data
         this.$store.commit('changeLogin',
             {
               authorization: res.data.token,
               localId: res.data.local_id,
               remoteId: res.data.remote_id,
               userName: res.data.user_name
             })
         this.$router.push("/")
       }).catch(e => {
         this.passwordIncorrect = true
         this.submitting = false
       })
     }
  }
}
</script>

<style lang="less">
@import "../assets/css/baseStyle";
.sign-up-wrap {
  margin-top: 180px;
  display: flex;
  justify-content: center;
  width: 100%;
  .sign-up-card {
    width: 60%;
    display: flex;
    justify-content: flex-start;
    .display-card();
    padding: 0;
    .left-box {
      width: 45%;
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      h2 {
        font-size: 26px;
        font-weight: 600;
        width: 100%;
        margin: 0;
        padding: 20px 20px 0 20px;
        & + span {
          margin-left: 30px;
        }
      }
      &  span {
        width: 100%;
        font-size: 13px;
        display: block;
        color: @font-medium-grey;
        margin-top: 7px;
        line-height: 24px;
      }
      input {
        width: 90%;
        transition: all 0.3s;
        outline: none;
        border-radius: 10px;
        border: 2px solid @font-light-grey;
        padding: 10px;
        background-color: white;
        &::-webkit-input-placeholder {
          color: @font-light-grey;
        }
        &:focus {
          border: 2px solid mediumpurple;
        }

        &.error {
          background-color: #ffeef0;
          border-color: #ff6e80;
        }
        &.warning {
          background-color: #fff2e5;
          border-color: orange;
        }
      }
    }
    .right-box {
      width: 55%;
      img {
        width: 100%;
        height: 100%;
        border-top-right-radius: 10px;
        border-bottom-right-radius: 10px;
      }
    }
  }
}
.hint {
  font-size: 11px;
  font-weight: 600;
  color: @font-dark-grey;
}
.data-form {
  width: 90%;
  position: relative;
  margin-bottom: 20px;
  i.error-message {
    display: inline;
    position: absolute;
    right: 15%;
    bottom: -18px;
    font-style: normal;
    font-size: 12px;
    color: #ff6e80;
  }
  i.warning-message {
    display: inline;
    position: absolute;
    right: 15%;
    bottom: -18px;
    font-style: normal;
    font-size: 12px;
    color: orange;
  }
}
#agree-checkbox {
  & + label {
    transition: all 0.3s;
    border: 1px solid @font-medium-grey;
    border-radius: 2px;
    height: 14px;
    width: 14px;
    background-color: transparent;
    color: white;
    font-size: 12px;
    margin-right: 10px;
  }
  display: none;
  &:checked + label {
    background-color: mediumpurple;
    & > i {
      display: block;
    }
  }
}
.agreement {
  display: flex;
  width: 90%;
  p.desc {
    margin: 0;
    font-size: 13px;
    //width: 85%;
    color: @font-medium-grey;
  }
}
.confirm-button {
  width: 90%;
  margin-top: 10px;
}
</style>