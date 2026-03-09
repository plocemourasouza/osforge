---
name: i18n-localization
description: Internationalization for Next.js applications. Trigger on multi-language support, locale routing, translation management, date/currency formatting, RTL support, or next-intl/i18next configuration.
metadata:
  author: osforge
  version: '1.0'
---

# i18n & Localization (Next.js)

## Recommended Stack
`next-intl` — best integration with App Router + Server Components.

## Setup
```typescript
// i18n/request.ts
import { getRequestConfig } from 'next-intl/server'

export default getRequestConfig(async ({ requestLocale }) => {
  const locale = await requestLocale ?? 'pt-BR'
  return {
    locale,
    messages: (await import(`../messages/${locale}.json`)).default,
  }
})
```

```typescript
// middleware.ts
import createMiddleware from 'next-intl/middleware'

export default createMiddleware({
  locales: ['pt-BR', 'en', 'es'],
  defaultLocale: 'pt-BR',
  localePrefix: 'as-needed', // /en/about but /about for pt-BR
})
```

## Translation Files
```jsonc
// messages/pt-BR.json
{
  "common": {
    "save": "Salvar",
    "cancel": "Cancelar",
    "loading": "Carregando..."
  },
  "dashboard": {
    "title": "Painel de Controle",
    "welcome": "Olá, {name}!",
    "projects": "{count, plural, =0 {Nenhum projeto} one {# projeto} other {# projetos}}"
  }
}
```

## Usage in Components
```typescript
// Server Component
import { useTranslations } from 'next-intl'

export default function Dashboard() {
  const t = useTranslations('dashboard')
  return <h1>{t('title')}</h1>
}

// With interpolation
<p>{t('welcome', { name: user.name })}</p>

// Plurals
<p>{t('projects', { count: projects.length })}</p>
```

## Date & Currency Formatting
```typescript
import { useFormatter } from 'next-intl'

function PriceDisplay({ amount }: { amount: number }) {
  const format = useFormatter()
  return (
    <>
      <span>{format.number(amount, { style: 'currency', currency: 'BRL' })}</span>
      <time>{format.dateTime(new Date(), { dateStyle: 'long' })}</time>
      <span>{format.relativeTime(new Date('2024-01-01'))}</span>
    </>
  )
}
```

## Best Practices
- Translation keys: `namespace.context.element` (e.g., `billing.invoice.title`)
- NEVER hardcode user-facing strings — even "OK" and "Cancel"
- Use ICU MessageFormat for plurals, gender, select
- Extract translations with `next-intl` CLI or i18n-ally VSCode extension
- Keep `defaultLocale` as the primary language (pt-BR for Paulo's projects)
- Test RTL with `dir="rtl"` on `<html>` even if not needed now
