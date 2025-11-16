# Chapter 5: Production Readiness

**Target Audience**: Teams deploying Claude-powered development workflows
**Reading Time**: 25-30 minutes
**Practice Time**: 4-6 hours
**Prerequisites**: Chapters 1-4, production deployment experience

**Learning Objectives**:
- Implement comprehensive monitoring and observability
- Establish logging best practices for AI-generated code
- Optimize costs and manage token budgets
- Handle rate limiting and API quotas
- Secure AI-generated code against OWASP Top 10 vulnerabilities
- Build robust testing strategies
- Design safe deployment patterns

---

## 5.1 Monitoring & Observability

### What to Monitor

**Four Key Metrics**:

**1. Token Usage**
```markdown
**Why Monitor**:
- Claude Code uses 10-100x more tokens than Cursor
- Max plan ($200/month) provides generous limits but not unlimited
- Understanding usage prevents surprise bills
- Identifies inefficient prompts

**What to Track**:
- Tokens per conversation
- Tokens per task type (feature, bug fix, refactor)
- Tokens per developer
- Tokens per project
- Model selection patterns (Sonnet vs. Opus usage)

**How to Track**:
- Anthropic Dashboard: anthropic.com/console
- Token counters: OpenAI tiktoken library (compatible)
- Custom logging: Log prompt + response tokens per session
```

**2. Quality Metrics**
```markdown
**What to Track**:
- Test coverage (before vs. after Claude changes)
- Type safety errors (TypeScript error count)
- Linting errors (ESLint, Prettier)
- Build success rate
- Code review iterations (how many fixes needed)

**Tools**:
- Jest coverage reports
- TypeScript compiler (--noEmit for validation)
- ESLint JSON output
- CI/CD success rates
```

**3. Error Rates**
```markdown
**What to Track**:
- Runtime errors in AI-generated code
- API failures (Anthropic API downtime)
- MCP server connection failures
- Tool timeout rates

**Implementation**:
- Error tracking: Sentry, Rollbar, or similar
- Tag AI-generated code: Add comments marking Claude-written sections
- Separate dashboards: AI-generated vs. human-written error rates
```

**4. Latency & Performance**
```markdown
**What to Track**:
- Average response time per model (Sonnet vs. Opus)
- MCP tool call latencies
- Time to first token (streaming)
- Total conversation time

**Why It Matters**:
- Identifies slow MCPs (optimize or replace)
- Tracks API performance degradation
- Measures developer productivity impact
```

### Dashboard Example

**Metrics Dashboard** (example structure):
```markdown
## Claude Code Usage (Last 7 Days)

**Token Usage**:
- Total: 8.2M tokens ($41.50 estimated cost)
- Sonnet: 6.1M tokens (75%)
- Opus: 2.1M tokens (25%)
- Average per session: 180K tokens
- Costliest session: 1.2M tokens (investigate!)

**Quality Metrics**:
- Test coverage: 87% (↑ 3% from last week)
- TypeScript errors: 0 (✅)
- ESLint errors: 12 (↓ 8 from last week)
- Build success rate: 98%

**Developer Productivity**:
- Features completed: 23
- Bugs fixed: 47
- Average time per feature: 2.3 hours (↓ 1.2 hours)

**MCP Server Health**:
- Context7: 99.8% uptime, 0.8s avg latency
- Supabase: 99.2% uptime, 2.1s avg latency
- Playwright: 94.5% uptime, 8.3s avg latency (⚠️ investigate)
```

---

## 5.2 Logging Best Practices

### What to Log

**Three Levels of Logging**:

**1. High-Level Sessions**
```typescript
// Log each Claude Code session
{
  "session_id": "sess_abc123",
  "timestamp": "2025-11-14T10:00:00Z",
  "developer": "alice@company.com",
  "project": "main-app",
  "model": "claude-sonnet-4",
  "duration_seconds": 1847,
  "tokens_used": 245000,
  "cost_usd": 0.12,
  "tasks_completed": ["feature-auth", "bugfix-validation"],
  "outcome": "success"
}
```

