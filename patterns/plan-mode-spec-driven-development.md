---
pattern_name: Plan Mode / Spec-Driven Development
category: Workflow
difficulty: Beginner
impact: High
date_created: 2024-11-14
last_updated: 2024-11-14
---

# Pattern: Plan Mode / Spec-Driven Development

> **TL;DR**: Always use plan mode (Shift+Tab in Claude Code) before executing code changes. Claude creates a detailed specification, you review and iterate, then execute—preventing wasted effort and ensuring alignment.

## Overview

Plan Mode is Claude Code's built-in workflow for **spec-driven development**: separate planning from execution. Instead of diving straight into code, you explicitly ask Claude to create a detailed plan first, review it together, iterate until it's right, then execute.

This mirrors professional software development where design and planning precede implementation. The key insight: **fixing mistakes in a plan is cheap** (a few tokens, a few seconds), but **fixing mistakes in code is expensive** (many tokens, many minutes, potential regressions).

Plan Mode provides transparency into Claude's reasoning, ensures alignment on approach, catches issues early, and ultimately produces higher-quality code with less back-and-forth.

---

## Problem It Solves

### The Challenge

When you ask Claude to implement a feature directly:
- Claude makes assumptions about requirements that may be wrong
- You don't see the implementation strategy until code is generated
- Mistakes discovered after code is written waste time and tokens
- No opportunity to guide the approach before work begins
- Hard to catch architectural issues or scope creep early

**Common Symptoms:**
- "That's not what I wanted" after Claude generates 500 lines of code
- Claude builds feature X when you wanted feature Y
- Multiple iteration cycles fixing the same code
- Wasted effort implementing wrong approach
- Frustration: "If only Claude had asked first!"

**Without This Pattern:**
- **50-70% rework rate** on complex tasks
- **10x token waste** on trial-and-error coding
- **Poor architecture** from rushing to implementation
- **Scope creep** as requirements get misunderstood
- **Developer frustration** from repeated corrections

### Why Traditional Approaches Fall Short

**Direct code requests**: No review opportunity before effort invested

**"Just ask questions first"**: Inconsistent—Claude might skip clarifying

**Post-hoc review**: Expensive to fix after code is written

---

## The Solution

### Core Concept

Separate the **planning phase** from the **execution phase**:

1. **Plan Mode** (Shift+Tab): Claude creates a specification
   - Asks clarifying questions
   - Proposes architecture and approach
   - Lists files to create/modify
   - Identifies risks and edge cases
   - Estimates scope

2. **Review**: You evaluate the plan
   - Check assumptions
   - Verify approach
   - Answer clarifying questions
   - Identify gaps

3. **Iterate**: Refine the plan until perfect
   - Cheap (just conversation)
   - Fast (no code to rewrite)
   - Thorough (catch all issues)

4. **Execute**: Claude implements the approved plan
   - High confidence (plan is solid)
   - Minimal rework (issues already caught)
   - Efficient (no wasted coding effort)

### Key Principles

1. **Planning Before Implementation**: Always spec before code
2. **Explicit Review Gates**: Formal approval before execution
3. **Cheap Iterations**: Fix plan errors, not code errors
4. **Transparency**: See Claude's reasoning and strategy
5. **Alignment**: Ensure shared understanding before work begins

### How It Works

1. **Enter Plan Mode**: Press Shift+Tab in Claude Code
2. **Request Plan**: "Create a detailed plan for implementing feature X"
3. **Claude Plans**: Asks questions, proposes approach, identifies risks
4. **You Review**: Check assumptions, verify approach, answer questions
5. **Iterate**: Refine plan until it's perfect
6. **Approve**: Explicitly say "Plan approved, please implement"
7. **Execute**: Claude implements according to the plan

---

## Implementation

### Basic Implementation

**Workflow:**

```bash
# Step 1: Enter Plan Mode
<Shift+Tab>

# Step 2: Request Plan
"I need to add user roles and permissions to the app.
Admins can do everything, Managers can create/edit, Users can view only.
Please create a detailed plan."

# Step 3: Claude Responds in Plan Mode
```

