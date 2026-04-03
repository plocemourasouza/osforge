# Interactive Elements Reference

Implementation patterns for every visual element used in plan breakdowns. Pick the elements that best serve each section's content.

## Table of Contents
1. [Expandable Detail Cards](#expandable-detail-cards)
2. [Flow Diagrams](#flow-diagrams)
3. [Numbered Step Cards](#numbered-step-cards)
4. [Callout Boxes](#callout-boxes)
5. [Pattern/Feature Cards](#patternfeature-cards)
6. [Stat Badges](#stat-badges)
7. [Visual File Tree](#visual-file-tree)
8. [Icon-Label Rows](#icon-label-rows)
9. [Architecture Diagram](#architecture-diagram)
10. [Comparison Table](#comparison-table)
11. [Code Blocks with Labels](#code-blocks-with-labels)
12. [Hero Section](#hero-section)
13. [Review System](#review-system)

---

## Expandable Detail Cards

For dense technical content that shouldn't overwhelm the main flow. Summary is always visible; details expand on click.

**HTML:**
```html
<div class="expandable-card animate-in">
  <button class="expandable-header" onclick="toggleExpand(this)" aria-expanded="false">
    <div class="expandable-title-row">
      <span class="expandable-icon">+</span>
      <strong>Card Title — Brief Summary</strong>
    </div>
    <span class="expandable-hint">Click to expand</span>
  </button>
  <div class="expandable-body">
    <p>Detailed content goes here. Can include any other elements — code blocks, lists, etc.</p>
  </div>
</div>
```

**CSS:**
```css
.expandable-card {
  background: var(--color-surface);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  margin: var(--space-4) 0;
  border: 1px solid var(--color-border-light);
}
.expandable-header {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4) var(--space-5);
  background: none;
  border: none;
  cursor: pointer;
  font-family: var(--font-body);
  font-size: var(--text-base);
  color: var(--color-text);
  text-align: left;
  transition: background var(--duration-fast);
}
.expandable-header:hover {
  background: var(--color-surface-warm);
}
.expandable-title-row {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}
.expandable-icon {
  font-family: var(--font-mono);
  font-size: var(--text-lg);
  color: var(--color-accent);
  font-weight: 700;
  width: 24px;
  text-align: center;
  transition: transform var(--duration-normal) var(--ease-out);
}
.expandable-card.open .expandable-icon {
  transform: rotate(45deg);
}
.expandable-hint {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.expandable-card.open .expandable-hint {
  display: none;
}
.expandable-body {
  max-height: 0;
  overflow: hidden;
  transition: max-height var(--duration-slow) var(--ease-out),
              padding var(--duration-slow) var(--ease-out);
  padding: 0 var(--space-5);
}
.expandable-card.open .expandable-body {
  max-height: 2000px;
  padding: 0 var(--space-5) var(--space-5);
}
.expandable-body p {
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  line-height: var(--leading-normal);
}
```

**JS:**
```javascript
window.toggleExpand = function(btn) {
  const card = btn.closest('.expandable-card');
  card.classList.toggle('open');
  btn.setAttribute('aria-expanded', card.classList.contains('open'));
};
```

---

## Flow Diagrams

CSS flexbox-based. Boxes with arrows showing how parts connect. Color-coded per component.

**Horizontal flow (default — wraps to vertical on mobile):**
```html
<div class="flow-steps animate-in">
  <div class="flow-step" style="border-top: 3px solid var(--color-section-1)">
    <div class="flow-step-label" style="background: var(--color-section-1)">Scanner</div>
    <p>Walks the directory tree and discovers all files</p>
  </div>
  <div class="flow-arrow">&rarr;</div>
  <div class="flow-step" style="border-top: 3px solid var(--color-section-2)">
    <div class="flow-step-label" style="background: var(--color-section-2)">Parser</div>
    <p>Extracts imports and builds dependency graph</p>
  </div>
  <div class="flow-arrow">&rarr;</div>
  <div class="flow-step" style="border-top: 3px solid var(--color-section-3)">
    <div class="flow-step-label" style="background: var(--color-section-3)">Renderer</div>
    <p>Displays the graph as 3D particles</p>
  </div>
</div>
```

**CSS:**
```css
.flow-steps {
  display: flex;
  align-items: stretch;
  gap: var(--space-2);
  margin: var(--space-8) 0;
  flex-wrap: wrap;
  justify-content: center;
}
.flow-step {
  flex: 1;
  min-width: 160px;
  max-width: 260px;
  background: var(--color-surface);
  border-radius: var(--radius-md);
  padding: var(--space-5);
  box-shadow: var(--shadow-sm);
  text-align: center;
}
.flow-step-label {
  display: inline-block;
  color: white;
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-full);
  margin-bottom: var(--space-3);
}
.flow-step p {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin: 0;
  line-height: var(--leading-normal);
}
.flow-arrow {
  display: flex;
  align-items: center;
  font-size: var(--text-2xl);
  color: var(--color-text-muted);
  font-weight: 300;
  padding: 0 var(--space-1);
}

@media (max-width: 768px) {
  .flow-steps { flex-direction: column; align-items: center; }
  .flow-step { max-width: 100%; width: 100%; }
  .flow-arrow { transform: rotate(90deg); }
}
```

**Vertical flow (for longer sequences):**
```html
<div class="flow-vertical animate-in">
  <div class="flow-v-step">
    <div class="flow-v-num" style="background: var(--color-section-1)">1</div>
    <div class="flow-v-content">
      <strong>Step Title</strong>
      <p>Description of what happens at this step</p>
    </div>
  </div>
  <div class="flow-v-line"></div>
  <div class="flow-v-step">
    <div class="flow-v-num" style="background: var(--color-section-2)">2</div>
    <div class="flow-v-content">
      <strong>Step Title</strong>
      <p>Description</p>
    </div>
  </div>
  <!-- more steps -->
</div>
```

**CSS:**
```css
.flow-vertical {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0;
  margin: var(--space-8) 0;
  padding-left: var(--space-4);
}
.flow-v-step {
  display: flex;
  align-items: flex-start;
  gap: var(--space-4);
}
.flow-v-num {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  color: white;
  font-weight: 700;
  font-family: var(--font-display);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.flow-v-content {
  padding-bottom: var(--space-4);
}
.flow-v-content p {
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  margin: var(--space-1) 0 0;
}
.flow-v-line {
  width: 2px;
  height: 24px;
  background: var(--color-border);
  margin-left: 17px;
}
```

---

## Numbered Step Cards

For sequential processes. Each step is a card with a number, title, and description.

```html
<div class="step-cards stagger-children">
  <div class="step-card animate-in">
    <div class="step-num">1</div>
    <div class="step-body">
      <strong>Step Title</strong>
      <p>Description of what happens in this step</p>
    </div>
  </div>
  <div class="step-card animate-in">
    <div class="step-num">2</div>
    <div class="step-body">
      <strong>Step Title</strong>
      <p>Description</p>
    </div>
  </div>
  <div class="step-card animate-in">
    <div class="step-num">3</div>
    <div class="step-body">
      <strong>Step Title</strong>
      <p>Description</p>
    </div>
  </div>
</div>
```

```css
.step-cards {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  margin: var(--space-6) 0;
}
.step-card {
  display: flex;
  align-items: flex-start;
  gap: var(--space-4);
  padding: var(--space-4) var(--space-5);
  background: var(--color-surface);
  border-radius: var(--radius-md);
  border-left: 3px solid var(--color-accent);
  box-shadow: var(--shadow-sm);
}
.step-num {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--color-accent);
  color: white;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-display);
  flex-shrink: 0;
}
.step-body p {
  margin: var(--space-1) 0 0;
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
}
```

---

## Callout Boxes

Highlighted boxes for key decisions, constraints, trade-offs, or important notes.

```html
<div class="callout callout-accent animate-in">
  <div class="callout-icon">&#x1f4a1;</div>
  <div class="callout-content">
    <strong class="callout-title">Key Decision</strong>
    <p>Explanation of why this decision was made and what it means for the project.</p>
  </div>
</div>
```

**CSS:**
```css
.callout {
  display: flex;
  gap: var(--space-4);
  padding: var(--space-5);
  border-radius: var(--radius-md);
  margin: var(--space-6) 0;
}
.callout-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
  line-height: 1;
}
.callout-title {
  display: block;
  margin-bottom: var(--space-2);
  font-family: var(--font-display);
  font-size: var(--text-base);
}
.callout p {
  margin: 0;
  font-size: var(--text-sm);
  line-height: var(--leading-normal);
}

/* Variants */
.callout-accent {
  background: var(--color-accent-light);
  border-left: 4px solid var(--color-accent);
}
.callout-accent .callout-title { color: var(--color-accent); }

.callout-info {
  background: var(--color-info-light);
  border-left: 4px solid var(--color-info);
}
.callout-info .callout-title { color: var(--color-info); }

.callout-warning {
  background: var(--color-error-light);
  border-left: 4px solid var(--color-error);
}
.callout-warning .callout-title { color: var(--color-error); }

.callout-success {
  background: var(--color-success-light);
  border-left: 4px solid var(--color-success);
}
.callout-success .callout-title { color: var(--color-success); }
```

**When to use each variant:**
- `callout-accent` — Key decisions, architectural choices, "why we chose this"
- `callout-info` — Good to know, context, background information
- `callout-warning` — Constraints, limitations, risks, things to watch out for
- `callout-success` — Wins, benefits, what makes this approach work well

---

## Pattern/Feature Cards

Grid of cards for listing components, features, tech stack items, or any set of related concepts.

```html
<div class="pattern-cards stagger-children">
  <div class="pattern-card animate-in" style="border-top: 3px solid var(--color-section-1)">
    <div class="pattern-icon" style="background: var(--color-section-1)">icon</div>
    <h4 class="pattern-title">Component Name</h4>
    <p class="pattern-desc">Brief description of what this component does and why it matters.</p>
  </div>
  <div class="pattern-card animate-in" style="border-top: 3px solid var(--color-section-2)">
    <div class="pattern-icon" style="background: var(--color-section-2)">icon</div>
    <h4 class="pattern-title">Component Name</h4>
    <p class="pattern-desc">Brief description.</p>
  </div>
  <!-- more cards -->
</div>
```

```css
.pattern-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--space-4);
  margin: var(--space-6) 0;
}
.pattern-card {
  background: var(--color-surface);
  border-radius: var(--radius-md);
  padding: var(--space-6);
  box-shadow: var(--shadow-sm);
  transition: transform var(--duration-normal) var(--ease-out),
              box-shadow var(--duration-normal);
}
.pattern-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
}
.pattern-icon {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  margin-bottom: var(--space-3);
  color: white;
}
.pattern-title {
  font-family: var(--font-display);
  font-weight: 600;
  font-size: var(--text-base);
  margin: 0 0 var(--space-2);
}
.pattern-desc {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin: 0;
  line-height: var(--leading-normal);
}
```

---

## Stat Badges

Small badges for key numbers and metrics. Use in the hero section or anywhere stats add context.

```html
<div class="stat-badges animate-in">
  <div class="stat-badge">
    <span class="stat-value">147</span>
    <span class="stat-label">Files</span>
  </div>
  <div class="stat-badge">
    <span class="stat-value">5</span>
    <span class="stat-label">Modules</span>
  </div>
  <div class="stat-badge">
    <span class="stat-value">Node.js</span>
    <span class="stat-label">Runtime</span>
  </div>
</div>
```

```css
.stat-badges {
  display: flex;
  gap: var(--space-4);
  flex-wrap: wrap;
  margin: var(--space-6) 0;
}
.stat-badge {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--space-3) var(--space-5);
  background: var(--color-surface);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border-light);
  min-width: 80px;
}
.stat-value {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: var(--text-xl);
  color: var(--color-accent);
}
.stat-label {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
```

---

## Visual File Tree

For showing project structure. Much better than a paragraph listing directories.

```html
<div class="file-tree animate-in">
  <div class="ft-folder open">
    <span class="ft-name">src/</span>
    <span class="ft-desc">Main source code</span>
    <div class="ft-children">
      <div class="ft-folder">
        <span class="ft-name">scanner/</span>
        <span class="ft-desc">File discovery and parsing</span>
      </div>
      <div class="ft-folder">
        <span class="ft-name">server/</span>
        <span class="ft-desc">Express server and API routes</span>
      </div>
      <div class="ft-file">
        <span class="ft-name">index.js</span>
        <span class="ft-desc">Entry point</span>
      </div>
    </div>
  </div>
</div>
```

```css
.file-tree {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  background: var(--color-surface);
  border-radius: var(--radius-md);
  padding: var(--space-5);
  box-shadow: var(--shadow-sm);
  margin: var(--space-6) 0;
}
.ft-folder, .ft-file {
  padding: var(--space-2) var(--space-3);
  border-left: 2px solid var(--color-border-light);
  margin-left: var(--space-4);
}
.ft-folder:first-child {
  border-left: none;
  margin-left: 0;
}
.ft-folder > .ft-name {
  color: var(--color-accent);
  font-weight: 600;
}
.ft-file > .ft-name {
  color: var(--color-text);
}
.ft-desc {
  color: var(--color-text-muted);
  font-family: var(--font-body);
  margin-left: var(--space-2);
  font-size: var(--text-xs);
}
.ft-children {
  margin-left: var(--space-4);
  margin-top: var(--space-1);
}
```

---

## Icon-Label Rows

For listing components, features, or tech stack visually. Replaces bullet-point paragraphs.

```html
<div class="icon-rows stagger-children">
  <div class="icon-row animate-in">
    <div class="icon-circle" style="background: var(--color-section-1)">icon</div>
    <div>
      <strong>Component Name</strong>
      <p>Brief description of what it does</p>
    </div>
  </div>
  <div class="icon-row animate-in">
    <div class="icon-circle" style="background: var(--color-section-2)">icon</div>
    <div>
      <strong>Component Name</strong>
      <p>Brief description</p>
    </div>
  </div>
</div>
```

```css
.icon-rows {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  margin: var(--space-6) 0;
}
.icon-row {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4);
  background: var(--color-surface);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}
.icon-row p {
  margin: 0;
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
}
.icon-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  flex-shrink: 0;
  color: white;
}
```

---

## Architecture Diagram

Box-and-arrow layout showing how major system components relate. CSS grid-based.

```html
<div class="arch-diagram animate-in">
  <div class="arch-zone">
    <h4 class="arch-zone-label">Client</h4>
    <div class="arch-components">
      <div class="arch-box" style="border-color: var(--color-section-1)">
        <strong>Browser UI</strong>
        <p>Three.js graph</p>
      </div>
    </div>
  </div>

  <div class="arch-connector">&darr; &uarr;</div>

  <div class="arch-zone">
    <h4 class="arch-zone-label">Server</h4>
    <div class="arch-components">
      <div class="arch-box" style="border-color: var(--color-section-2)">
        <strong>Express</strong>
        <p>REST + WebSocket</p>
      </div>
      <div class="arch-box" style="border-color: var(--color-section-3)">
        <strong>Scanner</strong>
        <p>File + AST parsing</p>
      </div>
    </div>
  </div>

  <div class="arch-connector">&darr; &uarr;</div>

  <div class="arch-zone">
    <h4 class="arch-zone-label">External</h4>
    <div class="arch-components">
      <div class="arch-box" style="border-color: var(--color-section-4)">
        <strong>Ollama</strong>
        <p>Local LLM</p>
      </div>
    </div>
  </div>
</div>
```

```css
.arch-diagram {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  margin: var(--space-8) 0;
}
.arch-zone {
  width: 100%;
  max-width: var(--content-width);
  background: var(--color-surface);
  border-radius: var(--radius-md);
  padding: var(--space-4) var(--space-5);
  box-shadow: var(--shadow-sm);
}
.arch-zone-label {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text-muted);
  margin: 0 0 var(--space-3);
}
.arch-components {
  display: flex;
  gap: var(--space-3);
  flex-wrap: wrap;
}
.arch-box {
  flex: 1;
  min-width: 140px;
  padding: var(--space-3) var(--space-4);
  border: 2px solid;
  border-radius: var(--radius-sm);
  text-align: center;
}
.arch-box strong {
  display: block;
  font-size: var(--text-sm);
  font-family: var(--font-display);
}
.arch-box p {
  margin: var(--space-1) 0 0;
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
}
.arch-connector {
  font-size: var(--text-xl);
  color: var(--color-text-muted);
  letter-spacing: 0.3em;
}
```

---

## Comparison Table

For "what makes this different" or "before/after" comparisons.

```html
<div class="comparison-table animate-in">
  <table>
    <thead>
      <tr>
        <th></th>
        <th>Before</th>
        <th>After</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="comp-label">First impression</td>
        <td>Wall of text</td>
        <td class="comp-highlight">Visual scroll-through</td>
      </tr>
      <tr>
        <td class="comp-label">Navigation</td>
        <td>Scroll and hunt</td>
        <td class="comp-highlight">Dot nav + keyboard shortcuts</td>
      </tr>
    </tbody>
  </table>
</div>
```

```css
.comparison-table {
  margin: var(--space-6) 0;
  overflow-x: auto;
}
.comparison-table table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--text-sm);
}
.comparison-table th {
  font-family: var(--font-display);
  font-weight: 600;
  padding: var(--space-3) var(--space-4);
  text-align: left;
  border-bottom: 2px solid var(--color-border);
}
.comparison-table td {
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--color-border-light);
  color: var(--color-text-secondary);
}
.comp-label {
  font-weight: 600;
  color: var(--color-text) !important;
}
.comp-highlight {
  color: var(--color-accent) !important;
  font-weight: 500;
}
```

---

## Code Blocks with Labels

For technical snippets from the plan (CLI commands, config examples, etc.).

```html
<div class="labeled-code animate-in">
  <span class="code-label">CLI Usage</span>
  <pre><code>$ npm install -g codeorb
$ codeorb ~/my-project

  codeorb v1.0.0
  Starting local server...
  Open http://localhost:3333</code></pre>
</div>
```

```css
.labeled-code {
  position: relative;
  margin: var(--space-6) 0;
}
.code-label {
  position: absolute;
  top: var(--space-2);
  right: var(--space-3);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: rgba(205, 214, 244, 0.4);
  z-index: 1;
}
```

---

## Hero Section

The opening section of every breakdown. Project name, description, and key stats.

```html
<section class="section hero-section" id="section-hero" style="background: var(--color-bg)">
  <div class="section-content">
    <div class="hero-content animate-in">
      <h1 class="hero-title">Project Name</h1>
      <p class="hero-description">One-line description of what this project does and why it matters.</p>
      <div class="stat-badges">
        <!-- stat badges here -->
      </div>
    </div>
  </div>
</section>
```

```css
.hero-section {
  display: flex;
  align-items: center;
}
.hero-title {
  font-family: var(--font-display);
  font-size: var(--text-5xl);
  font-weight: 800;
  line-height: var(--leading-tight);
  margin: 0 0 var(--space-4);
  color: var(--color-text);
}
.hero-description {
  font-size: var(--text-xl);
  color: var(--color-text-secondary);
  line-height: var(--leading-normal);
  margin: 0 0 var(--space-8);
  max-width: 600px;
}
```

---

## Review System

Every section gets a review toolbar. Users can thumbs up/down and leave comments. A floating "Copy Review" button collects all feedback and copies it to clipboard as formatted text, ready to paste into Claude.

**IMPORTANT:** The review system is REQUIRED on every breakdown. It must be included in every generated HTML file. It is not optional.

### Review Toolbar (one per section)

Appears at the bottom of each section. Minimal, clean, dark-themed (Claude-style).

**HTML — add inside each `<section class="section">`, after `.section-body`:**
```html
<div class="review-bar" data-section="section-N">
  <div class="review-actions">
    <button class="review-btn review-up" onclick="setReaction(this, 'up')" aria-label="Thumbs up">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M7 10v12"/><path d="M15 5.88 14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h2.76a2 2 0 0 0 1.79-1.11L12 2h0a3.13 3.13 0 0 1 3 3.88Z"/>
      </svg>
    </button>
    <button class="review-btn review-down" onclick="setReaction(this, 'down')" aria-label="Thumbs down">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M17 14V2"/><path d="M9 18.12 10 14H4.17a2 2 0 0 1-1.92-2.56l2.33-8A2 2 0 0 1 6.5 2H20a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-2.76a2 2 0 0 0-1.79 1.11L12 22h0a3.13 3.13 0 0 1-3-3.88Z"/>
      </svg>
    </button>
    <button class="review-btn review-comment-btn" onclick="toggleComment(this)" aria-label="Add comment">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
      </svg>
    </button>
  </div>
  <div class="review-comment-box" style="display:none">
    <textarea class="review-textarea" placeholder="Leave a note about this section..." rows="2" oninput="saveComment(this)"></textarea>
  </div>
</div>
```

**CSS:**
```css
/* --- REVIEW SYSTEM --- */
.review-bar {
  margin-top: var(--space-8);
  padding-top: var(--space-4);
  border-top: 1px solid var(--color-border-light);
}
.review-actions {
  display: flex;
  gap: var(--space-2);
  align-items: center;
}
.review-btn {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  color: var(--color-text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--duration-fast);
}
.review-btn:hover {
  border-color: var(--color-text-secondary);
  color: var(--color-text);
  background: var(--color-surface-warm);
}

/* Active states */
.review-up.active {
  background: var(--color-success-light);
  border-color: var(--color-success);
  color: var(--color-success);
}
.review-down.active {
  background: var(--color-error-light);
  border-color: var(--color-error);
  color: var(--color-error);
}
.review-comment-btn.has-comment {
  background: var(--color-info-light);
  border-color: var(--color-info);
  color: var(--color-info);
}

/* Comment box */
.review-comment-box {
  margin-top: var(--space-3);
}
.review-textarea {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  color: var(--color-text);
  background: var(--color-surface);
  resize: vertical;
  min-height: 60px;
  line-height: var(--leading-normal);
  transition: border-color var(--duration-fast);
  box-sizing: border-box;
}
.review-textarea:focus {
  outline: none;
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px rgba(217, 79, 48, 0.1);
}
.review-textarea::placeholder {
  color: var(--color-text-muted);
}
```

### Floating Copy Review Button

Fixed at the bottom-right of the viewport. Shows a count of how many sections have feedback. Clicking copies formatted review to clipboard and shows a confirmation toast.

**HTML — add before closing `</body>`:**
```html
<button class="copy-review-btn" id="copyReviewBtn" onclick="copyReview()" style="display:none">
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>
  </svg>
  <span>Copy Review</span>
  <span class="review-count" id="reviewCount">0</span>
</button>

<div class="toast" id="toast">Review copied to clipboard — paste into Claude</div>
```

**CSS:**
```css
.copy-review-btn {
  position: fixed;
  bottom: var(--space-6);
  right: var(--space-6);
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-5);
  background: var(--color-bg-code);
  color: #CDD6F4;
  border: none;
  border-radius: var(--radius-full);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: 500;
  cursor: pointer;
  box-shadow: var(--shadow-lg);
  transition: transform var(--duration-normal) var(--ease-out),
              box-shadow var(--duration-normal);
  z-index: 200;
}
.copy-review-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-xl);
}
.review-count {
  background: var(--color-accent);
  color: white;
  font-size: var(--text-xs);
  font-weight: 700;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Toast notification */
.toast {
  position: fixed;
  bottom: calc(var(--space-6) + 56px);
  right: var(--space-6);
  background: var(--color-success);
  color: white;
  padding: var(--space-3) var(--space-5);
  border-radius: var(--radius-sm);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: 500;
  box-shadow: var(--shadow-lg);
  opacity: 0;
  transform: translateY(10px);
  transition: opacity var(--duration-normal), transform var(--duration-normal);
  pointer-events: none;
  z-index: 201;
}
.toast.show {
  opacity: 1;
  transform: translateY(0);
}
```

### Review JavaScript

All review state stored in localStorage keyed by page title. Handles reactions, comments, copy-to-clipboard, and the floating button visibility.

**JS — add inside the main IIFE:**
```javascript
// --- REVIEW SYSTEM ---
const REVIEW_KEY = 'visualplanner-review-' + document.title.toLowerCase().replace(/[^a-z0-9]/g, '-');
let reviewData = JSON.parse(localStorage.getItem(REVIEW_KEY) || '{}');

function saveReviewData() {
  localStorage.setItem(REVIEW_KEY, JSON.stringify(reviewData));
  updateCopyButton();
}

function updateCopyButton() {
  const btn = document.getElementById('copyReviewBtn');
  const count = document.getElementById('reviewCount');
  const total = Object.keys(reviewData).filter(k => reviewData[k].reaction || reviewData[k].comment).length;
  count.textContent = total;
  btn.style.display = total > 0 ? 'flex' : 'none';
}

window.setReaction = function(btn, type) {
  const bar = btn.closest('.review-bar');
  const section = bar.dataset.section;
  if (!reviewData[section]) reviewData[section] = {};

  // Toggle — clicking same reaction again removes it
  if (reviewData[section].reaction === type) {
    reviewData[section].reaction = null;
    bar.querySelector('.review-up').classList.remove('active');
    bar.querySelector('.review-down').classList.remove('active');
  } else {
    reviewData[section].reaction = type;
    bar.querySelector('.review-up').classList.toggle('active', type === 'up');
    bar.querySelector('.review-down').classList.toggle('active', type === 'down');
  }
  saveReviewData();
};

window.toggleComment = function(btn) {
  const bar = btn.closest('.review-bar');
  const box = bar.querySelector('.review-comment-box');
  const isOpen = box.style.display !== 'none';
  box.style.display = isOpen ? 'none' : 'block';
  if (!isOpen) {
    box.querySelector('textarea').focus();
  }
};

window.saveComment = function(textarea) {
  const bar = textarea.closest('.review-bar');
  const section = bar.dataset.section;
  if (!reviewData[section]) reviewData[section] = {};
  reviewData[section].comment = textarea.value;

  // Update comment button indicator
  const commentBtn = bar.querySelector('.review-comment-btn');
  commentBtn.classList.toggle('has-comment', textarea.value.trim().length > 0);
  saveReviewData();
};

window.copyReview = function() {
  const sections = document.querySelectorAll('.section[id]');
  let output = '# Plan Review: ' + document.title + '\n\n';
  let hasContent = false;

  sections.forEach(section => {
    const id = section.id;
    const data = reviewData[id];
    if (!data || (!data.reaction && !data.comment)) return;
    hasContent = true;

    const title = section.querySelector('.section-title, .hero-title');
    const titleText = title ? title.textContent : id;

    output += '## ' + titleText + '\n';
    if (data.reaction) {
      output += '- **Reaction:** ' + (data.reaction === 'up' ? '👍' : '👎') + '\n';
    }
    if (data.comment && data.comment.trim()) {
      output += '- **Comment:** "' + data.comment.trim() + '"\n';
    }
    output += '\n';
  });

  if (!hasContent) return;

  navigator.clipboard.writeText(output).then(() => {
    const toast = document.getElementById('toast');
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 3000);
  });
};

// Restore saved state on load
function restoreReviewState() {
  document.querySelectorAll('.review-bar').forEach(bar => {
    const section = bar.dataset.section;
    const data = reviewData[section];
    if (!data) return;

    if (data.reaction === 'up') bar.querySelector('.review-up').classList.add('active');
    if (data.reaction === 'down') bar.querySelector('.review-down').classList.add('active');
    if (data.comment) {
      const textarea = bar.querySelector('.review-textarea');
      textarea.value = data.comment;
      bar.querySelector('.review-comment-btn').classList.toggle('has-comment', data.comment.trim().length > 0);
    }
  });
  updateCopyButton();
}

restoreReviewState();
```

### Clipboard Output Format

When the user clicks "Copy Review", this is what gets copied — formatted for Claude to read and act on:

```markdown
# Plan Review: CodeOrb

## The Experience
- **Reaction:** 👍
- **Comment:** "Love the build animation, this is the TikTok moment"

## Scanner Pipeline
- **Reaction:** 👎
- **Comment:** "tree-sitter too heavy, use regex first"

## Chat & AI
- **Reaction:** 👎
- **Comment:** "Skip voice input for v1"
```

### Rules
- The review toolbar MUST appear on every section (including the hero)
- The "Copy Review" button only appears after the user leaves at least one reaction or comment
- Review state persists in localStorage so the user can close and reopen the page
- The toast message says "Review copied to clipboard — paste into Claude" to guide the user
- Keep the review UI minimal and unobtrusive — it should not distract from reading the plan
- The review bar sits below the section content, separated by a thin border-top
- SVG icons are inline (no icon library dependencies)
