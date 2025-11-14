---
pattern_name: Claude.md / Persistent Memory
category: Context Management
difficulty: Beginner
impact: High
date_created: 2024-11-14
last_updated: 2024-11-14
---

# Pattern: Claude.md / Persistent Memory

> **TL;DR**: Create a `claude.md` file (or `.claud/` directory) in your project root to store persistent context, conventions, and patterns that Claude automatically reads in every session—eliminating repetitive explanations and ensuring consistency.

## Overview

The `claude.md` pattern (also known as persistent memory or project memory) is a simple but powerful technique: store your project's context, conventions, rules, and patterns in a special markdown file that Claude Code automatically includes in every session.

Think of `claude.md` as the "brain and memory" of your project—a single source of truth that persists across all Claude interactions. Instead of re-explaining your tech stack, coding standards, and project-specific patterns in every conversation, you document them once and Claude remembers forever.

This pattern eliminates one of the biggest pain points in AI-assisted development: **repetition**. It also ensures **consistency** across sessions and team members, saves **tokens** by avoiding redundant explanations, and enables **team alignment** through shared understanding.

---

## Problem It Solves

### The Challenge

Every time you start a new Claude Code session (or work with a new sub-agent), you need to re-establish context:
- "This project uses TypeScript with strict mode"
- "We use Prisma, not raw SQL"
- "Always return { success, data, error } from APIs"
- "Components go in /components, utilities in /lib"
- "We follow the Airbnb style guide"

**Common Symptoms:**
- Starting every session with a wall of context copy-pasted from notes
- Claude generates code that violates your conventions
- Inconsistency between different sessions or developers
- Wasting 30-60 seconds at the start of every session explaining the same things
- Different team members giving Claude different instructions

**Without This Pattern:**
- **Time waste**: 5-10 minutes per day explaining context = 20-40 hours per year
- **Inconsistency**: Session A follows convention X, Session B violates it
- **Token waste**: Paying for the same context over and over
- **Team friction**: Everyone has different "standard" prompts
- **Frustration**: "Why doesn't Claude remember what I told it yesterday?"

### Why Traditional Approaches Fall Short

**Copy-paste from notes**: Easy to forget, gets out of sync, inconsistent across team

**Rely on memory**: Humans forget, new team members don't know conventions

**Hope Claude infers**: Claude will use common patterns, not your specific ones

---

## The Solution

### Core Concept

Store persistent context in a markdown file that Claude Code automatically loads:
- **File location**: `claude.md` in project root, or `.claud/rules.md`
- **Content**: Tech stack, conventions, patterns, constraints, examples
- **Automatic**: Claude reads this in every session without prompting
- **Version controlled**: Git tracks changes, team stays in sync

### Key Principles

1. **Document Once, Use Forever**: Write context once, Claude reads it in every session
2. **Single Source of Truth**: One place for project conventions, not scattered across developer brains
3. **Explicit Over Implicit**: Make every convention and constraint explicit—don't assume Claude knows
4. **Examples Over Rules**: Show example code, not just descriptions
5. **Living Document**: Update as patterns evolve, conventions change

### How It Works

1. **Create**: Make a `claude.md` file in your project root
2. **Document**: Add tech stack, conventions, patterns, constraints
3. **Commit**: Version control ensures team stays synced
4. **Forget**: Claude automatically reads it every session
5. **Update**: Refine as you discover new patterns or constraints

Claude Code appends the contents of `claude.md` to the system message in every session, so it's always present in the context—no manual copying required.

---

## Implementation

### Basic Implementation

**File: `claude.md`**
```markdown
# Project: TaskMaster SaaS

## Tech Stack
- Frontend: React 18 + TypeScript + Tailwind CSS
- Backend: Node.js + Express + PostgreSQL
- ORM: Prisma
- Testing: Vitest + React Testing Library

## Coding Conventions

### TypeScript
- Always use explicit return types
- Prefer `interface` over `type` for object shapes
- Enable strict mode (tsconfig)

### File Naming
- Components: PascalCase (UserProfile.tsx)
- Utilities: camelCase (formatDate.ts)
- Types: PascalCase (User.ts)

### Database
- Never use raw SQL—always use Prisma
- All timestamps: use @default(now()) and @updatedAt
- Soft delete: Add deletedAt DateTime? field

## Before Starting Any Task

1. Read relevant files first—don't assume
2. Use plan mode for non-trivial changes
3. Ask clarifying questions if ambiguous
4. Follow existing patterns
```

