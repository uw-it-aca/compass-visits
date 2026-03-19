// student-profile.vue

<template>
  <div v-if="showProfile">
    <img :src="visitStore.studentProfile.data.photo_url" alt="Profile Image" />
    <h2>{{ visitStore.studentProfile.data.student_name }}</h2>
    <p>{{ visitStore.studentProfile.data.student_number }}</p>
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
  },
  methods: {},
};
</script>
