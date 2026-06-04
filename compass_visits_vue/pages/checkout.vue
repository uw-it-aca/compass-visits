// checkout.vue

<template>
  <DefaultLayout :page-title="pageTitle">
    <template #title>
      <div class="text-center">{{ pageTitle }}</div>
    </template>
    <template #content>
      <div v-if="showCheckout" class="text-center">
        <div class="alert alert-success" role="alert">
          <i class="bi-check-circle-fill me-1"></i>
          Check-in successful
          <button type="button" class="btn-close" aria-label="Close"></button>
        </div>
        <h2>{{ profile.student_name }}</h2>
        <visit-details :visit-data="profile.visit" />
        <div>
          <h6>Time</h6>
          {{ visitDuration }}
          (Total: {{ totalMinutes }} min)
        </div>
        <div class="row">
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
