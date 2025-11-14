---
title: Top 10 Best Practices for Coding with Claude
synthesis_date: 2024-11-14
sources_analyzed: 11 files (1 official docs, 10 YouTube tutorials/transcripts)
methodology: Cross-source frequency analysis
status: First synthesis - extracted from collected sources
---

# Top 10 Best Practices for Coding with Claude

This document synthesizes the most commonly mentioned best practices across all collected sources about coding with Claude. Each practice includes the principle, why it matters, a practical code example, and supporting sources.

---

## Practice #1: Context Management & Codebase Understanding

**Mentioned in**: 7+ sources

### The Principle

Proper context management involves strategically structuring how Claude receives information about your codebase. This includes document positioning, using MCP servers for up-to-date documentation, and semantic code retrieval tools.

### Why It Matters

- **30% accuracy improvement** from strategic document positioning (Anthropic research)
- Dramatically reduces errors from misinterpretation
- Enables Claude to work effectively with large, unfamiliar codebases
- Quick onboarding to projects without deep domain knowledge

### Code Example

```xml
<!-- ✅ GOOD: Document first, query last -->
<codebase_context>
<architecture>
This is a Next.js 14 app with:
- App router in /app directory
- API routes in /app/api
- Components in /components (Client) and /ui (Server)
- Database: PostgreSQL via Prisma
- Auth: NextAuth.js
</architecture>

<relevant_files>
File: /app/api/users/route.ts
Purpose: User CRUD operations
Dependencies: Prisma, zod for validation

File: /components/UserList.tsx
Purpose: Client component displaying users
State management: React Query
</relevant_files>
</codebase_context>

<task>
Add pagination to the user list. Support page size of 10, 25, 50.
</task>
```

**With MCP Servers:**
```bash
# Install Context7 MCP server for up-to-date docs
npm install -g @context7/mcp-server

# In your claude.md or MCP config
{
  "mcpServers": {
    "context7": {
      "command": "context7-mcp",
      "args": ["--libraries", "nextjs,react-query,prisma"]
    }
  }
}
```

### Sources

1. `/sources/docs/anthropic-prompt-engineering.md` - Document positioning strategies
2. `/sources/youtube/peter-yang-movie-app-summary.md` - Using Claude to understand codebases
3. `/sources/youtube/armin-ronacher-agentic-coding-summary.md` - Context management strategies
4. `/sources/youtube/800+ hours of Learning Claude Code in 8 minutes 2.md` - MCP Context7 server
5. `/sources/youtube/Claude Code Is The Best AI Coding Agent.md` - Excels with unfamiliar codebases
6. `/sources/youtube/A Complete Guide to Claude Code Here are ALL the.md` - Serena MCP for semantic retrieval
7. `/sources/youtube/7wGE I was using Claude Code wrong... The Ultimate Work.md` - Context strategies

---

## Practice #2: Claude.md / Persistent Memory

**Mentioned in**: 5 sources

### The Principle

Use a `claude.md` file (or `.claud` directory) in your project root to store persistent project-specific context, rules, conventions, and patterns. This file is automatically included in every Claude Code session.

### Why It Matters

- **Eliminates repetition** - No need to re-explain project context every session
- **Maintains consistency** - Enforces coding standards automatically
- **Saves tokens** - Core instructions stored once, not repeated in every prompt
- **Team alignment** - Shared understanding of project conventions

### Code Example

**File: `claude.md` (or `.claud/rules.md`)**

