# E2E Testing (Playwright)

**Trigger:** E2E, Playwright, visual regression, cross-page flow, checkout flow

---

## Setup

### Install
```bash
bun add -D @playwright/test
bunx playwright install
```

### Config
```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'Mobile Chrome', use: { ...devices['Pixel 5'] } },
  ],
  webServer: {
    command: 'bun run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

---

## Page Object Model

```typescript
// tests/e2e/pages/login.page.ts
import { type Page, type Locator } from '@playwright/test'

export class LoginPage {
  readonly page: Page
  readonly emailInput: Locator
  readonly passwordInput: Locator
  readonly submitButton: Locator
  readonly errorMessage: Locator

  constructor(page: Page) {
    this.page = page
    this.emailInput = page.getByLabel('Email')
    this.passwordInput = page.getByLabel('Password')
    this.submitButton = page.getByRole('button', { name: 'Sign in' })
    this.errorMessage = page.getByRole('alert')
  }

  async goto() {
    await this.page.goto('/login')
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email)
    await this.passwordInput.fill(password)
    await this.submitButton.click()
  }
}
```

---

## Auth State Fixtures

Login via API, not UI:

```typescript
// tests/e2e/fixtures/auth.ts
import { test as base } from '@playwright/test'

type AuthFixtures = {
  authenticatedPage: Page
}

export const test = base.extend<AuthFixtures>({
  authenticatedPage: async ({ page, request }, use) => {
    // Login via API
    const response = await request.post('/api/auth/login', {
      data: {
        email: 'test@example.com',
        password: 'password123',
      },
    })

    // Get cookies from response
    const cookies = response.headers()['set-cookie']

    // Set cookies on page context
    await page.context().addCookies([
      { name: 'session', value: extractCookie(cookies), domain: 'localhost', path: '/' }
    ])

    await use(page)
  },
})
```

---

## Multi-Step Flow Testing

```typescript
// tests/e2e/checkout.spec.ts
import { test, expect } from '@playwright/test'
import { ProductPage } from './pages/product.page'
import { CartPage } from './pages/cart.page'
import { CheckoutPage } from './pages/checkout.page'

test.describe('Checkout Flow', () => {
  test('complete purchase', async ({ page }) => {
    const productPage = new ProductPage(page)
    const cartPage = new CartPage(page)
    const checkoutPage = new CheckoutPage(page)

    // Step 1: Add to cart
    await productPage.goto('/products/widget')
    await productPage.addToCart()
    await expect(page.getByText('Added to cart')).toBeVisible()

    // Step 2: View cart
    await cartPage.goto()
    await expect(cartPage.items).toHaveCount(1)

    // Step 3: Checkout
    await cartPage.proceedToCheckout()
    await checkoutPage.fillShipping({
      name: 'John Doe',
      address: '123 Main St',
      city: 'Anytown',
    })
    await checkoutPage.fillPayment({
      card: '4242424242424242',
      expiry: '12/25',
      cvc: '123',
    })
    await checkoutPage.placeOrder()

    // Step 4: Confirmation
    await expect(page.getByText('Order confirmed')).toBeVisible()
    await expect(page.getByText('Order #')).toBeVisible()
  })
})
```

---

## Visual Regression

```typescript
test('homepage visual regression', async ({ page }) => {
  await page.goto('/')

  // Full page screenshot
  await expect(page).toHaveScreenshot('homepage.png', {
    fullPage: true,
    maxDiffPixels: 100,
  })

  // Component screenshot
  const hero = page.getByRole('region', { name: 'Hero' })
  await expect(hero).toHaveScreenshot('hero-section.png')
})
```

Update snapshots:
```bash
bunx playwright test --update-snapshots
```

---

## API Mocking

```typescript
test('handles API error gracefully', async ({ page }) => {
  // Mock API to return error
  await page.route('/api/products', (route) => {
    route.fulfill({
      status: 500,
      body: JSON.stringify({ error: 'Server error' }),
    })
  })

  await page.goto('/products')
  await expect(page.getByText('Something went wrong')).toBeVisible()
})

test('displays products from API', async ({ page }) => {
  // Mock API with test data
  await page.route('/api/products', (route) => {
    route.fulfill({
      status: 200,
      body: JSON.stringify([
        { id: 1, name: 'Widget', price: 9.99 },
        { id: 2, name: 'Gadget', price: 19.99 },
      ]),
    })
  })

  await page.goto('/products')
  await expect(page.getByText('Widget')).toBeVisible()
  await expect(page.getByText('Gadget')).toBeVisible()
})
```

---

## Best Practices

### Selectors
```typescript
// GOOD - Accessible selectors
page.getByRole('button', { name: 'Submit' })
page.getByLabel('Email')
page.getByText('Welcome')
page.getByTestId('product-card')  // Only when needed

// BAD - Fragile selectors
page.locator('.btn-primary')
page.locator('#submit-btn')
page.locator('div > span.text')
```

### Assertions
```typescript
// GOOD - Auto-waiting assertions
await expect(page.getByText('Success')).toBeVisible()
await expect(page.getByRole('button')).toBeEnabled()

// BAD - Manual waits
await page.waitForTimeout(1000)  // Never use fixed timeouts
```

### Test Isolation
```typescript
// Each test should be independent
test.beforeEach(async ({ page }) => {
  // Reset state if needed
})
```

---

## Running Tests

```bash
# Run all tests
bunx playwright test

# Run specific file
bunx playwright test tests/e2e/auth.spec.ts

# Run in headed mode
bunx playwright test --headed

# Run in debug mode
bunx playwright test --debug

# Run specific project
bunx playwright test --project=chromium

# Generate tests (codegen)
bunx playwright codegen localhost:3000
```