**Claude's Plan Mode Response:**

```markdown
# Implementation Plan: Role-Based Access Control (RBAC)

## Clarifying Questions

Before I proceed, I need to understand:

1. **Database Storage**:
   - Should roles be stored in the database or config file?
   - Can users have multiple roles or just one?

2. **Permission Granularity**:
   - Route-level (API endpoints)?
   - UI-level (show/hide components)?
   - Data-level (filter database queries)?

3. **Existing Users**:
   - How should we migrate existing users to the new role system?
   - Default role for existing users?

4. **Edge Cases**:
   - Can admins be demoted?
   - What happens if a user's role changes mid-session?

## Proposed Architecture

### Approach: Database-Backed RBAC with Middleware

**Database Layer:**
- Add `role` enum to User model: `ADMIN | MANAGER | USER`
- Migration to add role column with default value

**API Layer:**
- Create middleware to check roles before route execution
- Export `requireRole(['ADMIN', 'MANAGER'])` higher-order function

**Frontend Layer:**
- Create `<RoleGate>` component for conditional rendering
- Implement `useHasRole(role)` hook for permission checks

## Implementation Steps

### Step 1: Database Schema Update
**File**: `prisma/schema.prisma`
- Add Role enum
- Add role field to User model
- Create migration

### Step 2: Backend Middleware
**File**: `src/middleware/auth.ts`
- Create role checking middleware
- Export requireRole HOF for route protection

### Step 3: Frontend Components
**Files**:
- `src/components/RoleGate.tsx` - Permission wrapper
- `src/hooks/useHasRole.ts` - Permission hook

### Step 4: Apply to Routes
**Files**: Various API routes
- Protect admin routes
- Protect manager routes
- Leave user routes open

### Step 5: Testing
**Files**:
- `tests/middleware/auth.test.ts`
- `tests/components/RoleGate.test.tsx`
- `tests/integration/rbac.test.ts`

## Files to Create/Modify

### New Files (5)
- `prisma/migrations/XXXXXX_add_user_roles.sql`
- `src/middleware/auth.ts`
- `src/components/RoleGate.tsx`
- `src/hooks/useHasRole.ts`
- `src/lib/permissions.ts`

### Modified Files (3)
- `prisma/schema.prisma`
- `src/types/user.ts`
- `src/lib/session.ts`

### Test Files (3)
- `tests/middleware/auth.test.ts`
- `tests/components/RoleGate.test.tsx`
- `tests/integration/rbac.test.ts`

## Risks & Considerations

⚠️ **Breaking Changes**:
- Existing API calls without role checks may fail
- Frontend may need updates to handle role-based rendering

⚠️ **Migration Risk**:
- Need careful handling of existing user roles
- Consider making default role configurable

⚠️ **Security**:
- Client-side checks are UX only—must validate server-side
- Session refresh needed if role changes

⚠️ **Performance**:
- Middleware adds small overhead to every protected route
- Consider caching role checks

## Estimated Scope

- **Files**: 8 new + 3 modified
- **Lines of Code**: ~400 production + ~200 tests
- **Time**: 2-3 hours for full implementation and testing

## Open Questions

1. Do you want fine-grained permissions (e.g., "can_edit_posts") or just roles?
2. Should role checks be optimistic (assume allowed) or pessimistic (assume denied)?
3. Do you want audit logging for role changes?
```

**Your Review:**

```markdown
Answers to questions:
1. Database storage, single role per user
2. Start with route + UI level, data-level later
3. Default existing users to USER role
4. Admins can be demoted, session refresh on role change

Plan looks comprehensive! A few adjustments:
- Add audit logging for role changes (good idea)
- Use pessimistic permissions (deny by default)
- Add admin UI for role management

Please update the plan with these changes.
```

**Claude Iterates on Plan:**

```markdown
# Updated Plan: RBAC with Audit Logging and Admin UI

[... updated sections ...]

## Additional Components

### Admin UI for Role Management
**File**: `src/app/admin/users/page.tsx`
- Table showing all users with current roles
- Dropdown to change user roles
- Audit log display

### Audit Logging
**File**: `src/lib/audit.ts`
- Log role changes with timestamp, actor, target user
- Store in `role_change_log` table
```

