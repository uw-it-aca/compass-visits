import { defineStore } from "pinia";
import {
  getStudentProfile,
  updateVisit,
  createVisit,
  deleteVisit,
  getStudentVisits,
} from "@/utils/data";

export const useVisitStore = defineStore("visit", {
  state: () => {
    return {
      getStudentProfile,
      studentProfile: {},
      studentProfileError: null,
      studentProfileLoading: false,
      studentVisit: {},
      studentVisitList: {},
    };
  },
  getters: {
    totalMinutes: (state) => {
      if (state.studentProfile.data) {
        const totalMinutes = Number(state.studentProfile.data.total_minutes);
        return Number.isFinite(totalMinutes) ? Math.round(totalMinutes) : 0;
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
        this.studentProfileError = null;
        this.studentProfileLoading = true;
        this.studentProfile = {
          request: this.getStudentProfile()
            .then((response) => {
              this.studentProfile.data = response || {};
              this.studentVisit = response?.visit || {};
            })
            .catch((error) => {
              this.studentProfile.data = null;
              this.studentVisit = {};
              this.studentProfileError = error;
              throw error;
            })
            .finally(() => {
              this.studentProfileLoading = false;
            }),
        };
      }
      return this.studentProfile.request;
    },
    fetchStudentVisitList() {
      if (
        !Object.prototype.hasOwnProperty.call(this.studentVisitList, "request")
      ) {
        this.studentVisitList = {
          request: getStudentVisits().then((response) => {
            this.studentVisitList.data = response;
          }),
        };
      }
      return this.studentVisitList.request;
    },
    refreshStudentProfile() {
      this.studentProfile = {};
      this.studentProfileError = null;
      return this.fetchStudentProfile();
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
    handleCreateVisit(visitData) {
      return createVisit(visitData).then(() => {
        this.studentVisit = {};
      });
    },
    deleteVisit() {
      if (this.studentHasVisit) {
        return deleteVisit(this.studentVisit.id).then(() => {
          this.studentVisit = {};
          this.studentProfile = {};
          this.fetchStudentProfile();
        });
      }
      return Promise.resolve();
    },
  },
});
