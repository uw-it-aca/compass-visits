// verify.vue

<template>
  <DefaultLayout :page-title="pageTitle">
    <template #title>
      {{ pageTitle }}
    </template>
    <template #content>
      <p>Create Visit Page</p>
      <h3>Program Area<span style="color: red">*</span></h3>
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
      <h3>Tutoring Option<span style="color: red">*</span></h3>
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

      <h3>Course or Writing Service<span style="color: red">*</span></h3>
      <select
        v-model="selectedCourseOrWriting"
        class="form-select"
        aria-label="Select Course or Writing Service"
      >
        <option value="" disabled selected>
          Select a course or writing service
        </option>
        <optgroup label="Writing Services">
          <option
            v-for="writingService in visitOptionsStore.visitOptions
              .writing_services"
            :key="writingService.id"
            :value="writingService.id"
          >
            {{ writingService.name }}
          </option>
        </optgroup>
        <optgroup label="Courses">
          <option
            v-for="course in visitOptionsStore.visitOptions.courses"
            :key="course.id"
            :value="course.id"
          >
            {{ course.name }}
          </option>
        </optgroup>
      </select>
      <button
        class="btn btn-primary mt-3"
        :disabled="!allAreSelected"
        @click="createVisit"
      >
        Create Visit
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
