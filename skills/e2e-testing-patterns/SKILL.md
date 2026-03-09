---
name: e2e-testing-patterns
description: End-to-end testing with Playwright for Next.js applications. Trigger on E2E test setup, cross-page flow testing (checkout, onboarding, multi-step forms), visual regression, or Playwright debugging.
metadata:
  author: osforge
  version: '1.0'
---

# E2E Testing Patterns (Playwright + Next.js)

## Setup
```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [['html', { open: 'never' }]],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'mobile', use: { ...devices['Pixel 5'] } },
  ],
  webServer: {
    command: 'bun run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

## Page Object Model
```typescript
// e2e/pages/login.page.ts
import { type Page, type Locator } from '@playwright/test'

export class LoginPage {
  readonly emailInput: Locator
  readonly passwordInput: Locator
  readonly submitButton: Locator
  readonly errorMessage: Locator

  constructor(private page: Page) {
    this.emailInput = page.getByLabel('Email')
    this.passwordInput = page.getByLabel('Password')
    this.submitButton = page.getByRole('button', { name: 'Sign in' })
    this.errorMessage = page.getByRole('alert')
  }

  async goto() { await this.page.goto('/login') }

  async login(email: string, password: string) {
    await this.emailInput.fill(email)
    await this.passwordInput.fill(password)
    await this.submitButton.click()
  }
}
```

## Auth State Fixture
```typescript
// e2e/fixtures/auth.ts
import { test as base } from '@playwright/test'

export const test = base.extend<{ authenticatedPage: Page }>({
  authenticatedPage: async ({ page }, use) => {
    // Login via API (faster than UI)
    const response = await page.request.post('/api/auth/test-login', {
      data: { email: 'test@example.com', password: 'testpass123' },
    })
    const cookies = response.headers()['set-cookie']
    if (cookies) {
      await page.context().addCookies(parseCookies(cookies, 'localhost'))
    }
    await use(page)
  },
})
```

## Test Patterns

### Multi-Step Flow
```typescript
test('complete onboarding flow', async ({ authenticatedPage: page }) => {
  await page.goto('/onboarding')

  // Step 1: Profile
  await page.getByLabel('Company name').fill('Acme Corp')
  await page.getByRole('button', { name: 'Next' }).click()

  // Step 2: Team
  await page.getByLabel('Invite email').fill('dev@example.com')
  await page.getByRole('button', { name: 'Send invite' }).click()
  await expect(page.getByText('Invite sent')).toBeVisible()
  await page.getByRole('button', { name: 'Next' }).click()

  // Step 3: Complete
  await expect(page).toHaveURL('/dashboard')
  await expect(page.getByText('Welcome, Acme Corp')).toBeVisible()
})
```

### Visual Regression
```typescript
test('dashboard renders correctly', async ({ authenticatedPage: page }) => {
  await page.goto('/dashboard')
  await page.waitForLoadState('networkidle')
  await expect(page).toHaveScreenshot('dashboard.png', {
    maxDiffPixelRatio: 0.01,
  })
})
```

### API Mocking
```typescript
test('handles payment failure gracefully', async ({ page }) => {
  await page.route('**/api/payments', (route) =>
    route.fulfill({ status: 402, json: { error: 'CARD_DECLINED' } })
  )
  // ... proceed with checkout flow
  await expect(page.getByText('Payment failed')).toBeVisible()
})
```

## Best Practices
- Use `getByRole`, `getByLabel`, `getByText` — never CSS selectors
- Auth via API fixture, not UI login in every test
- `waitForLoadState('networkidle')` before screenshots
- Test critical paths: signup → onboarding → core action → billing
- Separate E2E from unit tests: `e2e/` folder, different config
- Run E2E in CI on deploy preview, not on every push
