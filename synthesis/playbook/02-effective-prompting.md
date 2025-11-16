# Chapter 2: Effective Prompting Fundamentals

**Target Audience**: Developers ready to level up their Claude interactions
**Reading Time**: 20-25 minutes
**Practice Time**: 2-3 hours
**Prerequisites**: Chapter 1 completed, one successful Claude session

**Learning Objectives**:
- Master prompt anatomy for consistent results
- Achieve 20-30% accuracy improvements through proven techniques
- Understand system vs. user prompts
- Apply few-shot learning effectively
- Enable chain-of-thought reasoning
- Optimize parameters for code generation
- Avoid common prompting pitfalls

---

## 2.1 Prompt Anatomy: The Five Essential Components

Every effective prompt contains five key elements. Master these, and you'll see dramatic quality improvements.

### The Five Components

**1. Context** - What Claude needs to know
**2. Task** - What you want accomplished
**3. Examples** - What good looks like
**4. Constraints** - What to avoid or follow
**5. Format** - How to structure the response

### Using XML Tags for Structure

Claude was specifically trained with XML in its training data, making XML tags particularly effective for structuring prompts.

**Basic Structure**:
```xml
<context>
This is a React 18 + TypeScript project using:
- Tailwind CSS for styling
- React Query for data fetching
- Zod for validation
- React Hook Form for forms
</context>

<task>
Create a user registration form with email, password, and password
confirmation fields.
</task>

<examples>
# Example of our form pattern:
export function LoginForm() {
  const form = useForm<LoginSchema>({
    resolver: zodResolver(loginSchema)
  });
  // ... rest of implementation
}
</examples>

<constraints>
- Must use React Hook Form + Zod (project standard)
- Password must be 8+ characters
- Show validation errors inline
- Tailwind styling only (no inline styles)
</constraints>

<format>
Please provide:
1. The FormSchema (Zod)
2. The RegisterForm component
3. Usage example
4. Explanation of validation strategy
</format>
```

**Why This Works**:
- Clear separation of concerns
- Easy for Claude to parse
- Simple to modify individual sections
- Consistent results

### Document Positioning: The 30% Boost

**Critical Finding from Anthropic Research**: Document positioning can improve accuracy by **30%**.

**The Rule**:
- Large documents (20K+ tokens): Place at **beginning** of prompt
- Queries and questions: Place at **end** of prompt
- Critical details: Place at beginning **or** end (not middle)

**Correct Structure**:
```xml
<documents>
[Your large codebase file or documentation - first]
</documents>

<examples>
[Example Q&A pairs showing expected format]
</examples>

<query>
[Your specific question or task - last]
</query>
```

**Why This Matters**:
Claude's 200K context window has "hot zones" at the beginning and end. Information in the middle is slightly less salient. For multi-document analysis, this positioning strategy is critical.

**Real Example**:
```markdown
# ❌ Poor positioning (query first):
"Based on the API documentation below, how do I authenticate?"
[50-page API documentation]

# ✅ Optimal positioning (docs first, query last):
<documentation>
[50-page API documentation]
</documentation>

<query>
How do I authenticate to this API? Show code examples for:
1. OAuth 2.0 flow
2. API key usage
3. Refresh token handling
</query>
```

---

## 2.2 System Prompts vs. User Prompts

Understanding the distinction between system and user prompts is crucial for effective Claude usage.

### System Prompts: Setting the Stage

**Purpose**: Define Claude's role, expertise, tone, and high-level behavior.

**Best For**:
- Setting expertise domain ("You are an expert React developer")
- Defining tone and style ("Be concise and technical")
- Establishing persistent rules ("Always use TypeScript")
- Scoping knowledge ("Only use React 18+ patterns")

**Where to Put System Prompts**:
1. `.claude.md` file (persistent, project-wide)
2. `.claude/subagents/*.md` (specialized agent roles)
3. Global `.claude.md` in home directory (applies everywhere)

