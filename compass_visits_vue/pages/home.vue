// home.vue

<template>
  <DefaultLayout :page-title="pageTitle" hide-title>
    <template #content>
      <div class="d-flex flex-column" style="min-height: calc(100vh - 240px)">
        <div class="mt-auto pb-2">
          <StudentProfile :profile="profile" />
        </div>
        <div v-if="isElligible" class="row mt-auto mx-0 text-center">
          <button class="btn btn-secondary btn-lg mb-3" @click="redirectToSummary">Summary</button>
          <button class="btn btn-primary btn-lg mb-2" @click="redirectToCreate">Check In</button>
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
      profile: null,
      isElligible: false,
      persMsg: window.persistent_msgs || [],
    };
  },
  computed: {
    pageTitle() {
      return this.profile?.student_name || "Home";
    },
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