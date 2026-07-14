// home.vue

<template>
  <DefaultLayout>
    <template #content>
      <div v-if="profileError" class="alert alert-danger" role="alert">
        <i class="bi bi-exclamation-octagon-fill"></i>
        {{ profileError }}
      </div>
      <StudentProfile :profile="profile" />
      <div v-if="isElligible && !profileError">
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
      profileError: null,
      isElligible: false,
      persMsg: window.persistent_msgs || [],
    };
  },
  created() {
    this.loadStudentProfile();
  },
  methods: {
    redirectToVerify() {
      this.$router.push({ name: "verify" });
    },
    redirectToCheckout() {
      this.$router.push({ name: "checkout" });
    },
    redirectToCreate() {
      this.$router.push({ name: "create" });
    },
    redirectToSummary() {
      this.$router.push({ name: "summary" });
    },
    loadStudentProfile() {
      this.visitStore.fetchStudentProfile().then(() => {
        this.profile = this.visitStore.studentProfile.data;
        this.profileError = null;
      }).catch((error) => {
        this.profile = null;
        this.profileError =
          error?.data?.error || "Unable to load your profile. Please try again.";
      });
    },
  },
  watch: {
    profile(newValue) {
      if (!newValue || typeof newValue !== "object") {
        this.isElligible = false;
        return;
      }

      if ("current_state" in newValue) {
        if (newValue.current_state === "pending_verification") {
          this.redirectToVerify();
        } else if (newValue.current_state === "active") {
          this.redirectToCheckout();
        }
      }
      this.isElligible = Boolean(newValue.ic_elligible);
    },
  },
};
</script>
