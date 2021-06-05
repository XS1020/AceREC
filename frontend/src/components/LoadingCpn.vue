<template>
  <div class="loading-pattern">
    <i class="fa fa-spinner"/>
  </div>
</template>

<script>
export default {
  name: "LoadingCpn"
}
</script>

<style scoped>
.loading-pattern {
  display: flex;
  justify-content: center !important;
  align-items: center;
}
.loading-pattern > i {
  font-size: 40px;
  color: mediumpurple;
  animation: spin 3s linear infinite both;
}
@keyframes spin {
  0%{transform: rotate(0)}
  25%{transform: rotate(90deg)}
  50%{transform: rotate(180deg)}
  75%{transform: rotate(270deg)}
  100%{transform: rotate(360deg)}
}
</style>