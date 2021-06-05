<template>
  <div class="cited-paper-container" v-if="genre === 'cited'">
    <CitedPaperItem v-for="(ref, index) in relatedPapers.Ref"
                    :paperInfo="{id: ref, click: relatedPapers.Clickable[index]}"
                    :key="ref"/>
    <span class="no-result" v-if="relatedPapers.Ref.length ===0"> No result </span>
  </div>
  <div class="cited-paper-container" v-else>
    <CitedPaperItem v-for="(ref, index) in relatedPapers.Rec"
                    :paperInfo="{id: ref, click: 1}"/>
  </div>
</template>

<script>
import CitedPaperItem from "@/components/Paper/CitedPaperItem";
export default {
  name: "CitedPaper",
  props: ['relatedPapers', 'genre'],
  data () {
    return {
    }
  },
  components: {CitedPaperItem}
}
</script>

<style lang="less">
@import "../../assets/css/baseStyle";
.cited-paper-container {
  display: flex;
  padding: 10px;
  flex-direction: column;
  justify-content: flex-start;
  position: relative;
  & > div {
    width: 100%;
    margin: 5px;
  }
  .cited-paper-item {
    position: relative;
    display: flex;
    justify-content: flex-start;
    border-radius: 8px;
    padding: 10px;
    transition: all 0.3s;
    &:hover {
      box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    & > img {
      position: relative;
      width: 18%;
    }
    &:hover {
      &:after, &:before {
        position: absolute;
        top: 20%;
        width: 4px;
        content: "";
        background-color: mediumpurple;
        height: 60%;
      }
      &:before{
        left: 0;
      }
      &:after{
        right: 0;
      }
    }
  }
}
.paper-item-info {
  margin-left: 10px;
  h2 {
    font-size: 16px;
    margin-bottom: 5px;
    & ~ span {
      display: block;
      font-size: 14px;
      margin: 5px;
      color: @font-medium-grey;
    }
  }
  ul.label-list {
    margin: 0;
    padding: 0;
    display: flex;
    list-style: none;
    li {
      margin: 5px;
      font-size: 12px;
      padding: 2px 5px;
      border-radius: 4px;
    }
    .label-list()
  }
}
.no-result {
  font-size: 18px;
  font-weight: 600;
  position: absolute;
  display: block;
  top: 100px;
  left: 50%;
}
</style>