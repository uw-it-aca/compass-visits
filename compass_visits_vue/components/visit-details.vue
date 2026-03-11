// student-profile.vue

<template>
  <p>Program Area</p>
  {{ this.visitData.program_area }}
  <br />
  <p>Tutoring Type</p>
  {{ this.visitData.tutoring_option }}
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
    courseString: function() {
      if (this.visitData.course) {
        return this.visitData.course;
      }
      return this.visitData.writing_service;
    },
  },
};
</script>
