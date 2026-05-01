// verify.vue

<template>
  <DefaultLayout :page-title="pageTitle">
    <template #title>
      {{ pageTitle }}
    </template>
    <template #content>
      <div class="alert alert-warning" role="alert">
        <i class="bi bi-exclamation-triangle-fill"></i>
        Your check-in is not yet complete. Please verify with the IC front desk,
        and refresh the page to see the most up-to-date status.
      </div>
      <visit-details :visit-data="visitDetails" />
      <br />
      <button class="btn btn-primary" @click="refreshPage">Refresh</button>
      <button class="btn btn-danger" @click="cancelVisit">Cancel</button>
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
      pageTitle: "Verify Visit",
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
