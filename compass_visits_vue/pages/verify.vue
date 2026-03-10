// verify.vue

<template>
  <DefaultLayout :page-title="pageTitle">
    <template #title>
      {{ pageTitle }}
    </template>
    <template #content>
      <p>Verify Visit Page</p>
    </template>
  </DefaultLayout>
</template>

<script>
import DefaultLayout from "@/layouts/default.vue";

export default {
  name: "Verify",
  components: { DefaultLayout },
  data() {
    return {
      pageTitle: "Verify Visit",
    };
  },
  computed: {},
  methods: {},
  watch: {},
};
</script>
