<template>
  <div class="export-options-popup">
    <i class="fa fa-times close-button"/>
    <h2> Export Options </h2>
    <div class="options">
      <span> BibTeX </span>
      <p> @article{1998Imperfections,
        title={Imperfections of the thermohaline circulation: latitudinal asymmetry and preferred northern sinking},
        author={ Dijkstra, H. A.  and  Neelin, J. D. },
        journal={Journal of Climate},
        volume={13},
        number={2},
        year={1998},
        }
        <i class="fa fa-copy"/>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "ExportOptions"
}
</script>

<style lang="less">
@import "../../assets/css/baseStyle";
.export-options-popup {
  width: 40%;
  position: relative;
  i.close-button {
    font-size: 14px;
    color: @font-medium-grey;
    position: absolute;
    right: 5px;
    top: 5px;
  }
  h2 {
    font-size: 20px;
    padding: 0;
    margin: 0 0 20px 0;
    text-align: center;
  }
  .options {
    display: flex;
    justify-content: flex-start;
    span {
      padding-top: 10px;
      font-size: 16px;
      display: block;
      width: 20%;
    }
    p {
      position: relative;
      border-radius: 5px;
      font-size: 16px;
      padding: 30px;
      margin: 0 0 0 20px;
      background-color: #f3f3f3;
      i {
        position: absolute;
        right: 10px;
        bottom: 10px;
      }
    }
  }
}
</style>