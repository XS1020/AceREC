<template>
  <div class="settings-wrap">
    <div class="settings-main">
      <h2> Public Profile. </h2>
      <div class="settings-flex">
        <section class="basic-info">
          <div class="input-form">
            <span> Name </span>
            <input type="text" placeholder="Your Name" v-model="name"
                   :class="{'error': status.name === 'error', 'warning': status.name === 'warning'}">
            <i :class="{'error-message': status.name === 'error', 'warning-message': status.name === 'warning'}"
               v-if="status.name !== 'normal'">
              {{message.name}}
            </i>
          </div>
          <div class="input-form">
            <span> Old Password </span>
            <input type="password" placeholder="Old Password" v-model="oldPassword"
                   :class="{'error': status.oldPwd === 'error', 'warning': status.oldPwd === 'warning'}">
            <i :class="{'error-message': status.oldPwd === 'error', 'warning-message': status.oldPwd === 'warning'}"
               v-if="status.oldPwd !== 'normal'">
              {{message.oldPwd}}
            </i>
          </div>
          <div class="input-form">
            <span> New Password </span>
            <input type="password" placeholder="New Password" v-model="newPassword"
                   :class="{'error': status.newPwd === 'error', 'warning': status.newPwd === 'warning'}">
            <i :class="{'error-message': status.newPwd === 'error', 'warning-message': status.newPwd === 'warning'}"
               v-if="status.newPwd !== 'normal'">
              {{message.newPwd}}
            </i>
          </div>
          <div class="input-form">
            <span> Confirm Password </span>
            <input type="password" placeholder="Confirm Password" v-model="confirmPassword"
                   :class="{'error': status.confirmPwd === 'error', 'warning': status.confirmPwd === 'warning'}">
            <i :class="{'error-message': status.confirmPwd === 'error', 'warning-message': status.confirmPwd === 'warning'}"
               v-if="status.confirmPwd !== 'normal'">
              {{message.confirmPwd}}
            </i>
          </div>
          <button @click="submit"> Save </button>
        </section>
        <section class="appendix-info">
          <span> Research List </span>
          <ul class="research-list">
            <li v-for="(tag, index) in researchList" :class="{'deleting': deleting === index}">
              {{tag}}
              <i class="fa fa-times" @click="removeTag(index)"/>
            </li>
            <li class="add-button">
              <i class="fa fa-plus" v-show="!addingTags" @click="addTag"/>
              <input type="text" v-show="addingTags" v-model="addedTag">
              <i class="fa fa-check" v-show="addingTags" @click="confirmTag"/>
            </li>
          </ul>
          <span> Field of Interest </span>
          <div class="field-of-interest" >
            <ul class="field-of-interest-0 clearfix" :class="{'move-left': showTier1}">
              <li v-for="(tag, index) in tagsTier0" @click="selectTier0(tag.id)"
                  :class="{'active': selectedTagsTier0.includes(tag.id)}"
              > {{tag.name}} </li>
            </ul>
            <ul class="field-of-interest-1 clearfix" :class="{'move-left': showTier1}">
              <li v-for="(tag, index) in tagsTier1" @click="selectTier1(tag.id)"
                  :class="{'active': selectedTagsTier1.includes(tag.id)}"
              > {{tag.name}} </li>
            </ul>
          </div>
          <button class="next-button" @click="switchTier" :class="{'rotate': showTier1}">
            <i class="fa fa-arrow-right"></i>
          </button>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
