// home.vue

<template>
  <DefaultLayout :page-title="pageTitle">
    <!-- page content -->
    <template #title>
      {{ pageTitle }}
    </template>

    <template #description>
      <div class="p-0 col-md-8 lead">
        <p>
          <a href="https://github.com/uw-it-aca/django-vue">django-vue</a>
          is a highly-opinionated template repository created and used by
          Coordination &amp; Design (DC) and Student &amp; Educational
          Technology Services (SETS) to make our build processes consistent and
          repeatable through established patterns across a containerized CICD
          infrastructure.
        </p>
      </div>
    </template>

    <template #content>
      <div class="row">
        <div class="col-md-6">
          <h2>Requirements</h2>
          <p>Download the following:</p>
          <ul>
            <li>
              <a href="https://www.docker.com" target="_blank">Docker </a>
            </li>
            <li>
              <a href="https://nodejs.org/en" target="_blank">Node</a>
            </li>
          </ul>

          <h2>Development</h2>
          <p>
            What's included? This template repository is intended to start you
            off with a supported development stack.
          </p>
          <ul>
            <li>
              <a href="https://www.djangoproject.com/" target="_blank"
                >Django</a
              >
              (back-end)
            </li>
            <li>
              <a href="https://vuejs.org/" target="_blank">Vue</a> (front-end)
            </li>
          </ul>

          <h2>Design</h2>
          <p>
            We use the
            <a href="https://test.solstice.uw.edu">Solstice Design System</a> as
            the basis of our design.
          </p>
        </div>
        <div class="col-md-6">
          <h2>Testing</h2>
          <ul>
            <li>
              <a
                href="https://docs.djangoproject.com/en/5.2/topics/testing/tools/#testing-tools"
                target="_blank"
                >Django Test Client</a
              >
            </li>
            <li>
              <a href="https://test-utils.vuejs.org/" target="_blank"
                >Vue Test Utils</a
              >
              with
              <a href="https://vitest.dev/" target="_blank">Vitest</a> (test
              runner)
            </li>
          </ul>

          <h2>Linting (code quality)</h2>
          <ul>
            <li>
              <a
                href="https://pycodestyle.pycqa.org/en/latest/index.html"
                target="_blank"
                >Pycodestyle</a
              >
              or
              <a
                href="https://black.readthedocs.io/en/stable/index.html"
                target="_blank"
                >Black</a
              >
              (Python)
            </li>
            <li>
              <a href="https://eslint.vuejs.org/" target="_blank"
                >eslint-plugin-vue</a
              >
              (Javascript)
            </li>
            <li>
              <a
                href="https://github.com/ota-meshi/stylelint-config-recommended-vue"
                target="_blank"
                >stylelint-config-recommended-vue</a
              >
              (CSS)
            </li>
          </ul>
        </div>

        <div class="col-md-8">
          <hr class="my-5 w-50" />

          <h2>Get Started</h2>
          <p>
            View the <a href="/customize">customizing your app</a> page to learn
            how to get started.
          </p>
        </div>
      </div>
    </template>
  </DefaultLayout>
</template>

<script>
import DefaultLayout from "@/layouts/default.vue";

export default {
  name: "PagesHome",
  components: { DefaultLayout },
  data() {
    return { pageTitle: "Getting started" };
  },
  methods: {},
};
</script>
