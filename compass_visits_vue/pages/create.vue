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
            :options="programAreaOptions"
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
                {{ courseOrWritingPlaceholder }}
              </BFormSelectOption>
            </template>
            <BFormSelectOptionGroup
              v-if="!noCourseOptions"
              :options="visitOptionsStore.visitOptions.courses"
              label="Courses"
              text-field="name"
              value-field="id"
            />
            <BFormSelectOptionGroup
              v-if="isWritingProgramArea || noCourseOptions"
              :options="visitOptionsStore.visitOptions.writing_services"
              label="Writing Services"
              text-field="name"
              value-field="id"
            />
          </BFormSelect>
          <p
            v-if="noCourseOptions && noWritingServiceOptions"
            class="text-danger mt-2 mb-0"
          >
            No writing services are available right now.
          </p>
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
          !this.noWritingServiceOptions &&
          this.selectedProgramArea &&
          this.selectedTutoringOption &&
          this.selectedCourseOrWriting
        );
      },
      noCourseOptions() {
        return (this.visitOptionsStore.visitOptions.courses || []).length === 0;
      },
      noWritingServiceOptions() {
        return (
          this.noCourseOptions &&
          (this.visitOptionsStore.visitOptions.writing_services || []).length === 0
        );
      },
      writingProgramAreaOption() {
        const programAreas = this.visitOptionsStore.visitOptions.program_areas || [];
        const writingById = programAreas.find((area) => String(area.id) === "7");
        if (writingById) {
          return writingById;
        }
        return programAreas.find((area) =>
          String(area.name || "").toLowerCase().includes("writing"),
        );
      },
      programAreaOptions() {
        if (this.noCourseOptions) {
          return this.writingProgramAreaOption ? [this.writingProgramAreaOption] : [];
        }
        return this.visitOptionsStore.visitOptions.program_areas;
      },
      isWritingProgramArea() {
        if (this.noCourseOptions) {
          return true;
        }
        if (!this.writingProgramAreaOption) {
          return false;
        }
        return (
          String(this.selectedProgramArea) ===
          String(this.writingProgramAreaOption.id)
        );
      },
      courseOrWritingPlaceholder() {
        if (this.noCourseOptions) {
          return "Select a writing service";
        }
        return "Select a course or writing service";
      },
      selectedCourse() {
        if (this.noCourseOptions || this.isWritingProgramArea) {
          return undefined;
        }
        return (this.visitOptionsStore.visitOptions.courses || []).find(
          (course) => String(course.id) === String(this.selectedCourseOrWriting),
        );
      },
      selectedWritingService() {
        if (!this.noCourseOptions && !this.isWritingProgramArea) {
          return undefined;
        }
        return (this.visitOptionsStore.visitOptions.writing_services || []).find(
          (service) =>
            String(service.id) === String(this.selectedCourseOrWriting),
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
    watch: {
      noCourseOptions: {
        immediate: true,
        handler(isNoCourseOptions) {
          if (!isNoCourseOptions) {
            return;
          }

          if (this.writingProgramAreaOption) {
            this.selectedProgramArea = this.writingProgramAreaOption.id;
          }

          if (
            this.selectedCourseOrWriting &&
            !this.selectedWritingService
          ) {
            this.selectedCourseOrWriting = "";
          }
        },
      },
      selectedProgramArea() {
        if (this.noCourseOptions && this.writingProgramAreaOption) {
          this.selectedProgramArea = this.writingProgramAreaOption.id;
        }
      },
    },
  };
</script>
