<template>
  <div class="browse-history-wrapper" :class="{'active': active}">
    <h2> History </h2>
    <section class="browse-scroll">
      <section v-for="record in history" @click="jumpToPaper (record.paperid)">
        <h2> {{record.title}} </h2>
        <span> {{record.time}} </span>
      </section>
    </section>
    <div @click="active = !active">
      <i class="fa fa-angle-double-right"></i>
    </div>
  </div>
</template>

<script>
export default {
  name: "BrowseHistory",
  created() {
    this.$http({
      url: "/api/userrecord",
      params: {
        local_id: this.$store.state.localId
      }
    }).then(res => {
      this.history = JSON.parse(JSON.stringify(res.data.record))
    })
  },
  data () {
    return {
      active: true,
      history: []
    }
  },
  methods: {
    jumpToPaper (id) {
      this.$router.push('/paper/' + id)
    }
  }
}
</script>

<style lang="less">
.browse-history-wrapper {
  & > h2 {
    text-align: center;
  }
  transition: all 0.3s;
  &.active {
    transform: translateX(100%);
    & > div > i {
      transform: rotate(180deg);
    }
  }
  z-index: 200;
  position: fixed;
  top: 0;
  height: 100%;
  right: 0;
  width: 400px;
  background-color: #f3f3f3;
  border-left: 2px solid mediumpurple;
  transform-style: preserve-3d;
  border-radius: 8px;
  & > div {
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    left: 0;
    top: 50%;
    color: white;
    transform: translate3d(-50%, -50%, 0);
    font: normal normal normal 24px/1 FontAwesome;
    background-color: mediumpurple;
    height: 60px;
    width: 60px;
    border-radius: 50%;
  }
  & > section > section {
    transition: all 0.3s;
    background-color: white;
    margin: 8px 0;
    border-radius: 5px;
    padding: 10px;
    &:hover {
      background-color: mediumpurple;
      color: white;
    }
    h2 {
      margin: 0;
      color: inherit;
      font-size: 16px;
      overflow: hidden;
      text-overflow: ellipsis;
      display: -webkit-box;
      -webkit-box-orient: vertical;
      -webkit-line-clamp: 2;
    }
    span {
      display: block;
      text-align: right;
      width: 100%;
      color: #989898;
      font-size: 14px;
    }
  }
}
.browse-scroll {
  overflow-y: scroll;
  max-height: 90%;
  &::-webkit-scrollbar {
    display: none;
  }
}
</style>