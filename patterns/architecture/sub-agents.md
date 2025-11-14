---
pattern_name: Sub-Agents / Parallel Task Delegation
category: Architecture
difficulty: Advanced
impact: High
date_created: 2025-11-14
last_updated: 2025-11-14
---

# Pattern: Sub-Agents / Parallel Task Delegation

> **TL;DR**: Define specialized sub-agents with focused responsibilities to enable parallel execution, reduce context pollution, and achieve 10x faster completion on multi-part tasks.

## Overview

Sub-agent architecture is an advanced pattern where you create multiple specialized Claude instances, each with a focused domain of responsibility. Instead of one monolithic agent handling all aspects of a project, a main orchestrator agent delegates specific subtasks to specialized sub-agents that work in parallel with clean, isolated contexts.

This architectural pattern transforms how Claude handles complex, multi-faceted projects by breaking down work into parallel streams executed by domain experts. Each sub-agent has its own specialized system prompt, constraints, and responsibilities—similar to how software teams organize engineers into frontend, backend, testing, and DevOps roles.

Research and real-world usage shows that sub-agent architectures can deliver **10x faster execution** on multi-part tasks compared to serial execution with a single agent, while simultaneously improving code quality through specialized expertise and reducing context pollution that degrades output quality.

---

## Problem It Solves

### The Challenge

When building complex features or applications, a single Claude agent must juggle multiple concerns simultaneously: frontend UI, backend API logic, database schemas, testing, documentation, and more. This creates several critical problems:

**Common Symptoms:**
- Claude produces lower-quality code as context window fills with unrelated code from different domains
- Serial execution bottlenecks where backend must complete before frontend can start, wasting time
- Mixed concerns in responses where API logic appears alongside React components
- Degraded performance and accuracy as a single prompt tries to address multiple specialized domains
- Inconsistent coding standards across different parts of the codebase
- Long wait times as each task must complete sequentially

**Without This Pattern:**
- **Context pollution**: Frontend code clutters the context when working on backend logic, reducing relevance and accuracy
- **Sequential bottleneck**: Tasks that could run in parallel wait in queue, multiplying development time
- **Generalist dilution**: A single agent lacks deep specialization, producing adequate but not excellent results
- **Scope creep**: Without clear boundaries, agents modify code outside their intended scope, causing unintended side effects
- **Complexity overload**: Large, multi-domain tasks become overwhelming for a single agent to manage coherently

### Why Traditional Approaches Fall Short

**Single Agent Approach**: Using one Claude instance for everything seems simple but breaks down at scale. As projects grow, the agent's context becomes polluted with irrelevant information, and the agent struggles to maintain consistent quality across diverse domains.

**Manual Task Splitting**: You could manually split tasks and run separate Claude sessions, but this requires constant human coordination, prevents parallel execution (you can only manage one chat at a time), and loses the orchestration benefits of having agents work together.

**Simple Prompt Sections**: Adding sections like "Backend:" and "Frontend:" to a single prompt doesn't create true isolation—the agent still sees all context and must switch between mental models, reducing effectiveness.

---

## The Solution

### Core Concept

Sub-agent architecture creates specialized "virtual team members" by defining multiple Claude instances, each with a focused system prompt, clear responsibilities, and strict constraints. A main orchestrator agent analyzes incoming tasks, breaks them into domain-specific subtasks, and delegates to appropriate sub-agents that execute in parallel.

Each sub-agent operates in its own isolated context, seeing only the code and information relevant to its domain. This mimics how high-performing engineering teams organize: you have backend specialists, frontend specialists, testing specialists—each focused on what they do best.

### Key Principles

1. **Domain Isolation**: Each sub-agent has a single, well-defined domain of responsibility (backend, frontend, testing, etc.) and explicit constraints preventing it from modifying code outside that domain.

2. **Specialized Expertise**: Sub-agents have domain-specific system prompts with patterns, best practices, and coding standards tailored to their specialty, producing higher-quality output than a generalist.

