<template>
  <div class="container-xl">
    <div class="px-3">
      <header
        class="d-flex justify-content-between align-items-center pb-3 my-4 border-bottom"
      >
        <div class="h4 flex-fill">
          <i class="bi bi-box-fill me-2 text-purple"></i>
          <a href="/" class="text-reset text-decoration-none">{{ appName }}</a>
        </div>
      </header>

      <main>
        <h1>
          <slot name="title">
            {{ pageTitle }}
          </slot>
        </h1>

        <slot name="description" />

        <slot name="content" />
      </main>

      <footer class="mb-2 ps-3 text-muted fixed-bottom">
        Copyright &copy; {{ new Date().getFullYear() }} University of Washington
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  name: "DefaultLayout",
  components: {},
  props: {
    pageTitle: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      // minimum application setup overrides
      appName: "Compass Visits",
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
