// checkout.vue

<template>
  <DefaultLayout :page-title="pageTitle">
    <template #title>
      {{ pageTitle }}
    </template>
    <template #content>
      <div v-if="showCheckout">
        <p>Visit Verified</p>
        <h2>{{ profile.student_name }}</h2>
        <visit-details :visit-data="profile.visit" />
        <br />
        Time
        <br />
        {{ visitDuration }}
        <br />
        (Total: {{ totalMinutes }} min)
        <button class="btn btn-primary" @click="handleSwitchSession">
          Switch <Search></Search>
        </button>
        <button class="btn btn-primary" @click="handleCheckout">
          Check Out
        </button>
      </div>
      <div v-else>
        <p>You are not currently checked in.</p>
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
      pageTitle: "Check Out of Visit",
      profile: null,
    };
  },
  created() {
    this.visitStore.fetchStudentProfile().then(() => {
      this.profile = this.visitStore.studentProfile.data;
      if(this.profile.visit && !this.profile.visit.is_verified) {
        this.$router.push({ name: "verify" });
      }
      if(!this.profile.visit) {
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
      this.visitStore.handleCheckout().then(() => {
        this.$router.push({ name: "create" });
      });
    },
  },
};
</script>
