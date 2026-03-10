// home.vue

<template>
  <DefaultLayout :page-title="pageTitle">
    <template #title>
      {{ pageTitle }}
    </template>
    <template #content>

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
  data() {
    return {
      pageTitle: "Home",
      visitStore: useVisitStore(),
      profile: null,
    };
  },
  computed: {
    studentProfile() {
      return this.visitStore.studentProfile;
    },
  },
  methods: {
    redirectToVerify() {
      console.log('verify')
      this.$router.push("/verify");
    },
    redirectToCheckout() {
      console.log('checkout')
      this.$router.push("/checkout");
    },
  },
  watch: {
      visitStore: {
        handler(newValue) {
          // Redirect students with in-progress visit to verificatin or
          // confirmation page based on the current state of the visit
          console.log('visit store changed', newValue)
          console.log('visit store changed student profile', newValue.data)


          if("data" in newValue && "current_state" in newValue.data){
            console.log('has state')
            if ( newValue.data.current_state === "pending_verification") {
              this.redirectToVerify();
            } else if (newValue.data.current_state === "active") {
              this.redirectToCheckout();
            }
          }
        },
        deep: true,
      },
  }
};
</script>
