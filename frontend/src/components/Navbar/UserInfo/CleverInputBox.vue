<template>
  <div class="clever-input-wrapper">
    <div class="clever-input-data">
      <input :type="type" required>
      <div class="clever-underline">
      </div>
      <label> {{text}} </label>
      <span class="clever-hint"> {{hint}} </span>
    </div>
  </div>
</template>

<script>
export default {
  name: "CleverInputBox",
  props: ['text', 'type', 'hint']
}
</script>

<style scoped>
.clever-input-wrapper {
  width: 250px;
}
.clever-input-wrapper .clever-input-data {
  height: 40px;
  width: 100%;
  position: relative;
}
.clever-input-data input {
  height: 100%;
  width: 100%;
  border: none;
  outline: none;
  padding: 0;
  margin: 0;
  box-sizing: border-box;
  font-size: 17px;
  border-bottom: 2px solid silver;
}
.clever-input-data label {
  position: absolute;
  bottom: 10px;
  left: 0;
  color: #989898;
  pointer-events: none;
  transition: all 0.3s ease;
  font-size: 15px;
}
.clever-input-data input:focus ~ label,
.clever-input-data input:valid ~ label{
  transform: translateY(-25px);
  font-size: 15px;
  color: rebeccapurple;
}
.clever-underline {
  position: absolute;
  bottom: 0;
  height: 2px;
  width: 100%;
}
.clever-underline:before {
  position: absolute;
  content: "";
  height: 100%;
  width: 100%;
  background-color: rebeccapurple;
  transition: all 0.3s ease;
  transform: scale(0);
}
.clever-input-data input:focus ~ .clever-underline:before,
.clever-input-data input:valid ~ .clever-underline:before {
  transform: scale(1);
}
.clever-hint {
  position: absolute;
  right: 0;
  bottom: -15px;
  font-size: 10px;
  color: silver;
}
</style>