```markdown
# Project: TaskMaster SaaS

## Tech Stack
- **Frontend**: React 18 + TypeScript + Tailwind CSS
- **Backend**: Node.js + Express + PostgreSQL
- **ORM**: Prisma
- **Auth**: JWT with refresh tokens
- **Testing**: Vitest + React Testing Library

## Coding Conventions

### TypeScript
- Use explicit return types for all functions
- Prefer `interface` over `type` for object shapes
- Use `const` assertions for literal types
- Enable strict mode in tsconfig

### React Components
- Use functional components with hooks
- Extract custom hooks when logic is reused 2+ times
- Props: Use destructuring with explicit types
- Name event handlers: `handleXxx` (e.g., `handleSubmit`)

### Database
- **Never** use raw SQL - always use Prisma
- All timestamps: Use `@default(now())` and `@updatedAt`
- Soft delete pattern: Add `deletedAt DateTime?` field
- Complex queries: Extract to `/lib/queries/*.ts`

### File Organization
```
/src
  /components
    /ui        # Shadcn/ui components
    /features  # Feature-specific components
  /lib
    /api       # API client functions
    /queries   # Database query functions
    /utils     # Pure utility functions
  /hooks       # Custom React hooks
  /types       # Shared TypeScript types
```

### Testing
- Unit tests: Co-locate with component (`.test.tsx`)
- Integration tests: `/tests/integration/`
- Test naming: `describe('ComponentName')` → `it('should do X when Y')`
- Mock external APIs using MSW

## Project-Specific Patterns

### Error Handling
```typescript
// Always use this pattern for API routes
try {
  const result = await someOperation();
  return res.json({ success: true, data: result });
} catch (error) {
  logger.error('Operation failed', { error, context });
  return res.status(500).json({
    success: false,
    error: 'Operation failed'
  });
}
```

### Form Validation
```typescript
// Use zod schemas + React Hook Form
import { z } from 'zod';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8)
});

type FormData = z.infer<typeof schema>;

const { register, handleSubmit } = useForm<FormData>({
  resolver: zodResolver(schema)
});
```

## Before Starting Any Task

1. **Read relevant files first** - Don't assume, verify
2. **Use plan mode** - Create spec before coding
3. **Ask clarifying questions** if anything is ambiguous
4. **Follow existing patterns** - Match the codebase style
5. **Write tests** for new features or bug fixes
```

**Quick initialization:**
```bash
# Claude Code will auto-generate claude.md
/init

# Or create manually
touch claude.md
```

### Sources

1. `/sources/youtube/peter-yang-movie-app-summary.md` - claude.md enables persistent context
2. `/sources/youtube/7wGE I was using Claude Code wrong... The Ultimate Work.md` - Appended to system message every run
3. `/sources/youtube/800+ hours of Learning Claude Code in 8 minutes 2.md` - Hash key to add instructions
4. `/sources/youtube/I was wrong about Claude Code UPDATED AI workflow.md` - "Brain and memory" of Claude
5. `/sources/youtube/A Complete Guide to Claude Code Here are ALL the.md` - Best practices and patterns

---

## Practice #3: Plan Mode / Spec-Driven Development

**Mentioned in**: 5 sources

### The Principle

Always use plan mode (Shift+Tab in Claude Code) before executing code changes. Have Claude create a detailed specification and game plan, review it thoroughly, iterate if needed, then execute.

### Why It Matters

- **Prevents wasted effort** - Catches issues before code is written
- **Ensures alignment** - You and Claude agree on approach
- **Provides transparency** - See Claude's reasoning and strategy
- **Reduces token waste** - Fix plan errors (cheap) vs. code errors (expensive)
- **Better results** - Well-planned code is higher quality

### Code Example

**User prompt:**
```
I need to add user roles and permissions to the app.
Admins can do everything. Managers can create/edit.
Users can only view.

<shift+tab to enter plan mode>

Please create a detailed plan for implementing this.
Ask me clarifying questions first.
```

**Claude's plan mode response:**
```markdown
# Implementation Plan: Role-Based Access Control (RBAC)

## Clarifying Questions

1. **Database**: Do you want to store roles in the database or use
   environment/config?
2. **Granularity**: Do permissions apply at:
   - Route level (API endpoints)?
   - UI level (show/hide components)?
   - Data level (filter queries)?
3. **Role assignment**: Can users have multiple roles or just one?
4. **Existing users**: How should we migrate existing users to the
   new role system?

## Proposed Architecture

### Database Schema Changes
- Add `role` enum to User model: `ADMIN | MANAGER | USER`
- Add `permissions` table for fine-grained control (future-proof)

### Implementation Steps

**Step 1: Database Migration**
- Create Prisma migration for `role` field
- Set default role to `USER`
- Backfill existing users

**Step 2: Middleware**
- Create `/middleware/auth.ts` with role checking
- Export `requireRole(['ADMIN', 'MANAGER'])` HOF
- Add to protected API routes

**Step 3: Frontend Guards**
- Create `<RoleGate>` component
- Implement `useHasRole()` hook
- Update UI to conditionally render based on role

**Step 4: Testing**
- Unit tests for middleware
- Integration tests for each role's access
- E2E test for complete user journey

## Files to Create/Modify
- `prisma/schema.prisma` - Add role enum
- `prisma/migrations/xxx_add_roles.sql` - New migration
- `src/middleware/auth.ts` - Role checking logic
- `src/components/RoleGate.tsx` - Permission UI wrapper
- `src/hooks/useHasRole.ts` - Permission checking hook
- `src/lib/permissions.ts` - Permission constants
- Tests for all above

## Risks & Considerations
- **Breaking change**: Existing API calls may fail if not updated
- **Migration risk**: Need to test role assignment for existing users
- **Security**: Ensure client-side checks are also validated server-side

## Estimated Scope
- ~8 files modified
- ~300 lines of new code
- ~150 lines of tests
- 1-2 hours implementation time
```

**After reviewing plan:**
```
Answers:
1. Database storage
2. Route + UI level for now
3. Single role per user
4. Default all existing to USER role

Plan looks good! Please proceed with execution.
```

**Plan mode workflow:**
```bash
# 1. Enter plan mode
<Shift+Tab>

# 2. Ask for plan
"Create a plan for implementing feature X"

# 3. Review plan output thoroughly
#    - Check assumptions
#    - Verify approach
#    - Look for missing pieces

# 4. Iterate if needed
"The plan looks good but I think we should use..."

# 5. Execute
"Plan approved. Please implement."

# 6. Return to plan mode for next change
<Shift+Tab>
```

### Sources

1. `/sources/youtube/peter-yang-movie-app-summary.md` - Plan mode provides transparency
2. `/sources/youtube/7wGE I was using Claude Code wrong... The Ultimate Work.md` - Always plan mode first
3. `/sources/youtube/800+ hours of Learning Claude Code in 8 minutes 2.md` - Q&A session before code
4. `/sources/youtube/I was wrong about Claude Code UPDATED AI workflow.md` - Review plan thoroughly
5. `/sources/youtube/A Complete Guide to Claude Code Here are ALL the.md` - Shift+Tab to toggle

---

## Practice #4: Step-by-Step Thinking / Chain of Thought

**Mentioned in**: 5 sources

### The Principle

Explicitly instruct Claude to think step-by-step, show its reasoning, and break down complex problems into smaller pieces. Use keywords like "think step by step", "show your work", "explain your reasoning".

### Why It Matters

- **20% accuracy improvement** on complex tasks (Anthropic research)
- **Reveals faulty assumptions** before execution
- **Better debugging** - See where logic goes wrong
- **Builds confidence** - Transparent reasoning process
- **Teaches you** - Learn from Claude's problem-solving approach

### Code Example

**❌ Without Chain of Thought:**
```
Fix the bug where users can't upload images larger than 5MB.
```

**✅ With Chain of Thought:**
```
Fix the bug where users can't upload images larger than 5MB.

Before writing any code:
1. Think step by step about what might be causing this
2. List all the places where file size might be restricted
3. Show your debugging approach
4. Explain your proposed fix and why it will work
5. Consider any edge cases or side effects

Use <thinking> tags to show your reasoning, then <solution>
for the final fix.
```

**Claude's Response:**
```xml
<thinking>
Let me analyze this systematically:

**Step 1: Potential restriction points**
- Frontend: Form input `accept` or `maxSize` attribute
- Client-side JS: File validation before upload
- Backend: Request body size limit (express.json/multer)
- Server: Nginx/Apache upload size limit
- Cloud storage: S3/GCS upload size restrictions

**Step 2: Most likely culprits for 5MB limit**
1. Express body-parser default: 100kb (too low, but not 5MB)
2. Multer default: No limit (not this)
3. Nginx default: 1MB (possible but usually causes 413 error)
4. **Common pattern: 5MB limit set in frontend or API route**

**Step 3: Debugging approach**
1. Check browser network tab - does request even send?
2. Check server logs - does request arrive?
3. Look for error messages - client or server?
4. Search codebase for "5" or "5MB" or "5000000"

**Step 4: Likely issue**
Based on common patterns, probably a validation check like:
```js
if (file.size > 5 * 1024 * 1024) {
  throw new Error('File too large');
}
```

**Step 5: Edge cases to consider**
- What's the new desired limit?
- Should we compress images client-side?
- Do we need different limits for different file types?
- What about multiple file uploads?
</thinking>

<solution>
Found the issue! In `src/lib/upload.ts` line 34:

```typescript
// Current code:
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB

if (file.size > MAX_FILE_SIZE) {
  throw new Error('File size exceeds 5MB limit');
}
```

**Recommended fix** (assuming we want to increase to 50MB):

```typescript
// Updated code:
const MAX_FILE_SIZE = 50 * 1024 * 1024; // 50MB

if (file.size > MAX_FILE_SIZE) {
  throw new Error(`File size exceeds ${MAX_FILE_SIZE / 1024 / 1024}MB limit`);
}
```

**Additional changes needed:**
1. Update backend body size limit (if using Express):
```javascript
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ limit: '50mb', extended: true }));
```

2. Update Multer config:
```javascript
const upload = multer({
  limits: { fileSize: 50 * 1024 * 1024 }
});
```

3. If using Nginx, update `/etc/nginx/nginx.conf`:
```nginx
client_max_body_size 50M;
```
</solution>
```

**Powerful Keywords for Claude Code:**
```markdown
# In your prompts or claude.md:

- "think step by step"
- "show your work"
- "explain your reasoning"
- "IMPORTANT" (Claude pays extra attention)
- "proactively" (Claude takes initiative)
- "ultrathink" (Claude uses more tokens for deeper thinking)
```

### Sources

1. `/sources/docs/anthropic-prompt-engineering.md` - 20% accuracy improvement, scratchpads
2. `/sources/youtube/7wGE I was using Claude Code wrong... The Ultimate Work.md` - Plan mode forces step-by-step
3. `/sources/youtube/800+ hours of Learning Claude Code in 8 minutes 2.md` - Breaking down problems
4. `/sources/youtube/Claude Code Is The Best AI Coding Agent.md` - Encourage deep thinking
5. `/sources/youtube/A Complete Guide to Claude Code Here are ALL the.md` - Keywords like "ultrathink"

---

## Practice #5: Sub-Agents / Parallel Task Delegation

**Mentioned in**: 5 sources

### The Principle

Define specialized sub-agents with focused responsibilities. The main Claude instance orchestrates, delegating subtasks to sub-agents that work in parallel with isolated contexts.

### Why It Matters

- **Reduces context pollution** - Each sub-agent has clean, focused context
- **Enables parallelization** - Multiple tasks execute simultaneously
- **Dramatically speeds up work** - 10x faster on multi-part tasks
- **Better quality** - Specialized prompts yield better results
- **Scalability** - Complex projects become manageable

### Code Example

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

**Using Sub-Agents:**

```markdown
# Main agent prompt:
I need to implement a new "forgot password" feature.

Please delegate as follows:
1. Backend expert: Implement password reset API endpoints
2. Frontend expert: Create reset password form
3. Testing expert: Add comprehensive tests

Each sub-agent should work independently and report back.

<thinking>
I'll coordinate three sub-agents in parallel:

**Sub-agent 1: backend-expert**
Task: Implement `/api/auth/forgot-password` and `/api/auth/reset-password`
- Generate reset token
- Send email with reset link
- Validate token and update password

**Sub-agent 2: frontend-expert**
Task: Create forgot password flow
- Page: /forgot-password
- Page: /reset-password/[token]
- Form validation and error handling

**Sub-agent 3: testing-expert**
Task: Test coverage
- Unit tests for token generation
- Integration tests for API endpoints
- E2E test for complete flow
</thinking>

[Sub-agents execute in parallel...]
```

**Configuration in Claude Code:**
```bash
# Create sub-agents directory
mkdir -p .claude/subagents

# Sub-agents are automatically discovered
# Reference them in prompts:
"Ask the backend-expert sub-agent to implement..."

# Or let Claude decide:
"Delegate this task to the appropriate sub-agent"
```

### Sources

1. `/sources/youtube/armin-ronacher-agentic-coding-summary.md` - Context management with sub-agents
2. `/sources/youtube/7wGE I was using Claude Code wrong... The Ultimate Work.md` - Sub-agent task completion
3. `/sources/youtube/800+ hours of Learning Claude Code in 8 minutes 2.md` - Task-based vs role-based
4. `/sources/youtube/I was wrong about Claude Code UPDATED AI workflow.md` - 10 parallel agents
5. `/sources/youtube/A Complete Guide to Claude Code Here are ALL the.md` - Specialized system prompts

---

## Practice #6: Clear, Explicit, and Direct Instructions

**Mentioned in**: 4+ sources (foundational to all)

### The Principle

State exactly what you want in simple, unambiguous language. Treat Claude like an intern on their first day - provide full context, explicit instructions, and clear expectations. Don't assume Claude will infer or guess.

### Why It Matters

- **Foundation of effective prompting** - Ambiguity is the #1 cause of poor output
- **Garbage in = garbage out** - Unclear prompts yield unclear results
- **Saves time** - Clear prompts reduce back-and-forth
- **Better results** - Claude 4.x models excel with explicit direction

### Code Example

**❌ Vague Instructions:**
```
Make the login better.
```

**❌ Ambiguous Instructions:**
```
Fix the auth issues and improve the UI.
```

**✅ Clear, Explicit Instructions:**
```markdown
# Task: Improve Login Experience

## Current Issues
1. No loading state - users unsure if login is processing
2. Error messages unclear ("Error 401" instead of "Invalid credentials")
3. No "Remember me" option
4. Can't see password while typing (no toggle)

## Requirements

### Backend Changes (if needed)
- [ ] Add rate limiting: Max 5 login attempts per 15 minutes per IP
- [ ] Return descriptive error messages (not just status codes)
- [ ] Support "remember me" with 30-day session vs 1-day default

### Frontend Changes
1. **Loading State**
   - Show spinner on submit button while authenticating
   - Disable form inputs during submission
   - Display "Signing in..." text

2. **Error Messages**
   - "Invalid email or password" (don't reveal which is wrong)
   - "Too many attempts. Try again in 15 minutes"
   - "Account locked. Contact support"

3. **Remember Me**
   - Add checkbox: "Keep me signed in for 30 days"
   - Persist choice in localStorage (for UX, not security)
   - Backend sets appropriate session expiry

4. **Password Visibility**
   - Add eye icon to toggle password visibility
   - Icon changes: eye (hidden) <-> eye-slash (visible)
   - Preserve toggle state if user unfocuses and refocuses

### Acceptance Criteria
- Loading state appears within 100ms of submit
- All error messages are user-friendly (no technical jargon)
- Remember me checkbox works and persists setting
- Password toggle works smoothly
- Form is keyboard accessible (Tab navigation works)
- Meets WCAG 2.1 AA accessibility standards

### Out of Scope
- Social login (OAuth)
- Two-factor authentication
- Password strength meter
- Email verification

### Files to Modify
- `/app/(auth)/login/page.tsx` - Login form component
- `/app/api/auth/login/route.ts` - Backend endpoint
- `/components/ui/password-input.tsx` - Create new component
- `/lib/auth.ts` - Session management logic

### Design Reference
Match the existing design system:
- Primary button: `bg-blue-600 hover:bg-blue-700`
- Error text: `text-red-600 text-sm`
- Input focus: `focus:ring-2 focus:ring-blue-500`

Please implement these changes and let me know when complete.
```

**Template for Clear Instructions:**
```markdown
# Task: [Concise title]

## Context
[Why are we doing this? What's the background?]

## Current State
[What exists now? What's the problem?]

## Desired State
[What should exist after this change?]

## Requirements
### Must Have
- [ ] Requirement 1
- [ ] Requirement 2

### Nice to Have
- [ ] Optional feature 1

### Out of Scope
- Thing we're NOT doing
- Another thing we're NOT doing

## Acceptance Criteria
How will we know this is done correctly?
- [ ] Criterion 1
- [ ] Criterion 2

## Files Involved
- `/path/to/file1.ts` - what changes here
- `/path/to/file2.tsx` - what changes here

## Constraints
- Don't break existing feature X
- Must maintain backwards compatibility
- Keep bundle size under Y

## Questions
[Any ambiguities I need clarified?]
```

### Sources

1. `/sources/docs/anthropic-prompt-engineering.md` - Treat Claude as "intern on first day"
2. `/sources/youtube/800+ hours of Learning Claude Code in 8 minutes 2.md` - Garbage in = garbage out
3. `/sources/youtube/A Complete Guide to Claude Code Here are ALL the.md` - Test, measure, iterate systematically

---

## Practice #7: Examples / Few-Shot Prompting

**Mentioned in**: 3 sources (including official Anthropic docs)

### The Principle

Provide 3-5 diverse, realistic examples showing the exact input/output pattern you want. Include edge cases. Show, don't just tell.

### Why It Matters

- **20% accuracy improvement** (Anthropic research with Fortune 500)
- **Reduces misinterpretation** - Claude sees exactly what you want
- **Format consistency** - Ensures output matches expectations
- **Handles edge cases** - Examples clarify boundary conditions
- **Faster results** - Less trial and error

### Code Example

**❌ Without Examples:**
```
Write API error responses in a consistent format.
```

**✅ With Few-Shot Examples:**
```markdown
# Task: Implement consistent error responses across all API routes

Use this exact format for ALL API errors:

## Examples

### Example 1: Validation Error
**Input:** POST /api/users with invalid email

**Output:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address",
        "received": "not-an-email"
      }
    ]
  },
  "timestamp": "2024-11-14T10:30:00Z"
}
```
**HTTP Status:** 400

### Example 2: Authentication Error
**Input:** GET /api/protected without auth header

**Output:**
```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required",
    "details": null
  },
  "timestamp": "2024-11-14T10:30:00Z"
}
```
**HTTP Status:** 401

### Example 3: Not Found Error
**Input:** GET /api/users/999 (non-existent user)

**Output:**
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "User not found",
    "details": {
      "resource": "User",
      "id": "999"
    }
  },
  "timestamp": "2024-11-14T10:30:00Z"
}
```
**HTTP Status:** 404

### Example 4: Server Error
**Input:** POST /api/process (database connection fails)

**Output:**
```json
{
  "success": false,
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred",
    "details": null
  },
  "timestamp": "2024-11-14T10:30:00Z"
}
```
**HTTP Status:** 500

### Example 5: Rate Limit Error (Edge Case)
**Input:** Too many requests from same IP

**Output:**
```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please try again later.",
    "details": {
      "retryAfter": 900,
      "limit": 100,
      "window": "15 minutes"
    }
  },
  "timestamp": "2024-11-14T10:30:00Z"
}
```
**HTTP Status:** 429

---

Now implement this pattern across all API routes:
- `/app/api/users/route.ts`
- `/app/api/posts/route.ts`
- `/app/api/auth/login/route.ts`
- `/app/api/auth/register/route.ts`

Create a helper function in `/lib/api-response.ts`:

```typescript
// Expected helper signature:
function errorResponse(
  code: string,
  message: string,
  details?: any,
  statusCode?: number
): Response

// Usage in routes:
return errorResponse('NOT_FOUND', 'User not found', { id }, 404);
```
```

**Few-Shot for Code Style:**
```markdown
# Task: Refactor utility functions to match our code style

## Examples of Our Style

### Example 1: Date Formatting
```typescript
/**
 * Formats a date as YYYY-MM-DD
 * @param date - Date to format
 * @returns Formatted date string
 * @example formatDate(new Date('2024-11-14')) // => '2024-11-14'
 */
