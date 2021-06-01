<template>
  <div class="history-container">
    <h2> Academic Experiences </h2>
    <ul class="history-options" :style="{'--selected-option': selectedOption * 70 + 'px'}">
      <li v-for="(option, index) in options" @click="selectedOption = index"> {{option}} </li>
    </ul>
    <div class="chart-main">
      <HistoryChartItem class="chart-item"/>
      <HistoryChartItem class="chart-item"/>
      <HistoryChartItem class="chart-item"/>
    </div>
  </div>
</template>

<script>
export default {
  name: "HistortyChart",
  components: {
    HistoryChartItem: () => import("@/components/UserProfile/HistoryChartItem")
  },
  data () {
    return {
      selectedOption: 0,
      options: [
          "All", "Paper", "Education", "Awards"
      ]
    }
  }
}
</script>

<style lang="less">
@import "../../assets/css/baseStyle";
.history-container {
  position: relative;
  h2 {
    display: inline-block;
    font-size: 20px;
    margin: 16px 20px;
    .dot-title(orange);
  }
}
.chart-main {
  position: relative;
  padding: 10px 40px;
  margin-left: 20px;
  &:before {
    position: absolute;
    left: 20px;
    content: "";
    display: block;
    width: 1px;
    height: 100%;
    //background-color: @font-medium-grey;
    border-left: 1px dashed @font-medium-grey;
    transform: translateY(-10px);
  }
  .chart-item {
    @margin-left: 20px;
    position: relative;
    margin-left: @margin-left;
    &:before {
      @size: 40px;
      position: absolute;
      left: -20px - @margin-left - @size / 2;
      content: "\f105";
      font: normal normal normal 14px/1 FontAwesome;
      line-height: @size;
      text-align: center;
      color: rebeccapurple;
      height: @size;
      width: @size;
      border-radius: 50%;
      background-color: #efebfd;
    }
    &:nth-child(n+2) {
      margin-top: 40px;
    }
  }
}
.history-options {
  position: absolute;
  padding: 4px 0;
  right: 20px;
  top: 10px;
  list-style: none;
  display: flex;
  justify-content: flex-end;
  li {
    font-size: 14px;
    font-weight: 600;
    min-width: 70px;
    text-align: center;
    cursor: pointer;
  }
  &:after {
    position: absolute;
    content: "";
    background-color: mediumpurple;
    height: 3px;
    width: 50px;
    bottom: -5px;
    left: 10px;
    transition: all 0.3s;
    transform: translateX(var(--selected-option));
  }
}
</style>