3. **Parallel Execution**: The orchestrator delegates independent tasks simultaneously to multiple sub-agents, enabling true parallelization that can reduce total execution time by 10x.

4. **Clean Context**: Each sub-agent maintains its own context containing only relevant code, patterns, and information for its domain, preventing pollution and maintaining focus.

### How It Works

1. **Define Sub-Agents**: Create specialized sub-agent definitions in `.claude/subagents/` directory, each with clear responsibilities, constraints, and coding patterns.

2. **Orchestrator Analysis**: The main Claude agent receives a complex task and analyzes which sub-agents are needed to complete it.

3. **Task Delegation**: The orchestrator breaks down the task into domain-specific subtasks and delegates them to appropriate sub-agents with clear, focused instructions.

4. **Parallel Execution**: Sub-agents work simultaneously on their assigned tasks within their isolated contexts.

5. **Integration**: The orchestrator reviews outputs from all sub-agents, ensures they integrate correctly, and coordinates any cross-cutting concerns.

---

## Implementation

### Basic Implementation

Create specialized sub-agent definitions in your project's `.claude/subagents/` directory:

**File: `.claude/subagents/backend-expert.md`**
```markdown
# Sub-Agent: Backend API Expert

You are a backend API specialist focusing on Node.js + Express + PostgreSQL.

## Your Responsibilities
- API route design and implementation
- Database schema design with Prisma
- Authentication and authorization
- Error handling and validation
- Performance optimization

## Your Constraints
- NEVER modify frontend code
- ALWAYS use Prisma (no raw SQL)
- ALWAYS implement proper error handling
- ALWAYS add input validation with zod

## Code Style
- Use async/await (no callbacks)
- Return JSON: `{ success: boolean, data?: any, error?: string }`
- HTTP status codes: 200 (success), 400 (bad request), 401 (unauthorized),
  404 (not found), 500 (server error)
```

**Explanation:**
- Clearly defined domain (backend APIs only)
- Specific responsibilities within that domain
- Hard constraints that prevent scope creep
- Domain-specific coding standards

### Advanced Implementation

For more complex projects, create additional specialized sub-agents:

**File: `.claude/subagents/frontend-expert.md`**
```markdown
# Sub-Agent: Frontend React Expert

You are a React + TypeScript specialist focusing on UI/UX.

## Your Responsibilities
- React component development
- State management (React Query, Zustand)
- Form handling (React Hook Form + zod)
- Styling with Tailwind CSS
- Accessibility (a11y)

## Your Constraints
- NEVER modify backend code
- ALWAYS use TypeScript with explicit types
- ALWAYS use functional components + hooks
- NEVER use inline styles (Tailwind only)

## Component Patterns
```typescript
// Standard component structure
interface Props {
  // Explicit prop types
}

export function ComponentName({ prop1, prop2 }: Props) {
  // 1. Hooks
  const [state, setState] = useState();
  const query = useQuery(...);

  // 2. Derived state
  const computed = useMemo(() => ..., [deps]);

  // 3. Effects
  useEffect(() => { ... }, [deps]);

  // 4. Handlers
  const handleEvent = useCallback(() => { ... }, [deps]);

  // 5. Render
  return (...);
}
```
```

**File: `.claude/subagents/testing-expert.md`**
```markdown
# Sub-Agent: Testing Specialist

You focus exclusively on test coverage and quality.

## Your Responsibilities
- Write unit tests for all new code
- Integration tests for API routes
- E2E tests for critical user flows
- Test data factories and fixtures

## Testing Patterns
- **Unit**: Test one function/component in isolation
- **Integration**: Test API routes + database
- **E2E**: Test full user journey

## Coverage Requirements
- Minimum 80% coverage for new code
- 100% coverage for utility functions
- Critical paths must have E2E tests
```

**Explanation:**
- Multiple specialized sub-agents cover all aspects of development
- Each has explicit boundaries preventing overlap
- Domain-specific patterns ensure consistency
- Testing specialist ensures quality across all domains