export function formatDate(date: Date): string {
  return date.toISOString().split('T')[0];
}
```

### Example 2: Array Operations
```typescript
/**
 * Removes duplicate items from an array
 * @param items - Array with potential duplicates
 * @returns Array with unique items only
 * @example unique([1, 2, 2, 3]) // => [1, 2, 3]
 */
export function unique<T>(items: T[]): T[] {
  return [...new Set(items)];
}
```

### Example 3: String Operations
```typescript
/**
 * Capitalizes the first letter of a string
 * @param str - String to capitalize
 * @returns Capitalized string
 * @example capitalize('hello') // => 'Hello'
 * @example capitalize('') // => ''
 */
export function capitalize(str: string): string {
  if (!str) return str;
  return str.charAt(0).toUpperCase() + str.slice(1);
}
```

Now refactor these utility functions to match this style:
- [existing functions to refactor]
```

### Sources

1. `/sources/docs/anthropic-prompt-engineering.md` - 3-5 examples, 20% improvement
2. `/sources/youtube/peter-yang-movie-app-summary.md` - Edge cases clarify expectations
3. `/sources/youtube/A Complete Guide to Claude Code Here are ALL the.md` - Examples in PRP framework

---

## Practice #8: Custom Commands / Reusable Workflows

**Mentioned in**: 3 sources

