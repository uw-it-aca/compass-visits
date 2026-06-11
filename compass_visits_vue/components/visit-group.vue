// visit-group.vue

<template>
  <div class="row align-items-center pt-4 pb-2">
    <h2 class="fs-5 fw-bold ff-open-sans col m-0">{{ groupTitle }}</h2>
    <p class="col-auto text-body-secondary m-0">
      {{ visitList.length }} {{ visitString }}, {{ totalVisitDuration }} min
    </p>
  </div>
  <div v-if="visitList.length === 0" class="text-muted">
    No visits in this time period.
  </div>
  <div v-for="visit in visitList" :key="visit.id">
    <visitRow :visit="visit" />
  </div>
</template>

<script>
import visitRow from "./visit-row.vue";
// import pluralize
import pluralize from "pluralize";

export default {
  name: "VisitGroup",
  components: { visitRow },
  props: {
    visitList: {
      type: Array,
      required: true,
    },
    groupTitle: {
      type: String,
      required: true,
    },
  },
  data() {
    return {};
  },
  computed: {
    totalVisitDuration() {
      // add up visit.active_minutes for all visits in visitList
      return this.visitList.reduce(
        (total, visit) => total + visit.active_minutes,
        0
      );
    },
    visitString() {
      return pluralize("visit", this.visitList.length);
    },
  },
  methods: {},
};
</script>
