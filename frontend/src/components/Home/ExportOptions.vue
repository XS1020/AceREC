<template>
  <div class="export-options-popup">
    <i class="fa fa-times close-button" @click="closePopup"/>
    <h2> Cite Source </h2>
    <div class="options">
      <span> BibTeX </span>
      <p>
        <pre><code>{{bib}}</code></pre>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "ExportOptions",
  props: ['id'],
  created() {
    this.$http({
      url: "/api/bib",
      params: {
        paperid: this.id
      }
    }).then(res => this.bib = res.data.bib)
  },
  methods: {
    closePopup () {
      this.$emit('closePopup')
    },
  },
  data () {
    return {
      bib: ""
    }
  }
}
</script>

<style lang="less">
@import "../../assets/css/baseStyle";
.export-options-popup {
  width: 50%;
  position: relative;
  i.close-button {
    cursor: pointer;
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
      font-weight: 600;
    }
    p {
      max-width: 80%;
      overflow-x: scroll;
      position: relative;
      border-radius: 5px;
      font-size: 16px;
      color: #989898;
      padding: 10px;
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