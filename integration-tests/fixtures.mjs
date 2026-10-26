import { test as base, expect } from "@playwright/test";
import { getTarget } from "./targets.mjs";

export const test = base.extend({
  compassStaffPage: async ({ browser }, use) => {
    const target = getTarget("compass-staff");
    const context = await browser.newContext({
      baseURL: target.origin,
      storageState: target.statePath,
    });
    try {
      await use(await context.newPage());
    } finally {
      await context.close();
    }
  },
});

export { expect };