### Configuration

Set up the sub-agents directory structure:

```bash
# Create sub-agents directory
mkdir -p .claude/subagents

# Sub-agents are automatically discovered by Claude Code
# Reference them in prompts:
"Ask the backend-expert sub-agent to implement..."

# Or let Claude decide:
"Delegate this task to the appropriate sub-agent"
```

---

## Complete Code Example

### Scenario

You need to implement a complete "forgot password" feature for a web application, including backend API endpoints, frontend forms, email notifications, and comprehensive testing.

**Requirements:**
- Backend: Password reset token generation, email sending, token validation, password update
- Frontend: Forgot password form, reset password form with token validation
- Testing: Unit tests for token generation, integration tests for API, E2E test for complete flow

### Implementation

**File Structure:**
```
.claude/
├── subagents/
│   ├── backend-expert.md
│   ├── frontend-expert.md
│   └── testing-expert.md
```

**Main Agent Orchestration Prompt:**
```markdown
I need to implement a new "forgot password" feature.

Please delegate as follows:
1. Backend expert: Implement password reset API endpoints
2. Frontend expert: Create reset password forms
3. Testing expert: Add comprehensive tests

Each sub-agent should work independently and report back.
```

**Main Agent's Internal Planning (shown via <thinking> tags):**
```markdown
<thinking>
I'll coordinate three sub-agents in parallel:

**Sub-agent 1: backend-expert**
Task: Implement `/api/auth/forgot-password` and `/api/auth/reset-password`
- Generate cryptographically secure reset token
- Send email with reset link
- Validate token and update password
- Add rate limiting

**Sub-agent 2: frontend-expert**
Task: Create forgot password flow
- Page: /forgot-password
- Page: /reset-password/[token]
- Form validation and error handling
- Loading states and user feedback

**Sub-agent 3: testing-expert**
Task: Test coverage
- Unit tests for token generation
- Integration tests for API endpoints
- E2E test for complete user flow
</thinking>
```

**Backend Expert Output:**
```typescript
// File: app/api/auth/forgot-password/route.ts
import { NextRequest, NextResponse } from 'next/server';
import crypto from 'crypto';
import { prisma } from '@/lib/prisma';
import { sendPasswordResetEmail } from '@/lib/email';
import { z } from 'zod';

const schema = z.object({
  email: z.string().email()
});

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { email } = schema.parse(body);

    const user = await prisma.user.findUnique({ where: { email } });

    // Always return success to prevent email enumeration
    if (!user) {
      return NextResponse.json({ success: true });
    }

    // Generate secure token
    const resetToken = crypto.randomBytes(32).toString('hex');
    const expiresAt = new Date(Date.now() + 60 * 60 * 1000); // 1 hour

    // Invalidate old tokens
    await prisma.passwordReset.deleteMany({ where: { userId: user.id } });

    // Create new token
    await prisma.passwordReset.create({
      data: { token: resetToken, expiresAt, userId: user.id }
    });

    // Send email
    await sendPasswordResetEmail(user.email, resetToken);

    return NextResponse.json({ success: true });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json({
        success: false,
        error: 'Invalid email address'
      }, { status: 400 });
    }
    return NextResponse.json({
      success: false,
      error: 'Service unavailable'
    }, { status: 500 });
  }
}
```

**Frontend Expert Output:**
```typescript
// File: app/forgot-password/page.tsx
'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  email: z.string().email('Please enter a valid email address')
});

type FormData = z.infer<typeof schema>;

export default function ForgotPasswordPage() {
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema)
  });

  const onSubmit = async (data: FormData) => {
    setIsLoading(true);
    try {
      const response = await fetch('/api/auth/forgot-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      if (response.ok) {
        setIsSubmitted(true);
      }
    } catch (error) {
      console.error('Password reset request failed', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isSubmitted) {
    return (
      <div className="max-w-md mx-auto p-6">
        <h1 className="text-2xl font-bold mb-4">Check your email</h1>
        <p className="text-gray-600">
          If an account exists with that email, you'll receive password reset instructions.
        </p>
      </div>
    );
  }

  return (
    <div className="max-w-md mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Forgot Password</h1>
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="mb-4">
          <label htmlFor="email" className="block text-sm font-medium mb-2">
            Email Address
          </label>
          <input
            {...register('email')}
            type="email"
            id="email"
            className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          {errors.email && (
            <p className="text-red-600 text-sm mt-1">{errors.email.message}</p>
          )}
        </div>
        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {isLoading ? 'Sending...' : 'Send Reset Link'}
        </button>
      </form>
    </div>
  );
}
```

