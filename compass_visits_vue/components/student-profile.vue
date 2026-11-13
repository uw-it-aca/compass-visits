<template>
  <div v-if="showProfile">
    <div class="pb-2">
      <BCard class="bg-body-tertiary rounded-3" border-variant="0">
        <h3 class="fs-6 fw-normal">Total:</h3>
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
};
</script>
