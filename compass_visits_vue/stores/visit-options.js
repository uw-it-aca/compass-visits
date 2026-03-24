import { defineStore } from "pinia";
import { getVisitOptions } from "@/utils/data";

export const useVisitOptionsStore = defineStore("visitOptions", {
  state: () => {
    return {
      visitOptions: {},
    };
  },
  getters: {

  },
  actions: {
    fetchVisitOptions() {
      if (!Object.keys(this.visitOptions).length) {
        return getVisitOptions().then((response) => {
          this.visitOptions = response;
        });
      }
      return Promise.resolve(this.visitOptions);
    },
  },
});