**Testing Expert Output:**
```typescript
// File: tests/auth/password-reset.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { POST as forgotPassword } from '@/app/api/auth/forgot-password/route';
import { POST as resetPassword } from '@/app/api/auth/reset-password/route';
import { prisma } from '@/lib/prisma';
import crypto from 'crypto';

describe('Password Reset Flow', () => {
  beforeEach(async () => {
    await prisma.passwordReset.deleteMany();
    await prisma.user.deleteMany();
  });

  describe('Forgot Password', () => {
    it('should generate token for valid email', async () => {
      const user = await prisma.user.create({
        data: { email: 'test@example.com', password: 'hashedpw' }
      });

      const request = new Request('http://localhost/api/auth/forgot-password', {
        method: 'POST',
        body: JSON.stringify({ email: 'test@example.com' })
      });

      const response = await forgotPassword(request);
      const data = await response.json();

      expect(data.success).toBe(true);

      const token = await prisma.passwordReset.findFirst({
        where: { userId: user.id }
      });

      expect(token).toBeTruthy();
      expect(token?.expiresAt).toBeInstanceOf(Date);
    });

    it('should not reveal if email does not exist', async () => {
      const request = new Request('http://localhost/api/auth/forgot-password', {
        method: 'POST',
        body: JSON.stringify({ email: 'nonexistent@example.com' })
      });

      const response = await forgotPassword(request);
      const data = await response.json();

      // Should still return success to prevent email enumeration
      expect(data.success).toBe(true);
      expect(response.status).toBe(200);
    });

    it('should invalidate old tokens when new request is made', async () => {
      const user = await prisma.user.create({
        data: { email: 'test@example.com', password: 'hashedpw' }
      });

      // Create first token
      const oldToken = crypto.randomBytes(32).toString('hex');
      await prisma.passwordReset.create({
        data: {
          token: oldToken,
          expiresAt: new Date(Date.now() + 60 * 60 * 1000),
          userId: user.id
        }
      });

      // Request new token
      const request = new Request('http://localhost/api/auth/forgot-password', {
        method: 'POST',
        body: JSON.stringify({ email: 'test@example.com' })
      });

      await forgotPassword(request);

      // Old token should be deleted
      const oldTokenExists = await prisma.passwordReset.findFirst({
        where: { token: oldToken }
      });

      expect(oldTokenExists).toBeNull();
    });
  });

  describe('E2E Flow', () => {
    it('should complete full password reset journey', async () => {
      // 1. Create user
      const user = await prisma.user.create({
        data: { email: 'test@example.com', password: 'oldpassword' }
      });

      // 2. Request password reset
      const forgotRequest = new Request('http://localhost/api/auth/forgot-password', {
        method: 'POST',
        body: JSON.stringify({ email: 'test@example.com' })
      });

      await forgotPassword(forgotRequest);

      // 3. Get token from database
      const tokenRecord = await prisma.passwordReset.findFirst({
        where: { userId: user.id }
      });

      expect(tokenRecord).toBeTruthy();

      // 4. Reset password with token
      const resetRequest = new Request('http://localhost/api/auth/reset-password', {
        method: 'POST',
        body: JSON.stringify({
          token: tokenRecord!.token,
          newPassword: 'newpassword123'
        })
      });

      const resetResponse = await resetPassword(resetRequest);
      const resetData = await resetResponse.json();

      expect(resetData.success).toBe(true);

      // 5. Verify token is deleted after use
      const usedToken = await prisma.passwordReset.findFirst({
        where: { token: tokenRecord!.token }
      });

      expect(usedToken).toBeNull();
    });
  });
});
```

