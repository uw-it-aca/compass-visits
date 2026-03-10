// student-profile.vue

<template>
  <p>{{ visitStore.studentProfile }}</p>
</template>

<script>
import { useVisitStore } from '../stores/visit';

export default {
  name: "StudentProfile",
  data() {
    return {
      visitStore: useVisitStore(),
    };
  },
  mounted() {
    console.log("StudentProfile mounted");
    this.visitStore.fetchStudentProfile();
  },
  methods: {},
};
</script>
