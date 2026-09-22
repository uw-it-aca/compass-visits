// student-profile.vue

<template>
  <div v-if="showProfile">
    <div class="d-flex justify-content-start mt-2 mb-4">
      <div class="mx-3">
        <img
          v-if="profileData.photo"
          :src="`data:image/png;base64,${profileData.photo}`"
          alt="Profile Image"
          class="img-profile rounded-circle"
        />
        <div v-else class="profile-photo-placeholder" aria-hidden="true"></div>
      </div>
      <div class="ms-2 my-auto">
        <h2 class="fw-normal ff-open-sans">
          {{ profileData.student_name }}
        </h2>
        <h3 class="fs-6 fw-normal"> {{ profileData.student_number }} </h3>
      </div>
    </div>

    <div class="pb-2">
      <BCard class="bg-body-tertiary rounded-3" border-variant="0">
        <h3 class="fs-6 fw-normal">Total hour:</h3>
        <p class="fs-1 fw-bold m-0 text-end">
          {{ totalHour.toFixed(2) }}
          <span class="fs-6 fw-normal text-body-secondary"> hrs </span>
          <span class="fs-5 fw-semibold ms-2"> {{ totalVisits }} </span>
          <span class="fs-6 fw-normal text-body-secondary"> visits</span>
        </p>
      </BCard>
    </div>

    <div class="row row-cols-2 g-2">
      <div v-for="(hour, course) in courseHour" :key="course" class="col">
        <BCard class="bg-body-tertiary rounded-3" border-variant="0">
          <h3 class="fs-6 fw-normal"> {{ course }}: </h3>
          <p class="fs-5 fw-semibold m-0 text-end">
            {{ hour.toFixed(2) }}
            <span class="fs-6 fw-normal text-body-secondary"> hrs</span>
          </p>
        </BCard>
      </div>
    </div>
  </div>
</template>

<script>
import { useVisitStore } from "@/stores/visit";
import { BCard } from "bootstrap-vue-next";

export default {
  name: "StudentProfile",
  components: { BCard },
  data() {
    return {
      visitStore: useVisitStore(),
    };
  },
  mounted() {
    this.visitStore.fetchStudentProfile();
    this.visitStore.fetchStudentVisitList();
  },
  computed: {
    profileData() {
      return this.visitStore.studentProfile.data || {};
    },
    showProfile() {
      return Boolean(this.visitStore.studentProfile.data);
    },
    totalHour() {
      return this.visitStore.totalMinutes / 60;
    },
    totalVisits() {
      const visits = this.visitStore.studentVisitList.data;
      return Array.isArray(visits) ? visits.length : 0;
    },
    courseHour() {
      const visits = this.visitStore.studentVisitList.data ?? [];
      const list = {};
      for (const visit of visits) {
        if (!visit.course || visit.active_minutes <= 0) continue;
        list[visit.course] = (list[visit.course] ?? 0) + visit.active_minutes / 60;
      }
      return list;
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
