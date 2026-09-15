// verify.vue

<template>
  <DefaultLayout :page-title="pageTitle">
    <template #content>
      <div class="d-flex flex-column">
        <BAlert :model-value="true" variant="warning" class="mb-3">
          <i class="bi bi-exclamation-triangle-fill"></i>
          Your check-in isn't complete yet. Verify with the IC front desk, then refresh.
        </BAlert>

        <div v-if="profile">
          <BCard class="bg-husky-gold-subtle bg-opacity-50 rounded-3" border-variant="0">
            <h2 class="fw-semibold ff-open-sans h4 text-center py-1">
              {{ profile.student_name }}
            </h2>
            <h3 class="fs-6 fw-normal text-center"> {{ profile.student_number }} </h3>
            <hr class="border-secondary py-1">
            <visit-details :visit-data="visitDetails" />
          </BCard>
        </div>
      </div>
    </template>
    <template #action>
      <BButton variant="primary" size="lg" @click="refreshPage">
        Refresh
      </BButton>
      <BButton variant="outline-danger" size="lg" @click="cancelVisit">
        Cancel
      </BButton>
    </template>
  </DefaultLayout>
</template>

<script>
  import DefaultLayout from "@/layouts/default.vue";
  import VisitDetails from "@/components/visit-details.vue";
  import { useVisitStore } from "@/stores/visit";
  import { BAlert, BButton, BCard } from "bootstrap-vue-next";

  export default {
    name: "Verify",
    components: { DefaultLayout, BAlert, BButton, BCard, VisitDetails },
    setup() {
      const visitStore = useVisitStore();
      return { visitStore };
    },
    data() {
      return {
        pageTitle: "Verify Visit",
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
