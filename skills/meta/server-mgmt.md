# Server Management

**Trigger:** Server management, process management, monitoring, health checks, scaling.

---

## Process Management Tools

| Tool | Use Case |
|------|----------|
| **PM2** | Node.js process manager |
| **systemd** | Linux service management |
| **Docker** | Containerization |
| **Kubernetes** | Container orchestration |

---

## PM2 Basics

```bash
# Start application
pm2 start npm --name "my-app" -- start

# Start with ecosystem file
pm2 start ecosystem.config.js

# Common commands
pm2 list              # List processes
pm2 logs my-app       # View logs
pm2 restart my-app    # Restart
pm2 stop my-app       # Stop
pm2 delete my-app     # Remove

# Monitoring
pm2 monit             # Real-time monitoring
```

### Ecosystem File
```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'my-app',
    script: 'npm',
    args: 'start',
    instances: 'max',
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'production',
    },
  }],
}
```

---

## Monitoring Strategy

### Metrics to Track
- **Response time** — p50, p95, p99
- **Error rate** — 4xx, 5xx responses
- **CPU usage** — Per process, total
- **Memory usage** — Heap, RSS
- **Request volume** — Requests per second

### Tools
| Tool | Purpose |
|------|---------|
| **Sentry** | Error tracking |
| **Datadog** | APM, infrastructure |
| **Vercel Analytics** | Web vitals |
| **Prometheus + Grafana** | Self-hosted metrics |

---

## Health Checks

```typescript
// Kubernetes liveness probe
app.get('/health/live', (req, res) => {
  res.status(200).json({ status: 'alive' })
})

// Kubernetes readiness probe
app.get('/health/ready', async (req, res) => {
  try {
    await db.query('SELECT 1')
    res.status(200).json({ status: 'ready' })
  } catch {
    res.status(503).json({ status: 'not ready' })
  }
})
```

---

## Scaling Decisions

### Vertical Scaling
- Add more CPU/RAM to existing server
- Simple, but has limits
- Good for: Database servers

### Horizontal Scaling
- Add more servers
- Requires load balancing
- Good for: Stateless applications

### Auto-scaling
```yaml
# Vercel: Automatic
# Fly.io
[[services]]
  internal_port = 3000
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 1

  [services.concurrency]
    type = "connections"
    hard_limit = 25
    soft_limit = 20
```

---

## Observability

### Structured Logging
```typescript
import pino from 'pino'

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label }),
  },
})

// Usage
logger.info({ userId, action: 'login' }, 'User logged in')
logger.error({ error, requestId }, 'Request failed')
```

### Log Format
```json
{
  "level": "info",
  "timestamp": "2024-01-15T10:30:00Z",
  "message": "User logged in",
  "userId": "user_123",
  "action": "login",
  "requestId": "req_abc"
}
```
