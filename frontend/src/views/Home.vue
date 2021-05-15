<template>
  <div class="home">
    <Carousel/>
    <HelloWorld msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script>
import HelloWorld from '@/components/HelloWorld.vue'
import Carousel from "@/components/Carousel";

export default {
  name: 'Home',
  components: {
    Carousel,
    HelloWorld
  }
}
</script>
