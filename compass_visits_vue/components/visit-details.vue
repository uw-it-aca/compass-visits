// student-profile.vue

<template>
  <div class="text-center">
    <div class="mb-2 pb-2">
      <h3 class="fs-6 fw-semibold ff-open-sans mb-1">Program Area</h3>
      <p>{{ programAreaString }}</p>
    </div>

    <div class="mb-2 pb-2">
      <h3 class="fs-6 fw-semibold ff-open-sans mb-1">Tutoring Type</h3>
      <p>{{ tutoringTypeString }}</p>
    </div>

    <div class="mb-2 pb-2">
      <h3 class="fs-6 fw-semibold ff-open-sans mb-1">Course</h3>
      <p>{{ courseString }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "VisitDetails",
  props: {
    visitData: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {};
  },
  computed: {
    programAreaString: function () {
      if (this.visitData && this.visitData.program_area) {
        return this.visitData.program_area;
      }
      return "";
    },
    tutoringTypeString: function () {
      if (this.visitData && this.visitData.tutoring_option) {
        return this.visitData.tutoring_option;
      }
      return "";
    },
    courseString: function () {
      if (this.visitData && this.visitData.course) {
        return this.visitData.course;
      }
      return this.visitData && this.visitData.writing_service
        ? this.visitData.writing_service
        : "";
    },
  },
};
</script>
