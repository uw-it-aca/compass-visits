import { defineStore } from "pinia";
import { getVisitOptions } from "@/utils/data";

export const useVisitOptionsStore = defineStore("visitOptions", {
  state: () => {
    return {
      visitOptions: {},
      isLoading: false,
    };
  },
  getters: {

  },
  actions: {
    fetchVisitOptions() {
      if (!Object.keys(this.visitOptions).length) {
        this.isLoading = true;
        return getVisitOptions()
          .then((response) => {
            this.visitOptions = response;
          })
          .finally(() => {
            this.isLoading = false;
          });
      }
      return Promise.resolve(this.visitOptions);
    },
  },
});
