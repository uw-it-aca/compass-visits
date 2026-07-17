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
    <BButton v-b-toggle.offcanvas-border>Toggle Offcanvas</BButton>
    <BOffcanvas
      id="offcanvas-border"
      title="Offcanvas"
      class="bg-primary"
      placement="bottom-start"
    >
      <div class="px-3 py-2">
        <p>
          Cras mattis consectetur purus sit amet fermentum. Cras justo odio,
          dapibus ac facilisis in, egestas eget quam. Morbi leo risus, porta ac
          consectetur ac, vestibulum at eros.
        </p>
        <BImg src="https://picsum.photos/500/500/?image=54" fluid thumbnail />
      </div>
    </BOffcanvas>
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

  <div
    v-if="$slots.action"
    class="fixed-bottom border-danger d-flex flex-column row-gap-2 mb-0 border p-2"
  >
    <slot name="action" />
  </div>
</template>

<script>
  import { ref } from "vue";
  import { SProfile, SColorMode } from "solstice-vue";
  import { useVisitStore } from "@/stores/visit";
  import { BButton, BOffcanvas, vBToggle } from "bootstrap-vue-next";

  export default {
    name: "DefaultLayout",
    components: { SProfile, SColorMode, BButton, BOffcanvas },
    directives: { 'b-toggle': vBToggle },
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
