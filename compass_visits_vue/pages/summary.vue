// summary.vue

<template>
  <DefaultLayout :page-title="pageTitle">
    <template #title>
      <div class="row align-items-center">
        <div class="col-1">
          <a href="/"><i class="bi bi-arrow-left fs-3"></i></a>
        </div>
        <h1 class="col fs-3 fw-light ff-encode-sans text-center m-0">
          {{ pageTitle }}
        </h1>
      </div>
    </template>
    <template #content>
      <visit-group :visit-list="visitsThisWeek" group-title="This Week" />
      <visit-group :visit-list="visitsLastWeek" group-title="Last Week" />
      <visit-group :visit-list="remainingVisits" group-title="This Quarter" />
    </template>
  </DefaultLayout>
</template>

<script>
import DefaultLayout from "@/layouts/default.vue";
import { useVisitStore } from "@/stores/visit";
import visitGroup from "../components/visit-group.vue";

export default {
  name: "Visit  Summary",
  components: { DefaultLayout, visitGroup },
  setup() {
    const visitStore = useVisitStore();
    return { visitStore };
  },
  data() {
    return {
      pageTitle: "Visit Summary",
      visitList: [],
    };
  },
  created() {
    this.visitStore.fetchStudentVisitList().then(() => {
      this.visitList = this.visitStore.studentVisitList.data;
    });
  },
  computed: {
    visitsThisWeek() {
      const now = new Date();
      const oneWeekAgo = new Date(
        now.getFullYear(),
        now.getMonth(),
        now.getDate() - 7
      );
      return this.visitList.filter((visit) => {
        const checkInDate = new Date(visit.check_in_date);
        return checkInDate >= oneWeekAgo && checkInDate <= now;
      });
    },
    visitsLastWeek() {
      const now = new Date();
      const oneWeekAgo = new Date(
        now.getFullYear(),
        now.getMonth(),
        now.getDate() - 7
      );
      const twoWeeksAgo = new Date(
        now.getFullYear(),
        now.getMonth(),
        now.getDate() - 14
      );
      return this.visitList.filter((visit) => {
        const checkInDate = new Date(visit.check_in_date);
        return checkInDate >= twoWeeksAgo && checkInDate < oneWeekAgo;
      });
    },
    remainingVisits() {
      const now = new Date();
      const twoWeeksAgo = new Date(
        now.getFullYear(),
        now.getMonth(),
        now.getDate() - 14
      );
      return this.visitList.filter((visit) => {
        const checkInDate = new Date(visit.check_in_date);
        return checkInDate < twoWeeksAgo;
      });
    },
  },
  methods: {},
  watch: {},
};
</script>
