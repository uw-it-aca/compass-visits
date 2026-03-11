import { defineStore } from "pinia";
import { getStudentProfile } from "@/utils/data";

export const useVisitStore = defineStore("visit", {
  state: () => {
    return {
      getStudentProfile,
      studentProfile: {},
    };
  },
  getters: {
    totalMinutes: (state) => {
      if (state.studentProfile.data) {
        return Math.round(state.studentProfile.data.total_minutes);
      }
      return 0;
    },
    visitDurationString: (state) => {
      if (state.studentProfile.data && state.studentProfile.data.visit) {
        const duration = state.studentProfile.data.visit.active_minutes || 0;
        const hours = Math.floor(duration / 60);
        const minutes = duration % 60;
        return `${hours}h ${minutes}m`;
      }
      return "0h 0m";
    }
  },
  actions: {
    fetchStudentProfile() {
      if (!Object.prototype.hasOwnProperty.call(this.studentProfile, "request")) {
        this.studentProfile = {
          request: this.getStudentProfile().then((response) => {
            this.studentProfile.data = response;
          }),
        };
      }
      return this.studentProfile.request;
    },
  },
});