**Explanation:**
- Tech stack section prevents Claude from making wrong assumptions
- Conventions ensure generated code matches your style
- "Before Starting" section establishes a workflow Claude follows

**Usage:**
```bash
# Create the file
touch claude.md

# Claude automatically reads it in every session—nothing else needed!
```

### Advanced Implementation

**File: `.claud/rules.md`** (alternative location)
```markdown
# Project: E-Commerce Platform

## Architecture

### System Overview
```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Next.js   │ ───▶ │  tRPC API    │ ───▶ │ PostgreSQL  │
│  (Frontend) │      │  (Backend)   │      │  (Database) │
└─────────────┘      └──────────────┘      └─────────────┘
       │                                           │
       └────────────────────┬──────────────────────┘
                            │
                      ┌─────────────┐
                      │   Prisma    │
                      │    (ORM)    │
                      └─────────────┘
```

### Directory Structure
```
/app                # Next.js 14 App Router
  /api              # API routes (REST if needed)
  /(marketing)      # Marketing pages (parallel route)
  /(app)            # Application pages (parallel route)
/server/api         # tRPC routers
/components         # React components
  /ui               # shadcn/ui components
  /features         # Feature-specific components
/lib                # Shared utilities
/prisma             # Database schema
/types              # TypeScript types
```

## Coding Standards

### Error Handling Pattern
```typescript
// ALWAYS use this exact pattern for errors:
try {
  const result = await operation();
  return { success: true, data: result };
} catch (error) {
  logger.error('Operation failed', { error, context: input });
  return {
    success: false,
    error: error instanceof CustomError
      ? error.message
      : 'Operation failed'
  };
}
```

### API Response Pattern
```typescript
// All API responses must match this shape:
type ApiResponse<T> =
  | { success: true; data: T }
  | { success: false; error: string };

// Example:
async function getUser(id: string): Promise<ApiResponse<User>> {
  // implementation
}
```

### React Component Pattern
```typescript
// Standard component structure:
interface Props {
  // Explicit props types
}

export function ComponentName({ prop1, prop2 }: Props) {
  // 1. Hooks (state, effects, queries)
  const [state, setState] = useState();
  const query = useQuery(...);

  // 2. Derived values
  const computed = useMemo(() => ..., [deps]);

  // 3. Event handlers
  const handleEvent = useCallback(() => {
    // handler logic
  }, [deps]);

  // 4. Render
  return (...);
}
```

### Testing Requirements
- All new features must have tests
- Unit tests: co-located with component (.test.tsx)
- Integration tests: /tests/integration/
- Test naming: `describe('Component') > it('should do X when Y')`

## Project-Specific Rules

### Database Constraints
- **Never** hard-delete records—always soft delete (deletedAt)
- All foreign keys must have onDelete behavior specified
- Enums defined in Prisma schema, not TypeScript
- Complex queries extracted to /lib/queries/, not inline

### Authentication
- All protected routes use `protectedProcedure` (tRPC)
- Session stored in database (NextAuth.js)
- Tokens: JWT with 7-day expiry
- Password hashing: bcrypt with 12 rounds

### Security Rules
- **Critical**: Always validate input with zod
- **Critical**: Never trust client-side validation alone
- **Critical**: Sanitize user input before database queries
- Never log sensitive data (passwords, tokens, PII)

## Common Patterns

### Form Validation
```typescript
// Use zod + React Hook Form for all forms:
import { z } from 'zod';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const schema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be at least 8 characters')
});

type FormData = z.infer<typeof schema>;

