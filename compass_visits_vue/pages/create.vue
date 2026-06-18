// verify.vue

<template>
  <DefaultLayout :page-title="pageTitle">
    <template #title>
      <div class="row mb-4 align-items-center">
        <div class="col-1">
          <a href="/"><i class="bi bi-arrow-left fs-3"></i></a>
        </div>
      </div>
    </template>
    <template #content>
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
            v-for="programArea in visitOptionsStore.visitOptions.program_areas"
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
      <div
        style="
          position: fixed;
          bottom: 92px;
          left: 16px;
          right: 16px;
          display: flex;
          background-color: white;
          justify-content: center;
        "
      >
        <div class="row" style="width: 100%; max-width: 1200px">
          <button
            class="btn btn-primary btn-lg my-2"
            :disabled="!allAreSelected"
            @click="createVisit"
          >
            Confirm
          </button>
        </div>
      </div>
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
  data() {
    return {
      pageTitle: "Create Visit",
      selectedProgramArea: "",
      selectedTutoringOption: "",
      selectedCourseOrWriting: "",
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
        (course) => course.id === this.selectedCourseOrWriting
      );
    },
    selectedWritingService() {
      return this.visitOptionsStore.visitOptions.writing_services.find(
        (service) => service.id === this.selectedCourseOrWriting
      );
    },
  },
  methods: {
    createVisit() {
      if (this.allAreSelected) {
        this.visitStore.handleCreateVisit({
          program_area: this.selectedProgramArea,
          tutoring_option: this.selectedTutoringOption,
          course: this.selectedCourse ? this.selectedCourse.id : null,
          writing_service: this.selectedWritingService
            ? this.selectedWritingService.id
            : null,
        });
        this.$router.push("/verify");
      }
    },
  },
  watch: {},
};
</script>