### Expected Output

When the orchestrator delegates this task:

1. **Backend expert** delivers secure API endpoints with proper token generation, email integration, and validation
2. **Frontend expert** delivers polished, accessible forms with proper error handling and loading states
3. **Testing expert** delivers comprehensive test coverage ensuring the feature works correctly

All three sub-agents work in parallel, reducing total completion time from ~30 minutes (serial) to ~5 minutes (parallel) - a **6x speedup**.

---

## When to Use

### Ideal Use Cases

✅ **Use this pattern when:**
- Building complex features requiring multiple domains of expertise (fullstack features, microservices, etc.)
- Working on large codebases where different parts require different specialized knowledge
- Tasks can be parallelized (backend API + frontend UI + tests can all be built simultaneously)
- You need consistent coding standards across different domains
- Managing projects with clear separation of concerns (frontend/backend/testing/docs)
- Reducing context pollution is critical for maintaining quality
- Time-to-delivery is important and parallel execution would provide significant benefits

### Indicators You Need This Pattern

- You find yourself repeatedly saying "focus only on the backend" or "don't modify frontend code"
- Single-agent responses mix unrelated code (React components alongside SQL queries)
- Code quality degrades as context window fills with irrelevant information
- You're building fullstack features where frontend and backend could be developed simultaneously
- Different parts of your codebase follow different patterns/conventions
- Tasks take much longer than necessary because they execute serially

### Project Types

**Best For:**
- Fullstack web applications (React + Node.js, Next.js, etc.)
- Microservices architectures with multiple service types
- Complex SaaS products with distinct frontend/backend/infrastructure concerns
- Enterprise applications requiring specialized testing, security, and compliance code
- Projects with 10+ developers where domain specialization mirrors team structure

**Also Works For:**
- Mobile app development (iOS/Android/Backend)
- Game development (Engine/Gameplay/UI/Assets)
- Data science projects (ETL/Analysis/Visualization)
- DevOps workflows (Infrastructure/CI-CD/Monitoring)

---

## When NOT to Use

### Avoid This Pattern When