function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema)
  });

  // ...
}
```

### Database Transactions
```typescript
// For multi-step database operations:
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({ data: userData });
  await tx.profile.create({ data: { userId: user.id, ...profileData } });
  return user;
});
```

## DON'Ts (Anti-Patterns)

❌ **Never** use `any` type—use `unknown` and type guard instead
❌ **Never** use inline styles—Tailwind only
❌ **Never** commit commented-out code—delete it (Git remembers)
❌ **Never** use `var`—use `const` or `let`
❌ **Never** mutate props—React components must be pure
❌ **Never** skip error handling on async operations

## Workflow

### For New Features
1. Switch to plan mode (Shift+Tab)
2. Ask Claude to create a detailed plan
3. Review and approve plan
4. Execute implementation
5. Review code for security and edge cases
6. Write tests
7. Run full test suite

### For Bug Fixes
1. Reproduce the bug
2. Write a failing test that captures the bug
3. Fix the bug
4. Ensure test passes
5. Check for similar bugs elsewhere

## Notes for Claude

- **IMPORTANT**: Always check existing code patterns before generating new code
- **IMPORTANT**: When in doubt, ask clarifying questions—don't assume
- **Proactively** suggest improvements to code quality, security, performance
- Use plan mode for any task that will modify 3+ files
- If you find outdated or incorrect patterns in this file, point them out
```

**Explanation:**
- ASCII diagram provides visual architecture understanding
- Explicit code patterns show exactly how to structure code
- Security rules prevent common vulnerabilities
- Workflow section establishes standard processes
- "Notes for Claude" section gives meta-instructions

### Configuration

**Option 1: Single File (Simple)**
```bash
# Create claude.md in project root
touch claude.md
# Add your content
# Commit to Git
git add claude.md
git commit -m "Add claude.md for persistent context"
```

**Option 2: Directory Structure (Advanced)**
```bash
# Create .claud directory
mkdir .claud

# Create separate files for organization
touch .claud/rules.md          # Core conventions
touch .claud/patterns.md       # Code patterns
touch .claud/architecture.md   # System architecture
touch .claud/workflows.md      # Development workflows

# Claude reads all .md files in .claud/
```

**Auto-generation:**
```bash
# Claude Code can generate claude.md for you
# (if using Claude Code CLI with /init command)
claude-code init

# This creates a basic claude.md with common sections
```

---

## Complete Code Example

### Scenario

You're building a full-stack SaaS application and want to ensure consistency across all Claude sessions and team members.

**Requirements:**
- Document tech stack and architecture
- Establish coding conventions for TypeScript, React, API design
- Define error handling and security patterns
- Provide example code showing correct patterns

### Implementation

**File: `claude.md`**
```markdown
# Project: AnalyticsPro SaaS

## Quick Reference
- **Tech Stack**: Next.js 14 + TypeScript + tRPC + Prisma + PostgreSQL
- **Conventions**: Strict TypeScript, Tailwind CSS, shadcn/ui
- **Testing**: Vitest + Playwright
- **Deployment**: Vercel

## Architecture

### Tech Stack
- **Framework**: Next.js 14 (App Router, React Server Components)
- **Language**: TypeScript 5.x (strict mode enabled)
- **API**: tRPC v10 (type-safe APIs)
- **Database**: PostgreSQL 15 via Prisma ORM
- **Authentication**: NextAuth.js v5
- **Styling**: Tailwind CSS + shadcn/ui
- **State**: Zustand (client), React Query (server state)
- **Testing**: Vitest (unit/integration), Playwright (E2E)

### Database Schema Principles
- All models have: `id` (cuid), `createdAt`, `updatedAt`
- Soft delete: `deletedAt DateTime?` (never hard delete user data)
- Enums in Prisma schema, not TypeScript
- Foreign keys always specify onDelete behavior

## Coding Conventions

### TypeScript
```typescript
// ✅ Good: Explicit types, interfaces for objects
interface User {
  id: string;
  email: string;
  name: string;
}

function getUser(id: string): Promise<User> {
  // implementation
}

// ❌ Bad: Implicit any, type instead of interface
type User = any;