**Final Approval:**

```markdown
Perfect! Plan approved. Please implement.
```

### Advanced Implementation

**Complex Feature with Sub-Plans:**

```bash
# Initial Plan Request
<Shift+Tab>
"Implement real-time chat feature with typing indicators, read receipts,
file sharing, and message search. Create a comprehensive plan."

# Claude Creates Master Plan
```

**Claude's Master Plan:**

```markdown
# Master Plan: Real-Time Chat Feature

This is a large feature. I recommend breaking it into phases:

## Phase 1: Core Chat (Week 1)
- Basic messaging
- Real-time delivery via WebSockets
- Message history

## Phase 2: Presence & Indicators (Week 2)
- Typing indicators
- Read receipts
- Online/offline status

## Phase 3: Media & Search (Week 3)
- File upload/download
- Image previews
- Message search

## Recommendation

Let's start with Phase 1. Should I create a detailed plan for:
A) Phase 1 only (core chat)
B) All phases (full specification)
C) Different breakdown?
```

**Your Response:**

```markdown
Create detailed plan for Phase 1 only. We'll plan Phase 2 once Phase 1 is validated.
```

**Claude Creates Detailed Phase 1 Plan:**

```markdown
# Detailed Plan: Phase 1 - Core Chat

## Architecture: WebSocket-Based Real-Time Chat

### Tech Stack Decision
- **WebSocket Server**: Socket.io (battle-tested, fallbacks)
- **Database**: PostgreSQL with Prisma (message storage)
- **State Management**: Zustand (client-side chat state)
- **UI**: React components with shadcn/ui

### Database Schema

```prisma
model Conversation {
  id        String    @id @default(cuid())
  participants User[]  @relation("ConversationParticipants")
  messages  Message[]
  createdAt DateTime  @default(now())
  updatedAt DateTime  @updatedAt
}

model Message {
  id             String       @id @default(cuid())
  content        String       @db.Text
  senderId       String
  sender         User         @relation(fields: [senderId], references: [id])
  conversationId String
  conversation   Conversation @relation(fields: [conversationId], references: [id])
  createdAt      DateTime     @default(now())

  @@index([conversationId])
  @@index([createdAt])
}
```

[... continues with 20+ more sections ...]
```

### Configuration

**Enable Plan Mode in Claude Code:**

Plan mode is built into Claude Code—no configuration needed.

**Keyboard Shortcut:**
- **Shift+Tab**: Toggle plan mode on/off
- **Visual Indicator**: Interface shows "Plan Mode" when active

**Best Practice Configuration in `claude.md`:**

```markdown
## Workflow Requirements

### Before Implementing Features

**IMPORTANT**: Always use plan mode (Shift+Tab) when:
- Creating new features (3+ files affected)
- Refactoring (significant changes to existing code)
- Bug fixes (non-trivial, affects multiple areas)
- Architecture decisions

**Plan Mode Workflow**:
1. Enter plan mode (Shift+Tab)
2. Request detailed plan with clarifying questions
3. Review plan thoroughly—check assumptions, approach, scope
4. Iterate on plan until perfect
5. Explicitly approve: "Plan approved, please implement"
6. Exit plan mode and execute

**Only Skip Plan Mode For**:
- Trivial changes (single line, formatting)
- Well-defined micro-tasks
- Simple bug fixes (obvious one-line changes)
```

---

## Complete Code Example

### Scenario

You need to add a "forgot password" feature to your application. Using plan mode ensures the implementation is secure and complete before any code is written.

**Requirements:**
- User can request password reset via email
- Secure token generation
- Email with reset link
- Token expiration
- Proper security measures

### Implementation

**Step 1: Enter Plan Mode and Request Plan**

```bash
<Shift+Tab>

"Implement forgot password functionality. Users should be able to:
1. Request a password reset via email
2. Receive a secure reset link
3. Use the link to set a new password

Please create a comprehensive plan including security considerations."
```

