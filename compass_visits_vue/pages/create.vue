// verify.vue

<template>
  <DefaultLayout :page-title="pageTitle">
    <template #title>
      {{ pageTitle }}
    </template>
    <template #content>
      <p>Create Visit Page</p>
    </template>
  </DefaultLayout>
</template>

<script>
import DefaultLayout from "@/layouts/default.vue";

export default {
  name: "Create",
  components: { DefaultLayout },
  data() {
    return {
      pageTitle: "Create Visit",
    };
  },
  computed: {},
  methods: {},
  watch: {},
};
</script>
