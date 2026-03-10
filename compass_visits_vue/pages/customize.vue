// about.vue

<template>
  <DefaultLayout :page-title="pageTitle">
    <!-- page content -->
    <template #title>
      {{ pageTitle }}
    </template>

    <template #description>
      <p class="p-0 col-md-8 lead">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eget
        pulvinar est. Sed gravida neque justo, pellentesque finibus velit
        scelerisque eu. Curabitur et dolor luctus, convallis magna at, mollis
        purus. Nunc tincidunt risus quis nisl bibendum volutpat. Praesent ut
        tincidunt ex.
      </p>
    </template>

    <template #content>
    </template>
  </DefaultLayout>
</template>

<script>
import DefaultLayout from "@/layouts/default.vue";

import { useMouse } from "@/composables/mouse";
import { formatPhoneNumber } from "@/utils/format";

export default {
  name: "PagesCustomize",

  components: {
    DefaultLayout,
  },
  inject: ["mq"],
  // setup() is needed for Composition API
  setup() {
    // instantiate composable
    const { x, y } = useMouse();

    // return all imported functions to be used in the component
    return {
      x,
      y,
      formatPhoneNumber,
    };
  },
  data() {
    return {
      pageTitle: "Customizing your app",
    };
  },
  methods: {},
};
</script>