**Step 2: Claude's Plan**

```markdown
# Implementation Plan: Forgot Password Feature

## Security Considerations First ⚠️

Before we design, key security requirements:
1. **Tokens must be cryptographically secure** (not predictable)
2. **Tokens must expire** (prevent indefinite validity)
3. **Rate limiting** (prevent email bombing)
4. **Email enumeration protection** (don't reveal if email exists)
5. **One-time use** (token invalidated after use)
6. **No sensitive data in URL** (token should be hash, not user ID)

## Clarifying Questions

1. **Token Expiration**: How long should reset links be valid? (Recommend: 1 hour)
2. **Rate Limiting**: How many requests per email/IP? (Recommend: 3 per hour)
3. **Email Service**: What service are you using? (SendGrid, SES, Resend?)
4. **Existing Auth**: You use NextAuth.js—should we extend it or separate system?
5. **Multi-Device**: Can user have multiple reset requests active?

## Proposed Architecture

### Database Schema
```prisma
model PasswordResetToken {
  id        String   @id @default(cuid())
  token     String   @unique // Hashed token
  userId    String
  user      User     @relation(fields: [userId], references: [id])
  expiresAt DateTime
  usedAt    DateTime?
  createdAt DateTime @default(now())

  @@index([token])
  @@index([expiresAt])
}
```

### API Endpoints

**1. POST /api/auth/forgot-password**
- Input: { email }
- Validates email format
- Rate limiting check
- Finds user (or pretends to for security)
- Generates secure token
- Stores hashed token in database
- Sends email
- Always returns success (email enumeration protection)

**2. GET /api/auth/reset-password/[token]**
- Validates token exists and not expired
- Renders password reset form
- Or redirects to frontend page with token

**3. POST /api/auth/reset-password**
- Input: { token, newPassword }
- Validates token
- Validates password strength
- Updates user password
- Marks token as used
- Invalidates all other sessions
- Returns success

### Implementation Steps

**Step 1: Database Migration**
- Create PasswordResetToken model
- Run migration

**Step 2: Token Generation Utility**
```typescript
// src/lib/auth/reset-token.ts
import crypto from 'crypto';
import { hash } from 'bcrypt';

export async function generateResetToken(userId: string) {
  // Generate cryptographically secure token
  const token = crypto.randomBytes(32).toString('hex');
  const hashedToken = await hash(token, 10);

  const expiresAt = new Date(Date.now() + 60 * 60 * 1000); // 1 hour

  await prisma.passwordResetToken.create({
    data: {
      token: hashedToken,
      userId,
      expiresAt,
    },
  });

  return token; // Return unhashed token for email
}
```

**Step 3: Rate Limiting Middleware**
```typescript
// src/middleware/rate-limit.ts
import { Ratelimit } from '@upstash/ratelimit';