**Example `.claude.md` System Prompt**:
```markdown
# Project: TaskMaster SaaS

You are an expert full-stack developer specializing in:
- Next.js 14 (App Router)
- TypeScript (strict mode)
- Tailwind CSS
- Prisma ORM
- React Query
- Jest + React Testing Library

## Your Approach

- Always think step-by-step before implementing
- Ask clarifying questions when requirements are ambiguous
- Prioritize type safety and error handling
- Write production-ready code with tests
- Follow functional programming patterns in React

## Code Style

- Explicit return types on all functions
- Prefer const over let, avoid var
- Use const assertions for literal types
- Destructure props with explicit types
- Name handlers: handleXxx (e.g., handleSubmit)
```

### User Prompts: Specific Tasks

**Purpose**: Give specific, actionable instructions for individual tasks.

**Best For**:
- Implementing features
- Debugging specific issues
- Refactoring code
- Analyzing code
- Answering questions

**Example User Prompt**:
```markdown
# User prompt (specific task):
Implement rate limiting for the /api/contact endpoint.

Requirements:
- Max 5 requests per 15 minutes per IP
- Use Redis for tracking (already configured)
- Return 429 status when limit exceeded
- Include Retry-After header

File: app/api/contact/route.ts
```

### The Division of Labor

**System Prompt (.claude.md)**:
```markdown
"Here's how we build things in this project..."
"These are our standards and conventions..."
"This is your role and expertise..."
```

**User Prompt**:
```markdown
"Here's what I need you to build today..."
"This is the specific problem to solve..."
"These are the unique requirements for this task..."
```

### Persistent Memory: `.claude.md` as System Prompt

The `.claude.md` file is automatically loaded and prepended to every conversation in Claude Code. This makes it the perfect place for system-level instructions.

**What to Include in `.claude.md`**:
1. **Tech Stack**: Frameworks, libraries, versions
2. **Coding Conventions**: Style guide, patterns, naming
3. **Architecture Rules**: Where things go, how they connect
4. **Quality Standards**: Testing requirements, type safety
5. **Project-Specific Patterns**: Error handling, API format, state management

