# Testing Patterns

**Trigger:** testing pyramid, unit test, integration test, mock, AAA pattern

---

## Testing Pyramid

```
        /\
       /  \      E2E (few)
      /----\
     /      \    Integration (some)
    /--------\
   /          \  Unit (many)
  /------------\
```

| Level | Speed | Coverage | Scope |
|-------|-------|----------|-------|
| Unit | Fast | Many | Single function/component |
| Integration | Medium | Some | Multiple units together |
| E2E | Slow | Few | Full user flows |

---

## AAA Pattern

```typescript
test('calculates total with discount', () => {
  // Arrange - Set up test data
  const items = [
    { price: 100, quantity: 2 },
    { price: 50, quantity: 1 },
  ]
  const discountPercent = 10

  // Act - Execute the code under test
  const total = calculateTotal(items, discountPercent)

  // Assert - Verify the result
  expect(total).toBe(225) // (200 + 50) * 0.9
})
```

---

## Unit Testing (Vitest/Bun)

### Pure Functions
```typescript
// utils/price.ts
export function formatPrice(cents: number): string {
  return `$${(cents / 100).toFixed(2)}`
}

// utils/price.test.ts
import { describe, it, expect } from 'bun:test'
import { formatPrice } from './price'

describe('formatPrice', () => {
  it('formats cents to dollars', () => {
    expect(formatPrice(1999)).toBe('$19.99')
  })

  it('handles zero', () => {
    expect(formatPrice(0)).toBe('$0.00')
  })

  it('handles large amounts', () => {
    expect(formatPrice(1000000)).toBe('$10000.00')
  })
})
```

### React Components
```typescript
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Button } from './button'

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByRole('button', { name: 'Click me' })).toBeInTheDocument()
  })

  it('calls onClick when clicked', async () => {
    const handleClick = vi.fn()
    render(<Button onClick={handleClick}>Click me</Button>)

    await userEvent.click(screen.getByRole('button'))

    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('is disabled when loading', () => {
    render(<Button loading>Click me</Button>)
    expect(screen.getByRole('button')).toBeDisabled()
  })
})
```

---

## Integration Testing

### API Routes
```typescript
// app/api/users/route.test.ts
import { describe, it, expect, beforeEach } from 'bun:test'
import { prisma } from '@/lib/prisma'

describe('POST /api/users', () => {
  beforeEach(async () => {
    await prisma.user.deleteMany()
  })

  it('creates a user', async () => {
    const response = await fetch('http://localhost:3000/api/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: 'test@example.com',
        name: 'Test User',
      }),
    })

    expect(response.status).toBe(201)

    const user = await response.json()
    expect(user.email).toBe('test@example.com')

    // Verify in database
    const dbUser = await prisma.user.findUnique({
      where: { email: 'test@example.com' },
    })
    expect(dbUser).not.toBeNull()
  })

  it('returns 400 for invalid email', async () => {
    const response = await fetch('http://localhost:3000/api/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: 'invalid-email',
        name: 'Test User',
      }),
    })

    expect(response.status).toBe(400)
  })
})
```

---

## Mocking

### Function Mocks
```typescript
import { vi, describe, it, expect } from 'vitest'

const mockFetch = vi.fn()
vi.stubGlobal('fetch', mockFetch)

describe('fetchUser', () => {
  it('returns user data', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ id: 1, name: 'John' }),
    })

    const user = await fetchUser(1)

    expect(user).toEqual({ id: 1, name: 'John' })
    expect(mockFetch).toHaveBeenCalledWith('/api/users/1')
  })
})
```

### Module Mocks
```typescript
// Mock entire module
vi.mock('@/lib/prisma', () => ({
  prisma: {
    user: {
      findUnique: vi.fn(),
      create: vi.fn(),
    },
  },
}))

import { prisma } from '@/lib/prisma'

describe('UserService', () => {
  it('finds user by email', async () => {
    vi.mocked(prisma.user.findUnique).mockResolvedValueOnce({
      id: '1',
      email: 'test@example.com',
    })

    const user = await userService.findByEmail('test@example.com')

    expect(user?.id).toBe('1')
  })
})
```

---

## Test Organization

```
tests/
├── unit/
│   ├── utils/
│   │   └── price.test.ts
│   └── components/
│       └── button.test.ts
├── integration/
│   └── api/
│       └── users.test.ts
└── e2e/
    └── checkout.spec.ts
```

Or colocate with source:
```
src/
├── components/
│   ├── button.tsx
│   └── button.test.tsx
├── utils/
│   ├── price.ts
│   └── price.test.ts
```

---

## Test Naming

```typescript
// Pattern: should [expected behavior] when [condition]
it('should return 0 when array is empty', () => {})
it('should throw error when user not found', () => {})
it('should redirect to login when unauthenticated', () => {})
```

---

## Coverage

```bash
# Run with coverage
bun test --coverage

# Vitest coverage
vitest run --coverage
```

Targets:
- Critical paths: 90%+
- Business logic: 80%+
- Overall: 70%+

Don't chase 100% — focus on meaningful tests.