**2. Individual Prompts**
```typescript
// Log each significant prompt/response pair
{
  "session_id": "sess_abc123",
  "prompt_id": "prompt_xyz789",
  "timestamp": "2025-11-14T10:15:00Z",
  "prompt_text": "Implement user roles with RBAC...",  // First 500 chars
  "prompt_tokens": 12500,
  "response_tokens": 18300,
  "files_modified": [
    "app/api/users/route.ts",
    "lib/auth.ts",
    "types/user.ts"
  ],
  "task_type": "feature_implementation",
  "plan_mode": true,
  "model": "claude-opus-4"
}
```

**3. Tool Calls**
```typescript
// Log MCP server usage
{
  "session_id": "sess_abc123",
  "prompt_id": "prompt_xyz789",
  "timestamp": "2025-11-14T10:16:30Z",
  "tool": "context7",
  "action": "fetch_docs",
  "params": { "library": "react-query", "version": "v5" },
  "latency_ms": 820,
  "success": true,
  "bytes_returned": 15420
}
```

### Privacy & PII Considerations

**What NOT to Log**:
- ❌ API keys, secrets, tokens
- ❌ User passwords (even hashed)
- ❌ PII: emails, names, addresses (unless necessary and secured)
- ❌ Full codebase content (too large, may contain secrets)

**What TO Log**:
- ✅ Prompt summaries (first 500 chars)
- ✅ File paths modified
- ✅ Task types and outcomes
- ✅ Token usage and costs
- ✅ Error messages (sanitized)

**Implementation**:
```typescript
// Sanitize logs before storing
function sanitizeLog(log: Log): SanitizedLog {
  return {
    ...log,
    prompt_text: log.prompt_text
      .slice(0, 500)  // Truncate
      .replace(/api[_-]?key[=:]\s*[\w-]+/gi, 'API_KEY=***')  // Redact keys
      .replace(/password[=:]\s*\S+/gi, 'PASSWORD=***'),  // Redact passwords
    response_text: undefined,  // Don't log full responses (too large)
    files_modified: log.files_modified.map(f => f.replace(/\/Users\/\w+/, '/Users/***'))  // Anonymize paths
  };
}
```

### Log Storage & Retention

**Recommended Strategy**:
```markdown
**Short-Term** (7 days):
- Detailed logs (prompts, responses, files)
- Queryable for debugging recent issues
- Storage: PostgreSQL, MongoDB, or similar

**Medium-Term** (90 days):
- Aggregated metrics (tokens, costs, outcomes)
- Compressed logs (summaries only)
- Storage: Time-series DB (InfluxDB, TimescaleDB)

**Long-Term** (1+ years):
- High-level metrics only (daily totals)
- Cost tracking and trends
- Storage: Data warehouse (BigQuery, Snowflake)
```

---

## 5.3 Cost Optimization

### Understanding Claude Code Costs

**Pricing Reality** (Max Plan):
```markdown
**Max Plan**: $200/month
- Generous token allowance
- Can support 40-60 hours/week of intensive use
- Effective cost: $3-5/hour (vs. $50-200/hour developer cost)

**ROI Calculation**:
- If Claude saves 2 hours/week: 2h × $100/hr = $200/week saved
- Monthly savings: $800
- Net benefit: $800 - $200 = $600/month
- ROI: 300%

**Conclusion**: Even heavy usage is cost-effective for productive developers.
```

### Token Optimization Strategies

**1. Model Selection**
```markdown
**Strategy**: Use Sonnet by default, Opus for complex tasks only.

**Sonnet for**:
- Feature implementation (known patterns)
- Bug fixes with clear reproduction
- Refactoring
- Documentation
- Tests

**Opus for**:
- Architecture decisions
- Complex algorithms
- Security reviews
- Performance optimization
- Unfamiliar domains

**Savings**: 40-50% token cost reduction vs. Opus-only approach
```

**2. Sub-Agents for Context Isolation**
```markdown
**Problem**: Main conversation context grows to 150K tokens, includes
irrelevant details from subtasks.

**Solution**: Delegate to sub-agents with focused contexts.

**Example**:
- Main agent: 20K tokens (architecture, coordination)
- Backend sub-agent: 30K tokens (API implementation only)
- Frontend sub-agent: 30K tokens (UI implementation only)
- Testing sub-agent: 20K tokens (test generation only)

**Total**: 100K tokens (focused)
vs.
**Without sub-agents**: 150K tokens (polluted with all subtask details)

**Savings**: 33% token reduction
```

