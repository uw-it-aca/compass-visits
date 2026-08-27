import { beforeEach, describe, expect, it, vi } from "vitest";
import { shallowMount } from "@vue/test-utils";

let visitOptionsStoreMock;
let visitStoreMock;

vi.mock("@/stores/visit-options", () => ({
  useVisitOptionsStore: () => visitOptionsStoreMock,
}));

vi.mock("@/stores/visit", () => ({
  useVisitStore: () => visitStoreMock,
}));

import CreatePage from "@/pages/create.vue";

describe("Create page option handling", () => {
  beforeEach(() => {
    visitOptionsStoreMock = {
      visitOptions: {
        program_areas: [{ slug: "ic-writing-assistance", name: "Writing Assistance" }],
        tutoring_options: [{ slug: "drop-in", name: "Drop In" }],
        courses: [],
        writing_services: [{ id: 1, name: "Application" }],
      },
      isLoading: false,
      fetchVisitOptions: vi.fn(),
    };

    visitStoreMock = {
      handleCreateVisit: vi.fn(() => Promise.resolve()),
      deleteVisit: vi.fn(() => Promise.resolve()),
    };
  });

  it("prefills and restricts to writing program area when courses are unavailable", () => {
    const wrapper = shallowMount(CreatePage);

    expect(visitOptionsStoreMock.fetchVisitOptions).toHaveBeenCalledTimes(1);
    expect(wrapper.vm.noCourseOptions).toBe(true);
    expect(wrapper.vm.selectedProgramArea).toBe("ic-writing-assistance");
    expect(wrapper.vm.programAreaOptions).toEqual([
      { slug: "ic-writing-assistance", name: "Writing Assistance" },
    ]);
    expect(wrapper.vm.courseOrWritingPlaceholder).toBe("Select a writing service");
  });

  it("shows a loading indicator while visit options are being fetched", () => {
    visitOptionsStoreMock.isLoading = true;

    const wrapper = shallowMount(CreatePage, {
      global: {
        stubs: {
          DefaultLayout: {
            template: "<div><slot name='content' /><slot name='action' /></div>",
          },
        },
      },
    });

    expect(wrapper.get('[role="status"]').text()).toContain(
      "Loading visit options...",
    );
  });

  it("submits writing_service and null course in no-course mode", async () => {
    const push = vi.fn();
    const wrapper = shallowMount(CreatePage, {
      global: {
        mocks: {
          $router: { push },
        },
      },
    });

    wrapper.vm.selectedProgramArea = "ic-writing-assistance";
    wrapper.vm.selectedTutoringOption = "drop-in";
    wrapper.vm.selectedCourseOrWriting = "1";

    expect(wrapper.vm.isWritingProgramArea).toBe(true);
    expect(wrapper.vm.selectedCourse).toBeUndefined();
    expect(wrapper.vm.selectedWritingService).toEqual({
      id: 1,
      name: "Application",
    });

    await wrapper.vm.createVisit();

    expect(visitStoreMock.handleCreateVisit).toHaveBeenCalledWith({
      program_area: "ic-writing-assistance",
      tutoring_option: "drop-in",
      course: null,
      writing_service: 1,
    });
    expect(push).toHaveBeenCalledWith({ name: "verify" });
  });

  it("disables confirmation when no writing services are available", () => {
    visitOptionsStoreMock.visitOptions.writing_services = [];

    const wrapper = shallowMount(CreatePage, {
      global: {
        stubs: {
          DefaultLayout: {
            template: "<div><slot name='content' /><slot name='action' /></div>",
          },
        },
      },
    });

    wrapper.vm.selectedTutoringOption = 1;
    wrapper.vm.selectedCourseOrWriting = "";

    expect(wrapper.vm.noCourseOptions).toBe(true);
    expect(wrapper.vm.noWritingServiceOptions).toBe(true);
    expect(wrapper.vm.allAreSelected).toBe(false);
    expect(wrapper.html()).toContain("No writing services are available right now.");
  });

  it("keeps normal course flow unchanged when courses exist", async () => {
    visitOptionsStoreMock.visitOptions = {
      ...visitOptionsStoreMock.visitOptions,
      program_areas: [
        { slug: "ic-drop-in-tutoring", name: "General Tutoring" },
        { slug: "ic-writing-assistance", name: "Writing Assistance" },
      ],
      courses: [{ id: 22, name: "MATH 101" }],
      writing_services: [{ id: 1, name: "Application" }],
    };

    const push = vi.fn();
    const wrapper = shallowMount(CreatePage, {
      global: {
        mocks: {
          $router: { push },
        },
      },
    });

    wrapper.vm.selectedProgramArea = "ic-drop-in-tutoring";
    wrapper.vm.selectedTutoringOption = "drop-in";
    wrapper.vm.selectedCourseOrWriting = 22;

    expect(wrapper.vm.noCourseOptions).toBe(false);
    expect(wrapper.vm.isWritingProgramArea).toBe(false);
    expect(wrapper.vm.selectedCourse).toEqual({ id: 22, name: "MATH 101" });
    expect(wrapper.vm.selectedWritingService).toBeUndefined();

    await wrapper.vm.createVisit();

    expect(visitStoreMock.handleCreateVisit).toHaveBeenCalledWith({
      program_area: "ic-drop-in-tutoring",
      tutoring_option: "drop-in",
      course: 22,
      writing_service: null,
    });
    expect(push).toHaveBeenCalledWith({ name: "verify" });
  });
});
