import { defineStore } from "pinia";
import { getStudentProfile, updateVisit } from "@/utils/data";

export const useVisitStore = defineStore("visit", {
  state: () => {
    return {
      getStudentProfile,
      studentProfile: {},
      studentVisit: {},
    };
  },
  getters: {
    totalMinutes: (state) => {
      if (state.studentProfile.data) {
        return Math.round(state.studentProfile.data.total_minutes);
      }
      return 0;
    },
    studentHasVisit: (state) => {
      return Object.keys(state.studentVisit).length > 0;
    },
    visitDurationString: (state) => {
      if (state.studentHasVisit) {
        const duration = state.studentVisit.active_minutes || 0;
        const hours = Math.floor(duration / 60);
        const minutes = duration % 60;
        return `${hours}h ${minutes}m`;
      }
      return "0h 0m";
    },
  },
  actions: {
    fetchStudentProfile() {
      if (
        !Object.prototype.hasOwnProperty.call(this.studentProfile, "request")
      ) {
        this.studentProfile = {
          request: this.getStudentProfile().then((response) => {
            this.studentProfile.data = response;
            this.studentVisit = response.visit || {};
          }),
        };
      }
      return this.studentProfile.request;
    },
    handleCheckout() {
      if (this.studentHasVisit) {
        return updateVisit(this.studentVisit.id, { checkout: true }).then(
          () => {
            this.studentVisit = {};
            this.studentProfile = {};
            this.fetchStudentProfile();
          }
        );
      }
      return Promise.resolve();
    },
  },
});
