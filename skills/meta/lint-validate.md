# Lint and Validate

**Trigger:** Linting, code validation, ESLint, Prettier, quality checks.

---

## ESLint Setup

```bash
# Install
bun add -d eslint @eslint/js typescript-eslint

# Initialize
bunx eslint --init
```

### eslint.config.mjs
```javascript
import eslint from '@eslint/js'
import tseslint from 'typescript-eslint'

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.strict,
  {
    rules: {
      '@typescript-eslint/no-unused-vars': 'error',
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/explicit-function-return-type': 'off',
    },
  },
  {
    ignores: ['node_modules/', '.next/', 'dist/'],
  }
)
```

---

## Prettier Setup

```bash
# Install
bun add -d prettier eslint-config-prettier
```

### .prettierrc
```json
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100
}
```

---

## TypeScript Validation

```bash
# Type check only (no emit)
bun tsc --noEmit

# With watch mode
bun tsc --noEmit --watch
```

### tsconfig.json (strict)
```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

---

## Pre-commit Hooks

```bash
# Install
bun add -d husky lint-staged

# Setup husky
bunx husky init
```

### .husky/pre-commit
```bash
#!/bin/sh
bunx lint-staged
```

### package.json
```json
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md}": [
      "prettier --write"
    ]
  }
}
```

---

## Security Audits

```bash
# npm audit
bun audit

# Snyk (more comprehensive)
bunx snyk test
```

---

## Full Validation Script

```json
// package.json
{
  "scripts": {
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "typecheck": "tsc --noEmit",
    "validate": "bun run lint && bun run typecheck && bun run format:check",
    "test": "vitest run",
    "ci": "bun run validate && bun run test"
  }
}
```

---

## CI Integration

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v1
      - run: bun install
      - run: bun run lint
      - run: bun run typecheck
      - run: bun run test
```
