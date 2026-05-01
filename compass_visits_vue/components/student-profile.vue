// student-profile.vue

<template>
  <div v-if="showProfile" class="text-center">
    <img
      :src="`data:image/png;base64,${visitStore.studentProfile.data.photo}`"
      alt="Profile Image"
    />
    <h2 class="my-3">{{ visitStore.studentProfile.data.student_name }}</h2>
    <p>student ID: {{ visitStore.studentProfile.data.student_number }}</p>
    <p>Total Hours:</p>
    <p class="fw-bold">{{ totalHours.toFixed(2) }}</p>
  </div>
</template>

<script>
import { useVisitStore } from "../stores/visit";

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
