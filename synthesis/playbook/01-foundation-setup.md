# Chapter 1: Foundation & Setup

**Target Audience**: Complete beginners to Claude Code
**Reading Time**: 15-20 minutes
**Hands-On Time**: 1-2 hours
**Prerequisites**: Basic programming knowledge, git familiarity

**Learning Objectives**:
- Understand what makes Claude unique for coding
- Choose the right Claude model for your needs
- Complete your first productive Claude coding session
- Master basic prompt structure
- Establish foundational best practices

---

## 1.1 Introduction to Claude for Coding

### What Makes Claude Different

Claude Code represents a fundamentally different approach to AI-assisted development compared to tools like GitHub Copilot or traditional autocomplete. While other tools focus on predicting your next line of code, Claude excels at understanding, reasoning, and conversation.

**Claude's Core Strengths**:

**1. Understanding Unfamiliar Codebases**
One of Claude's most powerful capabilities is rapidly understanding code you've never seen before. Whether you're joining a new team, working on a client project, or diving into open-source, Claude can analyze architecture, explain patterns, and identify how systems work together—all in minutes instead of days.

```bash
# Instead of spending hours reading documentation:
"Explain how authentication works in this codebase.
Show me the flow from login to protected resource access."
```

**2. Complex Multi-Step Reasoning**
Claude doesn't just complete code; it thinks through problems step-by-step. When you ask it to implement a feature, it considers architecture, edge cases, error handling, and testing—then explains its reasoning.

```markdown
# Claude's approach to "Add user roles":
1. Analyzes current auth system
2. Identifies database schema changes needed
3. Plans API modifications
4. Considers backward compatibility
5. Proposes testing strategy
6. Implements with full context awareness
```

**3. Conversational Development**
Unlike autocomplete tools, Claude engages in dialogue. You can clarify requirements, iterate on approaches, ask "why" questions, and course-correct mid-implementation. It's like pair programming with an expert who has infinite patience.

### When to Use Claude vs. Other Tools

**Choose Claude Code when**:
- ✅ Understanding unfamiliar codebases
- ✅ Implementing complex, multi-file features
- ✅ Needing detailed explanations and reasoning
- ✅ Architecting new systems or refactoring
- ✅ Debugging subtle, logic-based bugs
- ✅ Working with poor or outdated documentation

**Choose Cursor/Copilot when**:
- 🔄 Simple autocomplete while typing
- 🔄 Single-line code completion
- 🔄 You know exactly what code you need
- 🔄 Minimal context required

**The Reality**: Many developers use both. Claude Code for planning and complex implementation, Cursor for final refinements and quick edits.

### Understanding Token Usage

**Critical Insight**: Claude Code uses **10-100x more tokens than Cursor**.

This isn't a bug—it's by design. While Cursor aggressively compresses context to minimize costs, Claude Code provides full context for better quality. On Anthropic's Max plan ($200/month), you get significant token allowance, but understanding usage helps avoid surprises.

**What This Means**:
- More comprehensive context = better outputs
- Higher costs, but better quality
- Strategic model selection matters (covered next)
- Use sub-agents to manage context efficiently (covered in Part III)

---

## 1.2 Choosing the Right Model

Claude Code offers multiple models, each with distinct characteristics. Choosing wisely balances cost, speed, and quality.

### Model Options

**Claude Sonnet 4 (claude-sonnet-4)**
- **Best for**: Most tasks, good balance of speed and quality
- **Speed**: Fast (2-4 seconds for typical responses)
- **Quality**: Excellent for 80% of coding tasks
- **Cost**: Moderate
- **When to use**: Default choice, general development, iterations

**Claude Opus 4 (claude-opus-4)**
- **Best for**: Complex reasoning, critical code, architecture decisions
- **Speed**: Slower (5-10 seconds for responses)
- **Quality**: Maximum quality, deepest reasoning
- **Cost**: Higher
- **When to use**: Complex bugs, security-critical code, important architectural decisions

**Auto-Select**
- Claude Code can automatically choose the right model based on task complexity
- Generally effective but may over-select Opus
- Good for beginners; experts often manual-select

### Model Selection Strategy

**For Beginners**:
```bash
# Start with Sonnet for everything
claude --model sonnet

# After 2-3 weeks, graduate to strategic selection
```