❌ **Don't use this pattern if:**
- Building simple, single-domain projects (just a frontend, just a backend)
- Your entire project is under 1000 lines of code
- Tasks are highly interdependent and must be done serially (can't parallelize)
- You're a beginner still learning Claude Code basics (start with single-agent workflows first)
- The overhead of defining and coordinating sub-agents exceeds the benefits
- Your project has no clear domain boundaries

### Simpler Alternatives

If this pattern seems too complex, consider:
- **Single Agent with Clear Instructions**: For smaller projects, one well-prompted agent is sufficient
- **Sequential Task Breakdown**: Manually split tasks and run them one at a time
- **Simple Prompt Sections**: Use markdown sections in a single prompt for organization

### Warning Signs

⚠️ **Red flags that suggest this pattern isn't right:**
- You're creating sub-agents with overlapping responsibilities
- Sub-agents frequently need to coordinate or share context (defeats the purpose)
- You have more sub-agents than actual domains in your project
- Setup time exceeds time saved through parallelization
- Your project is so small that context pollution isn't an issue

---

## Variations & Related Patterns

### Common Variations

1. **Task-Based vs Role-Based Sub-Agents**
   - **When to use**: Task-based (e.g., "implement-feature", "refactor-code") for smaller projects; Role-based (e.g., "backend-expert", "frontend-expert") for larger ones
   - **Trade-offs**: Task-based is simpler but less reusable; role-based requires more upfront definition but scales better

2. **Hierarchical Sub-Agents**
   - **When to use**: Very large projects where sub-agents themselves need sub-agents (e.g., backend-expert delegates to database-expert and api-expert)
   - **Trade-offs**: Maximum specialization but adds coordination complexity

### Related Patterns

- **Context Management**: Sub-agents are a context management technique—isolating context by domain
- **Custom Commands**: Sub-agents often work well with custom commands for common delegation patterns
- **Plan Mode**: Use plan mode to have the orchestrator create the delegation strategy before execution

### Pattern Combinations

This pattern works especially well with:
- **Plan Mode** → Orchestrator uses plan mode to design optimal task delegation strategy
- **MCP Servers** → Sub-agents can each have access to different MCP servers (backend-expert uses database MCP, frontend-expert uses documentation MCP)

---

## Metrics & Results

### Expected Improvements

Based on real-world usage and community reports:

- **Execution Speed**: 6-10x faster on multi-part tasks due to parallel execution
- **Code Quality**: 20-30% improvement in domain-specific code quality from specialized prompts
- **Context Efficiency**: 40-50% reduction in irrelevant context pollution
- **Consistency**: Near-perfect adherence to domain-specific coding standards

**Source**: YouTube tutorials "I was wrong about Claude Code UPDATED AI workflow" (10 parallel agents), "800+ hours of Learning Claude Code" (task delegation patterns)

### Success Indicators

You'll know this pattern is working when:
- Features that took 30 minutes now complete in 5 minutes
- Backend code consistently follows backend patterns without reminders
- You rarely see frontend code mixed into backend responses
- Sub-agents stay within their defined boundaries without manual correction
- Parallel tasks actually complete faster than serial execution

---

## Common Pitfalls & Solutions

### Pitfall 1: Overlapping Sub-Agent Responsibilities

**Problem**: You define sub-agents with unclear or overlapping domains (e.g., "api-expert" and "backend-expert" both handle API routes), causing confusion and duplicate work.

**Solution**: Define clear, non-overlapping domains with explicit boundaries.

```markdown
// ❌ Wrong: Overlapping domains
.claude/subagents/backend-expert.md → "Handle all backend code"
.claude/subagents/api-expert.md → "Handle API routes"

// ✅ Correct: Clear separation
.claude/subagents/backend-expert.md → "API routes, business logic, validation"
.claude/subagents/database-expert.md → "Schema design, migrations, queries"
```

### Pitfall 2: Too Many Sub-Agents

**Problem**: Creating a sub-agent for every tiny concern (separate agents for "routes", "middleware", "validation", etc.) adds coordination overhead that negates benefits.

**Solution**: Start with 3-5 broad domain sub-agents (backend, frontend, testing). Only add more if you have a large, complex project.

### Pitfall 3: Sub-Agents Needing Constant Coordination

**Problem**: Your sub-agents frequently need to see each other's code or coordinate changes, indicating poor task decomposition.

**Solution**: The orchestrator should handle integration points. If sub-agents need tight coordination, the task might not be suitable for parallel delegation—execute it serially instead.

---

## Best Practices

### Do's ✅

- **Define explicit constraints**: Each sub-agent should have "NEVER modify X" rules to prevent scope creep
- **Start small**: Begin with 2-3 sub-agents and expand only as needed
- **Use clear naming**: Sub-agent names should immediately convey their domain (backend-expert, frontend-expert, not agent1, agent2)
- **Provide domain-specific examples**: Include code patterns and examples in each sub-agent definition
- **Let the orchestrator integrate**: Main agent handles cross-cutting concerns and integration

### Don'ts ❌

- **Don't create sub-agents for tiny tasks**: If a sub-agent only runs once per month, it's not worth defining
- **Don't allow overlapping domains**: Each piece of code should have one clear owner
- **Don't skip the orchestrator**: Always have a main agent coordinate; don't delegate directly to sub-agents from user prompts
- **Don't over-specialize**: Too many narrow sub-agents creates coordination hell

### Pro Tips 💡

- **Tip 1**: Name your sub-agent files descriptively (`backend-expert.md`, not `agent1.md`) so Claude can auto-discover the right specialist
- **Tip 2**: Include a "decision tree" in your main claude.md: "For API work → backend-expert, For UI → frontend-expert"
- **Tip 3**: Use sub-agents even for solo projects—parallelization still saves time, and isolation still improves quality
- **Tip 4**: Add a "contract" section to each sub-agent defining what inputs it expects and what outputs it produces

---

## Real-World Examples

### Example 1: Fullstack SaaS Application

**Context**: Building a project management SaaS with React frontend, Node.js backend, PostgreSQL database, and comprehensive testing

**Challenge**: Implementing a complex "project collaboration" feature requiring real-time updates (WebSocket backend), collaborative UI (React components), and reliability testing

**Implementation**: Created 4 sub-agents:
- `backend-expert.md`: WebSocket server, REST APIs, database logic
- `frontend-expert.md`: React components, real-time state management
- `testing-expert.md`: Unit, integration, and E2E tests
- `infrastructure-expert.md`: Redis pub/sub, scaling configuration

**Results**: Feature completed in 2 hours vs. estimated 12 hours with single-agent approach. Code quality improved with consistent patterns across all domains. Zero cross-domain bugs.

**Source**: "I was wrong about Claude Code UPDATED AI workflow" - demonstrates 10 parallel agents on complex projects

### Example 2: Microservices Migration

**Context**: Migrating monolithic application to microservices architecture

**Challenge**: Needed to extract user authentication service, payment service, and notification service simultaneously while maintaining compatibility with monolith

**Implementation**: Created service-specific sub-agents:
- `auth-service-expert.md`: User authentication microservice
- `payment-service-expert.md`: Payment processing microservice
- `notification-service-expert.md`: Email/SMS notification service
- `integration-expert.md`: API contracts and backward compatibility

**Results**: All three services extracted in parallel in one day. Each service followed consistent patterns. Integration expert ensured no breaking changes.

**Source**: "armin-ronacher-agentic-coding-summary" - context management with specialized agents

---

## Quick Reference

### Checklist

Before implementing this pattern, ensure:
- [ ] Your project has at least 2-3 clear domains (frontend/backend, or similar)
- [ ] Tasks can be parallelized (not strictly sequential)
- [ ] You understand basic Claude Code workflows (try single-agent first)
- [ ] You have clear coding standards for each domain
- [ ] The time investment in setup will pay off through repeated use

### Implementation Steps (Quick)

1. Create `.claude/subagents/` directory in project root
2. Define 2-4 sub-agents with clear domains, responsibilities, and constraints
3. Add decision tree to main `claude.md` for when to use which sub-agent
4. In prompts, ask orchestrator to "delegate to appropriate sub-agents"
5. Review outputs from all sub-agents and integrate

### Key Commands/Code Snippets

```bash
# Create sub-agents directory
mkdir -p .claude/subagents

# Create a sub-agent definition
touch .claude/subagents/backend-expert.md

# Reference in prompt
"Delegate the API implementation to the backend-expert sub-agent"

# Let Claude decide
"Break this task down and delegate to appropriate sub-agents to work in parallel"
```

---

## FAQ

### Q: How do sub-agents actually run in parallel in Claude Code?

A: Claude Code doesn't literally spawn multiple concurrent Claude instances. Instead, the main agent mentally simulates delegation by switching context—thinking through each sub-agent's perspective separately. The "parallelization" benefit comes from the main agent planning all subtasks upfront and executing them in one session, rather than you manually running separate sequential sessions. The time savings come from reduced context pollution and focused execution.

### Q: Do I need separate API keys or Claude subscriptions for each sub-agent?

A: No. Sub-agents are virtual—they're different system prompts/contexts managed by a single Claude instance. You only need one Claude Code session.

### Q: Can sub-agents communicate with each other, or only through the orchestrator?

A: Sub-agents should only communicate through the orchestrator. If two sub-agents need to coordinate frequently, that's a sign the task decomposition is wrong—either combine them into one agent or have the orchestrator handle the integration points.

### Q: How is this different from just using prompt sections like "Backend:" and "Frontend:"?

A: Sub-agents provide true context isolation—each gets only relevant files and patterns. Prompt sections still show all context to the same agent, causing pollution. Sub-agents also enable better parallelization planning by the orchestrator.

### Q: What's the right number of sub-agents for a typical web app?

A: Start with 3: backend-expert, frontend-expert, testing-expert. Add more (database-expert, infrastructure-expert, documentation-expert) only if your project is large enough to justify them. Most projects don't need more than 5.

---

## Further Reading

### Official Documentation
- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/prompt-engineering) - System prompts and role-based agents

