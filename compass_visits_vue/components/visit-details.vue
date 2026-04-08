// student-profile.vue

<template>
  <p>Program Area</p>
  {{ programAreaString }}
  <br />
  <p>Tutoring Type</p>
  {{ tutoringTypeString }}
  <br />
  <p>Course</p>
  {{ courseString }}

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
    programAreaString: function() {
      if (this.visitData && this.visitData.program_area) {
        return this.visitData.program_area;
      }
      return "";
    },
    tutoringTypeString: function() {
      if (this.visitData && this.visitData.tutoring_option) {
        return this.visitData.tutoring_option;
      }
      return "";
    },
    courseString: function() {
      if (this.visitData && this.visitData.course) {
        return this.visitData.course;
      }
      return this.visitData && this.visitData.writing_service ? this.visitData.writing_service : "";
    },
  },
};
</script>
