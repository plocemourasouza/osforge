# Editorial Review

**Trigger:** "editorial review", "review prose", "review structure", "review document", or in the final phase of any document.

---

## Purpose

Editorial review of technical documents in 2 modes:
- **Prose mode**: Clinical copy-editing
- **Structure mode**: Logical reorganization

---

## Prose Mode

### Focus Areas

1. **Clarity**
   - Ambiguous statements
   - Jargon without explanation
   - Passive voice overuse

2. **Conciseness**
   - Redundant phrases
   - Filler words
   - Unnecessary qualifiers

3. **Grammar**
   - Subject-verb agreement
   - Tense consistency
   - Punctuation

4. **Tone**
   - Appropriate for audience
   - Consistent throughout
   - Professional but approachable

### Examples

```markdown
// Before
"In order to utilize the authentication functionality, users
will need to first navigate to the login page."

// After
"To log in, go to the login page."
```

```markdown
// Before
"The system is basically designed to somewhat handle most
of the edge cases that might potentially occur."

// After
"The system handles most edge cases."
```

---

## Structure Mode

### Focus Areas

1. **Flow**
   - Logical progression
   - Topic transitions
   - Information hierarchy

2. **Headings**
   - Clear section titles
   - Consistent hierarchy
   - Scannable structure

3. **Redundancy**
   - Repeated information
   - Overlapping sections
   - Duplicate concepts

4. **Gaps**
   - Missing sections
   - Incomplete explanations
   - Undefined terms

### Reorganization Patterns

```markdown
// Before: Mixed concerns
## API
- Endpoints
- Error handling
- Authentication
- Rate limiting

// After: Separated concerns
## Authentication
- Methods
- Tokens

## API Endpoints
- List endpoints
- Request/response

## Error Handling
- Error codes
- Recovery

## Rate Limiting
- Limits
- Headers
```

---

## Output Format

### Prose Review
```markdown
## Editorial Review (Prose)

### Clarity Issues

1. **Line 45**: "The thing that handles stuff"
   - Issue: Vague reference
   - Suggestion: "The AuthService validates credentials"

### Conciseness

1. **Line 78**: "In order to"
   - Issue: Redundant phrase
   - Suggestion: "To"

### Grammar

1. **Line 102**: "The data are processed"
   - Issue: Subject-verb disagreement (data as singular)
   - Suggestion: "The data is processed"
```

### Structure Review
```markdown
## Editorial Review (Structure)

### Flow Issues

1. **Section 3**: Architecture before Requirements
   - Issue: Should understand requirements first
   - Suggestion: Move after Requirements

### Redundancy

1. **Sections 2.1 and 4.2**: Duplicate auth explanation
   - Suggestion: Consolidate in Section 2.1, reference from 4.2

### Gaps

1. **Missing**: Error handling section
   - Suggestion: Add after API section
```

---

## Combined Review

Run both modes in sequence:
```
1. Structure review first (fix organization)
2. Prose review second (polish text)
```

This prevents polishing text that will be moved or deleted.