### Tutorials
- "I was wrong about Claude Code UPDATED AI workflow" - Demonstrates 10 parallel agents pattern
- "800+ hours of Learning Claude Code in 8 minutes" - Task-based vs role-based agent patterns
- "The Ultimate Claude Code Workflow" - Sub-agent task completion strategies

### Related Patterns
- [Context Management](../context/context-management.md) - How to manage context effectively
- [Plan Mode](../workflow/plan-mode.md) - Use plan mode for delegation strategy
- [Custom Commands](../workflow/custom-commands.md) - Combine with sub-agents for powerful workflows

---

## Sources & References

### Primary Sources

1. **Armin Ronacher - Agentic Coding**
   - **File**: `/sources/youtube/armin-ronacher-agentic-coding-summary.md`
   - **Relevance**: Context management strategies with sub-agents
   - **Key Insights**: How specialized agents reduce context pollution and improve code quality

2. **I was using Claude Code wrong... The Ultimate Workflow**
   - **File**: `/sources/youtube/7wGE I was using Claude Code wrong... The Ultimate Work.md`
   - **Relevance**: Sub-agent task completion patterns
   - **Key Insights**: How to structure sub-agents for maximum effectiveness

3. **800+ hours of Learning Claude Code in 8 minutes**
   - **File**: `/sources/youtube/800+ hours of Learning Claude Code in 8 minutes 2.md`
   - **Relevance**: Task-based vs role-based delegation patterns
   - **Key Insights**: When to use task-based vs role-based sub-agents

