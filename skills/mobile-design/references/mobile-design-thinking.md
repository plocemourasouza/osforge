---
name: mobile-design-thinking
description: Mobile design thinking framework to prevent AI from using memorized patterns
---

# Mobile Design Thinking

> **This file prevents AI from using memorized patterns and forces genuine thinking.**
> The mobile equivalent of frontend's layout decomposition approach.

---

## 🧠 DEEP MOBILE THINKING PROTOCOL

### This Process is Mandatory Before Every Mobile Project

```
┌─────────────────────────────────────────────────────────────────┐
│                    DEEP MOBILE THINKING                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1️⃣ CONTEXT SCAN                                               │
│     └── What are my assumptions for this project?               │
│         └── QUESTION these assumptions                          │
│                                                                 │
│  2️⃣ ANTI-DEFAULT ANALYSIS                                      │
│     └── Am I applying a memorized pattern?                      │
│         └── Is this pattern REALLY the best for THIS project?   │
│                                                                 │
│  3️⃣ PLATFORM DECOMPOSITION                                     │
│     └── Did I think about iOS and Android separately?           │
│         └── What are the platform-specific patterns?            │
│                                                                 │
│  4️⃣ TOUCH INTERACTION BREAKDOWN                                │
│     └── Did I analyze each interaction individually?            │
│         └── Did I apply Fitts' Law, Thumb Zone?                 │
│                                                                 │
│  5️⃣ PERFORMANCE IMPACT ANALYSIS                                │
│     └── Did I consider performance impact of each component?    │
│         └── Is the default solution performant?                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚫 AI MOBILE DEFAULTS (FORBIDDEN LIST)

### Using These Patterns Automatically is FORBIDDEN!

The following patterns are "defaults" that AIs learned from training data.
Before using any of these, **QUESTION them and CONSIDER ALTERNATIVES!**

---

## 🔍 COMPONENT DECOMPOSITION (MANDATORY)

### Decomposition Analysis for Every Screen

Before designing any screen, perform this analysis:

```
SCREEN: [Screen Name]
├── PRIMARY ACTION: [What is the main action?]
│   └── Is it in thumb zone? [Yes/No → Why?]
│
├── TOUCH TARGETS: [All tappable elements]
│   ├── [Element 1]: [Size]pt → Sufficient?
│   ├── [Element 2]: [Size]pt → Sufficient?
│   └── Spacing: [Gap]pt → Accidental tap risk?
│
├── SCROLLABLE CONTENT:
│   ├── Is it a list? → FlatList/FlashList [Why this choice?]
│   ├── Item count: ~[N] → Performance consideration?
│   └── Fixed height? → Is getItemLayout needed?
│
├── STATE REQUIREMENTS:
│   ├── Is local state sufficient?
│   ├── Do I need to lift state?
│   └── Is global required? [Why?]
│
├── PLATFORM DIFFERENCES:
│   ├── iOS: [Anything different needed?]
│   └── Android: [Anything different needed?]
│
├── OFFLINE CONSIDERATION:
│   ├── Should this screen work offline?
│   └── Cache strategy: [Yes/No/Which one?]
│
└── PERFORMANCE IMPACT:
    ├── Any heavy components?
    ├── Is memoization needed?
    └── Animation performance?
```

---

## 📝 MOBILE DESIGN COMMITMENT

### Fill This at the Start of Every Mobile Project

```
📱 MOBILE DESIGN COMMITMENT

Project: _______________
Platform: iOS / Android / Both

1. Default pattern I will NOT use in this project:
   └── _______________

2. Context-specific focus for this project:
   └── _______________

3. Platform-specific differences I will implement:
   └── iOS: _______________
   └── Android: _______________

4. Area I will specifically optimize for performance:
   └── _______________

5. Unique challenge of this project:
   └── _______________

🧠 If I can't fill this commitment → I don't understand the project well enough.
   → Go back, understand context better, ask the user.
```

---

## 🚨 MANDATORY: Before Every Mobile Work

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRE-WORK VALIDATION                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  □ Did I complete Component Decomposition?                      │
│  □ Did I fill the Pattern Questioning Matrix?                   │
│  □ Did I pass the Anti-Memorization Test?                       │
│  □ Did I make context-based decisions?                          │
│  □ Did I analyze Interaction Breakdown?                         │
│  □ Did I fill the Mobile Design Commitment?                     │
│                                                                 │
│  ⚠️ Do not write code without completing these!                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

> **Remember:** If you chose a solution "because that's how it's always done," you chose WITHOUT THINKING. Every project is unique. Every context is different. Every user behavior is specific. **THINK, then code.**
