<template>

    <STopbar
    :app-name="appName"
    :app-root-url="appRootUrl"
    :page-title="pageTitle"
    :user-name="userNetid"
    :sign-out-url="signOutUrl"
    :topbar-class="'bg-spirit-purple'"
  >
    <!--<template #system>
      <div class="bg-deco-turquoise">
        <div class="container-xl text-center text-white p-2">
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Magnam,
          nostrum iste! Commodi magni natus provident mollitia. Illum officiis
          molestiae optio distinctio! Repellendus quod minima recusandae
          suscipit, natus hic atque ipsa.
        </div>
      </div>
    </template>-->
    <template #profile>
      <div class="d-flex justify-content-end">
        <SProfile
          :variant="'flyout'"
          :user-netid="userNetid"
          :user-official-name="userOfficial"
          :user-preferred-name="userPreferred"
          :profile-url="'https://identity.uw.edu'"
          :signout-url="signOutUrl"
        ></SProfile>
        <SColorMode color-class="text-white" class="ms-3"></SColorMode>
      </div>
    </template>
    <!--<template #navigation>
      <ul class="nav flex-column my-3">
        <li class="nav-item mb-1 bg-secondary bg-opacity-10 rounded-3">
          <a href="#" class="nav-link d-block px-3 py-2 text-body"
            ><i class="bi bi-house-door-fill me-3"></i>Home</a
          >
        </li>
        <li class="nav-item mb-1 rounded-3">
          <a href="#" class="nav-link text-body d-block px-3 py-2"
            ><i class="bi bi-mortarboard-fill me-3"></i>Academics</a
          >
        </li>
        <li class="nav-item mb-1rounded-3">
          <a href="#" class="nav-link text-body d-block px-3 py-2"
            ><i class="bi bi-pencil-square me-3"></i>Teaching</a
          >
        </li>
        <li class="nav-item rounded-3">
          <a href="#" class="nav-link text-body d-block px-3 py-2"
            ><i class="bi bi-credit-card me-3"></i>Accounts</a
          >
        </li>
        <li aria-hidden="true" class="nav-item my-2">
          <a
            href="#"
            class="nav-link disabled text-muted d-block p-0 internal-link"
            ><hr class="m-0 bg-light" />
            <span class="visually-hidden"> Navigation separator</span></a
          >
        </li>
        <li class="nav-item mb-1 rounded-3">
          <a href="#" class="nav-link text-body d-block px-3 py-2"
            ><i class="bi bi-calendar-check me-3"></i>Calendar</a
          >
        </li>
        <li class="nav-item rounded-3">
          <a href="#" class="nav-link text-dark d-block px-3 py-2"
            ><i class="bi bi-bookmark-fill me-3"></i>UW Resources</a
          >
        </li>
      </ul>
    </template>-->
    <template #bar></template>
    <template #main>
        <h1 class="fs-5 ff-open-sans m-2 py-1 text-center">
          {{ pageTitle }}
        </h1>
        <slot name="content" />
    </template>
    <template #footer></template>
  </STopbar>


</template>

<script>
  import { STopbar, SProfile, SColorMode } from "solstice-vue";

export default {
  name: "DefaultLayout",
  components: { STopbar, SProfile, SColorMode },
  props: {
    pageTitle: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      // minimum application setup overrides
      appName: "IC Visits",
      // automatically set year
      currentYear: new Date().getFullYear(),
    };
  },
  created: function () {
    // constructs page title in the following format "Page Title - AppName"
    document.title = this.pageTitle + " - " + this.appName;
  },
};
</script>
