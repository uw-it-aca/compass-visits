// student-profile.vue

<template>
  <div class="text-center">
    <div class="mb-4">
      <h6>Program Area</h6>
      {{ programAreaString }}
    </div>

    <div class="mb-4">
      <h6>Tutoring Type</h6>
      {{ tutoringTypeString }}
    </div>

    <div class="mb-4">
      <h6>Course</h6>
      {{ courseString }}
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
