<template>
  <div class="paper-wrapper">
    <div>
      <div class="paper-main-info">
        <div class="left-bar">
          <h2> {{title}} </h2>
          <span> From {{source}} </span>
          <div class="basic-info-container">
            <div> <i class="fa fa-user-circle-o"/> Authors:
              <strong v-for="(author, index) in authors" @click="jumpToUser(author.remote_id, author.clickable)">
                {{index < authors.length - 1? author.name + ", ":author.name}}
              </strong>
            </div>
            <div> <i class="fa fa-code"/> <strong> {{doi}} </strong></div>
            <div> <i class="fa fa-clock-o"/>Year: <strong>{{year}}</strong> </div>
            <div> <i class="fa fa-code-fork"/>Cited: <strong> {{citationCount}} </strong> </div>
          </div>
          <h4><i class="fa fa-quote-right"/> Abstract </h4>
          <p> {{abstract}}  </p>
          <button @click="showExportsOptions"> Cite Source <i class="fa fa-chevron-right"/> </button>
        </div>
        <ImageNotLoaded class="right-bar" v-if="!imgurl.length"/>
        <img src="../assets/1904.09730v1.png" alt="" class="right-bar" v-else>
      </div>
      <div class="paper-extra-info">
        <div class="left-bar">
          <div>
            <h2> Cited Trend </h2>
            <svg ref="cited-trend" class="chart"></svg>
          </div>
          <div>
            <h2> Keywords </h2>
            <div ref="word-cloud"></div>
          </div>
        </div>
        <div class="right-bar">
          <div>
            <h2> Related Papers </h2>
            <router-view></router-view>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LineChart from "@/utils/LineChart";
import Cloud from "@/utils/Cloud";
import ImageNotLoaded from "@/components/ImageNotLoaded";
export default {
  name: "Paper",
  components: {ImageNotLoaded},
  created() {
    this.$http({
      url: "/api/paperinfo",
      params: {
        paperid: 473532210
      }
    }).then(res => {
      const data = res.data
      this.title = data.title
      this.year = data.year
      this.imgurl = data.imgurl
      this.citationCount = data.citation_count
      this.doi = data.doi
      this.abstract = data.abstract
      this.source = data.url
      let idx = 0
      for (const author of data.Authors) {
        this.$set(this.authors, idx, Object.assign(data.Authors[idx]))
        idx++
      }
    })
  },
  mounted() {
    this.$http({
      url: "/api/ctrend",
      params: {
        paperid: 565
      }
    }).then(res => {
      let i = 0
      for (const item of res.data.cite_trend) {
        this.$set(this.citeTrend, i++, Object.assign(item))
      }
      return new Promise(resolve => resolve(res))
    }).then(() => {
      this.mountCitedTrend()
    })

    this.$http({
      url: "/api/paperkeyword",
      params: {
        paperid: 565
      }
    }).then(res => {
      let i = 0
      for (const item of res.data.keyword) {
        this.$set(this.keyWords, i++, Object.assign(item))
      }
      return new Promise(resolve => resolve(res))
    }).then(() => this.mountWordCloud())
  },
  data () {
    return {
      citeTrend: [],
      keyWords: [],
      year: 0,
      title: "",
      doi: "",
      imgurl: "",
      citationCount: 0,
      authors: [],
      abstract: "",
      source: ""
    }
  },
  methods: {
    showExportsOptions () {
      this.$emit('showExportOptions')
    },

    mountCitedTrend () {
      const svg = this.$refs["cited-trend"]
      const chart = new LineChart({
        target: svg,
        width: 320,
        height: 200,
        xTicks: 3,
        yTicks: 3
      })
      const newData = JSON.parse(JSON.stringify(this.citeTrend))
      const svgData = []
      for (const item of newData) {
        const {citation_count, year} = item
        svgData.push({time: year, value: citation_count})
      }
      chart.render(svgData)

    },
    mountWordCloud () {
      const keyWords = JSON.parse(JSON.stringify(this.keyWords))
      const newKeyWords = []
      for (const item of keyWords) {
        for (let copyNum = 0; copyNum < 10 * item.size + 2; copyNum ++) {
          newKeyWords.push({text: item.text, size: item.size})
        }

      }
      Cloud({
        wordList: newKeyWords,
        size: [330, 256],
        svgElement: this.$refs["word-cloud"]
      }, baseCallBack)
      function baseCallBack() {
        //  dddd
      }
    },
    jumpToUser (userId, clickable) {
      if (clickable)
        this.$router.push('/user/' + userId)
    }
  }
}
</script>

<style lang="less">
@import "../assets/css/baseStyle";
@import "../assets/css/lineChart.css";
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
    margin-left: 30px;
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
.paper-extra-info {
  display: flex;
  justify-content: flex-start;
  .left-bar {
    @color-list-1: green, mediumpurple, orange;
    .random-color(3, @color-list-1);
    width: 40%;
    display: flex;
    flex-direction: column;
    & > div {
      .display-card();
      padding: 10px;
    }
  }
  .right-bar {
    @color-list-1: orange, plum, aqua;
    .random-color(3, @color-list-1);
    width: 60%;
    display: flex;
    flex-direction: column;
    & > div {
      .display-card();
      padding: 10px;
    }
  }
}

</style>