// checkout.vue

<template>
  <DefaultLayout :page-title="pageTitle">
    <template #content>
      <div v-if="showCheckout" class="d-flex flex-column">
        <BAlert :model-value="true" variant="success" dismissible class="mb-4">
          <i class="bi-check-circle-fill me-1"></i>
          Check-in successful
        </BAlert>

        <div class="mt-auto text-center">
          <h2 class="fs-2 fw-semibold ff-encode-sans pb-4">
            {{ profile.student_name }}
          </h2>
          <visit-details :visit-data="profile.visit" />
          <div class="mb-2 pb-2">
            <h3 class="fs-6 fw-semibold ff-open-sans mb-1">Time</h3>
            {{ visitDuration }} <br />
            (Total: {{ totalMinutes }} min)
          </div>
        </div>
      </div>
      <div v-else>
        <div class="alert alert-danger" role="alert">
          <i class="bi bi-exclamation-octagon-fill"></i> You are not currently
          checked in.
        </div>
      </div>
    </template>

    <template v-if="showCheckout" #action>
      <BButton variant="outline-primary" size="lg" @click="handleSwitchSession">
        Switch Session
      </BButton>
      <BButton variant="danger" size="lg" @click="handleCheckout">
        Check Out
      </BButton>
    </template>
  </DefaultLayout>
</template>

<script>
  import DefaultLayout from "@/layouts/default.vue";
  import { useVisitStore } from "@/stores/visit";
  import VisitDetails from "@/components/visit-details.vue";
  import { BAlert, BButton } from "bootstrap-vue-next";

  export default {
    name: "Checkout",
    components: { DefaultLayout, BAlert, BButton, VisitDetails },
    setup() {
      const visitStore = useVisitStore();
      return { visitStore };
    },
    data() {
      return {
        pageTitle: "Visit Verfied",
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
    },
    computed: {
      showCheckout() {
        return this.profile && this.profile.current_state === "active";
      },
      visitDuration() {
        return this.visitStore.visitDurationString;
      },
      totalMinutes() {
        return this.visitStore.totalMinutes;
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