**What NOT to Include**:
- ❌ Specific task instructions (those go in user prompts)
- ❌ One-off configurations
- ❌ Temporary notes
- ❌ Code snippets (unless they're reusable patterns)

---

## 2.3 Few-Shot Examples: The 20% Boost

**Research Finding**: Providing 2-5 diverse, realistic examples improves accuracy by **20%** (Anthropic case study with Fortune 500 company).

### The Power of Examples

Humans learn by example. So does Claude. Instead of describing what you want in words, show exact input/output pairs.

### How Many Examples?

**Anthropic Recommendation**: 2-3 examples minimum
**Community Best Practice**: 3-5 examples for complex tasks
**Sweet Spot**: 3 examples covering:
1. Happy path (normal case)
2. Edge case #1
3. Edge case #2

### Example: API Error Responses

**❌ Without Examples (Description Only)**:
```markdown
Task: Implement consistent error responses across all API routes.
Use a standard format with error codes, messages, and optional details.
```

**Claude's likely response**: Varied, inconsistent format across different endpoints.

**✅ With Few-Shot Examples**:
```markdown
Task: Implement consistent error responses across all API routes.

Use this EXACT format:

## Example 1: Validation Error
Input: POST /api/users with invalid email

Output:
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
  "timestamp": "2025-11-14T10:00:00Z"
}
HTTP Status: 400

## Example 2: Unauthorized
Input: GET /api/protected without auth header

Output:
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required",
    "details": null
  },
  "timestamp": "2025-11-14T10:00:00Z"
}
HTTP Status: 401

## Example 3: Not Found
Input: GET /api/users/999 (non-existent)

Output:
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
  "timestamp": "2025-11-14T10:00:00Z"
}
HTTP Status: 404

Now implement this format across all API routes.
```

**Claude's response**: Perfect consistency across all endpoints, matching format exactly.

### Example: Code Style Consistency

**Task**: Refactor utility functions to match project style.

**With Few-Shot Examples**:
```markdown
Refactor the utility functions to match our project code style.

## Our Style (Examples)

### Example 1: Date Functions
\`\`\`typescript
/**
 * Formats a date as YYYY-MM-DD
 * @param date - Date to format
 * @returns Formatted date string
 * @example formatDate(new Date('2025-11-14')) // => '2025-11-14'
 */
export function formatDate(date: Date): string {
  return date.toISOString().split('T')[0];
}
\`\`\`

### Example 2: Array Operations
\`\`\`typescript
/**
 * Removes duplicate items from an array
 * @param items - Array with potential duplicates
 * @returns Array with unique items only
 * @example unique([1, 2, 2, 3]) // => [1, 2, 3]
 */
export function unique<T>(items: T[]): T[] {
  return [...new Set(items)];
}
\`\`\`

### Example 3: String Operations
\`\`\`typescript
/**
 * Capitalizes first letter of a string
 * @param str - String to capitalize
 * @returns Capitalized string
 * @example capitalize('hello') // => 'Hello'
 */
export function capitalize(str: string): string {
  if (!str) return str;
  return str.charAt(0).toUpperCase() + str.slice(1);
}
\`\`\`

Now refactor these functions to match this exact style:
[... your existing functions to refactor]
```

**Result**: Perfect style consistency including JSDoc format, type annotations, examples, and implementation patterns.

### Guidelines for Great Examples

1. **Be Realistic**: Use real-world scenarios, not toy examples
2. **Show Edge Cases**: Empty arrays, null values, errors
3. **Be Complete**: Full input/output, not fragments
4. **Be Diverse**: Cover different scenarios, not variations of the same
5. **Match Desired Format Exactly**: Claude will replicate precisely what you show

---

## 2.4 Chain-of-Thought Reasoning: The Step-by-Step Approach

**Research Finding**: Simply adding "think step by step" improves accuracy by **20%** on complex tasks.

### Why Chain-of-Thought Works

When Claude shows its reasoning:
1. Logic errors become visible
2. Faulty assumptions are caught early
3. You can course-correct mid-process
4. Complex problems are broken into manageable steps

### The Basic Technique

**Simple Addition**:
```markdown
Fix the bug where users can't upload images larger than 5MB.

Think step by step:
1. What might be causing this?
2. List all places where file size might be restricted
3. Show your debugging approach
4. Explain your proposed fix and why it will work
```

### Using `<thinking>` Tags

**Structured Approach**:
```markdown
Fix the authentication bug where sessions expire too quickly.

Use <thinking> tags to show your reasoning process, then provide
the solution in <solution> tags.
```

**Claude's Response**:
```xml
<thinking>
Let me analyze this systematically:

**Step 1: Current Session Configuration**
Looking at the NextAuth configuration in `/app/api/auth/[...nextauth]/route.ts`,
I see the session strategy is "jwt" with no maxAge specified.

**Step 2: Default Behavior**
Without explicit maxAge, NextAuth defaults to 30 days for JWTs.
But if sessions are expiring quickly, something is overriding this.

**Step 3: Potential Causes**
1. Client-side cookie expiration (httpOnly cookies with short max-age)
2. Token refresh not working (refreshToken mechanism)
3. Environmental differences (dev vs. prod)
4. NextAuth secret changing (invalidates all sessions)

**Step 4: Most Likely Culprit**
Checking the cookie configuration... found it! The cookie maxAge
is set to 60 seconds instead of 30 days.

**Step 5: Why This Happened**
Likely a testing configuration that wasn't reverted.
</thinking>

<solution>
Found the issue in `/app/api/auth/[...nextauth]/route.ts`:

\`\`\`typescript
// ❌ Current (wrong):
cookies: {
  sessionToken: {
    name: 'next-auth.session-token',
    options: {
      httpOnly: true,
      sameSite: 'lax',
      path: '/',
      secure: process.env.NODE_ENV === 'production',
      maxAge: 60  // ← 60 SECONDS! Should be 30 days
    }
  }
}

// ✅ Fixed:
cookies: {
  sessionToken: {
    name: 'next-auth.session-token',
    options: {
      httpOnly: true,
      sameSite: 'lax',
      path: '/',
      secure: process.env.NODE_ENV === 'production',
      maxAge: 30 * 24 * 60 * 60  // 30 days in seconds
    }
  }
}
\`\`\`

This was likely a testing configuration that accidentally made it to production.
The cookie was expiring after 60 seconds, forcing re-authentication.
</solution>
```

### Advanced: Multi-Step Complex Problems

**For Complex Debugging**:
```markdown
The application is experiencing intermittent 500 errors on the /api/checkout
endpoint, but only in production, not locally.

Please:
1. Analyze possible causes (think step-by-step in <thinking> tags)
2. Review the code for issues
3. Propose a debugging strategy
4. Suggest likely fixes

Use multiple <thinking> sections to break down each step.
```

### Magic Keywords for Deeper Thinking

**Proven Keywords**:
- **"important"**: Flags task as high priority, Claude allocates more attention
- **"proactively"**: Claude anticipates needs, does extra work
- **"ultra think"**: Triggers deeper reasoning mode (uses more tokens)

**Usage**:
```markdown
IMPORTANT: This is security-critical authentication code. Ultra think
through all potential vulnerabilities before suggesting changes.

Proactively consider:
- SQL injection vectors
- JWT token vulnerabilities
- Session fixation attacks
- Timing attacks
```

**Anti-Pattern**:
```markdown
❌ "Make this production ready"
```
This phrase causes Claude to over-engineer, adding unnecessary backward compatibility and complexity.

---

## 2.5 Temperature and Other Parameters

### Understanding Temperature

**Temperature Scale**: 0.0 to 1.0
- **0.0**: Maximum consistency, minimal creativity
- **0.5**: Balanced (default)
- **1.0**: Maximum creativity, more variation

### Best Settings for Code

**For Code Generation**:
```bash
# Maximum consistency, minimal hallucination
claude --temperature 0.0
```

**Recommended by Use Case**:

| Task | Temperature | Reasoning |
|------|-------------|-----------|
| **Production code** | 0.0 - 0.2 | Need consistency, avoid creative experiments |
| **Bug fixes** | 0.0 - 0.1 | Deterministic debugging |
| **Refactoring** | 0.1 - 0.3 | Some flexibility, mostly deterministic |
| **Architecture planning** | 0.3 - 0.5 | Balance structure and creativity |
| **Brainstorming** | 0.7 - 1.0 | Maximize creative options |
| **Tests** | 0.0 - 0.2 | Consistent, thorough coverage |

### Other Parameters

**top_p** (Nucleus Sampling):
- Default: 0.9
- Lower = more deterministic
- For code: Keep at default or lower to 0.7-0.8

**top_k**:
- Limits vocabulary to top K tokens
- Rarely adjusted for coding tasks
- Keep at default

**Best Practice**: For coding, only adjust temperature. Start at 0.0-0.2 for production code.

---

## 2.6 Common Prompting Mistakes

Learn from common pitfalls to avoid wasted time and tokens.

### Mistake #1: Vagueness

**❌ Vague**:
```markdown
"Make the login better"
"Fix the performance issues"
"Improve the UI"
```

**✅ Specific**:
```markdown
"Add loading state to login button while authenticating.
Show spinner, disable form, display 'Signing in...' text."

"The /api/users endpoint takes 5+ seconds for 1000+ users.
Add pagination (10/25/50 items per page) and use database
indexes on the frequently queried fields."

"Update the dashboard to match the new design system:
- Replace blue (#0066CC) with new brand blue (#1E40AF)
- Update button radius from 4px to 8px
- Replace font from Inter to Geist Sans"
```

### Mistake #2: Ambiguous Scope

**❌ Ambiguous**:
```markdown
"Add error handling"
```

**✅ Clear Scope**:
```markdown
"Add try/catch blocks to all database operations in the
/app/api/users/route.ts file. Log errors using our Winston
logger (import from @/lib/logger). Return this JSON format:

{
  \"success\": false,
  \"error\": \"User-friendly message here\"
}

Never expose stack traces to users."
```

### Mistake #3: Assuming Context

**❌ Assumption**:
```markdown
"Create a user profile component"
```

Claude doesn't know:
- Where to create it
- What framework/library to use
- What styling approach
- What data it should display
- What your existing patterns look like

**✅ Full Context**:
```markdown
"Create a user profile component at /components/UserProfile.tsx

Requirements:
- React functional component with TypeScript
- Shows: avatar, name, email, join date
- Use our Avatar component from @/components/ui/Avatar
- Tailwind CSS styling (no inline styles)
- Import user type from @/types/user

Example of our component pattern:
\`\`\`typescript
export function ExampleComponent({ user }: { user: User }) {
  return (
    <div className=\"rounded-lg border p-4\">
      {/* ... */}
    </div>
  );
}
\`\`\`
```

### Mistake #4: Negative Instructions

**❌ Negative Framing**:
```markdown
"Don't make it too technical"
"Don't use complex words"
"Don't write too much code"
```

**✅ Affirmative Instructions**:
```markdown
"Use simple, clear language"
"Keep explanations concise (2-3 sentences)"
"Implement only the core functionality—no extras"
```

**Why Affirmative Works Better**:
Telling Claude what TO do is more effective than what NOT to do. Negative instructions can be ambiguous and harder to follow consistently.

### Mistake #5: Asking Too Much at Once

**❌ Overwhelming**:
```markdown
"Build a complete e-commerce system with products, cart, checkout,
payments, user accounts, admin panel, inventory management, and
shipping integration"
```

**✅ Incremental**:
```markdown
Session 1: "Create product model and basic CRUD API endpoints"
Session 2: "Add shopping cart functionality"
Session 3: "Implement checkout flow UI"
Session 4: "Integrate Stripe payment processing"
... [continue step by step]
```

### Mistake #6: No Examples for Complex Formats

**❌ Description Only**:
```markdown
"Use consistent code formatting"
```

**✅ Show Example**:
```markdown
"Format all React components using this exact pattern:

\`\`\`typescript
// 1. Imports
import { useState } from 'react';
import type { User } from '@/types/user';

// 2. Types
interface Props {
  user: User;
  onUpdate: (user: User) => void;
}

// 3. Component
export function UserCard({ user, onUpdate }: Props) {
  // 3a. Hooks
  const [isEditing, setIsEditing] = useState(false);

  // 3b. Handlers
  const handleSave = () => {
    // ...
  };

  // 3c. Render
  return (
    <div>{/* ... */}</div>
  );
}
\`\`\`

Apply this pattern to all components."
```

---

## 2.7 Practical Templates

Use these templates to jumpstart your prompts.

### Template 1: Feature Implementation

```markdown
**Context**:
[Your tech stack, relevant files, existing patterns]

**Task**:
Implement [feature name] with the following requirements:
- Requirement 1
- Requirement 2
- Requirement 3

**Location**:
- Create/modify: /path/to/file

**Examples**:
[Show similar existing code or desired patterns]

**Constraints**:
- Must maintain backward compatibility
- Follow existing [pattern name] pattern
- Use [specific library/approach]

**Format**:
Please provide:
1. The implementation
2. Brief explanation of approach
3. Any assumptions made
```

### Template 2: Bug Fix

```markdown
**Bug Description**:
[What's broken, specific error messages, reproduction steps]

**Expected Behavior**:
[What should happen instead]

**Relevant Code**:
[Paste relevant code section or file path]

**Environment**:
[Browser, Node version, OS, etc. if relevant]

**Please**:
1. Think step-by-step to identify root cause
2. Explain why the bug occurs
3. Provide the fix
4. Suggest how to prevent similar bugs
```

### Template 3: Code Review

```markdown
**Review This Code**:
\`\`\`typescript
[Paste code to review]
\`\`\`

**Review Checklist**:
- Security vulnerabilities (SQL injection, XSS, etc.)
- Edge cases and error handling
- Performance issues
- Code style and best practices
- Type safety
- Test coverage needs

**Format**:
For each issue found:
- Severity (Critical/High/Medium/Low)
- Description
- Suggested fix
- Explanation
```

### Template 4: Refactoring

```markdown
**Current Code**:
[Paste code to refactor]

**Refactoring Goals**:
- [Goal 1: e.g., "Improve type safety"]
- [Goal 2: e.g., "Reduce duplication"]
- [Goal 3: e.g., "Better error handling"]

**Constraints**:
- Must maintain same public API
- Cannot introduce breaking changes
- Must improve or maintain test coverage

**Provide**:
1. Refactored code
2. Explanation of changes
3. Migration guide if API changes
```

---

## 2.8 The Prompt Iteration Cycle

Great prompts are built through iteration. Here's the process:

### Iteration Process

**1. Start Simple**:
```markdown
"Add validation to the contact form"
```

**2. Claude's Response**: Too generic, doesn't match your patterns

**3. Add Context and Examples**:
```markdown
"Add validation to the contact form at /app/contact/page.tsx

Use our validation pattern:
\`\`\`typescript
const schema = z.object({
  email: z.string().email(),
  message: z.string().min(10)
});
\`\`\`

Apply to: name (required), email (valid format), message (min 20 chars)"
```

**4. Claude's Response**: Better, but missing error display

**5. Refine Further**:
```markdown
"Add validation to the contact form at /app/contact/page.tsx

Validation requirements:
- name: required, 2-50 characters
- email: valid email format
- message: required, 20-500 characters

Use this exact pattern (from our login form):
\`\`\`typescript
const form = useForm<ContactSchema>({
  resolver: zodResolver(contactSchema)
});

// Error display:
{form.formState.errors.email && (
  <p className=\"text-sm text-red-600\">
    {form.formState.errors.email.message}
  </p>
)}
\`\`\`
"
```

**6. Claude's Response**: Perfect!

### Learning from Iterations

After each session, ask yourself:
- What could I have specified upfront?
- What examples would have helped?
- What assumptions did Claude make that I should have clarified?

Build a personal library of effective prompts. Reuse and refine them.

---

## 2.9 Key Takeaways

**The Five Components**: Context, Task, Examples, Constraints, Format

**Proven Techniques**:
- ✅ **Document positioning**: 30% accuracy boost (docs first, query last)
- ✅ **Few-shot examples**: 20% improvement (3-5 diverse examples)
- ✅ **Chain-of-thought**: 20% improvement ("think step-by-step")
- ✅ **Temperature 0.0-0.2**: Consistency for production code
- ✅ **XML tags**: Structure for complex prompts

**Common Mistakes to Avoid**:
- ❌ Vague instructions
- ❌ Assuming context
- ❌ Negative framing
- ❌ No examples for complex formats
- ❌ Asking too much at once

**The Mindset**:
Prompting is a skill. You'll improve with practice. Start with templates, iterate based on results, and build a library of effective patterns.

**Quick Reference**:
```markdown
<context>[Tech stack, files, patterns]</context>
<task>[Clear, specific task]</task>
<examples>[2-5 input/output pairs]</examples>
<constraints>[What to follow/avoid]</constraints>
<format>[How to structure response]</format>
```

---

## 2.10 Practice Exercises

Put these techniques into practice:

**Exercise 1: Rewrite a Vague Prompt**
Take: "Make the app faster"
Rewrite with: Context, specifics, measurements, constraints

**Exercise 2: Create Few-Shot Examples**
Pick a repetitive pattern in your codebase (API routes, components, tests).
Create 3 examples showing the pattern.
Ask Claude to apply it to new code.

**Exercise 3: Chain-of-Thought Debugging**
Find a bug in your code.
Ask Claude to debug it step-by-step with `<thinking>` tags.
Compare Claude's process to yours.

**Exercise 4: Temperature Experiment**
Run the same prompt at temperature 0.0, 0.5, and 1.0.
Observe differences in consistency and creativity.

**Exercise 5: Build a Template Library**
Create 5 templates for your most common tasks:
- Feature implementation
- Bug fix
- Code review
- Refactoring
- Testing

Save them for reuse.

---

**Next Chapter**: [Chapter 3: Architecture Patterns](./03-architecture-patterns.md) - Design robust, scalable Claude-powered workflows with streaming, context management, and error handling.

---

**Word Count**: ~3,450 words
**Reading Time**: 22 minutes
**Mastery Time**: 2-3 hours of practice

**Key Research Cited**:
- Anthropic Prompt Engineering: 30% positioning improvement
- Fortune 500 Case Study: 20% few-shot improvement
- Community Best Practices: 11 sources analyzed

**Sources**:
- Anthropic Official Prompt Engineering Documentation
- Pattern Confidence Matrix (validated across 7+ sources)
- "800+ hours of Learning Claude Code"
- "A Complete Guide to Claude Code"