import formatFieldOfInterest from "@/utils/formatFieldOfInterest";
const mappingFromTier1 = require("../assets/data/V1_to_V0.json")
export default {
  name: "Settings",
  created() {
    this.$http({
      url: "/user/user_info_to_update",
      params: {
        local_id: this.$store.state.localId,
        remote_id: this.$store.state.remoteId
      }
    }).then(res => {
      this.name = res.data.name
      this.researchList = JSON.parse(JSON.stringify(res.data.research_list))
      this.selectedTagsTier1 = JSON.parse(JSON.stringify(res.data.field_list))
      for (const tag of this.selectedTagsTier1) {
        for (const tier0 of mappingFromTier1[tag])
          if (!this.selectedTagsTier0.includes(tier0))
            this.$set(this.selectedTagsTier0, this.selectedTagsTier0.length, tier0.toString())
      }
    })
    let i = 0
    for (const key of Object.keys(this.fieldOfInterestBase)) {
      this.$set(this.tagsTier0, i,
          {
            id: key,
            name:this.fieldOfInterestBase[key].name
          })
      i++;
    }
  },
  data () {
    return {
      status: {
        name: "normal",
        oldPwd: "normal",
        newPwd: "normal",
        confirmPwd: "normal"
      },
      message: {
        name: "normal",
        oldPwd: "normal",
        newPwd: "normal",
        confirmPwd: "normal"
      },
      name: "",
      oldPassword: "",
      newPassword: "",
      confirmPassword: "",
      researchList: ['CV', 'NLP', 'Apolo_Program'],
      deleting: -1,
      addingTags: false,
      addedTag: "",
      fieldOfInterestBase: formatFieldOfInterest(),
      tagsTier0: [],
      selectedTagsTier0: [],
      showTier1: false,
      selectedTagsTier1: []
    }
  },
  computed: {
    tagsTier1 () {
      const tags = []
      for (let i = 0; i < this.selectedTagsTier0.length; i++)
          tags.push(...this.fieldOfInterestBase[this.selectedTagsTier0[i]].children)
      return tags
    }
  },
  methods: {
    removeTag (index) {
      this.deleting = index
      setTimeout(() => {
        this.researchList.splice(index, 1)
        this.deleting = -1
      },300)
    },
    addTag () {
      this.addingTags = true
    },
    confirmTag () {
      if (this.addedTag.length > 0) {
        this.researchList.push(this.addedTag)
        this.addedTag = ""
      }
      this.addingTags = false
    },
    selectTier0 (id) {
      if (this.selectedTagsTier0.includes(id))
        this.selectedTagsTier0 = this.selectedTagsTier0.filter(d => d !== id)
      else this.selectedTagsTier0.push(id)
    },
    selectTier1 (id) {
      if (this.selectedTagsTier1.includes(id))
        this.selectedTagsTier1 = this.selectedTagsTier1.filter(d => d !== id)
      else this.selectedTagsTier1.push(id)
    },
    switchTier () {
      if (this.selectedTagsTier0.length || this.showTier1)
        this.showTier1 = !this.showTier1
    },
    submit () {
      if (!this.checkSubmit())
        return
      const postData = new URLSearchParams()
      postData.append('local_id', this.$store.state.localId)
      postData.append('remote_id', this.$store.state.remoteId)
      postData.append('name', this.name)
      postData.append('old_password', this.oldPassword)
      postData.append('new_password', this.newPassword)
      postData.append('research_list', JSON.parse(JSON.stringify(this.researchList)))
      postData.append('field_list', JSON.parse(JSON.stringify(this.selectedTagsTier1)))
      this.$http({
        method: "post",
        url: "/user/update_user_info",
        data: postData
      }).then(res=>{
        this.$router.push('/')
      }).catch(e => {
        const text = e.response.data
        if (text === 'Wrong Password!') {
          this.$set(this.status, 'oldPwd', 'error')
          this.$set(this.message, 'oldPwd', 'Wrong Password')
        }
      })
    },
    checkSubmit () {
      if (this.oldPassword !== "" && this.newPassword === "") {
        this.$set(this.status, 'newPwd', 'error')
        this.$set(this.message, 'newPwd', 'New Password should not be empty')
        return false
      }
      if (this.newPassword !== this.confirmPassword) {
        this.$set(this.status, 'confirmPwd', 'error')
        this.$set(this.message, 'confirmPwd', 'Password Invalid')
        return false
      }
      return true
    }
  }
}
</script>

<style lang="less">
@import "../assets/css/baseStyle";
.settings-wrap {
  display: flex;
  width: 100%;
  justify-content: flex-start;
  flex-direction: column;
  align-items: center;
  .settings-main {
    width: 80%;
    .display-card();
    padding: 20px 50px;
  }
}
.settings-flex {
  display: flex;
  justify-content: flex-start;
  .basic-info {
    width: 40%;
  }
}
.input-form {
  margin: 10px 0;
  position: relative;
  width: 100%;
  padding-right: 40px;
  & > span {
    display: block;
    color: @font-medium-grey;
    font-weight: 600;
    font-size: 16px;
    margin: 5px 10px;
  }
  & > input {
    width: 100%;
    outline: none;
    padding: 10px;
    border-radius: 10px;
    margin-left: 10px;
    transition: all 0.3s;
    border: 2px solid @font-light-grey;
    &::-webkit-input-placeholder {
      color: @font-light-grey;
    }
    &:focus {
      border-color: mediumpurple;
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
.appendix-info {
  position: relative;
  width: 60%;
  & > span {
    display: block;
    color: @font-medium-grey;
    font-weight: 600;
    font-size: 16px;
    margin: 5px 10px;
  }
  .research-list {
    display: flex;
    width: 100%;
    list-style: none;
    flex-wrap: wrap;
    max-height: 250px;
    overflow-y: scroll;
    padding: 0;
    margin: 0;
    li {
      padding: 10px 20px;
      border-radius: 20px;
      margin: 10px 2px;
      color: white;
      background-color: mediumpurple;
      transition: all 0.3s;
      font-size: 13px;
      min-width: 40px;
      position: relative;
      &.add-button > i {
        margin: 0;
      }
      &:hover {
        background-color: rebeccapurple;
      }
      i {
        margin-left: 10px;
        font-size: 12px;
        line-height: 20px;
        cursor: pointer;
      }
    }
  }
}
.deleting {
  transform: scale(0);
}
.add-button > input {
  width: 100px;
  border: none;
  background-color: transparent;
  outline: none;
  color: white;
}
.field-of-interest-0, .field-of-interest-1 {
  transition: all 0.3s;
  position: absolute;
  list-style: none;
  padding: 0;
  margin: 0;
  width: 100%;
  li {
    float: left;
    cursor: pointer;
    padding: 10px 20px;
    border-radius: 20px;
    margin: 10px 2px;
    border: 2px solid mediumpurple;
    color: mediumpurple;
    background-color: transparent;
    transition: all 0.3s;
    font-size: 13px;
    min-width: 40px;
    font-weight: 600;
    position: relative;
    &:hover, &.active {
      background-color: mediumpurple;
      color: white;
    }
    &.active {
      color: white;
      background-color: mediumpurple;
    }
  }
}
.next-button {
  border-radius: 50%;
  height: 60px;
  width: 60px;
  font-size: 22px;
  position: absolute;
  right: 0;
  bottom: 0;
  & > i {
    transition: all 0.3s;
  }
  &.rotate {
    i {
      transform: rotate(180deg);
    }
  }
}
.field-of-interest {
  display: flex;
  overflow: hidden;
  position: relative;
  width: 100%;
  height: 300px;
  .field-of-interest-1 {
    left: 100%;
    height: inherit;
    overflow-y: scroll;
  }
}
.move-left {
  transform: translateX(-100%);
}
</style>