**For Intermediate Users**:
```markdown
**Sonnet for**:
- Feature implementation (known patterns)
- Bug fixes (clear reproduction)
- Refactoring (straightforward)
- Documentation
- Tests

**Opus for**:
- Architecture decisions
- Security reviews
- Complex algorithms
- Debugging subtle race conditions
- Performance optimization planning
```

**For Max Plan Users**:
Many developers on the Max plan default to Opus for everything, finding they rarely hit limits and the quality difference is worth it. The generous token allowance ($200/month plan) makes this viable.

### Cost Considerations

**Understanding Your Usage**:
```markdown
**Light usage** (5-10 hours/week): Sonnet primary, Opus sparingly
**Medium usage** (20-30 hours/week): Mix of Sonnet and Opus
**Heavy usage** (40+ hours/week): Max plan, Opus default

**Max Plan Reality**: $200/month can support 40-60 hours/week of intensive Claude Code use with Opus. This translates to $3-5/hour—far cheaper than any developer's hourly rate.
```

**Pro Tip**: Start with Sonnet. When you encounter a problem where Claude struggles, switch to Opus for that specific task. You'll quickly develop intuition for when you need the extra reasoning power.

---

## 1.3 Installation & Environment Setup

### Installing Claude Code

**Prerequisites**:
- macOS, Linux, or Windows WSL2
- Node.js 18+ or Python 3.8+
- Git
- API key from Anthropic Console

**Installation** (official instructions may vary—check docs):
```bash
# Using npm (recommended)
npm install -g @anthropic-ai/claude-code

# Using pip
pip install claude-code

# Verify installation
claude --version
```

**Initial Configuration**:
```bash
# Set API key
export ANTHROPIC_API_KEY="your-api-key-here"

# Or configure interactively
claude configure
```

### IDE Integration

While Claude Code works perfectly from the terminal, IDE integration provides context awareness and tighter workflows.

**VSCode Extension**:
```bash
# Install from VSCode marketplace
# Search: "Claude Code"

# Benefits:
- Auto-detects current file
- Works with selected text
- "Run Claude Code" button
- Seamless terminal integration
```

**Cursor Integration**:
Claude Code also works within Cursor, allowing you to use both tools in the same editor.

**Windsurf Support**:
Cross-compatible workflows enable conversation export/import between tools.

### Workspace Initialization

Navigate to your project and initialize:

```bash
cd /path/to/your/project

# Start Claude Code
claude

# Initialize project (creates .claude directory)
/init
```

**What `/init` Does**:
1. Scans codebase structure
2. Detects tech stack (package.json, requirements.txt, etc.)
3. Creates `.claude` directory
4. Generates initial `claude.md` with project context
5. Sets up recommended configuration

**The `.claude` Directory Structure**:
```
.claude/
├── claude.md              # Persistent project memory
├── commands/              # Custom slash commands
│   ├── add-feature.md
│   └── review-code.md
├── subagents/             # Specialized agents (advanced)
│   ├── backend-expert.md
│   └── frontend-expert.md
└── mcp_settings.json      # MCP server configuration (advanced)
```

---

## 1.4 Your First Claude Session

Let's walk through a complete first session, from start to finish.

### Starting Claude Code

```bash
# Navigate to project
cd my-nextjs-app

# Start Claude
claude

# You'll see:
Claude Code (sonnet-4)
Type /help for commands, or just start chatting.

>
```

### The Conversation Interface

**Basic Navigation**:
- Type naturally, press Enter to send
- `Ctrl+C` to cancel current operation
- `/help` for command list
- `/clear` to start fresh conversation
- `Shift+Tab` to toggle plan mode
- Double-tap `ESC` to revert changes

**Understanding Responses**:
Claude's responses include:
1. **Thinking section**: Claude's reasoning process
2. **Code**: Actual implementation
3. **Explanation**: What was done and why
4. **Next steps**: Suggested follow-ups

### Your First Prompt

Let's implement a simple feature together.

**Scenario**: You have a Next.js app and need to add a contact form.

**❌ Poor First Prompt**:
```
Add a contact form
```

**✅ Good First Prompt**:
```markdown
I need to add a contact form to my Next.js app.

**Requirements**:
- Form fields: name, email, message
- Validation: email must be valid, all fields required
- Submit to /api/contact endpoint
- Show success/error messages
- Use Tailwind CSS (project standard)

**Location**: Create form at /app/contact/page.tsx

**Questions**:
- Should this use server actions or API route?
- Any specific validation library preference?
```

