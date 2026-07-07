// student-profile.vue

<template>
  <div v-if="showProfile">
    <img
      v-if="profileData.photo"
      :src="`data:image/png;base64,${profileData.photo}`"
      alt="Profile Image"
    />
    <div v-else class="profile-photo-placeholder" aria-hidden="true"></div>
    <h2>{{ profileData.student_name }}</h2>
    <p>{{ profileData.student_number }}</p>
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
    profileData() {
      return this.visitStore.studentProfile.data || {};
    },
    showProfile() {
      return Boolean(this.visitStore.studentProfile.data);
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

<style scoped>
.profile-photo-placeholder {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  background: #d8dee6;
}
</style>