### The Principle

Create custom slash commands for repetitive tasks and multi-step workflows. Store them in `.claude/commands/` directory for easy reuse.

### Why It Matters

- **Eliminates repetition** - One command instead of long prompts
- **Consistency** - Same workflow every time
- **Complex workflows** - Multi-step processes in one command
- **Team sharing** - Standardized commands across team
- **Faster development** - Common tasks become trivial

### Code Example

**File: `.claude/commands/add-api-route.md`**
```markdown
---
description: Create a new API route with validation and tests
---

# Add API Route

You will create a complete API route following our project patterns.

## Step 1: Gather Requirements
Ask the user:
1. What's the route path? (e.g., `/api/products`)
2. What HTTP methods? (GET, POST, PUT, DELETE)
3. What's the data model? (fields and types)
4. Any special business logic?

## Step 2: Create Files

### API Route: `app/api/[route]/route.ts`
```typescript
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { prisma } from '@/lib/prisma';
import { errorResponse } from '@/lib/api-response';

// Validation schema
const schema = z.object({
  // ... based on user's data model
});

export async function GET(request: NextRequest) {
  try {
    const items = await prisma.[model].findMany();
    return NextResponse.json({ success: true, data: items });
  } catch (error) {
    return errorResponse('INTERNAL_ERROR', 'Failed to fetch items', null, 500);
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const validated = schema.parse(body);

    const item = await prisma.[model].create({
      data: validated
    });

    return NextResponse.json({ success: true, data: item }, { status: 201 });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return errorResponse('VALIDATION_ERROR', 'Invalid data', error.errors, 400);
    }
    return errorResponse('INTERNAL_ERROR', 'Failed to create item', null, 500);
  }
}
```

### Test File: `tests/api/[route].test.ts`
```typescript
import { describe, it, expect } from 'vitest';
import { POST, GET } from '@/app/api/[route]/route';

