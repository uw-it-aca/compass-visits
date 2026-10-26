import { test, expect } from "../fixtures.mjs";
import { getTarget, isTargetResponse } from "../targets.mjs";

test("authenticated visits loads the current user's live profile", async ({ page }) => {
  const target = getTarget();
  const responsePromise = page.waitForResponse(
    (response) => isTargetResponse(response, target, /^\/api\/internal\/profile\/$/),
  );
  await page.goto(target.entry);
  const response = await responsePromise;
  expect(response.status(), "Profile API must succeed").toBe(200);
  expect(response.headers()["content-type"]?.includes("application/json")).toBe(true);
  const payload = await response.json();
  expect(typeof payload === "object" && payload !== null && !Array.isArray(payload)).toBe(true);
  await expect(page.getByText("Total Hours:", { exact: true })).toBeVisible();
});