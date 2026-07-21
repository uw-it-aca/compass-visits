<template>
  <div class="container">
    <div class="p-3">
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
      <BButton v-b-toggle.offcanvas-border>About {{ appName }}</BButton>
      <BOffcanvas
        id="offcanvas-border"
        :title="appName"
        class="bg-body rounded-top-5"
        placement="bottom-start"
        shadow="lg"
      >
        <div class="p-0">
          <p>
            Cras mattis consectetur purus sit amet fermentum. Cras justo odio,
            dapibus ac facilisis in, egestas eget quam. Morbi leo risus, porta
            ac consectetur ac, vestibulum at eros.
          </p>
          <p>&copy; Copyright 2026 Univeristy of Washington</p>
          <ul>
            <li>Accessiblity</li>
            <li>Privacy Policy</li>
            <li>Terms</li>
          </ul>
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
    <div class="p-3">
      <slot name="content" />
    </div>

    <div
      v-if="$slots.action"
      class="fixed-bottom bg-body "
      style="box-shadow: 0 -0.25rem 0.4rem rgba(0, 0, 0, 0.15)"
    >
      <div class="container d-flex flex-column row-gap-2 mb-0 p-3">
        <slot name="action" />
      </div>
    </div>
  </div>
</template>

<script>
  import { SProfile, SColorMode } from "solstice-vue";
  import { useVisitStore } from "@/stores/visit";
  import { BButton, BOffcanvas, vBToggle } from "bootstrap-vue-next";

  export default {
    name: "DefaultLayout",
    components: { SProfile, SColorMode, BButton, BOffcanvas },
    directives: { "b-toggle": vBToggle },
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

  .pb-action {
    padding-bottom: 8rem;
  }
</style>

<style>
  .offcanvas.offcanvas-bottom-start {
    height: 50vh;
    transition: transform 0.45s cubic-bezier(0.22, 0.61, 0.36, 1);
    will-change: transform;
  }

  .offcanvas-backdrop {
    transition: opacity 0.4s ease;
  }

  .offcanvas.showing,
  .offcanvas.show:not(.hiding) {
    transform: translateY(0) translateZ(0);
  }

  .offcanvas.offcanvas-bottom-start:not(.show) {
    transform: translateY(100%) translateZ(0);
  }
</style>
