<template>
  <div class="all-genres-container clearfix">
    <PaperDisplay/>
    <PaperDisplay/>
    <PaperDisplay/>
  </div>
</template>

<script>
import PaperDisplay from "@/components/Home/PaperDisplay";
export default {
  name: "AllGenres",
  components: {PaperDisplay}
}
</script>

<style scoped>
.all-genres-container {
  width: 100%;
  margin: 50px 0;
  padding: 40px 40px;
}
.all-genres-container > div {
  float: left;
  width: 50%;
  box-sizing: border-box;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;

}
</style>