**Why This is Better**:
1. ✅ Clear requirements (fields, validation, styling)
2. ✅ Context (Next.js, Tailwind)
3. ✅ Specific location
4. ✅ Opens dialogue with questions
5. ✅ Sets expectations

**Claude's Response Flow**:
```markdown
Let me help you create a contact form. I'll use Next.js server actions
for simplicity, and zod for validation (common Next.js pattern).

<creates files>
- /app/contact/page.tsx (form component)
- /app/actions/contact.ts (server action)
- /components/ui/input.tsx (reusable input)

<explains implementation>
The form uses React Hook Form with zod validation...

<suggests next steps>
Would you like me to:
1. Add email sending functionality (with Resend or SendGrid)?
2. Add rate limiting to prevent spam?
3. Create tests for the form?
```

### Iterating on the Response

Development is iterative. Claude expects follow-up:

```markdown
# You:
"Great! Let's add email sending with Resend. Also, can you add
a loading state to the submit button?"

# Claude implements updates to existing code
# Shows what changed and why
```

---

## 1.5 Basic Prompt Structure

Every effective Claude prompt has four core components:

### The Anatomy of an Effective Prompt

**1. Context** (What Claude needs to know)
```markdown
<context>
This is a Next.js 14 app using:
- App router
- TypeScript
- Tailwind CSS
- Prisma (PostgreSQL database)
- NextAuth.js for authentication
</context>
```

**2. Task** (What you want done)
```markdown
<task>
Add pagination to the /api/users endpoint. Support page sizes of
10, 25, and 50. Return total count and current page metadata.
</task>
```

**3. Constraints** (What to avoid or follow)
```markdown
<constraints>
- Must maintain backward compatibility
- Use Prisma cursor-based pagination (not offset)
- Follow existing API response format
- Add TypeScript types for pagination params
</constraints>
```

**4. Format** (How you want the response)
```markdown
<format>
Please:
1. Show the updated API route code
2. Provide example API calls with curl
3. Explain the pagination strategy chosen
</format>
```

### Simplified Template for Beginners

You don't always need XML tags. Here's a natural language version:

```markdown
**What I'm working on**: [Context about your project/file]

**What I need**: [Clear description of the task]

**Important**: [Any constraints, standards, or patterns to follow]

**Questions**: [Anything you're unsure about—invite dialogue]
```

### Real Example

```markdown
**What I'm working on**: E-commerce checkout flow in React. Using
React Hook Form for forms and Stripe for payments.

**What I need**: Add a "Save payment method" checkbox. If checked,
save the payment method to the user's account for future use.

**Important**:
- Must comply with PCI DSS (don't store card numbers)
- Use Stripe's SetupIntent for saving payment methods
- Checkbox should default to checked
- Add this to components/checkout/PaymentForm.tsx

**Questions**: Should I create a separate API route for saving the
payment method, or handle it in the existing checkout endpoint?
```

**Why This Works**:
1. Provides project context (React, Stripe, existing setup)
2. Specific task with clear requirements
3. Security consideration (PCI compliance)
4. Exact file location
5. Invites architectural discussion

---

## 1.6 Initial Best Practices

These six practices will save you hours of frustration as a beginner.

### 1. Treat Claude Like an Intern on Their First Day

**The Principle**: Don't assume Claude knows anything about your project, your preferences, or your constraints. Spell everything out.

**Example**:
```markdown
❌ "Add error handling"
✅ "Add try/catch blocks around all database queries.
    Log errors using our Winston logger (imported from @/lib/logger).
    Return user-friendly error messages, never expose stack traces."
```

### 2. Use Plan Mode Before Coding (Shift+Tab)

**The Principle**: Planning is cheap. Coding is expensive (in tokens and time). Always plan first.

**Workflow**:
```bash
1. Press Shift+Tab to enter plan mode
2. Ask Claude to create a plan: "Plan how to implement user roles"
3. Claude creates detailed specification
4. Review plan, iterate if needed
5. Approve plan
6. Press Shift+Tab again to exit plan mode
7. Execute: "Please implement the approved plan"
```

**Why It Matters**:
- Catches misunderstandings before code is written
- Saves tokens (planning uses fewer tokens than coding)
- Allows you to course-correct early
- Provides transparency into Claude's approach