function getUser(id) {
  // implementation
}
```

### React Components
```typescript
// ✅ Good: Functional component, explicit props, hooks pattern
interface UserProfileProps {
  userId: string;
}

export function UserProfile({ userId }: UserProfileProps) {
  // 1. Hooks
  const { data: user, isLoading } = trpc.user.getById.useQuery({ id: userId });
  const [isEditing, setIsEditing] = useState(false);

  // 2. Derived state
  const displayName = useMemo(() =>
    user?.name || user?.email || 'Unknown',
    [user]
  );

  // 3. Event handlers
  const handleEdit = useCallback(() => {
    setIsEditing(true);
  }, []);

  // 4. Early returns
  if (isLoading) return <Skeleton />;
  if (!user) return <NotFound />;

  // 5. Render
  return (
    <div className="space-y-4">
      {/* component content */}
    </div>
  );
}

// ❌ Bad: Class component, inline styles, unclear structure
class UserProfile extends React.Component {
  render() {
    return <div style={{ padding: '10px' }}>...</div>;
  }
}
```

### API Routes (tRPC)
```typescript
// ✅ Good: Protected procedure, zod validation, proper error handling
export const userRouter = createTRPCRouter({
  getById: protectedProcedure
    .input(z.object({ id: z.string().cuid() }))
    .query(async ({ ctx, input }) => {
      const user = await ctx.db.user.findUnique({
        where: { id: input.id },
      });

      if (!user) {
        throw new TRPCError({
          code: 'NOT_FOUND',
          message: 'User not found',
        });
      }

      return user;
    }),

  update: protectedProcedure
    .input(z.object({
      id: z.string().cuid(),
      name: z.string().min(1),
    }))
    .mutation(async ({ ctx, input }) => {
      // Ensure user can only update their own profile
      if (ctx.session.user.id !== input.id) {
        throw new TRPCError({
          code: 'FORBIDDEN',
          message: 'Cannot update another user\'s profile',
        });
      }

      return ctx.db.user.update({
        where: { id: input.id },
        data: { name: input.name },
      });
    }),
});

// ❌ Bad: No validation, no auth check, no error handling
export const userRouter = createTRPCRouter({
  update: publicProcedure.mutation(async ({ input }) => {
    return db.user.update({ where: { id: input.id }, data: input });
  }),
});
```

### Error Handling
```typescript
// ✅ Good: Comprehensive error handling with logging
try {
  const result = await riskyOperation();
  return { success: true, data: result };
} catch (error) {
  logger.error('Operation failed', {
    error: error instanceof Error ? error.message : 'Unknown error',
    stack: error instanceof Error ? error.stack : undefined,
    context: { userId, operationId },
  });

  if (error instanceof PrismaClientKnownRequestError) {
    return { success: false, error: 'Database error occurred' };
  }

  if (error instanceof ValidationError) {
    return { success: false, error: error.message };
  }

  return { success: false, error: 'An unexpected error occurred' };
}

// ❌ Bad: Swallowing errors, no logging
try {
  await riskyOperation();
} catch (e) {
  // Silent failure
}
```

## Security Rules ⚠️

### Input Validation
```typescript
// ✅ ALWAYS validate with zod on the server
const userInput = z.object({
  email: z.string().email(),
  age: z.number().min(13).max(120),
}).parse(input); // Throws if invalid

// ❌ NEVER trust client-side validation alone
```

### SQL Injection Prevention
```typescript
// ✅ Good: Prisma parameterized queries
await prisma.user.findMany({
  where: { email: userInput },
});

// ❌ Bad: Raw SQL with string interpolation
await prisma.$executeRaw`SELECT * FROM users WHERE email = ${userInput}`;
// Use $executeRaw with template literals for proper escaping, or better yet, use Prisma's query builder
```

### Authentication
```typescript
// ✅ Good: Check auth in every protected route
export const protectedRouter = createTRPCRouter({
  getData: protectedProcedure.query(async ({ ctx }) => {
    // ctx.session.user guaranteed to exist due to protectedProcedure
    return getData(ctx.session.user.id);
  }),
});

