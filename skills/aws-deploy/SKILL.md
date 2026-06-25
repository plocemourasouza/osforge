---
name: aws-deploy
description: "Deploy to AWS — pick the right service (Amplify, App Runner, ECS/Fargate, Lambda, S3+CloudFront), with least-privilege IAM, managed secrets, and rollback. Use when: deploying to AWS, choosing an AWS compute/hosting service, IAM/secrets for a deploy, CI/CD to AWS, or moving off Vercel to AWS. Keywords: AWS, deploy AWS, ECS, Fargate, Lambda, Amplify, App Runner, S3 CloudFront, IAM, Secrets Manager. Do NOT use for: Vercel (vercel-deploy), generic deploy discipline (deployment-procedures), infra-as-code authoring of unrelated stacks."
model: sonnet
allowed-tools: Read, Grep, Glob, Edit, Bash
metadata:
  version: "1.0.0"
  note: "AWS service APIs/CLI change constantly. This skill is the decision discipline; for current CLI/service syntax use Context7 (context7-docs-first) / AWS docs."
---

# AWS Deploy (service choice · IAM · secrets · rollback)

**Iron Law:** `LEAST-PRIVILEGE IAM AND MANAGED SECRETS — NO CREDENTIALS IN CODE, REPO, OR COMMITTED ENV FILES`

> **Current API:** AWS CLI flags and service options change often. For exact commands and service config, **use Context7** (`context7-docs-first`) / AWS docs — this skill is the decision framework.

## When NOT to use
- Deploying to Vercel → use `vercel-deploy`
- Provider-agnostic deploy discipline (rollback triggers, checklists) → `deployment-procedures`
- Local/dev environment setup → `server-management`

## Process
### 1. Pick the service by workload
Match the app to the simplest fit: **S3 + CloudFront** (static/SPA), **Amplify / App Runner** (managed web apps, low ops), **ECS/Fargate** (containers, control), **Lambda** (event/edge, spiky). Record the choice as an ADR.
**Done when:** the chosen service is justified in one or two sentences against the workload.

### 2. IAM least-privilege
Create a deploy role scoped to exactly the actions/resources needed — no wildcards in production. Humans assume roles; CI uses OIDC (no long-lived keys).
**Done when:** the deploy succeeds and the policy has no `"*"` action on a real resource.

### 3. Secrets & config
Store secrets in SSM Parameter Store / Secrets Manager and inject at runtime. Never bake secrets into images, code, or committed `.env`.
**Done when:** a grep of the image/repo shows zero secrets; the app reads them at runtime.

### 4. Deploy + rollback
Automate the deploy in CI; define the rollback trigger and the previous-version target **before** shipping (App Runner/ECS revision, Lambda alias, CloudFront invalidation).
**Done when:** a rollback path is documented and verified on the chosen service.

## Anti-patterns
| WRONG | RIGHT |
|---|---|
| `AdministratorAccess` for the deploy role | Scoped least-privilege policy |
| Long-lived access keys in CI | OIDC role assumption |
| Secrets in the Docker image / `.env` commit | SSM / Secrets Manager at runtime |
| Shipping without a rollback target | Rollback trigger + target defined first |

## References
- Current CLI/service config → **Context7** (`context7-docs-first`) / AWS docs
- Vercel alternative → `skills/vercel-deploy`
- Rollback/verification discipline → `skills/deployment-procedures`
- Secrets/IAM hygiene → `skills/security-best-practices`