**3. Prompt Optimization**
```markdown
**Technique**: Clear, focused prompts reduce back-and-forth iterations.

**Example**:
❌ Vague prompt: "Add authentication" → 3 clarification rounds → 150K tokens
✅ Clear prompt: "Add NextAuth.js with email/password, PostgreSQL sessions" → Direct implementation → 50K tokens

**Savings**: 66% token reduction through clarity
```

**4. Conversation Cleanup**
```markdown
**Strategy**: Use `/clear` when switching to unrelated tasks.

**Example**:
Session 1: Implement authentication (80K tokens)
[Use /clear]
Session 2: Add analytics dashboard (60K tokens)

vs.

Single session: Both tasks (140K tokens, lots of context pollution)

**Savings**: 15-20% reduction
```

### Budget Alerts

**Implementation**:
```typescript
// Monitor token usage, alert on thresholds
const DAILY_TOKEN_BUDGET = 500000;  // 500K tokens/day
const ALERT_THRESHOLD = 0.8;  // Alert at 80%

let dailyTokensUsed = 0;

function trackTokens(tokens: number) {
  dailyTokensUsed += tokens;

  if (dailyTokensUsed > DAILY_TOKEN_BUDGET * ALERT_THRESHOLD) {
    sendAlert({
      type: 'token_budget_warning',
      used: dailyTokensUsed,
      budget: DAILY_TOKEN_BUDGET,
      percentUsed: (dailyTokensUsed / DAILY_TOKEN_BUDGET * 100).toFixed(1)
    });
  }
}
```

---

## 5.4 Rate Limiting & Quotas

### Anthropic API Rate Limits

**Limits** (as of 2025, check current docs):
```markdown
**Max Plan**:
- Requests per minute: 50-100 (varies)
- Tokens per minute: 100K-200K (varies)
- Concurrent requests: 5-10

**Note**: Limits evolve; always check latest at docs.anthropic.com
```

### Handling Rate Limits

**Exponential Backoff Pattern**:
```typescript
async function callClaudeWithRetry(
  prompt: string,
  maxRetries: number = 4
): Promise<Response> {
  let attempt = 0;

  while (attempt < maxRetries) {
    try {
      return await callClaude(prompt);
    } catch (error) {
      if (error.code === 'RATE_LIMIT_EXCEEDED') {
        attempt++;
        if (attempt >= maxRetries) throw error;

        // Exponential backoff: 2s, 4s, 8s, 16s
        const delay = Math.pow(2, attempt) * 1000;
        console.log(`Rate limited. Retrying in ${delay}ms (attempt ${attempt}/${maxRetries})`);

        await sleep(delay);
      } else {
        throw error;  // Non-rate-limit error
      }
    }
  }

  throw new Error('Max retries exceeded');
}
```

### Queue Management

**For High-Volume Usage**:
```typescript
// Queue system for managing concurrent requests
class ClaudeQueue {
  private queue: Task[] = [];
  private activeRequests = 0;
  private readonly maxConcurrent = 5;

  async enqueue(task: Task): Promise<Response> {
    this.queue.push(task);
    return this.process();
  }

  private async process(): Promise<Response> {
    if (this.activeRequests >= this.maxConcurrent) {
      // Wait for slot to open
      await this.waitForSlot();
    }

    this.activeRequests++;
    const task = this.queue.shift()!;

    try {
      const result = await callClaude(task.prompt);
      return result;
    } finally {
      this.activeRequests--;
      this.processNext();  // Process next in queue
    }
  }
}
```

---

## 5.5 Security Considerations

### OWASP Top 10 for AI-Generated Code

Claude generates high-quality code, but **humans must verify** security.

**Critical Checks**:

**1. SQL Injection**
```typescript
// ❌ AI might generate (if not careful):
const query = `SELECT * FROM users WHERE email = '${userEmail}'`;

// ✅ Always use parameterized queries:
const query = 'SELECT * FROM users WHERE email = $1';
const result = await db.query(query, [userEmail]);
```

**Verification**:
- Use `/review-code` command with security checklist
- Search for string interpolation in SQL queries
- Require ORM usage (Prisma, TypeORM) in `.claude.md`

---

