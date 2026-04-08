// home.vue

<template>
  <DefaultLayout :page-title="pageTitle">
    <template #title>
      {{ pageTitle }}
    </template>
    <template #content>
      <StudentProfile :profile="profile" />
      <div v-if="isElligible">
        <button class="btn btn-primary"  @click="redirectToCreate">
          Check In
        </button>
        <button class="btn btn-secondary" @click="redirectToSummary">
          Visit Summary
        </button>
      </div>
      <div v-else>
        <div class="alert alert-danger" role="alert">
          <i class="bi bi-exclamation-octagon-fill"></i> You are not
          Instructional Center elligible.
        </div>
        <p>
          Please contact Director of the Instructional Center
          <a href="mailto:therese@uw.edu">therese@uw.edu</a> for assistance.
        </p>
      </div>
    </template>
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
      isElligible: false,
      persMsg: window.persistent_msgs || [],
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
    redirectToCreate() {
      this.$router.push("/create");
    },
    redirectToSummary() {
      this.$router.push("/summary");
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
      this.isElligible = newValue.ic_elligible;
    },
  },
};
</script>
