import { defineConfig, devices } from "@playwright/test";

/**
 * E2E smoke config. By default it builds and starts the production web app on
 * port 3100 and runs the smoke specs against it. Point at an already-running
 * deploy with E2E_BASE_URL=https://conversease.com (then no local server starts).
 */
const baseURL = process.env.E2E_BASE_URL ?? "http://127.0.0.1:3100";
const useExternal = Boolean(process.env.E2E_BASE_URL);

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  forbidOnly: Boolean(process.env.CI),
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? "github" : "list",
  use: {
    baseURL,
    trace: "on-first-retry"
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: useExternal
    ? undefined
    : {
        command: "npm run build && npm run start -- --port 3100",
        url: baseURL,
        timeout: 180_000,
        reuseExistingServer: !process.env.CI
      }
});
