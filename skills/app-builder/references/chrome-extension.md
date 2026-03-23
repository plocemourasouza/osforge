---
name: chrome-extension
description: Chrome Extension template principles. Manifest V3, React, TypeScript.
---

# Chrome Extension Template

## Tech Stack

| Component | Technology |
|-----------|------------|
| Manifest | V3 |
| UI | React 18 |
| Language | TypeScript |
| Styling | Tailwind CSS |
| Bundler | Vite |
| Storage | Chrome Storage API |

---

## Directory Structure

```
project-name/
├── src/
│   ├── popup/           # Extension popup
│   ├── options/         # Options page
│   ├── background/      # Service worker
│   ├── content/         # Content scripts
│   ├── components/
│   ├── hooks/
│   └── lib/
│       ├── storage.ts   # Chrome storage helpers
│       └── messaging.ts # Message passing
├── public/
│   ├── icons/
│   └── manifest.json
└── package.json
```

---

## Manifest V3 Concepts

| Component | Purpose |
|-----------|---------|
| Service Worker | Background processing |
| Content Scripts | Page injection |
| Popup | User interface |
| Options Page | Settings |

---

## Permissions

| Permission | Use |
|------------|-----|
| storage | Save user data |
| activeTab | Current tab access |
| scripting | Inject scripts |
| host_permissions | Site access |

---

## Development Tips

| Task | Method |
|------|--------|
| Debug Popup | Right-click icon → Inspect |
| Debug Background | Extensions page → Service worker |
| Debug Content | DevTools console on page |
| Hot Reload | `npm run dev` with watch |

---

## Best Practices

- Use type-safe messaging
- Wrap Chrome APIs in promises
- Minimize permissions
- Handle offline gracefully
