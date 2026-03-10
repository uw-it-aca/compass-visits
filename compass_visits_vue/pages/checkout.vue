// checkout.vue

<template>
  <DefaultLayout :page-title="pageTitle">
    <template #title>
      {{ pageTitle }}
    </template>
    <template #content>
      <p>Checkout Page</p>
    </template>
  </DefaultLayout>
</template>

<script>
import DefaultLayout from "@/layouts/default.vue";

export default {
  name: "Checkout",
  components: { DefaultLayout },
  data() {
    return {
      pageTitle: "Check Out of Visit",
    };
  },
  computed: {},
  methods: {},
  watch: {},
};
</script>
