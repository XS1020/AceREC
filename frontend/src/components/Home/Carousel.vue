<template>
  <div class="carousel-wrapper">
<!--    <input type="radio" name="carousel-control"-->
<!--    v-for="(control, index) in items"-->
<!--    :checked="index === displayItemIdx"-->
<!--    />-->
    <Billboard class="carousel-item"
        v-for="(item, index) in items"
        :data="item"
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
          text: "CVPR: Internaltional Conference on Computer Vision and Pattern Recogintion",
          imgurl: require('../../assets/CVPR.png'),
          desc: ["05/26 - Paper Presentation Requirements for CVPR 2021 available\n",
              "05/26 - CVPR'21 is accepting applicants for DEI registration waivers\n",
              "5/14 - The 24 hour Main Conference, Workshop and Tutorial schedules have been posted",
              "03/25 - Media information is available"],
          time: "June 19th to June 25th",
          originURL: "http://cvpr2021.thecvf.com/"
        },
        {
          text: "IJCAI 2021",
          imgurl: require('../../assets/ijicai.png'),
          desc: ["04/30 Paper notification",
          "03/24~28 Author response period",
          "02/07 Summary reject notification",
          "01/20 Full paper submission deadline",
          "01/16 Author information deadline"],
          time: "August 21st to August 26th",
          originURL: "https://ijcai-21.org/"
        },
        {
          text: "ICCV 2021",
          imgurl: require('../../assets/iccv.png'),
          desc: ["08/17 Camera Ready Deadline",
          "07/22 Final Decision to Authors",
          "06/17 Rebuttals Due",
          "03/24 Supplementary Materials Deadline"],
          originURL: "http://iccv2021.thecvf.com/home"
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