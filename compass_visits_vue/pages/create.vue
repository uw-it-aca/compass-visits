// verify.vue

<template>
  <DefaultLayout :page-title="pageTitle">
    <template #content>
      <div class="d-flex flex-column">
        <h2 class="fs-6 fw-bold ff-open-sans mb-2">
          Program Area<span style="color: red">*</span>
        </h2>
        <div class="pb-4">
          <BFormSelect
            v-model="selectedProgramArea"
            :options="visitOptionsStore.visitOptions.program_areas"
            text-field="name"
            value-field="id"
            aria-label="Select Program Area"
          >
            <template #first>
              <BFormSelectOption value="" disabled>
                Select a program area
              </BFormSelectOption>
            </template>
          </BFormSelect>
        </div>
        <h2 class="fs-6 fw-bold ff-open-sans mb-2">
          Tutoring Option<span style="color: red">*</span>
        </h2>
        <div class="pb-4">
          <BFormSelect
            v-model="selectedTutoringOption"
            :options="visitOptionsStore.visitOptions.tutoring_options"
            text-field="name"
            value-field="id"
            aria-label="Select Tutoring Option"
          >
            <template #first>
              <BFormSelectOption value="" disabled>
                Select a tutoring option
              </BFormSelectOption>
            </template>
          </BFormSelect>
        </div>
        <h2 class="fs-6 fw-bold ff-open-sans mb-2">
          Course or Writing Service<span style="color: red">*</span>
        </h2>
        <div class="pb-4">
          <BFormSelect
            v-model="selectedCourseOrWriting"
            aria-label="Select Course or Writing Service"
          >
            <template #first>
              <BFormSelectOption value="" disabled>
                Select a course or writing service
              </BFormSelectOption>
            </template>
            <BFormSelectOptionGroup
              :options="visitOptionsStore.visitOptions.courses"
              label="Courses"
              text-field="name"
              value-field="id"
            />
            <BFormSelectOptionGroup
              v-if="selectedProgramArea === 7"
              :options="visitOptionsStore.visitOptions.writing_services"
              label="Writing Services"
              text-field="name"
              value-field="id"
            />
          </BFormSelect>
        </div>
      </div>
    </template>

    <template #action>
      <BButton
        variant="primary"
        size="lg"
        :disabled="!allAreSelected"
        @click="createVisit"
      >
        Confirm
      </BButton>
      <BButton variant="outline-danger" size="lg" @click="cancelVisit">
        Cancel
      </BButton>
    </template>
  </DefaultLayout>
</template>

<script>
  import DefaultLayout from "@/layouts/default.vue";
  import { useVisitOptionsStore } from "@/stores/visit-options";
  import { useVisitStore } from "@/stores/visit";
  import {
    BButton,
    BFormSelect,
    BFormSelectOption,
    BFormSelectOptionGroup,
  } from "bootstrap-vue-next";

  export default {
    name: "Create",
    components: {
      DefaultLayout,
      BButton,
      BFormSelect,
      BFormSelectOption,
      BFormSelectOptionGroup,
    },
    setup() {
      const visitOptionsStore = useVisitOptionsStore();
      const visitStore = useVisitStore();
      visitOptionsStore.fetchVisitOptions();
      return { visitOptionsStore, visitStore };
    },
    props: {
      switch: {
        type: Boolean,
        default: false,
      },
    },
    data() {
      return {
        selectedProgramArea: "",
        selectedTutoringOption: "",
        selectedCourseOrWriting: "",
        createError: null,
        isSubmitting: false,
      };
    },
    computed: {
      allAreSelected() {
        return (
          this.selectedProgramArea &&
          this.selectedTutoringOption &&
          this.selectedCourseOrWriting
        );
      },
      selectedCourse() {
        return this.visitOptionsStore.visitOptions.courses.find(
          (course) => course.id === this.selectedCourseOrWriting,
        );
      },
      selectedWritingService() {
        return this.visitOptionsStore.visitOptions.writing_services.find(
          (service) => service.id === this.selectedCourseOrWriting,
        );
      },
      pageTitle() {
        return this.switch ? "Switch Session" : "Create Visit";
      },
    },
    methods: {
      async createVisit() {
        if (this.allAreSelected) {
          this.createError = null;
          this.isSubmitting = true;
          try {
            await this.visitStore.handleCreateVisit({
              program_area: this.selectedProgramArea,
              tutoring_option: this.selectedTutoringOption,
              course: this.selectedCourse ? this.selectedCourse.id : null,
              writing_service: this.selectedWritingService
                ? this.selectedWritingService.id
                : null,
            });
            if (this.switch) {
              this.$router.push({ name: "checkout" });
            } else {
              this.$router.push({ name: "verify" });
            }
          } catch (error) {
            this.createError =
              error?.data?.error ||
              "Unable to create your visit. Please review your selections and try again.";
          } finally {
            this.isSubmitting = false;
          }
        }
      },
      cancelVisit() {
        this.visitStore.deleteVisit().then(() => {
          this.profile = null;
          this.$router.push("/");
        });
      },
    },
    watch: {},
  };
</script>
