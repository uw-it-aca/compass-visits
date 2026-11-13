import { describe, expect, it } from "vitest";
import { mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";

import StudentProfile from "@/components/student-profile.vue";
import { useVisitStore } from "@/stores/visit";

describe("StudentProfile", () => {
  it("shows a placeholder when profile photo is missing", async () => {
    const pinia = createPinia();
    setActivePinia(pinia);
    const visitStore = useVisitStore();

    visitStore.studentProfile = {
      data: {
        student_name: "Test Student",
        student_number: "1234567",
        total_minutes: 90,
        photo: null,
      },
      request: Promise.resolve(),
    };

    const wrapper = mount(StudentProfile, {
      global: {
        plugins: [pinia],
      },
    });

    await Promise.resolve();

    expect(wrapper.find(".profile-photo-placeholder").exists()).toBe(true);
    expect(wrapper.find("img").exists()).toBe(false);
    expect(wrapper.text()).toContain("Test Student");
  });

  it("shows 0.00 total hours when total minutes is missing", async () => {
    const pinia = createPinia();
    setActivePinia(pinia);
    const visitStore = useVisitStore();

    visitStore.studentProfile = {
      data: {
        student_name: "No Minutes Student",
        student_number: "7654321",
        photo: null,
      },
      request: Promise.resolve(),
    };

    const wrapper = mount(StudentProfile, {
      global: {
        plugins: [pinia],
      },
    });

    await Promise.resolve();

    expect(wrapper.text()).toContain("Total Hours:");
    expect(wrapper.text()).toContain("0.00");
  });
});