describe('[Route] API', () => {
  it('should create item with valid data', async () => {
    // Test implementation
  });

  it('should return 400 with invalid data', async () => {
    // Test implementation
  });

  it('should fetch all items', async () => {
    // Test implementation
  });
});
```

## Step 3: Update Prisma Schema
Add the model to `prisma/schema.prisma` if needed.

## Step 4: Create TypeScript Types
Add to `src/types/[model].ts`:
```typescript
import { z } from 'zod';

export const [Model]Schema = z.object({
  // ... schema
});

export type [Model] = z.infer<typeof [Model]Schema>;
```

## Step 5: Summary
After creation, show:
- Files created
- Next steps (run migration if DB schema changed)
- Example API calls with curl
```

**Usage:**
```bash
# User types:
/add-api-route

# Claude asks clarifying questions, then creates all files
```

**More Custom Command Examples:**

**File: `.claude/commands/fix-eslint.md`**
```markdown
---
description: Fix all ESLint errors in the codebase
---

1. Run `npm run lint` to identify errors
2. For each error:
   - If it's auto-fixable: Run `npm run lint:fix`
   - If manual: Fix following our code style guide
3. Verify: Run `npm run lint` again
4. Show summary of what was fixed
```

**File: `.claude/commands/pre-commit.md`**
```markdown
---
description: Pre-commit checks before pushing code
---

Run these checks in order:

1. **Type checking:** `npm run type-check`
   - If fails: Fix TypeScript errors

2. **Linting:** `npm run lint`
   - If fails: Fix ESLint errors

3. **Tests:** `npm run test`
   - If fails: Fix failing tests

4. **Build:** `npm run build`
   - If fails: Fix build errors

5. **Summary:**
   - ✅ All checks passed
   - Or ❌ Failed at step X with error Y

Only say "Ready to commit" if ALL checks pass.
```