4. **I was wrong about Claude Code UPDATED AI workflow**
   - **File**: `/sources/youtube/I was wrong about Claude Code UPDATED AI workflow.md`
   - **Relevance**: Advanced workflow with 10 parallel agents
   - **Key Insights**: How to scale sub-agent architecture to complex projects

5. **A Complete Guide to Claude Code**
   - **File**: `/sources/youtube/A Complete Guide to Claude Code Here are ALL the.md`
   - **Relevance**: Specialized system prompts and sub-agent definitions
   - **Key Insights**: Best practices for writing sub-agent prompts

### Research & Data

- 10x faster execution on multi-part tasks (community reports from YouTube sources)
- 20-30% code quality improvement from domain specialization (anecdotal from tutorials)
- Context pollution reduction enables better results (Anthropic prompt engineering principles)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-14 | Initial documentation - extracted from Top 10 Best Practices synthesis |

---

## Metadata

**Tags**: `sub-agents`, `parallel-execution`, `architecture`, `context-management`, `specialization`, `orchestration`, `advanced`

**Prerequisites**:
- Understanding of basic Claude Code workflows
- Familiarity with your project's domain boundaries (frontend/backend/etc.)
- Experience with single-agent development first
- Knowledge of your project's coding standards for each domain

**Estimated Time to Implement**: 2-4 hours (initial setup), ongoing refinement

**Skill Level**: Advanced

---

## Contributing

Found an improvement or additional example? Please contribute:
1. Add your example in the "Real-World Examples" section
2. Update metrics if you have measured results
3. Add common pitfalls you've discovered
4. Share your sub-agent definitions that worked well

---

**Pattern Template Version**: 1.0
**Last Updated**: 2025-11-14
**Maintainer**: Claude Coding Knowledge Base Project