**2. Cross-Site Scripting (XSS)**
```tsx
// ❌ Dangerous:
<div dangerouslySetInnerHTML={{__html: userInput}} />

// ✅ Safe:
<div>{userInput}</div>  // React auto-escapes
// Or use DOMPurify if HTML is needed:
<div dangerouslySetInnerHTML={{__html: DOMPurify.sanitize(userInput)}} />
```

**Verification**:
- Grep for `dangerouslySetInnerHTML`
- Ensure user input is sanitized before rendering
- Use Content Security Policy (CSP) headers

---

**3. Authentication & Authorization**
```typescript
// ❌ Insecure:
function getUser(req: Request) {
  const userId = req.query.userId;  // User-provided!
  return db.user.findUnique({ where: { id: userId } });
}

// ✅ Secure:
function getUser(req: Request) {
  const userId = req.session.userId;  // From authenticated session
  return db.user.findUnique({ where: { id: userId } });
}
```

**Verification**:
- Never trust user input for authentication
- Always verify session/token on server
- Implement role-based access control (RBAC)

---

**4. Secrets Management**
```typescript
// ❌ Hardcoded secrets (AI might do this if not specified):
const stripe = new Stripe('sk_live_abc123...');

// ✅ Environment variables:
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
```

**Verification**:
- Grep codebase for common secret patterns: `api_key`, `secret`, `password`, `sk_live`, `sk_test`
- Use `.env.example` with dummy values
- Add `.env` to `.gitignore`

---

### Security Review Checklist

**File**: `.claude/commands/review-security.md`

```markdown
---
description: Security review checklist for AI-generated code
---

# Security Review Checklist

Review the recently modified code for these vulnerabilities:

## OWASP Top 10

- [ ] **SQL Injection**: All queries parameterized? No string interpolation in SQL?
- [ ] **XSS**: User input sanitized? Avoid `dangerouslySetInnerHTML`?
- [ ] **Broken Authentication**: Sessions validated server-side? No user-provided auth?
- [ ] **Sensitive Data Exposure**: Secrets in environment variables? Not hardcoded?
- [ ] **XXE**: XML parsing disabled or sanitized? (if applicable)
- [ ] **Broken Access Control**: Authorization checks in place? RBAC enforced?
- [ ] **Security Misconfiguration**: HTTPS enforced? Security headers set?
- [ ] **Insecure Deserialization**: User input validated before deserializing?
- [ ] **Insufficient Logging**: Security events logged? PII not logged?
- [ ] **SSRF**: User-provided URLs validated? Internal endpoints protected?

## Additional Checks

- [ ] **CSRF Protection**: POST/PUT/DELETE protected with CSRF tokens?
- [ ] **Rate Limiting**: Authentication endpoints rate-limited?
- [ ] **Input Validation**: All user input validated (zod, joi, etc.)?
- [ ] **Error Messages**: No stack traces exposed to users?
- [ ] **Dependencies**: No known vulnerabilities (run `npm audit`)?

Provide findings with severity (Critical/High/Medium/Low) and remediation.
```

**Usage**:
```bash
# After Claude implements a feature:
/review-security

# Claude performs systematic security review
```

---

## 5.6 Testing Strategies

### Test Coverage for AI-Generated Code

**Philosophy**: AI generates code, humans own it. That includes testing.

**Strategies**:

**1. Validation Gates (Autonomous Testing)**
```markdown
**Pattern**: Sub-agent writes and runs tests until they pass.

**Workflow**:
1. Main agent implements feature
2. Validation gate sub-agent automatically triggers
3. Sub-agent writes comprehensive tests (unit + integration)
4. Sub-agent runs tests
5. If failures: Sub-agent fixes code (not tests) and reruns
6. Repeats until 100% passing
7. Reports coverage and results

**Configuration**: See Chapter 6 (Sub-Agents) for setup
```

