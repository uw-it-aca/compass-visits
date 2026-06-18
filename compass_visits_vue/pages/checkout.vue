// checkout.vue

<template>
  <DefaultLayout :page-title="pageTitle">
    <template #content>
      <div 
        v-if="showCheckout" 
        class="d-flex flex-column align-content-between" 
        style="min-height: calc(100vh - 265px)">
        <div class="alert alert-success alert-dismissible mb-4" role="alert">
          <i class="bi-check-circle-fill me-1"></i>
          Check-in successful
          <button
            type="button"
            class="btn-close"
            aria-label="Close"
            data-bs-dismiss="alert"
          ></button>
        </div>
        <div class="mt-auto text-center">
          <h2 class="fs-2 fw-semibold ff-encode-sans pb-4">
            {{ profile.student_name }}
          </h2>
          <visit-details :visit-data="profile.visit" />
          <div class="mb-2 pb-2">
            <h3 class="fs-6 fw-semibold ff-open-sans mb-1">Time</h3>
            {{ visitDuration }} <br>
            (Total: {{ totalMinutes }} min)
          </div>
        </div>
        <div class="row mt-auto mx-0 text-center">
          <button
            class="btn btn-outline-primary btn-lg my-2"
            @click="handleSwitchSession"
          >
            Switch <Search></Search>
          </button>
          <button class="btn btn-danger btn-lg my-2" @click="handleCheckout">
            Check Out
          </button>
        </div>
      </div>
      <div v-else>
        <div class="alert alert-danger" role="alert">
          <i class="bi bi-exclamation-octagon-fill"></i> You are not currently
          checked in.
        </div>
      </div>
    </template>
  </DefaultLayout>
</template>

<script>
import DefaultLayout from "@/layouts/default.vue";
import { useVisitStore } from "@/stores/visit";
import VisitDetails from "@/components/visit-details.vue";

export default {
  name: "Checkout",
  components: { DefaultLayout, VisitDetails },
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
        this.$router.push("/");
      });
    },
    handleSwitchSession() {
      this.visitStore.handleCheckout().then(() => {
        this.$router.push("/create");
      });
    },
  },
};
</script>
