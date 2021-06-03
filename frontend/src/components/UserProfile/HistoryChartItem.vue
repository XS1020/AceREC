<template>
  <div class="chart-item-container">
<!--    <span>-->
<!--      <img src="../../assets/avatar.webp" alt="">-->
<!--      Wenzel-->
<!--    </span>-->
    <span class="chart-item-time" v-if="eduInfo.year > 0"> {{eduInfo.year}} </span>
    <span class="chart-item-time-unknown" v-else> Unknown </span>
<!--    <span> {{eduInfo.action}} <strong> from </strong> {{eduInfo.institute + eduInfo.department}}</span>-->
    <p> {{eduInfo.action}} <strong> of </strong> {{eduInfo.institute + eduInfo.department}} </p>
  </div>
</template>

<script>
export default {
  name: "HistoryChartItem",
  props: ['eduInfo'],
}
</script>

<style lang="less">
@import "../../assets/css/baseStyle";
.chart-item-container {
  width: 100%;
  color: @font-medium-grey;
  line-height: 16px;
  span {
    color: #222222;
    font-weight: 600;
    font-size: 16px;
    margin: 0 2px;
    img {
      .avatar-inline(16px)
    }
    strong {
      margin: 0 10px;
      color: @font-medium-grey;
    }
  }
  span.chart-item-time {
    color: mediumpurple;
    font-size: 25px;
    border-radius: 4px;
    background-color: #efebfd;
    padding: 2px 5px;
    margin-left: 0;
  }
  span.chart-item-time-unknown {
    color: mediumpurple;
    font-size: 18px;
    border-radius: 4px;
    background-color: #efebfd;
    padding: 2px 5px;
    margin-left: 0;
  }
  p {
    background-color: #f7f7f7;
    padding: 10px;
    border-radius: 5px;
    font-size: 14px;
    font-weight: 600;
    line-height: 30px;
    i {
      font-style: normal;
      font-size: 14px;
      font-weight: 400;
      color: rebeccapurple;
      cursor: pointer;

      &:hover {
        text-decoration: underline;
      }
    }
    strong {
      margin: 0 5px;
    }
  }
}
</style>