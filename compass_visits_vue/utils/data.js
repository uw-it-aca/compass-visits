import "regenerator-runtime/runtime";
import { useCustomFetch } from "@/composables/customFetch";

async function getStudentProfile() {
  const url = "/api/internal/profile/";
  return useCustomFetch(url);
}

async function updateVisit(visitId, data) {
  const url = `/api/internal/visit/${visitId}/`;
  return useCustomFetch(url, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
}

async function deleteVisit(visitId) {
  const url = `/api/internal/visit/${visitId}/`;
  return useCustomFetch(url, {
    method: "DELETE",
  });
}

async function createVisit(data) {
  const url = "/api/internal/visit/";
  return useCustomFetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
}

async function getStudentVisits() {
  const url = "/api/internal/studentvisits/";
  return useCustomFetch(url);
}

async function getVisitOptions() {
  const url = "/api/v1/visitoptions/";
  return useCustomFetch(url);
}

export {
  getStudentProfile,
  updateVisit,
  deleteVisit,
  createVisit,
  getStudentVisits,
  getVisitOptions,
};
