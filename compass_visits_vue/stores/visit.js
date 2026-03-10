import { defineStore } from "pinia";
import { getStudentProfile } from "@/utils/data";

export const useVisitStore = defineStore("visit", {
  state: () => (
    {
      _student_profile: {},

    }
  ),
  getters: {
    studentProfile(state) {
      if (
        !Object.prototype.hasOwnProperty.call(this._student_profile, "request")
      ) {
        this._student_profile.request = getStudentProfile().then(
          (response) => {
            this._student_profile.data = response;
          }
        );
      }
      return this._student_profile.data;
    },
  },
  actions: {},
});
