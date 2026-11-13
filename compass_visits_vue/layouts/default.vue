<template>
  <STopbarBlanco :app-name="appName" :app-root-url="appRootUrl">
    <template #settings>
      <SUser
        :user-netid="userNetid"
        :photo-url="userPhotoUrl"
        :mode="'dynamic'"
      >
        <ul class="list-unstyled">
          <li>{{ userPreferred }}</li>
          <li>{{ userNetid }}</li>
          <li v-if="userStudentNumber">{{ userStudentNumber }}</li>
        </ul>

        <BButton v-b-toggle.offcanvas-border>About {{ appName }}</BButton>
        <template #action>
          <a :href="signOutUrl" class="link-quiet-danger"
            ><i class="bi bi-x-circle me-1"></i>Sign out now</a
          >
        </template>
      </SUser>
      <SColorMode color-class="text-body" class="ms-3"></SColorMode>
    </template>

    <template #main>
      <h1
        :class="[
          'fw-bold ff-encode-sans my-4',
          { 'visually-hidden': hideTitle },
        ]"
      >
        {{ pageTitle }}
      </h1>

      <div class="">
        <slot name="content" />
      </div>

      <div
        v-if="$slots.action"
        :class="['fixed-bottom', bgClass]"
        style="box-shadow: 0 -0.25rem 0.4rem rgba(0, 0, 0, 0.15)"
      >
        <div class="d-flex flex-column row-gap-2 container mb-0 p-3">
          <slot name="action" />
        </div>
      </div>
    </template>
  </STopbarBlanco>

  <BOffcanvas
    id="offcanvas-border"
    class="w-100"
    :header-class="bgClass"
    :body-class="bgClass"
    placement="bottom-start"
    style="box-shadow: 0 -0.25rem 0.4rem rgba(0, 0, 0, 0.15)"
    no-backdrop
  >
    <div class="container">
      <h2>{{ appName }}</h2>
      <p>
        Kiosk lets students check in for visits to campus services, such as
        tutoring and writing support. Sign in with your UW NetID, confirm your
        details, and choose the type of visit you need. Your visit is recorded
        in Compass so staff can see who has arrived and follow up afterward.
      </p>

      <ul class="list-inline sol-middot-list m-0">
        <li class="list-inline-item">
          <a
            href="https://www.washington.edu/accessibility/"
            target="_blank"
            rel="noopener"
            class="link-body-emphasis"
            >Accessibility</a
          >
        </li>
        <li class="list-inline-item">
          <a
            href="https://www.washington.edu/online/privacy/"
            target="_blank"
            rel="noopener"
            class="link-body-emphasis"
            >Privacy</a
          >
        </li>
        <li class="list-inline-item">
          <a
            href="https://www.washington.edu/online/terms/"
            target="_blank"
            rel="noopener"
            class="link-body-emphasis"
            >Terms</a
          >
        </li>
      </ul>
      <div class="">
        Copyright &copy; {{ currentYear }} University of Washington
      </div>
    </div>
  </BOffcanvas>
</template>

<script>
  import { STopbarBlanco, SUser, SColorMode } from "solstice-vue";
  import { useVisitStore } from "@/stores/visit";
  import { BButton, BOffcanvas, vBToggle } from "bootstrap-vue-next";
  import { ref, onMounted, onUnmounted } from "vue";

  export default {
    name: "DefaultLayout",
    components: { STopbarBlanco, SUser, SColorMode, BButton, BOffcanvas },
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

      // Track Bootstrap's color mode (data-bs-theme on <html>) reactively so
      // backgrounds can switch: bg-body-tertiary (dark) / bg-body (light).
      const colorMode = ref(
        document.documentElement.getAttribute("data-bs-theme") || "light",
      );
      let observer = null;

      onMounted(() => {
        observer = new MutationObserver(() => {
          colorMode.value =
            document.documentElement.getAttribute("data-bs-theme") || "light";
        });
        observer.observe(document.documentElement, {
          attributes: true,
          attributeFilter: ["data-bs-theme"],
        });
      });

      onUnmounted(() => {
        if (observer) {
          observer.disconnect();
          observer = null;
        }
      });

      return { visitStore, colorMode };
    },
    data() {
      return {
        // minimum application setup overrides
        appName: "Kiosk",
        appRootUrl: "/",
        // automatically set year
        currentYear: new Date().getFullYear(),
        // sign out url from Django template
        signOutUrl: document.body.getAttribute("data-logout-url") || "/",
      };
    },
    computed: {
      bgClass() {
        return this.colorMode === "dark" ? "bg-body-tertiary" : "bg-body";
      },
      userNetid() {
        return this.visitStore.studentProfile?.data?.netid || "";
      },
      userPhotoUrl() {
        const photo = this.visitStore.studentProfile?.data?.photo;
        // undefined makes Vue fall back to SUser's default photoUrl
        return photo ? `data:image/png;base64,${photo}` : undefined;
      },
      userStudentNumber() {
        return this.visitStore.studentProfile?.data?.student_number || "";
      },
      userOfficial() {
        return this.visitStore.studentProfile?.data?.official_name || "";
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
  /*
   * The responsive-offcanvas base rule (.offcanvas { position: static;
   * z-index: auto; transform: none !important; }) strips positioning from
   * our About offcanvas. Without a stacking context it renders in normal
   * flow and gets covered by the .fixed-bottom #action bar (z-index 1030)
   * on pages that use the action slot (e.g. verify.vue). Force it back to a
   * fixed overlay above that bar and restore the slide transition.
   */
  #offcanvas-border.offcanvas {
    position: fixed !important;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 1046 !important; /* above .fixed-bottom (1030) and bs backdrop (1040) */
    height: 50vh !important;
    width: 100% !important;
    background-color: var(--bs-body-bg) !important;
    transition: transform 0.45s cubic-bezier(0.22, 0.61, 0.36, 1) !important;
    will-change: transform;
  }

  #offcanvas-border.offcanvas:not(.show) {
    transform: translateY(100%) translateZ(0) !important;
  }

  #offcanvas-border.offcanvas.showing,
  #offcanvas-border.offcanvas.show:not(.hiding) {
    transform: translateY(0) translateZ(0) !important;
  }

  .offcanvas-backdrop {
    transition: opacity 0.4s ease;
  }
</style>