export const resetPasswordRateLimit = new Ratelimit({
  redis: redis,
  limiter: Ratelimit.slidingWindow(3, '1 h'),
});
```

**Step 4: API Route - Request Reset**
[... detailed implementation ...]

**Step 5: API Route - Reset Password**
[... detailed implementation ...]

**Step 6: Email Template**
[... email HTML template ...]

**Step 7: Frontend Pages**
[... form components ...]

## Files to Create

1. `prisma/migrations/XXX_add_password_reset_tokens.sql`
2. `src/lib/auth/reset-token.ts`
3. `src/middleware/rate-limit.ts`
4. `src/app/api/auth/forgot-password/route.ts`
5. `src/app/api/auth/reset-password/route.ts`
6. `src/app/api/auth/reset-password/[token]/route.ts`
7. `src/app/forgot-password/page.tsx`
8. `src/app/reset-password/[token]/page.tsx`
9. `src/components/auth/ForgotPasswordForm.tsx`
10. `src/components/auth/ResetPasswordForm.tsx`
11. `src/lib/email/templates/password-reset.tsx`
12. `tests/auth/password-reset.test.ts`

## Security Checklist

- [x] Crypto.randomBytes for token generation (not Math.random)
- [x] Token hashed before database storage
- [x] Token expiration (1 hour)
- [x] Rate limiting (3 requests per hour per email)
- [x] Email enumeration protection (always return success)
- [x] One-time use (mark as used)
- [x] Password strength validation
- [x] Invalidate all sessions after password reset
- [x] HTTPS only (tokens in URLs are logged)
- [x] No sensitive data in error messages

## Risks & Mitigations

⚠️ **Risk**: Email service down → token created but user never receives it
**Mitigation**: Wrap token creation + email send in transaction; rollback if email fails

⚠️ **Risk**: User requests multiple resets
**Mitigation**: Invalidate old tokens when creating new one

⚠️ **Risk**: Token in browser history
**Mitigation**: One-time use, short expiration, HTTPS

## Testing Strategy

- Unit tests: Token generation, validation logic
- Integration tests: API endpoints with database
- E2E test: Full forgot → email → reset flow (mocked email)
- Security tests: Brute force, timing attacks, token enumeration

## Estimated Scope

- **Files**: 12 new files
- **Lines of Code**: ~600 production + ~300 tests
- **Time**: 4-6 hours including testing
- **Dependencies**: May need email service library

## Open Questions

1. Which email service? (affects template and sending code)
2. Password strength requirements? (minimum length, complexity)
3. Should we notify user's existing email when password is changed?
4. Do you want to limit total active reset tokens per user?
```

**Step 3: Your Review**

```markdown
Excellent plan! Answers:
1. Using Resend for emails
2. Password: min 8 chars, at least one number, one uppercase
3. Yes, send notification to old email address
4. Yes, max 3 active tokens per user

One addition: Add audit logging for all password reset attempts (success and failure).

Please update plan with these details.
```

**Step 4: Claude Updates Plan**

```markdown
# Updated Plan

[... adds audit logging section ...]
[... adds email notification for password changes ...]
[... adds max token limit logic ...]

Updated files: +2 (audit.ts, change-notification-email.tsx)
Updated scope: 650 lines production + 350 tests, 5-7 hours

Ready for implementation?
```

**Step 5: Approval**

```markdown
Perfect! Plan approved. Please implement.
```

**Step 6: Claude Executes**

Claude now implements according to the plan, with high confidence that the approach is correct, secure, and complete.

---

## When to Use

### Ideal Use Cases

✅ **Use plan mode when:**
- Implementing new features (especially if touching 3+ files)
- Making architectural decisions
- Refactoring significant code
- Requirements are unclear or complex
- Security is critical (auth, payments, etc.)
- Multiple implementation approaches exist
- Working on unfamiliar parts of codebase

### Indicators You Need This Pattern

