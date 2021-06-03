<template>
  <div class="user-avatar-container">
    <div class="user-avatar-wrap">
      <img :src="imgurl" alt="">
      <div class="user-basic-info">
        <h2> {{name}} </h2>
        <span><i class="fa fa-bank"/> {{affiliation}} </span>
        <span><i class="fa fa-location-arrow"/> Shanghai, China Mainland </span>
        <span><i class="fa fa-envelope-o"/> -- </span>
      </div>
    </div>
    <i class="follow-button fa fa-ellipsis-v"/>
    <div class="user-stat">
      <div>
        {{citeCount}}
        <span> Cited </span>
      </div>
      <div>
        {{ paperCount }}
        <span> Papers </span>
      </div>
      <div>
        {{hIndex}}
        <span> H-Index </span>
      </div>
    </div>
  </div>
</template>

<script>
function nameToUpperCase (str) {
  return str.toLowerCase().replace(/( |^)[a-z]/g, (L) => L.toUpperCase());
}
export default {
  name: "UserAvatarContainer",
  props: ['userId'],
  created() {
    this.$http({
      url: "/api/authorcitecount",
      params: {
        local_id: this.userId
      }
    }).then(res => {
      this.citeCount = res.data.citation_count
      this.paperCount = res.data.paper_count
      this.hIndex = res.data.h_index
    })
    this.$http({
      url: "/user/user_info",
      params: {
        local_id: this.userId,
      }
    }).then(res => {
      const data = res.data
      this.name = JSON.parse(JSON.stringify(data.pinyin))
      this.name = this.name.join(" ")
      this.name = nameToUpperCase(this.name)
      this.imgurl = data.avatar_url
      this.affiliation = data.affiliation
    }).catch(e => console.log(e))

    // this.$translate('上海交通大学',{to: 'en'}).then(res => console.log(res))
  },
  data () {
    return {
      name: "",
      imgurl: "",
      affiliation: "",
      citeCount: 0,
      paperCount: 0,
      hIndex: 0
    }
  }
}
</script>

<style lang="less">
@import "../../assets/css/baseStyle";
.user-avatar-container {
  position: relative;
  .display-card();
  padding: 10px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  .user-avatar-wrap {
    width: 100%;
    position: relative;
    display: flex;
    justify-content: flex-start;
    img {
      margin: 20px;
      width: 80px;
      height: 80px;
      border-radius: 50%;
      object-fit: contain;
      border: 2px solid mediumpurple;
    }
    .user-basic-info {
      display: flex;
      flex-direction: column;
      h2 {
        font-size: 20px;
        margin-bottom: 10px;
      }
      span {
        display: block;
        font-size: 14px;
        font-weight: 600;
        color: #979797;
        margin: 3px 0;
        i {
          margin-right: 10px;
          color: mediumpurple;
        }
      }
    }
  }
}
.user-stat {
  width: 70%;
  margin: 10px;
  display: flex;
  justify-content: space-between;
  & > div {
    text-align: center;
    font-weight: 600;
    font-size: 22px;
    & > span {
      display: block;
      font-size: 12px;
      color: @font-medium-grey;
      font-weight: 400;
    }
  }
}
.follow-button {
  position: absolute;
  transition: all 0.3s;
  right: 40px;
  top: 20px;
  &:hover {
    color: mediumpurple;
  }
}
</style>