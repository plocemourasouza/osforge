# Requirements Clarify

**Trigger:** clarificar requisitos, requirements clarification, ambiguous, spec vagas

---

## Purpose

Clarificação estruturada por dimensões de cobertura ANTES do plano técnico. Máximo 8-10 perguntas priorizadas por impacto.

---

## Dimensions of Coverage

### 1. Functional
```
- What exactly should happen?
- What are the inputs and outputs?
- What are the edge cases?
- What happens on error?
```

### 2. Data
```
- What data is needed?
- Where does it come from?
- What format?
- What validation rules?
- Data retention requirements?
```

### 3. UX
```
- Who is the user?
- What's the happy path?
- What feedback do users need?
- Loading/empty/error states?
- Accessibility requirements?
```

### 4. Integration
```
- What systems does this touch?
- What APIs are involved?
- Authentication/authorization?
- Rate limits? Timeouts?
```

### 5. Security
```
- Who can access this?
- What data is sensitive?
- Audit logging needed?
- Compliance requirements?
```

---

## Question Prioritization

Prioritize by impact on implementation:

| Priority | Criteria |
|----------|----------|
| **P0** | Blocks understanding of core feature |
| **P1** | Affects architecture decisions |
| **P2** | Affects implementation details |
| **P3** | Nice to know, can assume default |

---

## Question Format

```markdown
### [Dimension]: [Short Topic]
**Impact:** [What decision this affects]
**Question:** [Clear, specific question]
**Default assumption:** [What we'll assume if not answered]
```

---

## Example Clarification Record

```markdown
# Clarifications: User Authentication

## Functional

### F1: Password Requirements
**Impact:** Validation logic, UX messaging
**Question:** What are the password requirements? (min length, special chars, etc.)
**Default assumption:** Min 8 chars, 1 uppercase, 1 number

### F2: Session Duration
**Impact:** Token expiry, refresh logic
**Question:** How long should a session last before requiring re-login?
**Default assumption:** 7 days with refresh

## Data

### D1: User Data Storage
**Impact:** Schema design, privacy compliance
**Question:** What user data do we store? Is any of it PII requiring special handling?
**Default assumption:** Email, hashed password, created_at only

## UX

### U1: Login Error Messages
**Impact:** Security vs usability trade-off
**Question:** Should we reveal if email exists? (Security: no, UX: yes)
**Default assumption:** Generic "Invalid credentials" message

## Integration

### I1: OAuth Providers
**Impact:** Integration complexity, dependencies
**Question:** Which OAuth providers are required? (Google, GitHub, etc.)
**Default assumption:** Email/password only for MVP

## Security

### S1: Rate Limiting
**Impact:** Infrastructure, abuse prevention
**Question:** What rate limits for login attempts?
**Default assumption:** 5 attempts per 15 minutes per IP
```

---

## Process

### 1. Read Requirements
```
- Identify what's clear
- Flag what's ambiguous
- Note assumptions being made
```

### 2. Generate Questions
```
- Cover all 5 dimensions
- Prioritize by impact
- Limit to 8-10 questions
- Provide default assumptions
```

### 3. Get Answers
```
- Present questions to stakeholder
- Document answers
- Confirm assumptions where not answered
```

### 4. Update Spec
```
- Incorporate clarifications
- Mark assumptions as confirmed
- Proceed with implementation
```

---

## Output Location

```
.osforge/designs/{feature}-clarifications.md
```

This feeds into `spec-builder` for the technical specification.

---

## When to Clarify

### Do Clarify
- Multiple valid interpretations exist
- Security/compliance implications
- Significant effort difference between interpretations
- User-facing behavior unclear

### Don't Over-Clarify
- Standard patterns (use codebase conventions)
- Technical implementation details (developer's choice)
- Obvious defaults (pagination = 20 items)
- Already documented elsewhere
