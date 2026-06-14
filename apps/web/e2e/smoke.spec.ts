import { expect, test } from "@playwright/test";

/**
 * Critical-path smoke. These run without a database, LLM, or real auth: they
 * verify the app builds, renders, and that auth guards redirect — the kind of
 * integration regression unit tests cannot catch. Authenticated flows (lessons,
 * coach, exam) are exercised manually or against a seeded staging deploy.
 */

test("landing page renders the brand and entry links", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveTitle(/Conversease/i);
  await expect(page.getByRole("link", { name: /masuk|login/i }).first()).toBeVisible();
});

test("login page shows email and password fields", async ({ page }) => {
  await page.goto("/login");
  await expect(page.locator('input[type="email"]')).toBeVisible();
  await expect(page.locator('input[type="password"]')).toBeVisible();
});

test("register page renders", async ({ page }) => {
  await page.goto("/register");
  await expect(page.locator('input[type="email"]')).toBeVisible();
});

test("pricing page shows IDR plan prices", async ({ page }) => {
  await page.goto("/pricing");
  await expect(page.getByText(/Rp/).first()).toBeVisible();
});

test("protected dashboard redirects unauthenticated users to login", async ({ page }) => {
  await page.goto("/dashboard");
  await page.waitForURL(/\/login/, { timeout: 15_000 });
  await expect(page).toHaveURL(/\/login/);
});

test("protected conversation coach redirects unauthenticated users to login", async ({ page }) => {
  await page.goto("/conversation-coach");
  await page.waitForURL(/\/login/, { timeout: 15_000 });
  await expect(page).toHaveURL(/\/login/);
});