**2. Test-Driven Development with Claude**
```markdown
**Workflow**:
1. Write test first (or have Claude write it based on requirements)
2. Test fails (no implementation yet)
3. Have Claude implement feature to make test pass
4. Refactor if needed
5. Repeat

**Example**:
User: "Write a test for a function that validates email addresses.
       Then implement the function to make the test pass."

Claude:
// Step 1: Test
\`\`\`typescript
describe('validateEmail', () => {
  it('should return true for valid emails', () => {
    expect(validateEmail('test@example.com')).toBe(true);
    expect(validateEmail('user+tag@domain.co.uk')).toBe(true);
  });

  it('should return false for invalid emails', () => {
    expect(validateEmail('notanemail')).toBe(false);
    expect(validateEmail('@example.com')).toBe(false);
    expect(validateEmail('test@')).toBe(false);
  });
});
\`\`\`

// Step 2: Implementation
\`\`\`typescript
export function validateEmail(email: string): boolean {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}
\`\`\`

Test result: ✅ All tests passing
```

**3. Testing Requirements in `.claude.md`**
```markdown
# Testing Standards

**All new features MUST include**:
- Unit tests (80%+ coverage)
- Integration tests for API routes
- E2E tests for critical user flows

**Testing Patterns**:
- Use Jest + React Testing Library
- Tests co-located with components (`.test.tsx`)
- Integration tests in `/tests/integration/`
- E2E tests in `/tests/e2e/` (Playwright)

**Before Considering Feature Complete**:
1. All tests passing
2. Coverage meets threshold
3. Edge cases tested
4. Error paths tested
```

---

## 5.7 Deployment Patterns

### Staging Environments for AI Changes

**Best Practice**: Never deploy AI-generated code directly to production without review.

**Recommended Flow**:
```
1. Claude generates code
   ↓
2. Run tests locally
   ↓
3. Commit to feature branch
   ↓
4. Push to staging environment
   ↓
5. Automated tests run (CI/CD)
   ↓
6. Manual QA review
   ↓
7. Code review (human)
   ↓
8. Merge to main
   ↓
9. Deploy to production (gradual rollout)
```

### CI/CD Integration

**GitHub Actions Example**:
```yaml
name: AI-Generated Code Review

on:
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install dependencies
        run: npm install

      - name: Type checking
        run: npm run type-check

      - name: Linting
        run: npm run lint

      - name: Unit tests
        run: npm test -- --coverage

      - name: Coverage threshold
        run: |
          COVERAGE=$(jq -r '.total.lines.pct' coverage/coverage-summary.json)
          if [ $(echo "$COVERAGE < 80" | bc) -eq 1 ]; then
            echo "Coverage is below 80% ($COVERAGE%)"
            exit 1
          fi

      - name: Security audit
        run: npm audit --audit-level=moderate

      - name: Build
        run: npm run build

      # Tag AI-generated PRs for extra scrutiny
      - name: Label AI PR
        if: contains(github.event.pull_request.title, 'AI:') || contains(github.event.pull_request.title, 'Claude:')
        run: |
          gh pr edit ${{ github.event.pull_request.number }} --add-label "ai-generated,needs-security-review"
```

### Gradual Rollouts

**Pattern**: Deploy to subset of users first, monitor, then full rollout.

**Implementation** (with feature flags):
```typescript
// Feature flag for AI-generated feature
const featureConfig = {
  "new-user-roles": {
    enabled: true,
    rolloutPercentage: 10,  // Start with 10% of users
    aiGenerated: true,
    monitoring: {
      errorRateThreshold: 0.01,  // Alert if error rate > 1%
      rollbackOnThreshold: true
    }
  }
};

// Usage
if (isFeatureEnabled('new-user-roles', user.id)) {
  // New AI-generated role system
} else {
  // Old system
}
```

**Rollout Schedule**:
```markdown
Day 1: 10% of users (monitor closely)
Day 2: 25% of users (if stable)
Day 3: 50% of users (if stable)
Day 5: 100% of users (full rollout)

If errors spike at any point:
- Automatic rollback to 0%
- Alert on-call engineer
- Investigate and fix
- Restart gradual rollout
```

---

## 5.8 Production Checklist

Use this checklist before deploying AI-generated code to production:

### Pre-Deployment Checklist

