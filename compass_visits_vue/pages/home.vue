// home.vue

<template>
  <DefaultLayout>
    <template #content>
      <div
        v-if="isElligible"
        style="
          display: flex;
          align-items: center;
          justify-content: center;
          min-height: calc(100vh - 180px);
          padding-bottom: 180px;
        "
      >
        <StudentProfile :profile="profile" />
      </div>
      <div
        class="position-absolute bottom-0"
        v-if="isElligible"
      >
        <div class="row" style="width: 100%; max-width: 1200px">
          <button
            class="btn btn-secondary btn-lg my-2"
            @click="redirectToSummary"
          >
            Summary
          </button>
          <button class="btn btn-primary btn-lg my-2" @click="redirectToCreate">
            Check In
          </button>
        </div>
      </div>
      <div v-else class="text-center">
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
