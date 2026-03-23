---
name: auth
description: Authentication patterns for APIs
---

# Authentication Patterns

> Choose auth pattern based on use case.

## Selection Guide

| Pattern | Best For |
|---------|----------|
| **JWT** | Stateless, microservices |
| **Session** | Traditional web, simple |
| **OAuth 2.0** | Third-party integration |
| **API Keys** | Server-to-server, public APIs |
| **Passkey** | Modern passwordless (2026+) |

## JWT Principles

```
Important:
├── Always verify signature
├── Check expiration
├── Include minimal claims
├── Use short expiry + refresh tokens
└── Never store sensitive data in JWT
```
