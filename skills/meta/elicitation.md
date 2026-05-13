# Elicitation Engine

**Trigger:** "elicitar", "refinar output", "melhorar spec", ou invocável dentro de outros skills para melhorar qualquer artefato.

---

## Purpose

Refinamento iterativo de outputs usando técnicas de elicitação estruturadas. Pode ser standalone ou composable dentro de spec-builder, prd-builder, arch-builder.

---

## Techniques

### 5 Whys
```
Problem: Users are churning

Why? → They stop using the app after day 3
Why? → They can't find value in premium features
Why? → Premium features are hard to discover
Why? → Onboarding doesn't highlight them
Why? → Onboarding was rushed for launch

Root cause: Poor onboarding design
```

### Assumption Surfacing
```
Assumption: Users want real-time notifications

Evidence for:
- Competitor apps have it
- 3 users mentioned it in interviews

Evidence against:
- No usage data yet
- Could be annoying

Confidence: Medium
Test: Build minimal version, measure engagement
```

### Scenario Planning
```
Scenario: Traffic 10x overnight

What happens:
- Database connections exhaust
- API rate limits hit
- Costs spike

Mitigations:
- Connection pooling
- Caching layer
- Auto-scaling
- Budget alerts
```

### Pre-Mortem
```
It's 6 months from now. The feature failed.

Why it failed:
- Users didn't understand the value prop
- Performance was too slow
- Integration with X broke
- Security vulnerability discovered

Prevention:
- User testing before launch
- Performance budget
- Integration tests
- Security audit
```

### Socratic Questioning
```
Q: Why do we need this feature?
A: Users requested it.

Q: How many users? What did they specifically request?
A: 5 users, they wanted better reporting.

Q: What problem does better reporting solve for them?
A: They spend too much time manually compiling data.

Q: Could we solve that without building a full reporting feature?
A: Maybe an export to CSV would work...
```

---

## Usage in Skills

### Spec Builder
```
1. Initial spec draft
2. Apply Assumption Surfacing
3. Identify weak assumptions
4. Ask clarifying questions
5. Refine spec
```

### PRD Builder
```
1. Initial requirements
2. Apply 5 Whys for each problem
3. Find root causes
4. Apply Pre-Mortem
5. Add mitigations
```

### Architecture
```
1. Design draft
2. Apply Scenario Planning
3. Identify scale issues
4. Refine design
```

---

## Methods Catalog

Located in `~/.claude/skills/meta/elicitation-methods.csv`:

| Method | Best For | Time |
|--------|----------|------|
| 5 Whys | Root cause | 15min |
| Assumption Surfacing | Validating beliefs | 30min |
| Scenario Planning | Future risks | 45min |
| Pre-Mortem | Failure prevention | 30min |
| Socratic Questioning | Requirements clarity | 20min |
| Analogical Reasoning | Novel problems | 30min |
| Devil's Advocate | Decision validation | 20min |
