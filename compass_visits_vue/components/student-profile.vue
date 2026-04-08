// student-profile.vue

<template>
  <div v-if="showProfile">
    <img :src="`data:image/png;base64,${visitStore.studentProfile.data.photo}`" alt="Profile Image" />
    <h2>{{ visitStore.studentProfile.data.student_name }}</h2>
    <p>{{ visitStore.studentProfile.data.student_number }}</p>
    <p>Total Hours: {{ totalHours.toFixed(2) }}</p>
  </div>
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
    this.visitStore.fetchStudentProfile();
  },
  computed: {
    showProfile() {
      return this.visitStore.studentProfile.data !== undefined;
    },
    totalHours() {
      if (this.visitStore.studentProfile.data) {
        return this.visitStore.totalMinutes / 60;
      }
      return 0;
    },
  },
  methods: {},
};
</script>
