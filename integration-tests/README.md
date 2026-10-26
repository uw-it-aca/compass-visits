# Deployed Integration Tests

This app-owned Playwright suite targets `https://test-checkin.compass.uw.edu`,
not local builds. Dependencies are real; no browser APIs or services are mocked.
The initial read-only profile smoke test establishes UI/API access, not yet a
completed visit workflow, synchronization, or comprehensive DB/API/GCS coverage.

## Setup And Run

Requires Node 20+, a graphical desktop for login, and access to the test host.
From this directory:

```bash
npm install
npx playwright install chromium
npm run check
npm run auth
npm test
```

Complete normal SAML/MFA login in the browser as an authorized student, then
press Enter in the terminal after the app loads. No passwords are collected.
Cookie presence is only a heuristic; the smoke test verifies application access.
Repeat login when sessions expire. Use `npm run test:headed` for a visible run
or `npm test -- --list` to list scenarios without accessing protected services.

## Workflow Ownership

Each app owns its suite. Normally other apps are live data sources, not UIs
tested here. Visits is an explicit exception: its workflow requires staff
verification in Compass, so Visits owns orchestration of that dependency.
Compass still owns its independent staff UI regression tests.

For a future verification scenario, first save a separate authorized staff
session in this suite:

```bash
npm run auth -- compass-staff
```

Import `test` and `expect` from `fixtures.mjs`. The normal `page` fixture is
the Visits student; the optional `compassStaffPage` fixture is a separate
browser context authenticated to Compass. It is created only when requested.
No sibling checkout, Compass test import, or shared session file is required.
The existing smoke test does not require the staff session.

The intended workflow is: student creates an approved test visit, staff verifies
that exact visit in Compass, student refreshes Visits and checks out, then the
test polls for the expected synchronized result. Carry the created visit ID in
memory, never match an arbitrary student or verify unrelated pending visits.
This mutation scenario is not implemented or enabled by the starter: it first
needs an approved identity/data lifecycle and cleanup policy.

## Live Data And Credentials

- No hardcoded NetIDs, names, student numbers, or record IDs. The smoke test uses
  the signed-in student's normal requests and stable UI labels/response shape.
- Existing API clients can later discover authorized candidates and obtain
  expected values at runtime. Keep identifiers in memory and discovery scoped.
- Prefer independent source data. Comparing the UI with its own API checks
  rendering but can miss backend defects. Compare source visits with their
  synchronized representation for cross-app assertions.
- Recheck mutable prerequisites and use bounded polling for eventual consistency.
  Missing candidates are a prerequisite outcome, not a silent passing test.
- API clients need their own authorized environment/credentials; browser SAML
  does not supply these. Never copy production secrets locally or export data
  to committed fixtures. Do not mutate randomly discovered real records.
- Sessions live in ignored `.auth/` with directory permissions 700 and file
  permissions 600. Never upload, commit, or share them. Deleting the directory
  removes local state but does not revoke server sessions.
- Screenshots, traces, and video are disabled; errors may still include sensitive
  URLs or page text. Treat terminal output and ignored `test-results/` as
  sensitive. Do not log bodies/identifiers or upload raw CI artifacts.

## Future Pipeline

The same suite can run headlessly after approved authentication, network access,
safe data handling, artifact controls, and deployed readiness/version checks are
established. Tests run serially without retries. No workflow or auth bypass is
added by this starter.