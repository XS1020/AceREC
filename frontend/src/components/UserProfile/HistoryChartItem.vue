<template>
  <div class="chart-item-container">
    <span>
      <img src="../../assets/avatar.webp" alt="">
      Wenzel
    </span>
    publish on <span> USENIX ATC </span>
    <span class="chart-item-time"> 2021 July </span>
    <p>
      Characterizing and Optimizing Remote Persistent Memory with RDMA and NVM.
      <i> View Detail </i>
    </p>
  </div>
</template>

<script>
export default {
  name: "HistoryChartItem"
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
  }
  span.chart-item-time {
    color: mediumpurple;
    font-size: 12px;
    border-radius: 4px;
    background-color: @bg-light-purple;
    padding: 2px 5px;
    margin-left: 20px;
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
  }
}
</style>