// ❌ Bad: Assuming user is authenticated
export const router = createTRPCRouter({
  getData: publicProcedure.query(async ({ ctx }) => {
    return getData(ctx.session.user.id); // ctx.session might be null!
  }),
});
```

## Testing Standards

### Unit Tests
```typescript
// ✅ Good: Descriptive test names, arrange-act-assert
describe('formatDate', () => {
  it('should format ISO date as MM/DD/YYYY', () => {
    // Arrange
    const isoDate = '2024-11-14T10:30:00Z';

    // Act
    const result = formatDate(isoDate);

    // Assert
    expect(result).toBe('11/14/2024');
  });

  it('should return empty string for invalid date', () => {
    expect(formatDate('invalid')).toBe('');
  });
});
```

### Integration Tests
```typescript
// ✅ Good: Test actual API routes with database
describe('User API', () => {
  it('should create user and return user data', async () => {
    const caller = appRouter.createCaller(createMockContext());

    const user = await caller.user.create({
      email: 'test@example.com',
      name: 'Test User',
    });

    expect(user).toMatchObject({
      email: 'test@example.com',
      name: 'Test User',
    });
  });
});
```

## Workflow

### Feature Development
1. **Plan**: Use plan mode (Shift+Tab) to create detailed spec
2. **Database**: Update Prisma schema if needed, run migration
3. **Backend**: Create tRPC router with input validation
4. **Frontend**: Create components with proper TypeScript types
5. **Tests**: Write unit tests for utils, integration tests for APIs
6. **Review**: Check for security issues, error handling, edge cases
7. **Commit**: Write clear commit message following Conventional Commits

### Bug Fixes
1. **Reproduce**: Write a failing test that captures the bug
2. **Fix**: Implement the fix
3. **Verify**: Test passes, no regressions
4. **Document**: Add comment explaining non-obvious fixes

## Notes for Claude

- **CRITICAL**: Always validate user input with zod on the server
- **CRITICAL**: Never trust client-side validation for security
- **IMPORTANT**: Check authentication before accessing user data
- **Proactively** suggest security improvements
- **Always** use plan mode for features touching 3+ files
- If you notice code violating these conventions, point it out
```

### Expected Behavior

**Session 1:**
```
You: "Add user profile editing functionality"

Claude:
"I'll implement this following the project patterns from claude.md.

I'll create:
1. tRPC router with protectedProcedure and zod validation
2. React component with proper TypeScript types
3. Form using React Hook Form + zod resolver
4. Unit and integration tests

Let me start with plan mode to detail the approach..."

[Claude automatically follows all conventions without being reminded]
```

**Session 2 (different day, different developer):**
```
You: "Add password reset functionality"

Claude:
"Following the project architecture in claude.md, I'll implement:
- tRPC router with email validation and rate limiting
- Database migration for reset tokens with expiry
- Email sending (what service are you using for emails?)
- Frontend form following the established patterns

Should I create a detailed plan first?"

[Same conventions, consistent behavior across sessions]
```

---

## When to Use

### Ideal Use Cases

✅ **Use this pattern when:**
- Working on a team project (ensures everyone gets same Claude behavior)
- Project has specific conventions or patterns
- Using less common tech stacks or framework versions
- Working across multiple Claude sessions on the same project
- Onboarding new developers (they can read claude.md to understand standards)
- Want to save time not repeating context every session

### Indicators You Need This Pattern

- You copy-paste the same context at the start of every session
- Different team members get inconsistent results from Claude
- Claude keeps forgetting your conventions
- You've explained your tech stack 10+ times
- New developers ask "what are our coding standards?"
- You waste the first 5 minutes of every session on setup

### Project Types

**Best For:**
- Team projects (2+ developers)
- Long-running projects (months/years)
- Projects with specific conventions
- Open source projects with contribution guidelines
- Projects using newer framework versions with breaking changes

**Also Works For:**
- Solo projects you'll maintain long-term
- Learning projects where you want to enforce good habits
- Client work where consistency matters

---

## When NOT to Use

### Avoid This Pattern When

