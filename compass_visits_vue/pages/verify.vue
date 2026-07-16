// verify.vue

<template>
  <DefaultLayout :page-title="pageTitle">
    <template #content>
      <div class="d-flex flex-column" style="min-height: calc(100vh - 265px)">
        <div class="alert alert-warning mb-4" role="alert">
          <i class="bi bi-exclamation-triangle-fill"></i>
          Your check-in is not yet complete. Please verify with the IC front
          desk, and refresh the page.
        </div>
        <div class="mt-auto text-center">
          <h2 class="fs-2 fw-semibold ff-encode-sans pb-4">
            {{ profile.student_name }}
          </h2>
          <visit-details :visit-data="visitDetails" />
        </div>
      </div>
    </template>
    <template #action>
      <button class="btn btn-primary btn-lg mb-3" @click="refreshPage">
        Refresh
      </button>
      <button class="btn btn-outline-danger btn-lg mb-2" @click="cancelVisit">
        Cancel
      </button>
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
      this.visitStore.refreshStudentProfile().then(() => {
        this.profile = this.visitStore.studentProfile.data;
        if (
          this.profile &&
          this.profile.visit &&
          this.profile.visit.is_verified
        ) {
          this.redirectToCheckout();
        }
        if (!this.profile.visit) {
          this.redirectToHome();
        }
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
          if (this.profile.visit.is_verified) {
            this.redirectToCheckout();
          }
        });
      },
      cancelVisit() {
        this.visitStore.deleteVisit().then(() => {
          this.profile = null;
          this.redirectToHome();
        });
      },
      redirectToCheckout() {
        this.$router.push({ name: "checkout" });
      },
      redirectToHome() {
        this.$router.push({ name: "home" });
      },
    },
  };
</script>
