<template>
  <div class="error-pattern">
    <i class="fa fa-times" aria-hidden="true"></i>
  </div>
</template>

<script>
export default {
  name: "ErrorCpn"
}
</script>

<style scoped>
.error-pattern {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.error-pattern > i {
  font-size: 40px;
  color: palevioletred;
}
@keyframes spin {
  0%{transform: rotate(0)}
  25%{transform: rotate(90deg)}
  50%{transform: rotate(180deg)}
  75%{transform: rotate(270deg)}
  100%{transform: rotate(360deg)}
}
</style>