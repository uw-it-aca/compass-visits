// student-profile.vue

<template>
  <div class="text-center">
    <div class="mb-4">
      <h3 class="fs-6 ff-open-sans mb-2">Program Area</h3>
      {{ programAreaString }}
    </div>

    <div class="mb-4">
      <h3 class="fs-6 ff-open-sans mb-2">Tutoring Type</h3>
      {{ tutoringTypeString }}
    </div>

    <div class="mb-4">
      <h3 class="fs-6 ff-open-sans mb-2">Course</h3>
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
