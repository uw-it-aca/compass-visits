// student-profile.vue

<template>
  <div v-if="showProfile" class="text-center">
    <img
      v-if="profileData.photo"
      :src="`data:image/png;base64,${profileData.photo}`"
      alt="Profile Image"
      class="img-profile rounded-circle mb-4"
    />
    <div v-else class="profile-photo-placeholder" aria-hidden="true"></div>
    <h2 class="fs-2 fw-semibold ff-encode-sans">
      {{ profileData.student_name }}
    </h2>
    <p class="pb-3">student ID: {{ profileData.student_number}}</p>
    <p class="m-0">Total Hours:</p>
    <p class="fs-3 fw-bold m-0">{{ totalHours.toFixed(2) }}</p>
  </div>
</template>

<script>
import { useVisitStore } from "@/stores/visit";

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