**File: `.claude/commands/refactor-component.md`**
```markdown
---
description: Refactor a component to follow our patterns
---

# Component Refactor Workflow

## Step 1: Analysis
Analyze the target component for:
- Missing TypeScript types
- Inline styles (should use Tailwind)
- Missing prop validation
- Accessibility issues
- Performance issues (missing useMemo/useCallback)

## Step 2: Refactor
Apply these patterns:
1. Explicit TypeScript interface for props
2. Destructure props
3. Group hooks logically
4. Extract complex logic to custom hooks
5. Add JSDoc comments
6. Ensure accessibility (a11y)

## Step 3: Create Tests
Add test file with:
- Rendering test
- User interaction tests
- Edge case tests

## Step 4: Show Diff
Show before/after comparison and list improvements.
```

### Sources

1. `/sources/youtube/7wGE I was using Claude Code wrong... The Ultimate Work.md` - Custom slash commands
2. `/sources/youtube/800+ hours of Learning Claude Code in 8 minutes 2.md` - Command library for repetitive tasks
3. `/sources/youtube/A Complete Guide to Claude Code Here are ALL the.md` - Agentic workflows as prompts

---

## Practice #9: MCP Servers / External Tool Integration

**Mentioned in**: 3 sources

### The Principle

Use Model Context Protocol (MCP) servers to extend Claude's capabilities beyond code. Connect Claude to databases, documentation, browsers, file systems, and external APIs.

### Why It Matters

- **Access up-to-date documentation** - Never out of date
- **Database operations** - Query prod data directly
- **Browser automation** - Research and data gathering
- **File system access** - Read/write files outside project
- **API integration** - Connect to external services

### Code Example

**Installation:**
```bash
# Install Context7 (documentation MCP)
npm install -g @context7/mcp-server

# Install Filesystem MCP
npm install -g @modelcontextprotocol/server-filesystem

# Install Browser MCP
npm install -g @modelcontextprotocol/server-playwright

# Install Database MCP
npm install -g @supabase/mcp-server
```

**Configuration: `.claude/mcp_settings.json`**
```json
{
  "mcpServers": {
    "context7": {
      "command": "context7-mcp",
      "args": ["--libraries", "nextjs,react,tailwindcss,prisma"],
      "description": "Up-to-date documentation for popular libraries"
    },

    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/username/Documents"],
      "description": "Access to local file system"
    },

    "browser": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-playwright"],
      "description": "Browser automation for research"
    },

    "supabase": {
      "command": "npx",
      "args": [
        "-y",
        "@supabase/mcp-server",
        "--supabase-url", "https://xxx.supabase.co",
        "--supabase-key", "your-service-key"
      ],
      "description": "Direct database access"
    },

    "serena": {
      "command": "npx",
      "args": ["-y", "@serena-ai/mcp-server"],
      "description": "Semantic code search and retrieval"
    }
  }
}
```

**Usage Example 1: Documentation Lookup**
```markdown
# Without MCP:
User: "How do I use React Query's useInfiniteQuery?"
Claude: [May provide outdated or generic info from training data]

# With Context7 MCP:
User: "How do I use React Query's useInfiniteQuery?"
Claude: [Fetches latest docs from tanstack.com]
"According to the current React Query documentation (v5.0),
useInfiniteQuery works like this:

```typescript
import { useInfiniteQuery } from '@tanstack/react-query'

function Projects() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetching,
  } = useInfiniteQuery({
    queryKey: ['projects'],
    queryFn: ({ pageParam = 0 }) => fetchProjects(pageParam),
    getNextPageParam: (lastPage) => lastPage.nextCursor,
  })
}
```
[Rest of current, accurate documentation]"
```

**Usage Example 2: Database Queries**
```markdown
User: "How many users signed up in the last 7 days?"

Claude (with Supabase MCP):
Let me query the database directly.

[Executes via MCP]:
SELECT COUNT(*) FROM users
WHERE created_at >= NOW() - INTERVAL '7 days';

Result: 247 users signed up in the last 7 days.

Breakdown by day:
- Nov 14: 42 users
- Nov 13: 38 users
- Nov 12: 31 users
- Nov 11: 45 users
- Nov 10: 29 users
- Nov 9: 35 users
- Nov 8: 27 users
```

**Usage Example 3: Research with Browser**
```markdown
User: "Find the best practices for Next.js 14 app router from
recent articles"

Claude (with Browser MCP):
I'll search for recent articles and summarize best practices.

[Executes browser automation]:
1. Searches "Next.js 14 app router best practices 2024"
2. Opens top 5 articles
3. Extracts relevant information
4. Synthesizes findings

**Summary of Best Practices:**

1. **Server Components by Default**
   - Use "use client" sparingly
   - Reduces bundle size
   - Better performance

2. **Parallel Routes for Layouts**
   - Use (@folder) convention
   - Enables complex layouts
   [etc.]

Sources:
- vercel.com/blog/next14-app-router
- leerob.io/nextjs-patterns
- [etc.]
```

**Usage Example 4: Semantic Code Search (Serena MCP)**
```markdown
User: "Find all places where we handle user authentication"

Claude (with Serena MCP):
Using semantic search across the codebase...

**Found 7 relevant locations:**

1. `/lib/auth.ts` (lines 45-89)
   - Main authentication logic
   - JWT token generation and validation

2. `/middleware.ts` (lines 12-34)
   - Route protection middleware
   - Checks auth status before page load

3. `/app/api/auth/login/route.ts`
   - Login endpoint
   - Validates credentials

4. `/app/api/auth/logout/route.ts`
   - Logout endpoint
   - Clears session

5. `/components/auth/LoginForm.tsx`
   - Frontend login UI
   - Handles login form submission

6. `/hooks/useAuth.ts`
   - React hook for auth state
   - Provides user info and auth functions

7. `/lib/session.ts`
   - Session management
   - Cookie handling

Would you like me to show the code for any of these?
```

