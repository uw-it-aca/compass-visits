<template>
  <div>
    <SProfile
      :variant="'flyout'"
      :user-netid="userNetid"
      :user-official-name="userOfficial"
      :user-preferred-name="userPreferred"
      :profile-url="'https://identity.uw.edu'"
      :signout-url="signOutUrl"
      class="text-dark"
    ></SProfile>
    <SColorMode color-class="text-body" class="ms-3"></SColorMode>
  </div>

  <h1
    :class="[
      'fs-5 ff-open-sans m-2 py-1 text-center',
      { 'visually-hidden': hideTitle },
    ]"
  >
    {{ pageTitle }}
  </h1>
  <div>
    <slot name="content" />
  </div>

  <div v-if="$slots.action" class="fixed-bottom border border-danger d-flex flex-column row-gap-2 mb-0 p-2">
    <slot name="action" />
  </div>
</template>

<script>
  import { SProfile, SColorMode } from "solstice-vue";
  import { useVisitStore } from "@/stores/visit";

  export default {
    name: "DefaultLayout",
    components: { SProfile, SColorMode },
    props: {
      pageTitle: {
        type: String,
        required: true,
      },
      hideTitle: {
        type: Boolean,
        default: false,
      },
    },
    setup() {
      const visitStore = useVisitStore();
      return { visitStore };
    },
    data() {
      return {
        // minimum application setup overrides
        appName: "IC Visits",
        appRootUrl: "/",
        // automatically set year
        currentYear: new Date().getFullYear(),
        // sign out url from Django template
        signOutUrl: document.body.getAttribute("data-logout-url") || "/",
      };
    },
    computed: {
      userNetid() {
        return this.visitStore.studentProfile?.data?.netid || "";
      },
      userOfficial() {
        return this.visitStore.studentProfile?.data?.student_name || "";
      },
      userPreferred() {
        return this.visitStore.studentProfile?.data?.preferred_name || "";
      },
    },
    created: function () {
      // constructs page title in the following format "Page Title - AppName"
      document.title = this.pageTitle + " - " + this.appName;
      // ensure profile data is loaded for the header
      this.visitStore.fetchStudentProfile();
    },
    watch: {
      pageTitle(newVal) {
        document.title = newVal + " - " + this.appName;
      },
    },
  };
</script>

<style scoped>
:deep(.text-white) {
  color: var(--bs-body-color) !important;
}
</style>