**Real Example**:
```markdown
> Shift+Tab (enter plan mode)

> "Create a plan for adding two-factor authentication to our app"

# Claude responds with:
## 2FA Implementation Plan

### Questions First:
1. Which 2FA methods? (SMS, TOTP app, email)
2. Mandatory or optional for users?
3. Recovery code strategy?
4. Existing auth system details?

[You answer questions]

### Implementation Plan:
1. Database changes (add 2FA fields to users table)
2. TOTP generation library (speakeasy)
3. QR code generation for setup
4. Verification flow
5. Recovery codes
6. UI components
... [detailed plan]

> "Plan looks good, let's use TOTP with recovery codes"

> Shift+Tab (exit plan mode)

> "Implement the approved 2FA plan"
```

### 3. Git Checkpointing: Commit Before and After

**The Principle**: Git is your safety net. Commit before asking Claude to make changes. Commit after if you like them. Revert if you don't.

**Workflow**:
```bash
# Before Claude makes changes
git add .
git commit -m "Before: Add 2FA feature"

# Let Claude work...

# If good:
git add .
git commit -m "After: Add 2FA feature (Claude)"

# If bad:
git reset --hard HEAD^
# Try again with better prompt
```

**Why It Matters**:
- Claude Code lacks Cursor's "restore to point" feature
- Easy rollback of bad changes
- Audit trail of what Claude changed
- Enables experimentation without risk

**Pro Tip**: Use descriptive commit messages noting AI-generated code:
```bash
git commit -m "AI: Implement user roles with RBAC"
git commit -m "AI: Refactor auth middleware for performance"
```

### 4. Be Explicit About File Locations

**The Principle**: Always specify exactly which files to modify or create.

```markdown
❌ "Create a user profile component"

✅ "Create a user profile component at app/profile/UserProfile.tsx.
    It should import types from @/types/user.ts and use our
    existing Avatar component from @/components/ui/Avatar.tsx"
```

### 5. Provide Examples for Complex Formatting

**The Principle**: If you need specific output format or code style, show an example.

```markdown
❌ "Write API error responses consistently"

✅ "Write API error responses in this exact format:

Example:
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email address",
    "details": { "field": "email", "value": "bad@" }
  },
  "timestamp": "2025-11-14T12:00:00Z"
}

Apply this format to all API routes."
```

### 6. Start Simple, Iterate

**The Principle**: Don't ask for everything at once. Build incrementally.

**Good Progression**:
```markdown
# Step 1:
"Create a basic user profile page showing name and email"

# Step 2:
"Add an edit button that opens a modal"

# Step 3:
"Add form validation to the edit modal"

# Step 4:
"Add profile picture upload"
```

**Why This Works**:
- Easier to verify each step
- Faster iterations
- Clearer debugging if something goes wrong
- Builds context naturally

---

## 1.7 Your First Productive Session: Checklist

Ready to dive in? Follow this checklist for your first successful session.

### Pre-Session Setup (5 minutes)

```markdown
[ ] Install Claude Code
[ ] Set up API key
[ ] Navigate to project directory
[ ] Run git status (clean working tree recommended)
[ ] Identify a small, self-contained task (1-2 hours max)
```

### Session Execution (30-60 minutes)

```markdown
[ ] Start Claude: claude
[ ] Run /init if first time in this project
[ ] Press Shift+Tab to enter plan mode
[ ] Ask Claude to create a plan for your task
[ ] Review plan, ask clarifying questions
[ ] Approve plan (or iterate until satisfied)
[ ] Exit plan mode (Shift+Tab)
[ ] Commit current state: git commit -m "Before: [task]"
[ ] Ask Claude to execute the plan
[ ] Review generated code
[ ] Ask Claude to explain anything unclear
[ ] Test the implementation
[ ] If issues found, ask Claude to fix them
[ ] Once working, commit: git commit -m "After: [task] (Claude)"
```

### Post-Session Reflection (5 minutes)

```markdown
[ ] Did the code work as expected?
[ ] What could I have specified better in my prompt?
[ ] Did plan mode help, or could I have skipped it?
[ ] What did I learn about prompting Claude?
[ ] What would I do differently next time?
```

---

## 1.8 Common Beginner Mistakes

Learn from others' mistakes. Here are the most common pitfalls:

### Mistake #1: Vague Prompts

```markdown
❌ "Fix the bug"
❌ "Make it better"
❌ "Add features"

✅ "The login form throws a 500 error when submitted with a valid
    email but no password. Add validation to catch this on the
    client side before submission."
```

