// home.vue

<template>
  <DefaultLayout :page-title="pageTitle" hide-title>
    <template #content>
      <div class="d-flex flex-column" style="">
        <div class="mt-auto pb-2">
          <StudentProfile :profile="profile" />
        </div>

        <div v-if="profile && !isElligible" class="text-center">
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

    <template v-if="profile && isElligible" #action>
      <BButton variant="secondary" size="lg" @click="redirectToSummary">
        Summary
      </BButton>
      <BButton variant="primary" size="lg" @click="redirectToCreate">
        Check In
      </BButton>
    </template>
  </DefaultLayout>
</template>

<script>
  import DefaultLayout from "@/layouts/default.vue";
  import StudentProfile from "@/components/student-profile.vue";
  import { useVisitStore } from "@/stores/visit";
  import { BButton } from "bootstrap-vue-next";

  export default {
    name: "PagesHome",
    components: { DefaultLayout, BButton, StudentProfile },
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
