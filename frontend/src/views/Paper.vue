<template>
  <div class="paper-wrapper">
    <div>
      <div class="paper-main-info">
        <div class="left-bar">
          <h2> Imperfections of the thermohaline circulation: latitudinal asymmetry and preferred northern sinking </h2>
          <span> From Research Gate </span>
          <div class="basic-info-container">
            <div> <i class="fa fa-user-circle-o"/> Authors: <strong>HA Dijkstra，JD Neelin</strong> </div>
            <div> <i class="fa fa-code"/> <strong> 10.1175/1520-0442(2000)0132.0.CO;2 </strong></div>
            <div> <i class="fa fa-clock-o"/>Year: <strong>1998</strong> </div>
            <div> <i class="fa fa-code-fork"/>Cited: <strong> 3476 </strong> </div>
          </div>
          <h4><i class="fa fa-quote-right"/> Abstract </h4>
          <p> The present Atlantic thermohaline circulation is dominated by deep water formation inthe north despite the fact that surface buoyancy forcing has relatively modest latitudinalasymmetry.Many studies have shown that even with buoyancy forcing that is symmetricabout the equator,spontaneous symmetry breaking can produce a single overturning cellwith intense sinking in the north.This occurs by salt advection at sufficiently large fresh-water forcing.In this symmetry-breaking case,a southern sinking solution and a symmetricsolution are  </p>
          <button @click="showExportsOptions"> Export Options <i class="fa fa-chevron-right"/> </button>
        </div>
        <img src="../assets/1904.09730v1.png" alt="" class="right-bar">
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Paper",
  data () {
    return {
    }
  },
  methods: {
    showExportsOptions () {
      this.$emit('showExportOptions')
    }
  }
}
</script>

<style lang="less">
@import "../assets/css/baseStyle";
.paper-wrapper {
  margin-top: 100px;
  display: flex;
  width: 100%;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  & > div {
    width: 70%;
    padding: 10px;
    display: flex;
    flex-direction: column;
    .paper-main-info {
      display: flex;
      justify-content: flex-start;
      .display-card();
      padding: 40px;
    }
  }
}
.paper-main-info {
  .left-bar {
    width: 60%;
    h2 {
      margin: 0;
      font-size: 20px;
    }
    & > span {
      display: block;
      font-size: 14px;
      color: @font-medium-grey;
      margin-top: 10px;
    }
    h4 {
      color: mediumpurple;
      transition: all 0.3s;
      &:hover {
        color: rebeccapurple;
      }
    }
    p {
      font-size: 14px;
      font-weight: 400;
      line-height: 24px;
      .p-ellipsis(4);
      padding: 0 20px;
      color: @font-medium-grey;
    }
  }
  .right-bar {
    width: 30%;
  }
}
.basic-info-container {
  width: 100%;
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
  margin-top: 20px;
  & > div {
    width: 50%;
    margin: 10px 0;
    color: mediumpurple;
    font-size: 14px;
    font-weight: 600;
    & > i {
      margin-right: 5px;
      font-size: 16px;
    }
    & > strong {
      font-weight: 500;
      color: @font-medium-grey;
    }
  }
}
</style>