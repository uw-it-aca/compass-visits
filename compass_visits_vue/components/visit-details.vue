// student-profile.vue

<template>
      <div class="d-flex align-items-center pt-4">
        <i class="bi bi-mortarboard fs-2 px-4"></i>
        <div>
          <h3 class="h6 fw-bold ff-open-sans m-0">Program Area</h3>
          <p class="lead m-0">{{ programAreaString }}</p>
        </div>
      </div>

      <div class="d-flex align-items-center pt-4">
        <i class="bi bi-person-video3 fs-2 px-4"></i>
        <div>
          <h3 class="h6 fw-bold ff-open-sans m-0">Tutoring Type</h3>
          <p class="lead m-0">{{ tutoringTypeString }}</p>
        </div>
      </div>

      <div class="d-flex align-items-center pt-4">
        <i class="bi bi-journal-check fs-2 px-4"></i>
        <div>
          <h3 class="h6 fw-bold ff-open-sans m-0">Course</h3>
          <p class="lead m-0">{{ courseString }}</p>
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
