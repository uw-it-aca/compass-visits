// home.vue

<template>
  <DefaultLayout :page-title="pageTitle">
    <template #title>
      {{ pageTitle }}
    </template>
    <template #content> </template>
  </DefaultLayout>
</template>

<script>
import DefaultLayout from "@/layouts/default.vue";
import StudentProfile from "@/components/student-profile.vue";
import { useVisitStore } from "@/stores/visit";

export default {
  name: "PagesHome",
  components: { DefaultLayout, StudentProfile },
  setup() {
    const visitStore = useVisitStore();
    return { visitStore };
  },
  data() {
    return {
      pageTitle: "Home",
      profile: null,
    };
  },
  created() {
    this.loadStudentProfile();
  },
  methods: {
    redirectToVerify() {
      this.$router.push("/verify");
    },
    redirectToCheckout() {
      this.$router.push("/checkout");
    },
    loadStudentProfile() {
      this.visitStore.fetchStudentProfile().then(() => {
        this.profile = this.visitStore.studentProfile.data;
      });
    },
  },
  watch: {
    profile(newValue) {
      if ("current_state" in newValue) {
        if (newValue.current_state === "pending_verification") {
          this.redirectToVerify();
        } else if (newValue.current_state === "active") {
          this.redirectToCheckout();
        }
      }
    },
  },
};
</script>
