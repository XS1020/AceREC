<template>
  <div class="carousel-wrapper">
<!--    <input type="radio" name="carousel-control"-->
<!--    v-for="(control, index) in items"-->
<!--    :checked="index === displayItemIdx"-->
<!--    />-->
    <Billboard class="carousel-item"
        v-for="(item, index) in items"
        :style="{left: (50 * index - 25) + '%',
                  backgroundColor: color[index + 1],
                  transform: 'translateX(' + 100 * (displayItemIdx - defaultItemIdx) + '%)'
                  }">

    </Billboard>
    <div class="carousel-control carousel-left" @click="displayItemIdx ++"
    v-if="displayItemIdx < items.length - 1">
      <i class="fa fa-chevron-left"/>
    </div>
    <div class="carousel-control carousel-right" @click="displayItemIdx --"
    v-if="displayItemIdx > 0">
      <i class="fa fa-chevron-right"/>
    </div>
  </div>
</template>

<script>
import Billboard from "@/components/Home/Billboard";
export default {
  name: "Carousel",
  components: {Billboard},
  data () {
    return {
      displayItemIdx: 1,
      defaultItemIdx: 1,
      color: ['#FBADAF', '#ECB7D4', '#91D3E1', "#2978b5"],
      items: [
        {
          text: "100",
        },
        {
          text: "200",
        },
        {
          text: "300",
        }
      ]
    }
  }
}
</script>

<style scoped>
.carousel-wrapper {
  list-style: none;
  width: 80%;
  overflow: hidden;
  display: flex;
  justify-content: center;
  min-height: 500px;
  z-index: 1;
}
.carousel-wrapper:after {
  content: "";
  display: block;
  clear: both;
}
div.carousel-item {
  width: 50%;
  position: absolute;
  transition: all 0.3s ease-in-out;
}
.carousel-control {
  position: absolute;
  color: #989898;
  font-size: 30px;
  width: 50px;
  height: 50px;
  font-weight: 200;
  display: flex;
  justify-content: center;
  align-items: center;
  top: 220px;
  z-index: 1;
}
.carousel-control >i {
  margin: auto;
}
.carousel-control:before {
  content: "";
  display: block;
  position: absolute;
  top: 0; right: 0; bottom: 0; left: 0;
  border-radius: 50%;
  backdrop-filter: blur(2px);
  background-color: rgba(255, 255, 255, 0.2);
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2);
  z-index: -1;
}
.carousel-left {
  left: 10%;
}
.carousel-right {
  right: 10%;
}
</style>