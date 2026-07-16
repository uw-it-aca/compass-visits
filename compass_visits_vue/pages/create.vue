// verify.vue

<template>
  <DefaultLayout :page-title="pageTitle">
    <template #content>
      <div class="d-flex flex-column" style="min-height: calc(100vh - 265px)">
        <h2 class="fs-6 fw-bold ff-open-sans mb-2">
          Program Area<span style="color: red">*</span>
        </h2>
        <div class="pb-4">
          <select
            v-model="selectedProgramArea"
            class="form-select"
            aria-label="Select Program Area"
          >
            <option value="" disabled selected>Select a program area</option>
            <option
              v-for="programArea in visitOptionsStore.visitOptions
                .program_areas"
              :key="programArea.id"
              :value="programArea.id"
            >
              {{ programArea.name }}
            </option>
          </select>
        </div>
        <h2 class="fs-6 fw-bold ff-open-sans mb-2">
          Tutoring Option<span style="color: red">*</span>
        </h2>
        <div class="pb-4">
          <select
            v-model="selectedTutoringOption"
            class="form-select"
            aria-label="Select Tutoring Option"
          >
            <option value="" disabled selected>Select a tutoring option</option>
            <option
              v-for="tutoringOption in visitOptionsStore.visitOptions
                .tutoring_options"
              :key="tutoringOption.id"
              :value="tutoringOption.id"
            >
              {{ tutoringOption.name }}
            </option>
          </select>
        </div>
        <h2 class="fs-6 fw-bold ff-open-sans mb-2">
          Course or Writing Service<span style="color: red">*</span>
        </h2>
        <div class="pb-4">
          <select
            v-model="selectedCourseOrWriting"
            class="form-select"
            aria-label="Select Course or Writing Service"
          >
            <option value="" disabled selected>
              Select a course or writing service
            </option>
            <optgroup label="Courses">
              <option
                v-for="course in visitOptionsStore.visitOptions.courses"
                :key="course.id"
                :value="course.id"
              >
                {{ course.name }}
              </option>
            </optgroup>

            <optgroup v-if="selectedProgramArea === 7" label="Writing Services">
              <option
                v-for="writingService in visitOptionsStore.visitOptions
                  .writing_services"
                :key="writingService.id"
                :value="writingService.id"
              >
                {{ writingService.name }}
              </option>
            </optgroup>
          </select>
        </div>
      </div>
    </template>

    <template #action>
      <button
        class="btn btn-primary btn-lg mb-3"
        :disabled="!allAreSelected"
        @click="createVisit"
      >
        Confirm
      </button>
      <button class="btn btn-outline-danger btn-lg mb-2" @click="cancelVisit">
        Cancel
      </button>
    </template>
  </DefaultLayout>
</template>

<script>
  import DefaultLayout from "@/layouts/default.vue";
  import { useVisitOptionsStore } from "../stores/visit-options";
  import { useVisitStore } from "@/stores/visit";

  export default {
    name: "Create",
    components: { DefaultLayout },
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