```markdown
## Code Quality
- [ ] All tests passing (unit, integration, E2E)
- [ ] Test coverage ≥ 80%
- [ ] TypeScript errors: 0
- [ ] ESLint errors: 0
- [ ] Build successful

## Security
- [ ] Security review completed (`/review-security`)
- [ ] No hardcoded secrets (grep for common patterns)
- [ ] All user input validated
- [ ] SQL queries parameterized (no string interpolation)
- [ ] XSS vulnerabilities addressed
- [ ] Authentication/authorization verified
- [ ] `npm audit` shows no high/critical vulnerabilities

## Performance
- [ ] No N+1 database queries
- [ ] API endpoints respond < 200ms (P95)
- [ ] Frontend bundle size acceptable
- [ ] Images optimized
- [ ] Proper caching headers

## Monitoring
- [ ] Error tracking configured (Sentry, Rollbar)
- [ ] Logging in place
- [ ] Dashboards updated with new metrics
- [ ] Alerts configured for critical paths

## Documentation
- [ ] README updated (if applicable)
- [ ] API documentation current
- [ ] Inline code comments for complex logic
- [ ] Deployment notes added

## Deployment
- [ ] Staging deployment successful
- [ ] Manual QA completed
- [ ] Rollback plan documented
- [ ] Feature flags configured (gradual rollout)
- [ ] On-call engineer notified

## Post-Deployment
- [ ] Monitor error rates (first 1 hour)
- [ ] Check performance metrics
- [ ] Verify user flows work as expected
- [ ] Review logs for unexpected issues
```

---

## 5.9 Key Takeaways

**Monitoring**:
- ✅ Track tokens, quality metrics, errors, latency
- ✅ Build dashboards for visibility
- ✅ Set up budget alerts

**Logging**:
- ✅ Log sessions, prompts (sanitized), tool calls
- ✅ Respect privacy (no PII, secrets)
- ✅ Retain: 7 days detailed, 90 days aggregated, 1+ years metrics

**Cost Optimization**:
- ✅ Sonnet default, Opus for complex tasks (40-50% savings)
- ✅ Sub-agents for context isolation (33% reduction)
- ✅ Clear prompts reduce iterations (66% savings potential)

**Security**:
- ✅ Review AI code for OWASP Top 10
- ✅ Use `/review-security` command
- ✅ Never trust AI for security-critical decisions without verification

**Testing**:
- ✅ Validation gates for autonomous testing
- ✅ 80%+ coverage requirement
- ✅ Test requirements in `.claude.md`

**Deployment**:
- ✅ Staging → QA → Code Review → Production
- ✅ CI/CD integration with quality gates
- ✅ Gradual rollouts with monitoring
- ✅ Rollback plan always ready

---

## 5.10 Practice Exercises

**Exercise 1: Set Up Monitoring**
- Track token usage for one week
- Build a simple dashboard (spreadsheet or actual dashboard)
- Identify your costliest tasks
- Optimize one high-token workflow

**Exercise 2: Security Review**
- Create `/review-security` command
- Have Claude implement a feature
- Run security review
- Fix any issues found

**Exercise 3: Testing Strategy**
- Configure testing requirements in `.claude.md`
- Have Claude implement a feature with tests
- Verify coverage meets threshold
- Set up CI/CD integration

**Exercise 4: Deployment Pipeline**
- Create feature branch for AI changes
- Set up basic CI/CD (GitHub Actions or similar)
- Deploy to staging
- Practice rollback procedure

**Exercise 5: Cost Analysis**
- Analyze one week of token usage
- Identify opportunities for optimization
- Implement sub-agents for one complex task
- Measure token reduction

---

**Congratulations!** You've completed the core Claude Coding Master Playbook chapters. You now have:

- ✅ Foundation and setup mastery
- ✅ Advanced prompting techniques (20-30% improvements)
- ✅ Architecture patterns for robust workflows
- ✅ Tool integration with MCPs
- ✅ Production-ready deployment strategies

**Next Steps**:
- Practice these techniques daily
- Build your custom command library
- Share learnings with your team
- Contribute patterns back to the community

---

**Word Count**: ~3,950 words
**Reading Time**: 26 minutes
**Implementation Time**: 4-6 hours

**Validation**:
- Code Review Patterns: High confidence (4+ sources)
- Security Practices: Industry standard (OWASP)
- Testing Strategies: Community validated
- Deployment Patterns: Production proven

**Sources**:
- Pattern Confidence Matrix (11 sources)
- "A Complete Guide to Claude Code"
- "800+ hours Learning Claude Code"
- OWASP Top 10
- Anthropic Best Practices
- Production deployment case studies
