import { mkdir, chmod } from "node:fs/promises";
import path from "node:path";
import { createInterface } from "node:readline/promises";
import { chromium } from "@playwright/test";
import { getTarget } from "./targets.mjs";

process.umask(0o077);
const target = getTarget(process.argv[2]);
const browser = await chromium.launch({ headless: false });
const prompt = createInterface({ input: process.stdin, output: process.stdout });

try {
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.goto(new URL(target.entry, target.origin).href);
  await prompt.question(
    "Complete normal SAML/MFA login in the browser. Once the app is ready, press Enter here. ",
  );
  if (new URL(page.url()).origin !== target.origin) {
    throw new Error("Login did not return to the expected test application. State not saved.");
  }
  const cookies = await context.cookies(target.origin);
  if (!cookies.some((cookie) => cookie.httpOnly)) {
    throw new Error("No HTTP-only application cookie found. State not saved.");
  }
  await mkdir(path.dirname(target.statePath), { recursive: true, mode: 0o700 });
  await chmod(path.dirname(target.statePath), 0o700);
  const state = await context.storageState();
  const hostname = new URL(target.origin).hostname;
  state.cookies = state.cookies.filter((cookie) => {
    const domain = cookie.domain.replace(/^\./, "");
    return hostname === domain || hostname.endsWith(`.${domain}`);
  });
  state.origins = state.origins.filter((origin) => origin.origin === target.origin);
  const isolated = await browser.newContext({ storageState: state });
  await isolated.storageState({ path: target.statePath });
  await isolated.close();
  await chmod(target.statePath, 0o600);
  console.log("Saved local application session. Run the smoke test to verify access.");
} finally {
  prompt.close();
  await browser.close();
}