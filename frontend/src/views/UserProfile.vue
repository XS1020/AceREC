<template>
  <div class="profile-wrapper">
    <div class="profile-top-container">
      <div class="profile-left-box">
        <div class="avatar-container">
          <img src="../assets/avatar.webp" alt=""/>
          <div class="name-container">
            Hori Miona
            <i class="fa fa-twitter"/>
            <i class="fa fa-github"/>
            <i class="fa fa-facebook-square"/>
            <span><i class="fa fa-star-o"/> CS Professor </span>
            <span class="location-display"><i class="fa fa-location-arrow"/> Tokyo, Japan </span>
          </div>
          <button class="follow-button" :class="{'disabled': following}" @click="changeFollowingState">
            <i class="fa fa-plus" v-if="!following"/>
            <i class="fa fa-minus" v-else/>
            {{following? "Followed":"Follow"}}
          </button>
        </div>
        <div>
          <ul class="tag-list">
            <li v-for="tag in tags"> {{tag}} </li>
            <li class="add-tag"><i class="fa fa-plus"/> Add Tag </li>
          </ul>
        </div>
      </div>
      <div class="profile-right-box">
        <RelatedScholars/>
      </div>
    </div>
    <div class="profile-top-container">
      <div class="profile-left-box">
        <div>
          <h2> Cited Trend </h2>
        </div>
        <div></div>
      </div>
      <div class="profile-right-box">
        <HistoryChart/>
      </div>
    </div>
  </div>
</template>

<script>
import RelatedScholars from "@/components/UserProfile/RelatedScholars";
export default {
  name: "UserProfile",
  components: {
    HistoryChart: () => import("@/components/UserProfile/HistoryChart"),
    RelatedScholars
  },
  data () {
    return {
      following: false,
      tags: ['Front End', 'HTML', 'CSS', 'JavaScript']
    }
  },
  methods: {
    changeFollowingState () {
      this.following = !this.following
    }
  }
}
</script>

<style scoped lang="less">
@import "../assets/css/baseStyle";

.profile-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  flex-direction: column;
}
.profile-top-container {
  width: 80%;
  display: flex;
  justify-content: flex-start;
  .profile-left-box {
    width: 40%;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    & > div {
      .display-card();
      padding: 10px;
      h2 {
        .dot-title(purple);
      }
    }
    .avatar-container {
      display: flex;
      justify-content: flex-start;
      position: relative;
      img {
        .avatar-medium();
      }
      .name-container {
        margin-left: 20px;
        padding: 10px 0;
        font-size: 18px;
        font-weight: 600;
        color: @font-dark-grey;
        & > i {
          margin-left: 10px;
          cursor: pointer;
          transition: all 0.3s;
          &:hover {
            color: rebeccapurple;
          }
        }
        span {
          display: block;
          font-size: 14px;
          font-weight: 500;
          color: rebeccapurple;
          margin-top: 5px;
        }
        span.location-display {
          display: inline-block;
          color: @font-medium-grey;
        }
      }
    }
  }
  .profile-right-box {
    width: 60%;
    & > div {
      .display-card();
      padding: 10px;
    }
  }
}
.follow-button {
  .button-base();
  position: absolute;
  bottom: 10px;
  right: 10px;
}
.tag-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
  & > li {
    padding: 2px 5px;
    margin: 0 4px;
    background-color: #e7e7e7;
    border-radius: 5px;
    font-size: 12px;
    &.add-tag {
      background-color: transparent;
      color: @font-dark-grey;
      cursor: pointer;
    }
  }
}
</style>