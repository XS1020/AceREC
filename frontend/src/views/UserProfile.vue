<template>
  <div class="profile-wrapper">
    <div class="profile-top-container">
      <div class="profile-left-box">
        <UserAvatarContainer :userId="userId" :key="'avatar-container' + userId"/>
        <div>
          <ul class="tag-list">
            <li v-for="tag in tags"> {{tag}} </li>
          </ul>
        </div>
      </div>
      <div class="profile-right-box">
        <RelatedScholars :localId="userId" :key="'related-scholar' + userId"/>
      </div>
    </div>
    <div class="profile-top-container">
      <div class="profile-left-box">
        <div>
          <h2> Cited Trend </h2>
          <div ref="cited-trend" style="height: 200px"></div>
        </div>
        <div>
          <HistoryChart :eduList="eduList" :workList="workList" :paperList="paperList" :key="'history' + userId"/>
        </div>
      </div>
      <div class="profile-right-box">
        <div class="history-container">
          <h2> Published Papers </h2>
          <CitedPaper :relatedPapers="paperList" :genre="'cited'"></CitedPaper>
        </div>
<!--        <HistoryChart :eduList="eduList" :workList="workList" :paperList="paperList"/>-->
      </div>
    </div>
  </div>
</template>

<script>
import RelatedScholars from "@/components/UserProfile/RelatedScholars";
import UserAvatarContainer from "@/components/UserProfile/UserAvatarContainer";
import renderLineChart from "@/utils/ECharts-LineChart";
export default {
  name: "UserProfile",
  beforeRouteUpdate (to, from, next) {
    next()
    if (to.path.startsWith('/profile') && from.params.id !== to.params.id) {
      this.renderData()
      this.renderSvg()
    }
  },
  created() {
    this.renderData()
  },
  mounted() {
    this.renderSvg()
  },
  components: {
    UserAvatarContainer,
    HistoryChart: () => import("@/components/UserProfile/HistoryChart"),
    RelatedScholars,
    CitedPaper: () => import("@/components/Paper/CitedPaper")
  },
  data () {
    return {
      following: false,
      tags: [],
      userId: 0,
      name: "",
      citationTrend: [],
      cited: 0,
      eduList: {},
      workList: {},
      paperList: {
        Ref: {},
        Rec: {},
        Clickable: []
      }
    }
  },
  methods: {
    renderData () {
      this.userId = this.$route.params.id
      this.$http({
        url: "/user/user_info",
        params: {
          local_id: this.userId,
        }
      }).then(res => {
        this.tags = JSON.parse(JSON.stringify(res.data.research_list)).slice(0, 4)
      })
      this.$http({
        url: "/user/user_edu",
        params: {
          local_id: this.userId
        }
      }).then(res => {
        const data = res.data
        this.eduList = JSON.parse(JSON.stringify(res.data.edu_list))
      })
      this.$http({
        url: "/user/user_work",
        params: {
          local_id: this.userId
        }
      }).then(res => {
        const data = res.data
        this.workList = JSON.parse(JSON.stringify(res.data.work_list))
      })

      this.$http({
        url: "/user/user_papers",
        params: {
          local_id: this.userId
        }
      }).then(res => {
        this.$set(this.paperList, 'Ref', JSON.parse(JSON.stringify(res.data.paper_list)).slice(0, 20))
        for (let i = 0; i < this.paperList.Ref.length; i++)
          this.paperList.Clickable.push(1)
      })
    },
    renderSvg () {
      this.$http({
        url: "/api/ptrend",
        params: {
          local_id: this.userId
        }
      }).then(res => {
        let i = 0
        for (const item of res.data.trend) {
          this.$set(this.citationTrend, i, {time: item.year, value: item.citation_count})
          i++
        }
        return new Promise(resolve => resolve())
      }).then(res => {
        const svg = this.$refs["cited-trend"]
        // const chart = new LineChart({
        //   target: svg,
        //   width: 320,
        //   height: 200,
        //   xTicks: 3,
        //   yTicks: 3
        // })
        const svgData = JSON.parse(JSON.stringify(this.citationTrend))
        // chart.render(svgData)
        renderLineChart(svg, svgData)
      })
    }
  }
}
</script>

<style scoped lang="less">
@import "../assets/css/baseStyle";
@import "../assets/css/lineChart.css";
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
.history-container {
  position: relative;
  &>h2 {
    display: inline-block;
    font-size: 20px;
    margin: 16px 20px;
    .dot-title(orange);
  }
}
</style>