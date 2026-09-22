// visit-row.vue

<template>
  <div class="row">
    <div class="col-auto">
      <i class="bi bi-calendar-check"></i>
      <br />
      <span class="border-start pb-4 ms-2"></span>
    </div>

    <div class="col pb-4">
      {{ visitTitle }} 
      <br />
      <small class="text-body-secondary">
        {{ dateString }} ({{ visit.active_minutes }} min)
      </small>
    </div>
  </div>
</template>

<script>
export default {
  name: "VisitRow",
  props: {
    visit: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {};
  },
  computed: {
    visitTitle() {
      if (this.visit.course) {
        return this.visit.course;
      } else if (this.visit.writing_service) {
        return this.visit.writing_service;
      }
    },
    dateString() {
      const start_date = new Date(this.visit.check_in_date);
      const end_date = new Date(this.visit.check_out_date);
      if (start_date.toDateString() === end_date.toDateString()) {
        return `${start_date.toLocaleDateString()} ${start_date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })} - ${end_date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}`;
      } else {
        return `${start_date.toLocaleDateString()} ${start_date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })} - ${end_date.toLocaleDateString()} ${end_date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}`;
      }
    },
  },
  methods: {},
};
</script>
