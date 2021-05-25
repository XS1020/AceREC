<template>
  <div class="related-scholar">
    <h2> Related Scholars </h2>
    <span> 22 </span>
    <div class="scholar-list">
      <div v-for="i in 4">
        <img src="../../assets/avatar.webp" alt="">
        <div class="scholar-info-container">
          Hori Miona
          <span> Front End@Microsoft </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "RelatedScholars"
}
</script>

<style lang="less">
@import "../../assets/css/baseStyle";
.related-scholar {
  h2 {
    display: inline-block;
    font-size: 20px;
    margin: 16px 20px;
    .dot-title(green);
  }
  & > span {
    display: inline-block;
    font-weight: 600;
    font-size: 20px;
    color: @font-medium-grey;
  }
}
.scholar-list {
  display: flex;
  flex-wrap: wrap;
  width: 100%;
  & > div {
    box-sizing: border-box;
    width: 50%;
    display: flex;
    justify-content: flex-start;
    padding: 10px;
    position: relative;
    & > img {
      .avatar-small();
    }
    &:hover:after {
      content: "\f054";
      font: normal normal normal 14px/1 FontAwesome;
      position: absolute;
      right: 80px;
      top: 50%;
      transform: translateY(-50%);
    }
    .scholar-info-container {
      margin: 10px 20px;
      color: @font-dark-grey;
      font-weight: 600;
      & > span {
        display: block;
        color: @font-medium-grey;
        font-size: 13px;
        margin-top: 5px;
      }
    }
  }
}
</style>