❌ **Don't use this pattern if:**
- Prototyping or throwaway code (conventions don't matter yet)
- Project is <500 lines (overhead not worth it)
- Solo weekend project (you won't forget in 2 days)
- Exploring different approaches (rigid conventions limit experimentation)
- Every session is completely different context/task

### Simpler Alternatives

If this pattern seems too heavy:
- **Session Notes**: Keep a notes.md for yourself, copy-paste when needed
- **README.md**: Use the existing README for basic conventions
- **Inline Comments**: Document patterns directly in code

### Warning Signs

⚠️ **Red flags that suggest this pattern isn't right:**
- claude.md is >2000 lines (too much, split or simplify)
- You update claude.md multiple times per day (too much churn, let patterns stabilize)
- Different team members have conflicting conventions (solve human problem first)
- You spend more time documenting than coding (diminishing returns)

---

## Variations & Related Patterns

### Common Variations

1. **Single File (`claude.md`)**
   - **When to use**: Simple projects, getting started
   - **Trade-offs**: Easier to manage, but can get unwieldy >500 lines

2. **Directory Structure (`.claud/`)**
   - **When to use**: Complex projects, many conventions
   - **Trade-offs**: Better organization, but more files to maintain
   - **Files**: `rules.md`, `patterns.md`, `architecture.md`, `workflows.md`

3. **Minimal claude.md + MCP Servers**
   - **When to use**: Standard tech stack, documentation elsewhere
   - **Trade-offs**: Less to maintain, relies on external docs
   - **Example**: Just project-specific patterns, use Context7 MCP for library docs

### Related Patterns

- **Context Management**: claude.md provides persistent context automatically
- **Custom Commands**: Reference claude.md patterns in slash commands
- **Sub-Agents**: Each sub-agent reads claude.md for consistent behavior

### Pattern Combinations

This pattern works especially well with:
- **Context Management** → claude.md handles persistent context, prompts handle task-specific context
- **Plan Mode** → claude.md provides conventions, plan mode ensures they're followed
- **Code Review** → claude.md defines quality standards, review checks compliance

---

## Metrics & Results

### Expected Improvements

Based on community reports and user testimonials:

- **5-10 minutes saved** per session (no context re-explanation)
- **80-90% consistency** across sessions and team members
- **Token savings**: 500-1000 tokens per session (context not repeated)
- **Faster onboarding**: New team members productive in hours, not days

**Source**: Claude Code community feedback, user testimonials

### Success Indicators

You'll know this pattern is working when:
- You start sessions immediately without preamble
- Code Claude generates matches your conventions on first try
- Different team members get consistent results
- New developers can reference claude.md instead of asking questions
- You haven't explained your tech stack in weeks

---

## Common Pitfalls & Solutions

### Pitfall 1: claude.md Gets Too Long

**Problem**: File grows to 1000+ lines, becomes hard to maintain and navigate

**Solution**: Split into .claud/ directory with focused files

```bash
# Before: One massive file
claude.md (1500 lines)

# After: Organized directory
.claud/
├── architecture.md (200 lines)
├── conventions.md (300 lines)
├── patterns.md (400 lines)
├── security.md (200 lines)
└── workflows.md (150 lines)
```

### Pitfall 2: Conflicting Conventions

**Problem**: Different team members add contradictory rules to claude.md

**Solution**: Treat claude.md like code—review in PRs, discuss conflicts

```markdown
<!-- ❌ Conflict -->
# Developer A added:
"Use `type` for all TypeScript definitions"

# Developer B added:
"Use `interface` for object shapes"

<!-- ✅ Resolution via PR discussion -->
"Use `interface` for object shapes, `type` for unions and aliases"
```

### Pitfall 3: Outdated Information

**Problem**: claude.md references old patterns or deprecated libraries

**Solution**: Regular reviews, mark patterns with version/date

```markdown
## React Patterns (Updated: 2024-11-14, Next.js 14)

### Server Components (Current Standard)
```typescript
// Current: Use Server Components by default
export default async function ProductPage({ params }: Props) {
  const product = await getProduct(params.id);
  return <ProductView product={product} />;
}
```

### Client Components (Legacy Pattern - before Next.js 13)
~~Use useEffect to fetch data~~
**Deprecated**: Use Server Components or React Query instead
```

---

## Best Practices

### Do's ✅

- **Show, don't tell**: Include code examples, not just descriptions
- **Be specific**: "Use Prisma for all database queries" not "Use an ORM"
- **Include anti-patterns**: Show what NOT to do
- **Version control**: Commit claude.md, track changes
- **Review regularly**: Update quarterly or when patterns change
- **Start small**: Begin with basics, add as patterns emerge

### Don'ts ❌

- **Don't document everything**: Focus on project-specific, not general knowledge
- **Don't let it stagnate**: Outdated claude.md is worse than none
- **Don't make it a novel**: Keep it practical and scannable
- **Don't contradict yourself**: Ensure conventions are consistent
- **Don't skip examples**: Rules without examples are ambiguous

### Pro Tips 💡

- **Tip 1**: Add a "Quick Reference" section at the top for instant context
- **Tip 2**: Use "CRITICAL" and "IMPORTANT" keywords for must-follow rules
- **Tip 3**: Include a "Notes for Claude" section with meta-instructions
- **Tip 4**: Link to external docs for standard conventions (e.g., "Follow Airbnb style guide")
- **Tip 5**: Have Claude help write/maintain claude.md based on your existing code

---

## Real-World Examples

### Example 1: SaaS Application

**Context**: Multi-tenant SaaS with strict security requirements

**claude.md Highlights:**
```markdown
## Security Rules ⚠️

### Tenant Isolation
**CRITICAL**: All database queries MUST filter by tenantId
```typescript
// ✅ Correct
const users = await prisma.user.findMany({
  where: {
    tenantId: session.user.tenantId,
    // other filters
  },
});

// ❌ WRONG - Data leak!
const users = await prisma.user.findMany();
```
```

**Results:**
- Zero tenant isolation bugs after implementing
- New developers avoid common security mistakes
- Consistent security patterns across 50+ API routes

### Example 2: Open Source Project

**Context**: React component library with many contributors

**claude.md Highlights:**
```markdown
## Component Development

### Accessibility Requirements
All components MUST:
- Support keyboard navigation
- Include ARIA labels
- Pass axe-core tests
- Have focus indicators
- Support screen readers

### Example:
```typescript
<button
  onClick={handleClick}
  aria-label="Close dialog"
  aria-pressed={isPressed}
>
  <CloseIcon aria-hidden="true" />
</button>
```
```

**Results:**
- Consistent accessibility across components
- Contributors follow standards without deep a11y knowledge
- Reduced PR review cycles (Claude generates compliant code)

---

## Quick Reference

### Checklist

Before implementing this pattern:
- [ ] You have project-specific conventions (not just standard practices)
- [ ] You've worked on the project enough to know patterns
- [ ] The project will have multiple sessions or developers
- [ ] You're willing to maintain and update the file

### Implementation Steps (Quick)

1. Create `claude.md` in project root
2. Add basic sections: Tech Stack, Conventions, Patterns
3. Include code examples for key patterns
4. Commit to Git
5. Test: Start new Claude session, verify Claude follows conventions

### Key Commands/Code Snippets

```bash
# Create claude.md
touch claude.md

# Or create .claud directory
mkdir .claud
touch .claud/rules.md

# Auto-generate (if using Claude Code CLI)
claude-code init

# Test it works
# Start Claude Code, ask it to describe your tech stack
# It should recite what's in claude.md
```

**Minimal Template:**
```markdown
# Project: [Name]

## Tech Stack
- [Framework]
- [Language]
- [Database]
- [Key libraries]

## Conventions
- [Convention 1 with example]
- [Convention 2 with example]

## Patterns
```[language]
// Show code pattern example
```

## DON'Ts
- [Anti-pattern 1]
- [Anti-pattern 2]
```

---

## FAQ

### Q: What's the difference between claude.md and .claud/rules.md?

A: Both work the same way—Claude reads markdown files in the root directory or `.claud/` subdirectory.

- **claude.md**: Single file, simpler, good for most projects
- **.claud/**: Multiple files, better organization for complex projects

Choose based on project size and preference.

### Q: How long should claude.md be?

A: **Ideal**: 200-500 lines covering essentials

**Maximum**: ~1000 lines before splitting into .claud/ directory

**Focus**: Project-specific patterns, not general programming knowledge

### Q: Will claude.md slow down Claude Code?

A: No significant performance impact. Claude reads it once per session. Even a 1000-line claude.md is <10K tokens, well within Claude's context window.

### Q: Should I document general best practices or only project-specific patterns?

A: **Project-specific only**. Claude already knows general best practices. Document:
- Your specific tech stack and versions
- Project-specific conventions
- Patterns unique to your codebase
- Domain-specific rules

Don't document: General React patterns, standard TypeScript syntax, etc.

### Q: How often should I update claude.md?

A: Update when:
- Adopting a new convention or pattern
- Changing tech stack versions with breaking changes
- Discovering common mistakes or anti-patterns
- Onboarding reveals missing context

**Review**: Quarterly check for outdated information

---

## Further Reading

### Official Documentation
- [Claude Code Documentation](https://docs.claude.com) - Official guidance on project memory

### Tutorials
- "800+ Hours of Learning Claude Code" - Hash key to add instructions
- "I was wrong about Claude Code" - "Brain and memory" of Claude
- Peter Yang's Movie App Tutorial - Using claude.md for initialization

### Related Patterns
- [Context Management](./context-management.md) - Strategic information positioning
- [Plan Mode](./plan-mode.md) - Spec-driven development workflow
- [Custom Commands](../tooling/custom-commands.md) - Reusable workflows

---

## Sources & References

### Primary Sources

1. **Peter Yang Movie App Summary**
   - **File**: `/sources/youtube/peter-yang-movie-app-summary.md`
   - **Relevance**: claude.md initialization and basic usage
   - **Key Insights**: Claude.md enables persistent context across sessions

2. **"7wGE I was using Claude Code wrong... The Ultimate Work"**
   - **File**: `/sources/youtube/7wGE I was using Claude Code wrong... The Ultimate Work.md`
   - **Relevance**: Advanced claude.md usage
   - **Key Insights**: Appended to system message every run

3. **"800+ hours of Learning Claude Code in 8 minutes 2"**
   - **File**: `/sources/youtube/800+ hours of Learning Claude Code in 8 minutes 2.md`
   - **Relevance**: Hash key to add instructions
   - **Key Insights**: Simple but powerful mechanism

4. **"I was wrong about Claude Code UPDATED AI workflow"**
   - **File**: `/sources/youtube/I was wrong about Claude Code UPDATED AI workflow.md`
   - **Relevance**: "Brain and memory" concept
   - **Key Insights**: Persistent context enables consistency

5. **"A Complete Guide to Claude Code Here are ALL the"**
   - **File**: `/sources/youtube/A Complete Guide to Claude Code Here are ALL the.md`
   - **Relevance**: Best practices and patterns documentation
   - **Key Insights**: Include examples and anti-patterns

### Community Resources

- Claude Code GitHub discussions - Real-world claude.md examples
- Community-shared templates - Starting points for different project types

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-11-14 | Initial documentation in standardized template format |

---

## Metadata

**Tags**: `claude-md`, `persistent-memory`, `project-memory`, `context-management`, `conventions`, `team-alignment`

**Prerequisites**:
- Basic understanding of Claude Code
- Project with established conventions (or willingness to establish them)

**Estimated Time to Implement**:
- Basic: 30-60 minutes (document tech stack and key conventions)
- Comprehensive: 2-4 hours (detailed patterns, examples, anti-patterns)

**Skill Level**: Beginner

---

## Contributing

Found an improvement or additional example? Please contribute:
1. Add your real-world example showing claude.md impact
2. Share effective patterns you've documented
3. Add common pitfalls you've discovered

---

**Pattern Documentation**: v1.0
**Last Updated**: 2024-11-14
**Maintainer**: Claude Coding Knowledge Base Project