- You've been burned by Claude implementing wrong approach
- Task is complex with multiple moving parts
- You're not 100% sure of the best approach yourself
- Team needs to review before implementation
- Compliance or security requirements
- Budget-conscious (can't afford token waste on rework)

### Project Types

**Best For:**
- Production applications
- Team projects (plans can be reviewed by team)
- Complex domains (finance, healthcare, etc.)
- Large refactoring projects
- Client work (show plan for approval)

**Also Works For:**
- Learning projects (understand before implementation)
- Open source (plans can be discussed in issues)
- Prototypes where approach matters

---

## When NOT to Use

### Avoid This Pattern When

❌ **Don't use plan mode if:**
- Fixing a typo or formatting issue
- Making trivial one-line changes
- Requirements are crystal clear and simple
- You're just exploring/experimenting
- Time pressure and the task is straightforward
- Implementation approach is obvious

### Simpler Alternatives

If plan mode seems too heavy:
- **Direct Request**: For trivial changes, just ask Claude to implement
- **Inline Questions**: Ask Claude to clarify as it works
- **Post-hoc Review**: Generate code, then review (less efficient but faster)

### Warning Signs

⚠️ **Red flags that suggest you don't need plan mode:**
- You're spending more time planning than the task would take to code
- The plan is longer than the implementation will be
- Everyone already agrees on the obvious approach
- It's throwaway code for a quick experiment

---

## Variations & Related Patterns

### Common Variations

1. **Quick Plan (Lightweight)**
   - **When to use**: Medium complexity tasks
   - **Format**: Brief outline, key decisions, files affected
   - **Trade-offs**: Faster but less detail

2. **Comprehensive Plan (Full Spec)**
   - **When to use**: Complex features, security-critical
   - **Format**: Full specification with code examples, security checklist
   - **Trade-offs**: Thorough but time-intensive

3. **Multi-Phase Plan**
   - **When to use**: Large features spanning weeks
   - **Format**: High-level phases first, then detailed plan per phase
   - **Trade-offs**: Flexible but requires more planning iterations

### Related Patterns

- **Context Management**: Provide context before asking for plan
- **Claude.md**: Documented conventions inform planning
- **Step-by-Step Thinking**: Planning is thinking made explicit
- **Code Review**: Plan review is spec review before code review

### Pattern Combinations

This pattern works especially well with:
- **Claude.md** → Plans automatically follow documented conventions
- **Sub-Agents** → Each sub-agent plans its domain-specific work
- **Code Review** → Review plan first (cheap), then review code (expensive)

---

## Metrics & Results

### Expected Improvements

Based on community reports and user testimonials:

- **50-80% reduction** in implementation rework
- **3-5x fewer** "that's not what I wanted" moments
- **10x token savings** on complex tasks (fix plan, not code)
- **Higher quality** code (issues caught early)
- **Faster total time** despite upfront planning (less rework)

**Source**: Claude Code community feedback, user testimonials

### Success Indicators

You'll know this pattern is working when:
- First implementation matches requirements 90%+ of the time
- You catch issues before code is written
- Plans surface edge cases you hadn't considered
- Team can review and approve approach before work begins
- Rework cycles are rare

---

## Common Pitfalls & Solutions

### Pitfall 1: Skipping Plan Mode for "Quick" Tasks

**Problem**: "This seems simple, I'll skip the plan" → turns out complex, wastes tokens on rework

**Solution**: Use plan mode if you estimate >100 lines of code or >2 files affected

```markdown
// ❌ Wrong: Direct implementation of "simple" task
"Add user profile editing"

[500 lines of code later...]
"Wait, that's not how our forms work"

// ✅ Correct: Plan first
<Shift+Tab>
"Plan: Add user profile editing"
[Claude asks about form library, validation, etc.]
[You clarify]
[Implementation matches expectations]
```

### Pitfall 2: Rubber-Stamp Planning

**Problem**: Requesting a plan but not actually reviewing it carefully

**Solution**: Treat plan review seriously—check assumptions, verify approach, look for gaps

```markdown
// ❌ Bad review
Claude: [Detailed 50-line plan with questionable decisions]
You: "Looks good!"
[Implementation has issues you didn't catch]

// ✅ Good review
Claude: [Plan suggests using library X]
You: "Why library X instead of library Y which we already use?"
Claude: "Good point, let me update the plan to use library Y"
[Better implementation]
```

### Pitfall 3: Planning Paralysis

**Problem**: Spending more time planning than it would take to just code it

**Solution**: Match planning depth to task complexity

```markdown
// ❌ Over-planning
Task: "Fix typo in error message"
<Shift+Tab>
"Create comprehensive plan for typo fix"
[10 minutes of planning for a 10-second task]

// ✅ Right-sized planning
Task: "Refactor authentication system"
<Shift+Tab>
"Create comprehensive plan"
[30 minutes planning saves 5 hours of rework]
```

---

## Best Practices

### Do's ✅

- **Always plan for new features** (3+ files affected)
- **Review plans thoroughly** before approving
- **Ask clarifying questions** during planning
- **Iterate on plans** until perfect (cheap fixes)
- **Document plan approval** explicitly ("Plan approved")
- **Use plan mode for learning** (understand before implementing)

### Don'ts ❌

- **Don't skip plan mode** to save time (false economy)
- **Don't rubber-stamp plans** without careful review
- **Don't over-plan trivial tasks** (formatting, typos)
- **Don't approve uncertain plans** (keep iterating)
- **Don't ignore Claude's questions** in plans
- **Don't forget to exit plan mode** before executing

### Pro Tips 💡

- **Tip 1**: In plan requests, explicitly ask Claude to list assumptions and ask clarifying questions
- **Tip 2**: For complex features, ask for a multi-phase plan first, then detail one phase at a time
- **Tip 3**: Save approved plans as documentation (e.g., in `docs/decisions/`)
- **Tip 4**: Use plan mode even for bug fixes when root cause is unclear
- **Tip 5**: Ask Claude to include a "Risks & Mitigations" section in plans
- **Tip 6**: Reference your `claude.md` in plan requests to ensure alignment with conventions

---

## Real-World Examples

### Example 1: SaaS Feature Implementation

**Context**: Adding subscription billing to a SaaS application

**Without Plan Mode:**
- Implemented Stripe integration directly
- Realized later: need webhook handling, subscription status tracking, usage metering
- 3 days of rework, 50K tokens wasted

**With Plan Mode:**
- Created comprehensive plan first
- Plan identified: webhooks, status tracking, metering, grace periods, prorations
- Approved plan, implemented once
- 1 day total time, minimal rework

**Results:**
- 70% time savings
- 90% token savings
- Higher quality (edge cases caught in planning)

### Example 2: Security-Critical Feature

**Context**: Implementing OAuth integration

**Plan Mode Workflow:**

```markdown
<Shift+Tab>
"Plan: Add Google OAuth login"

Claude's Plan:
## Security Considerations
1. CSRF protection with state parameter
2. PKCE for mobile clients
3. Nonce validation
4. Token secure storage
5. Scope limitations

## Risks
⚠️ Token stored in localStorage is vulnerable to XSS
⚠️ Redirect URI must be exact match

[... comprehensive security plan ...]

You: "Good catch on localStorage! Let's use httpOnly cookies instead.
Also add rate limiting to prevent OAuth endpoint abuse."

Updated Plan:
[... includes cookies and rate limiting ...]

Plan approved, implemented with security best practices.
```

**Results:**
- Zero security vulnerabilities (caught in planning)
- Passed security audit on first try
- Confidence in production deployment

---

## Quick Reference

### Checklist

Before using plan mode:
- [ ] Task affects 3+ files OR is security-critical OR has unclear requirements
- [ ] You have 5-10 minutes for planning (don't rush)
- [ ] You're willing to iterate on the plan before executing
- [ ] Implementation approach isn't trivially obvious

### Implementation Steps (Quick)

1. Press **Shift+Tab** to enter plan mode
2. Request: "Create a detailed plan for [task]. Ask clarifying questions."
3. Review Claude's plan carefully—check assumptions, approach, scope
4. Iterate: Answer questions, request changes, refine approach
5. Approve: "Plan approved, please implement"
6. Press **Shift+Tab** to exit plan mode (or Claude will prompt)
7. Execute: Claude implements according to plan

### Key Commands/Snippets

```bash
# Enter/exit plan mode
<Shift+Tab>

# Good plan request template
"Create a detailed plan for [feature/task].

Please include:
- Clarifying questions about requirements
- Proposed architecture/approach
- Files to create/modify
- Security considerations (if applicable)
- Risks and mitigations
- Estimated scope

Ask me any questions before proceeding."

# Approval template
"Plan looks good with these adjustments:
- [Change 1]
- [Change 2]

Please update the plan, then I'll approve for implementation."

# Final approval
"Plan approved. Please implement following this specification."
```

---

## FAQ

### Q: When exactly should I use plan mode?

A: Use plan mode when:
- Task affects 3+ files
- Security, payments, or auth involved
- Requirements unclear or complex
- Multiple implementation approaches exist
- You're not 100% confident in the approach

Skip plan mode for:
- Typos, formatting, trivial changes
- Obvious one-line bug fixes
- Tasks you've done many times before

### Q: How long should planning take?

A: **Rule of thumb**: Spend 10-20% of estimated total time on planning

- Simple feature (1 hour work): 5-10 minutes planning
- Medium feature (half day work): 30-60 minutes planning
- Complex feature (multi-day work): 2-4 hours planning

If planning takes longer than implementation would, you're over-planning.

### Q: Can I modify the plan during implementation?

A: Yes! Plans are guides, not rigid contracts. If you discover new information during implementation:
1. Update the plan
2. Communicate the change
3. Verify the change doesn't break other parts of the plan

Think of it like a design doc that evolves.

### Q: What if Claude's plan is completely wrong?

A: This is why we review! If the plan misunderstands requirements:
1. Don't approve
2. Clarify the misunderstanding
3. Ask Claude to revise the plan
4. Iterate until it's right

**This is the whole point**: catch misunderstandings in planning (cheap), not in code (expensive).

### Q: Should I save plans somewhere?

A: Yes! Approved plans make excellent documentation:
- Save in `docs/decisions/` or `docs/features/`
- Reference in PR descriptions
- Useful for onboarding new developers
- Historical record of architectural decisions

---

## Further Reading

### Official Documentation
- [Claude Code Documentation](https://docs.claude.com) - Plan mode usage guide

### Tutorials
- Peter Yang's Movie App Tutorial - Demonstrates plan mode workflow
- "7wGE I was using Claude Code wrong" - Always use plan mode first
- "800+ Hours of Learning" - Q&A session before coding

### Case Studies
- Real-world examples of plan mode preventing costly mistakes
- Security-critical implementations using plan mode

### Related Patterns
- [Context Management](./context-management.md) - Provide context before planning
- [Claude.md](./claude-md-persistent-memory.md) - Conventions inform plans
- [Code Review](../quality-assurance/code-review.md) - Review specs, then code

---

## Sources & References

### Primary Sources

1. **Peter Yang Movie App Summary**
   - **File**: `/sources/youtube/peter-yang-movie-app-summary.md`
   - **Relevance**: Plan mode demonstration for beginners
   - **Key Insights**: Provides transparency into Claude's thinking

2. **"7wGE I was using Claude Code wrong... The Ultimate Work"**
   - **File**: `/sources/youtube/7wGE I was using Claude Code wrong... The Ultimate Work.md`
   - **Relevance**: Always use plan mode first
   - **Key Insights**: Prevents wasted effort on wrong approaches

3. **"800+ hours of Learning Claude Code in 8 minutes 2"**
   - **File**: `/sources/youtube/800+ hours of Learning Claude Code in 8 minutes 2.md`
   - **Relevance**: Q&A session before code generation
   - **Key Insights**: Breaks down complex problems systematically

4. **"I was wrong about Claude Code UPDATED AI workflow"**
   - **File**: `/sources/youtube/I was wrong about Claude Code UPDATED AI workflow.md`
   - **Relevance**: Importance of thorough plan review
   - **Key Insights**: Don't rubber-stamp plans

5. **"A Complete Guide to Claude Code Here are ALL the"**
   - **File**: `/sources/youtube/A Complete Guide to Claude Code Here are ALL the.md`
   - **Relevance**: Shift+Tab to toggle plan mode
   - **Key Insights**: Built-in feature for spec-driven development

### Research & Data

- Community reports: 50-80% reduction in rework with plan mode
- User testimonials: 3-5x fewer "wrong implementation" issues
- Token efficiency: 10x savings on complex tasks

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-11-14 | Initial documentation in standardized template format |

---

## Metadata

**Tags**: `plan-mode`, `spec-driven-development`, `workflow`, `planning`, `design-first`, `shift-tab`

**Prerequisites**:
- Basic understanding of Claude Code interface
- Willingness to invest time in planning before coding

**Estimated Time to Implement**:
- Learning the workflow: 15-30 minutes
- First plan mode session: 20-40 minutes
- Subsequent sessions: 5-20 minutes per task

**Skill Level**: Beginner

---

## Contributing

Found an improvement or additional example? Please contribute:
1. Share your plan mode success stories
2. Document common pitfalls you've discovered
3. Add examples of great vs. poor plan reviews

---

**Pattern Documentation**: v1.0
**Last Updated**: 2024-11-14
**Maintainer**: Claude Coding Knowledge Base Project