### Mistake #2: Not Using Plan Mode

**Symptom**: Claude implements something different from what you wanted.

**Solution**: Always use plan mode (Shift+Tab) for anything non-trivial. Planning takes 30 seconds and saves 30 minutes of rework.

### Mistake #3: Forgetting to Commit

**Symptom**: Claude makes changes you don't like, and now your code is a mess.

**Solution**:
```bash
# Before asking Claude to make changes:
git add . && git commit -m "Before Claude changes"

# If you don't like the changes:
git reset --hard HEAD^
```

### Mistake #4: Not Providing Context

```markdown
❌ "Add authentication"

✅ "Add authentication to this Next.js app. We're using:
    - NextAuth.js (already installed)
    - PostgreSQL database via Prisma
    - Email/password auth (not OAuth yet)

    Please:
    1. Create the API route at /app/api/auth/[...nextauth]/route.ts
    2. Add login form at /app/login/page.tsx
    3. Use our existing Input component from @/components/ui
    4. Follow our Tailwind styling conventions"
```

### Mistake #5: Trying to Do Too Much at Once

**Symptom**: Claude's response is overwhelming, touches many files, introduces bugs.

**Solution**: Break tasks into smaller pieces.

```markdown
# Instead of:
"Build a complete blog system with posts, comments, tags, and admin panel"

# Do this:
1. "Create a blog post model in Prisma with title, content, and author"
2. "Create API routes for CRUD operations on blog posts"
3. "Create a blog post list page showing all posts"
4. "Create a blog post detail page"
5. [Continue step by step...]
```

---

## 1.9 Next Steps

You now have the foundation to use Claude Code effectively. Here's what to explore next:

**Immediate Next Steps** (This Week):
1. Complete one small feature using the checklist above
2. Practice using plan mode for every task
3. Experiment with both Sonnet and Opus to feel the difference
4. Start building a `.claude.md` file (Chapter 4 covers this in depth)

**Short-Term Goals** (Next 2 Weeks):
1. Read Chapter 2: Effective Prompting Fundamentals
2. Create your first custom command (Chapter 5)
3. Install your first MCP server—Context7 recommended (Chapter 7)
4. Build confidence through daily practice

**Long-Term Goals** (Next Month):
1. Master sub-agents for complex tasks (Chapter 6)
2. Implement hooks for automation (Chapter 9)
3. Establish team workflows (Chapter 11)
4. Contribute patterns back to the community

---

## 1.10 Key Takeaways

**The Essentials**:
1. ✅ Claude excels at understanding, reasoning, and multi-step tasks
2. ✅ Sonnet 4 for most tasks, Opus 4 for complex reasoning
3. ✅ Always use plan mode (Shift+Tab) for non-trivial work
4. ✅ Git checkpointing is your safety net
5. ✅ Be explicit: file locations, requirements, constraints, format
6. ✅ Treat Claude like an intern on their first day—assume nothing

**The Mindset Shift**:

Traditional autocomplete tools complete your code. Claude Code completes your thinking. Engage it in conversation, iterate on plans, ask questions, and course-correct. It's pair programming with an expert who has infinite patience and vast knowledge—but only if you communicate clearly.

**Quick Reference: First Session Template**

```markdown
# 1. Start and Initialize
cd my-project
git commit -m "Checkpoint before Claude"
claude
/init

# 2. Plan (Shift+Tab)
> "Create a plan to implement [feature]"
[Review plan, iterate]

# 3. Execute (Shift+Tab to exit plan mode)
> "Implement the approved plan"

# 4. Test and Commit
[Test the code]
git add .
git commit -m "Implement [feature] with Claude"
```

You're now ready for your first productive Claude Code session. Take it slow, use plan mode, commit often, and enjoy the experience of pair programming with AI.

**Next Chapter**: [Chapter 2: Effective Prompting Fundamentals](./02-effective-prompting.md) - Master advanced prompting techniques for 20-30% accuracy improvements.

---

**Word Count**: ~2,950 words
**Reading Time**: 18 minutes
**Practice Time**: 1-2 hours

**Sources**:
- Anthropic Official Prompt Engineering Documentation
- "A Complete Guide to Claude Code" (community)
- "800+ hours of Learning Claude Code" (community)
- "I was wrong about Claude Code - Updated Workflow" (community)
- Peter Yang Movie App Tutorial
- Pattern Confidence Matrix (11 sources analyzed)
