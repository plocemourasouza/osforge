# Node.js Best Practices

**Trigger:** Node.js, Express patterns, async Node, Node architecture

---

## Project Structure

```
src/
├── index.ts              # Entry point
├── config/
│   └── index.ts          # Configuration
├── api/
│   ├── routes/
│   │   └── users.ts
│   ├── middleware/
│   │   ├── auth.ts
│   │   └── error.ts
│   └── controllers/
│       └── users.ts
├── services/
│   └── user.service.ts
├── repositories/
│   └── user.repository.ts
├── models/
│   └── user.ts
├── utils/
│   └── logger.ts
└── types/
    └── index.ts
```

---

## Async Patterns

### Promises
```typescript
// Sequential
async function processSequential(items: string[]) {
  const results = []
  for (const item of items) {
    results.push(await processItem(item))
  }
  return results
}

// Parallel
async function processParallel(items: string[]) {
  return Promise.all(items.map(processItem))
}

// Parallel with limit
import pLimit from 'p-limit'

async function processWithLimit(items: string[], concurrency = 5) {
  const limit = pLimit(concurrency)
  return Promise.all(items.map(item => limit(() => processItem(item))))
}
```

### Error Handling
```typescript
// Wrapper for async route handlers
const asyncHandler = (fn: RequestHandler): RequestHandler => {
  return (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next)
  }
}

// Usage
app.get('/users', asyncHandler(async (req, res) => {
  const users = await userService.getAll()
  res.json(users)
}))

// Central error handler
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error(err.stack)
  res.status(500).json({ error: 'Something went wrong' })
})
```

---

## Configuration

```typescript
// config/index.ts
import { z } from 'zod'

const configSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']),
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  REDIS_URL: z.string().url().optional(),
})

export const config = configSchema.parse(process.env)

// Fail fast if config is invalid
```

---

## Security

### Input Validation
```typescript
import { z } from 'zod'

const createUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).max(100),
  name: z.string().min(1).max(100),
})

app.post('/users', asyncHandler(async (req, res) => {
  const data = createUserSchema.parse(req.body)
  const user = await userService.create(data)
  res.status(201).json(user)
}))
```

### Rate Limiting
```typescript
import rateLimit from 'express-rate-limit'

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per window
  standardHeaders: true,
  legacyHeaders: false,
})

app.use('/api', limiter)

// Stricter for auth
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  message: 'Too many login attempts',
})

app.use('/auth/login', authLimiter)
```

### Helmet
```typescript
import helmet from 'helmet'

app.use(helmet())
```

---

## Database Patterns

### Repository Pattern
```typescript
// repositories/user.repository.ts
import { prisma } from '@/lib/prisma'
import { User, Prisma } from '@prisma/client'

export const userRepository = {
  async findById(id: string): Promise<User | null> {
    return prisma.user.findUnique({ where: { id } })
  },

  async findByEmail(email: string): Promise<User | null> {
    return prisma.user.findUnique({ where: { email } })
  },

  async create(data: Prisma.UserCreateInput): Promise<User> {
    return prisma.user.create({ data })
  },

  async update(id: string, data: Prisma.UserUpdateInput): Promise<User> {
    return prisma.user.update({ where: { id }, data })
  },

  async delete(id: string): Promise<void> {
    await prisma.user.delete({ where: { id } })
  },
}
```

### Service Layer
```typescript
// services/user.service.ts
import { userRepository } from '@/repositories/user.repository'
import { hashPassword, verifyPassword } from '@/utils/crypto'

export const userService = {
  async create(data: CreateUserInput): Promise<User> {
    const existing = await userRepository.findByEmail(data.email)
    if (existing) {
      throw new ConflictError('Email already exists')
    }

    const hashedPassword = await hashPassword(data.password)
    return userRepository.create({
      ...data,
      password: hashedPassword,
    })
  },

  async authenticate(email: string, password: string): Promise<User> {
    const user = await userRepository.findByEmail(email)
    if (!user) {
      throw new AuthError('Invalid credentials')
    }

    const valid = await verifyPassword(password, user.password)
    if (!valid) {
      throw new AuthError('Invalid credentials')
    }

    return user
  },
}
```

---

## Logging

```typescript
// utils/logger.ts
import pino from 'pino'

export const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport: process.env.NODE_ENV === 'development'
    ? { target: 'pino-pretty' }
    : undefined,
})

// Usage
logger.info({ userId: user.id }, 'User created')
logger.error({ err, requestId }, 'Request failed')
```

### Request Logging
```typescript
import pinoHttp from 'pino-http'

app.use(pinoHttp({
  logger,
  customLogLevel: (req, res, err) => {
    if (res.statusCode >= 500) return 'error'
    if (res.statusCode >= 400) return 'warn'
    return 'info'
  },
  customSuccessMessage: (req, res) => {
    return `${req.method} ${req.url} completed`
  },
}))
```

---

## Graceful Shutdown

```typescript
import { Server } from 'http'

let server: Server

async function startServer() {
  server = app.listen(config.PORT, () => {
    logger.info(`Server running on port ${config.PORT}`)
  })
}

async function shutdown(signal: string) {
  logger.info(`${signal} received, shutting down`)

  server.close(() => {
    logger.info('HTTP server closed')
  })

  // Close database connections
  await prisma.$disconnect()

  // Close Redis connections
  await redis.quit()

  process.exit(0)
}

process.on('SIGTERM', () => shutdown('SIGTERM'))
process.on('SIGINT', () => shutdown('SIGINT'))

startServer()
```

---

## Best Practices

1. **Validate all input** with Zod or similar
2. **Use async/await** over callbacks
3. **Central error handling** middleware
4. **Environment-based config** validated at startup
5. **Structured logging** with context
6. **Graceful shutdown** handling
7. **Health check endpoint** for load balancers
8. **Security headers** with Helmet
9. **Rate limiting** on sensitive endpoints
10. **Separation of concerns** (routes → controllers → services → repositories)
