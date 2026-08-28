// checkout.vue

<template>
  <DefaultLayout :page-title="pageTitle">
    <template #content>
      <div v-if="showCheckout" class="d-flex flex-column">
        <BAlert :model-value="true" variant="success" dismissible class="mb-4">
          <i class="bi-check-circle-fill me-1"></i>
          Check-in successful
        </BAlert>

        <BCard class="bg-body-tertiary rounded-3" border-variant="0">
          <h2 class="h2 fw-semibold ff-encode-sans text-center">
            {{ profile.student_name }}
          </h2>
          <visit-details :visit-data="profile.visit" />

          <div class="d-flex align-items-center pt-4">
            <i class="bi bi-hourglass-bottom fs-2 px-4"></i>
            <div>
              <h3 class="h6 fw-bold ff-open-sans m-0">Time</h3>
              <p class="lead m-0">
                {{ visitDuration }} (Total: {{ totalMinutes }} min)
              </p>
            </div>
          </div>

        </BCard>
      </div>

      <div v-else>
        <div class="alert alert-danger" role="alert">
          <i class="bi bi-exclamation-octagon-fill"></i> You are not currently
          checked in.
        </div>
      </div>
    </template>

    <template v-if="showCheckout" #action>
      <BButton variant="primary" size="lg" @click="handleSwitchSession">
        Switch Session
      </BButton>
      <BButton variant="outline-danger" size="lg" @click="handleCheckout">
        Check Out
      </BButton>
    </template>
  </DefaultLayout>
</template>

<script>
  import DefaultLayout from "@/layouts/default.vue";
  import { useVisitStore } from "@/stores/visit";
  import VisitDetails from "@/components/visit-details.vue";
  import { BAlert, BButton, BCard } from "bootstrap-vue-next";

  export default {
    name: "Checkout",
    components: { DefaultLayout, BAlert, BButton, BCard, VisitDetails },
    setup() {
      const visitStore = useVisitStore();
      return { visitStore };
    },
    data() {
      return {
        pageTitle: "Visit Verified",
        profile: null,
      };
    },
    created() {
      this.visitStore.fetchStudentProfile().then(() => {
        this.profile = this.visitStore.studentProfile.data;
        if (this.profile.visit && !this.profile.visit.is_verified) {
          this.$router.push({ name: "verify" });
        }
        if (!this.profile.visit) {
          this.$router.push({ name: "home" });
        }
      });
      this.visitStore.fetchStudentVisitList();
    },
    computed: {
      showCheckout() {
        return this.profile && this.profile.current_state === "active";
      },
      visitDuration() {
        return this.visitStore.visitDurationString;
      },
      totalMinutes() {
        const course = this.profile.visit.course;
        if (!course) return 0;
        const visits = this.visitStore.studentVisitList.data ?? [];
        return visits
          .filter((v) => v.course === course && v.active_minutes > 0)
          .reduce((sum, v) => sum + v.active_minutes, 0);
      },
    },
    methods: {
      handleCheckout() {
        this.visitStore.handleCheckout().then(() => {
          this.$router.push({ name: "home" });
        });
      },
      handleSwitchSession() {
        this.profile = null;
        // Reset to empty object (not null) so fetchStudentProfile can re-fetch
        this.visitStore.studentProfile = {};
        this.$router.push({ name: "create", query: { switch: true } });
      },
    },
  };
</script>