**Common MCP Servers:**

| MCP Server | Purpose | Use Case |
|------------|---------|----------|
| **context7** | Live documentation | Get latest library docs |
| **serena** | Semantic code search | Find code by meaning, not just keywords |
| **filesystem** | File system access | Read/write files outside project |
| **browser** | Web automation | Research, scraping, testing |
| **supabase** | Database access | Query/modify production data |
| **github** | GitHub operations | Issues, PRs, repo management |
| **postgres** | PostgreSQL | Direct database queries |
| **gitlab** | GitLab operations | Issues, MRs, pipelines |

### Sources

1. `/sources/youtube/armin-ronacher-agentic-coding-summary.md` - MCP for context sharing
2. `/sources/youtube/800+ hours of Learning Claude Code in 8 minutes 2.md` - Context7 and Supabase MCP
3. `/sources/youtube/A Complete Guide to Claude Code Here are ALL the.md` - Serena MCP for semantic retrieval

---

## Practice #10: Code Review & Validation

**Mentioned in**: 3 sources

### The Principle

Always review Claude's code output. Don't blindly accept. Ask Claude to review its own code, check for edge cases, run tests, and validate assumptions.

### Why It Matters

- **Prevents security vulnerabilities** - Catch SQL injection, XSS, etc.
- **Finds edge cases** - Logic bugs in unusual scenarios
- **Maintains quality standards** - Consistent code quality
- **Learns from review** - Improves your understanding
- **Ownership** - Humans own the code, not AI

### Code Example

**Step 1: Initial Implementation**
```markdown
User: "Implement user password reset functionality"

Claude: [Generates code]

User: "Before I accept this, please review your own code for:
1. Security vulnerabilities
2. Edge cases
3. Error handling
4. Potential bugs

Be critical and honest."
```

**Step 2: Self-Review by Claude**
```markdown
Claude: "Let me review the code I just wrote:

<review>
## Security Issues Found

1. **CRITICAL: Token not cryptographically secure**
```typescript
// ❌ Current code:
const resetToken = Math.random().toString(36);

// ✅ Should be:
import crypto from 'crypto';
const resetToken = crypto.randomBytes(32).toString('hex');
```
**Risk:** Predictable tokens could be brute-forced.

2. **HIGH: No token expiration**
```typescript
// ❌ Current code:
const resetLink = `${baseUrl}/reset-password/${resetToken}`;

// ✅ Should include expiry:
const expiresAt = new Date(Date.now() + 60 * 60 * 1000); // 1 hour
await prisma.passwordReset.create({
  data: { token, expiresAt, userId }
});
```
**Risk:** Tokens never expire, can be used indefinitely.

3. **MEDIUM: No rate limiting**
No protection against spam/DoS via password reset.
**Recommendation:** Add rate limit of 3 requests per hour per email.

## Edge Cases Not Handled

1. **User doesn't exist:** Currently returns success to avoid email enumeration,
   but doesn't handle gracefully. Good for security, but should still log attempt.

2. **Multiple reset requests:** If user requests reset twice, old token should
   be invalidated.

3. **Email send failure:** If email service is down, token is created but user
   never receives it. Should rollback token creation on email failure.

4. **Account already locked:** Should we allow reset for locked accounts?

## Error Handling Issues

1. **Database errors not caught properly:**
```typescript
// ❌ Current:
const user = await prisma.user.findUnique({ where: { email } });

// ✅ Should be:
try {
  const user = await prisma.user.findUnique({ where: { email } });
} catch (error) {
  logger.error('Database error during password reset', { error });
  return res.status(500).json({ error: 'Service temporarily unavailable' });
}
```

## Recommendations

1. Use crypto.randomBytes() for tokens
2. Add expiration timestamp (1 hour)
3. Implement rate limiting
4. Add comprehensive error handling
5. Invalidate old tokens on new request
6. Add transaction wrapper for token creation + email send
7. Add tests for all edge cases

Would you like me to implement these fixes?
</review>
```

**Step 3: Validation Checklist**

Create a standard review checklist in `.claude/commands/review-code.md`:

```markdown
---
description: Review code for quality, security, and correctness
---

# Code Review Checklist

Review the recently modified files and check ALL of the following:

## Security
- [ ] No SQL injection vulnerabilities (use parameterized queries)
- [ ] No XSS vulnerabilities (sanitize user input)
- [ ] No hardcoded secrets or API keys
- [ ] Authentication properly enforced
- [ ] Authorization checks in place
- [ ] Sensitive data properly encrypted
- [ ] CSRF protection where needed

## Error Handling
- [ ] All async operations have try/catch
- [ ] Errors logged with sufficient context
- [ ] User-friendly error messages (no stack traces)
- [ ] Graceful degradation on failures
- [ ] Proper HTTP status codes

## Data Validation
- [ ] All user inputs validated
- [ ] Type checking with TypeScript
- [ ] Zod schemas for runtime validation
- [ ] Null/undefined checks where needed
- [ ] Array bounds checking

## Edge Cases
- [ ] Empty arrays/objects handled
- [ ] Null/undefined inputs handled
- [ ] Very large inputs handled (pagination?)
- [ ] Concurrent requests handled (race conditions?)
- [ ] Network failures handled

## Performance
- [ ] No N+1 queries
- [ ] Database queries optimized
- [ ] Appropriate caching
- [ ] No unnecessary re-renders (React)
- [ ] Efficient algorithms (no O(n²) unless necessary)

## Code Quality
- [ ] Follows project coding standards
- [ ] Functions are single responsibility
- [ ] No code duplication
- [ ] Clear variable/function names
- [ ] Adequate comments for complex logic
- [ ] TypeScript types are explicit

## Testing
- [ ] Unit tests exist and pass
- [ ] Integration tests if needed
- [ ] Edge cases covered by tests
- [ ] Happy path tested
- [ ] Error paths tested

## Accessibility (if UI)
- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] ARIA labels where needed
- [ ] Color contrast sufficient
- [ ] Focus indicators visible

## Final Checks
- [ ] No console.log() or debugging code
- [ ] No commented-out code
- [ ] All TODOs have issue numbers
- [ ] Dependencies are necessary
- [ ] Breaking changes documented

---

After reviewing, provide:
1. List of issues found (with severity)
2. Recommended fixes
3. Overall quality score (1-10)
```

