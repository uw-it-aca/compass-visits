import path from "node:path";
import { fileURLToPath } from "node:url";

const directory = path.dirname(fileURLToPath(import.meta.url));
export const targets = {
  visits: { origin: "https://test-checkin.compass.uw.edu", entry: "/" },
  "compass-staff": { origin: "https://test.compass.uw.edu", entry: "/" },
};

export function getTarget(name = "visits") {
  if (!Object.hasOwn(targets, name)) {
    throw new Error("Choose a target: visits or compass-staff.");
  }
  return {
    ...targets[name],
    statePath: path.join(directory, ".auth", `${name}.json`),
  };
}

export function isTargetResponse(response, target, pathnamePattern) {
  const url = new URL(response.url());
  return url.origin === target.origin &&
    response.request().method() === "GET" &&
    pathnamePattern.test(url.pathname);
}