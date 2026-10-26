import { defineConfig } from "@playwright/test";
import { getTarget } from "./targets.mjs";

export default defineConfig({
  testDir: "./scenarios",
  testMatch: "**/*.pw.mjs",
  workers: 1,
  retries: 0,
  timeout: 60_000,
  expect: { timeout: 15_000 },
  reporter: [["line"]],
  use: {
    browserName: "chromium",
    baseURL: getTarget().origin,
    storageState: getTarget().statePath,
    navigationTimeout: 45_000,
    actionTimeout: 15_000,
    trace: "off",
    screenshot: "off",
    video: "off",
  },
});