**Usage:**
```bash
# After Claude generates code:
/review-code

# Claude runs through checklist and reports issues
```

**Step 4: Automated Testing**

```markdown
User: "Please write tests for the password reset functionality
covering all edge cases you identified."

Claude: [Generates comprehensive tests]
```

**Step 5: Human Review**

```typescript
// As a human reviewer, check:
// 1. Does the code make sense?
// 2. Are there business logic issues AI wouldn't catch?
// 3. Does it fit the broader architecture?
// 4. Are there non-obvious security implications?
```

**Validation Workflow:**
```
1. Claude implements feature
     ↓
2. Claude self-reviews (security, edge cases, errors)
     ↓
3. Claude fixes issues found
     ↓
4. Claude writes tests
     ↓
5. Run tests: npm run test
     ↓
6. Human reviews code (PR-style)
     ↓
7. Accept or request changes
```

### Sources

1. `/sources/youtube/800+ hours of Learning Claude Code in 8 minutes 2.md` - AI generates, humans own
2. `/sources/youtube/I was wrong about Claude Code UPDATED AI workflow.md` - Always review code
3. `/sources/youtube/A Complete Guide to Claude Code Here are ALL the.md` - Validation gates

---

## Honorable Mentions

### Practice 11: XML Tags for Structure
**Mentioned in**: 2 sources (but official Anthropic recommendation)

Use XML tags to structure complex prompts:
```xml
<context>Background info</context>
<task>What to do</task>
<examples>Sample inputs/outputs</examples>
<constraints>What to avoid</constraints>
```

### Practice 12: Iterative Testing & Experimentation
**Mentioned in**: 3 sources

"Prompt engineering is a science"—test, measure, iterate systematically. Learn from failures.

### Practice 13: Git-Based Checkpointing
**Mentioned in**: 2 sources

Commit frequently. Use Git as a checkpoint system. Easy to revert if Claude goes wrong.

```bash
git add .
git commit -m "Before Claude makes changes"
# Let Claude work...
# If bad: git reset --hard HEAD^
# If good: git commit -m "After Claude changes"
```

---

## Summary Matrix

| Practice | Frequency | Impact | Difficulty | Priority |
|----------|-----------|--------|------------|----------|
| Context Management | 7+ | High (30%) | Medium | Critical |
| Claude.md Memory | 5 | High | Easy | Critical |
| Plan Mode | 5 | High | Easy | Critical |
| Step-by-Step Thinking | 5 | High (20%) | Easy | Critical |
| Sub-Agents | 5 | High | Hard | Important |
| Clear Instructions | 4+ | High | Easy | Critical |
| Few-Shot Examples | 3 | High (20%) | Easy | Important |
| Custom Commands | 3 | Medium | Medium | Important |
| MCP Servers | 3 | High | Medium | Important |
| Code Review | 3 | High | Easy | Critical |

---

## How to Implement All 10 Practices

**Week 1: Foundations**
1. Create `claude.md` with project conventions
2. Practice clear, explicit instructions
3. Always use plan mode before coding

**Week 2: Advanced Techniques**
4. Add step-by-step thinking to prompts
5. Create 2-3 few-shot examples for common tasks
6. Set up basic MCP servers (Context7)

**Week 3: Optimization**
7. Build first custom command for repetitive task
8. Implement code review workflow
9. Configure context management strategy

**Week 4: Mastery**
10. Set up sub-agents for complex projects
11. Refine all practices based on learnings
12. Document your personalized workflow

---

## Recommended Reading Order

1. **Start here**: Practice #6 (Clear Instructions)
2. **Then**: Practice #2 (Claude.md)
3. **Next**: Practice #3 (Plan Mode)
4. **Follow with**: Practice #1 (Context Management)
5. **Advanced**: Practice #4, #5, #7-10

---

## Sources Analyzed

### Official Documentation (1)
- `/sources/docs/anthropic-prompt-engineering.md`

### YouTube Tutorials (10)
1. `/sources/youtube/peter-yang-movie-app-summary.md`
2. `/sources/youtube/armin-ronacher-agentic-coding-summary.md`
3. `/sources/youtube/simon-willison-github-actions-summary.md`
4. `/sources/youtube/800+ hours of Learning Claude Code in 8 minutes 2.md`
5. `/sources/youtube/Claude Code Is The Best AI Coding Agent.md`
6. `/sources/youtube/A Complete Guide to Claude Code Here are ALL the.md`
7. `/sources/youtube/7wGE I was using Claude Code wrong... The Ultimate Work.md`
8. `/sources/youtube/I was wrong about Claude Code UPDATED AI workflow.md`
9. `/sources/youtube/mobile-app-monetization-guide-transcript.md`
10. `/sources/youtube/top-tutorials.json`

**Total Sources**: 11 files
**Analysis Date**: November 14, 2024
**Methodology**: Cross-reference frequency analysis, extracting practices mentioned in 3+ sources

---

**Next Steps**:
1. Review patterns directory for complementary architecture patterns
2. Create personalized workflow combining these practices
3. Build template projects demonstrating all 10 practices
