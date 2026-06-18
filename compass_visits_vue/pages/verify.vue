// verify.vue

<template>
  <DefaultLayout :page-title="pageTitle">
    <template #content>
      <div class="mt-3">
        <div class="alert alert-warning" role="alert">
          <i class="bi bi-exclamation-triangle-fill"></i>
          Your check-in is not yet complete. Please verify with the IC front
          desk, and refresh the page.
        </div>
        <h2 class="display-6 fw-bold ff-encode-sans my-5 text-center">
          {{ profile.student_name }}
        </h2>
        <visit-details :visit-data="visitDetails" />
        <div
          style="
            position: fixed;
            bottom: 92px;
            left: 16px;
            right: 16px;
            display: flex;
            background-color: white;
            justify-content: center;
          "
        >
          <div class="row" style="width: 100%; max-width: 1200px">
            <button class="btn btn-primary btn-lg my-2" @click="refreshPage">
              Refresh
            </button>
            <button
              class="btn btn-outline-danger btn-lg my-2"
              @click="cancelVisit"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </template>
  </DefaultLayout>
</template>

<script>
import DefaultLayout from "@/layouts/default.vue";
import VisitDetails from "../components/visit-details.vue";
import { useVisitStore } from "@/stores/visit";

export default {
  name: "Verify",
  components: { DefaultLayout, VisitDetails },
  setup() {
    const visitStore = useVisitStore();
    return { visitStore };
  },
  data() {
    return {
      pageTitle: "Verification Required",
      profile: null,
    };
  },
  created() {
    this.visitStore.fetchStudentProfile().then(() => {
      this.profile = this.visitStore.studentProfile.data;
    });
  },
  computed: {
    visitDetails() {
      return this.profile ? this.profile.visit : null;
    },
  },
  methods: {
    refreshPage() {
      this.visitStore.refreshStudentProfile().then(() => {
        this.profile = this.visitStore.studentProfile.data;
        this.$router.push("/checkout");
      });
    },
    cancelVisit() {
      this.visitStore.deleteVisit().then(() => {
        this.profile = null;
        this.$router.push("/");
      });
    },
  },
  watch: {},
};
</script>
