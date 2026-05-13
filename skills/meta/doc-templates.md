# Documentation Templates

**Trigger:** Documentation template, README template, API docs template, changelog, ADR.

---

## README Template

```markdown
# Project Name

Brief description of what this project does.

## Features

- Feature 1
- Feature 2
- Feature 3

## Quick Start

\`\`\`bash
# Clone
git clone https://github.com/org/project

# Install
bun install

# Configure
cp .env.example .env.local

# Run
bun dev
\`\`\`

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `NEXT_PUBLIC_API_URL` | API base URL | Yes |

## Architecture

Brief overview of architecture decisions.

## Contributing

1. Fork the repo
2. Create feature branch
3. Make changes
4. Submit PR

## License

MIT
```

---

## API Documentation

```markdown
# API Reference

## Authentication

All requests require Bearer token in Authorization header.

\`\`\`
Authorization: Bearer <token>
\`\`\`

## Endpoints

### GET /api/users

List all users.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | number | 1 | Page number |
| `limit` | number | 20 | Items per page |

**Response:**
\`\`\`json
{
  "data": [
    { "id": "1", "name": "John", "email": "john@example.com" }
  ],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
\`\`\`

### POST /api/users

Create a new user.

**Request Body:**
\`\`\`json
{
  "name": "John Doe",
  "email": "john@example.com"
}
\`\`\`

**Response:** `201 Created`
```

---

## ADR Template (Architecture Decision Record)

```markdown
# ADR-001: Use Supabase for Authentication

## Status

Accepted

## Context

We need an authentication solution that supports:
- Email/password login
- OAuth providers (Google, GitHub)
- Row Level Security integration

## Decision

Use Supabase Auth because:
1. Native RLS integration with PostgreSQL
2. Built-in OAuth support
3. Open source, can self-host
4. Good developer experience

## Consequences

**Positive:**
- Simplified auth implementation
- Automatic session management
- RLS policies work out of the box

**Negative:**
- Vendor dependency (mitigated by self-host option)
- Learning curve for team
```

---

## Changelog Template

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- New feature X

### Changed
- Updated dependency Y

### Fixed
- Bug in component Z

## [1.0.0] - 2024-01-15

### Added
- Initial release
- User authentication
- Dashboard

### Security
- Implemented RLS policies
```

---

## Code Comments

```typescript
/**
 * Calculates the total price including tax and discounts.
 *
 * @param items - Array of cart items
 * @param taxRate - Tax rate as decimal (e.g., 0.08 for 8%)
 * @param discountCode - Optional discount code
 * @returns Total price in cents
 *
 * @example
 * const total = calculateTotal(items, 0.08, 'SAVE10')
 */
export function calculateTotal(
  items: CartItem[],
  taxRate: number,
  discountCode?: string
): number {
  // Implementation
}
```
