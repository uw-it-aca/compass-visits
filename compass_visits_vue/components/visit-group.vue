// visit-group.vue

<template>
  <div class="row pt-3">
    <h3 class="col">{{ groupTitle }}</h3>
    <p class="col-auto text-body-secondary pt-1">
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
