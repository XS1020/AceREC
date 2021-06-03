<template>
  <div class="search-wrap">
    <div class="search-main">
      <div class="sidebar">
        <ul class="sidebar">
          <li v-for="(option, index) in options" :class="{'active': index===selectedOption}"
          @click="switchMode(index)"> {{option}} </li>
        </ul>
      </div>
      <div class="main-content">
        <CitedPaper :related-papers="papers" :genre="'cited'" :key="queryString + mode + page">
        </CitedPaper>
        <SwitchPage :totalPages="Math.ceil(totalNum / 20)" :curIndex="page" @switchPage="switchPage"/>
      </div>
    </div>
  </div>
</template>

<script>
import CitedPaper from "@/components/Paper/CitedPaper";
export default {
  name: "Search",
  beforeRouteUpdate (to, from, next) {
    next()
    if (to.path.startsWith('/search') && to.query !== from.query) {
      this.renderData()
    }
  },
  created() {
    this.renderData()
  },
  data () {
    return {
      totalNum: 0,
      page: 1,
      mode: this.$route.query.mode,
      queryString: "",
      papers: {
        Ref: [],
        Clickable: [],
      },
      options: ['All', 'Title', 'Author', 'Conference', 'Journal'],
    }
  },
  components: {
    CitedPaper,
    SwitchPage: () => import("../components/SwitchPage")
  },
  computed: {
    selectedOption: function () {
      return this.options.indexOf(this.$route.query.mode)
    }
  },
  methods: {
    switchMode (index) {
      this.mode = this.options[index]
      this.$router.push({
            path: "/search",
            query: { queryString: this.queryString, mode: this.mode}
      })
      this.renderData()
    },
    renderData () {
      this.queryString = this.$route.query.queryString
      this.page = this.$route.query.page ? this.$route.query.page : 1
      this.$http({
        url: "/api/search",
        params: {
          keyword: encodeURI(this.queryString),
          mode: this.$route.query.mode,
          page: this.page
        }
      }).then(res => {
        this.$set(this.papers, 'Ref', JSON.parse(JSON.stringify(res.data.paper_id_list)))
        for (let i = 0; i < this.papers.Ref.length; i++)
          this.papers.Clickable.push(1)
        this.totalNum = res.data.number
      })
    },
    switchPage (e) {
      this.page = e
      this.$router.push({
        path: "/search",
        query: {
          queryString: this.queryString,
          mode: this.mode,
          page: e
        }
      })
      this.renderData()
    }
  },
}
</script>

<style lang="less">
@import "../assets/css/baseStyle";
.search-wrap {
  display: flex;
  width: 100%;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  .search-main {
    margin: 20px;
    display: flex;
    width: 80%;
    justify-content: flex-start;
    .sidebar {
      width: 20%;
    }
    .sidebar ul {
      width: 100%;
      background-color: white;
      border-radius: 5px;
      list-style: none;
      padding: 0;
      li {
        position: relative;
        padding: 8px 20px;
        display: flex;
        justify-content: space-between;
        font-weight: 600;
        span {
          font-size: 13px;
          border-radius: 8px;
          color: white;
          background-color: mediumpurple;
          padding: 2px 8px;
        }
        border-bottom: 1px solid #e7e7e7;
      }
      li:nth-child(1) {
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
      }
      li:before {
        position: absolute;
        width: 2px;
        height: 100%;
        content: "";
        left: 0;
        top: 0;
        background-color: transparent;
        transition: all 0.3s;
      }
      li:hover:before, li.active:before {
        background-color: mediumpurple;
      }
    }
    .main-content {
      width: 80%;
      .display-card()
    }
  }
}
</style>