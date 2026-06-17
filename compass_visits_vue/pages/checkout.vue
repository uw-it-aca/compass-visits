// checkout.vue

<template>
  <DefaultLayout :page-title="pageTitle">
    <template #title>
      <h1 class="fs-5 fw-medium ff-open-sans text-center">
        {{ pageTitle }}
      </h1>
    </template>
    <template #content>
      <div v-if="showCheckout">
        <div class="alert alert-success alert-dismissible" role="alert">
          <i class="bi-check-circle-fill me-1"></i>
          Check-in successful
          <button
            type="button"
            class="btn-close"
            aria-label="Close"
            data-bs-dismiss="alert"
          ></button>
        </div>
        <div class="text-center">
          <h2 class="fs-2 fw-semibold ff-encode-sans mb-3">
            {{ profile.student_name }}
          </h2>
          <visit-details :visit-data="profile.visit" />
          <div>
            <h3 class="fs-6 ff-open-sans mb-2">Time</h3>
            {{ visitDuration }}
            (Total: {{ totalMinutes }} min)
          </div>
        </div>
        <div
          style="
            position: fixed;
            bottom: 32px;
            left: 16px;
            right: 16px;
            display: flex;
            background-color: white;
            justify-content: center;
          "
        >
          <div class="row" style="width: 100%; max-width: 1200px">
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
        <div style="height: 100px"></div>
      </div>
      <div v-else class="text-center">
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
