<template>
  <b-alert>
    <div :class="`alert alert-${level}`" role="alert">
      <ul>
        <li v-for="(msg, index) in messages" :key="index">{{ msg }}</li>
      </ul>
    </div>
  </b-alert>
</template>

<script>
export default {
  props: {
    messages: {
      type: Object,
      required: true,
    },
    level: {
      type: String,
      required: false,
      default: "info",
    },
  },
  data() {
    return {};
  },
};
</script>
