# Chapter 3: Architecture Patterns

**Target Audience**: Intermediate developers building production workflows
**Reading Time**: 25-30 minutes
**Practice Time**: 4-6 hours
**Prerequisites**: Chapters 1-2, 5+ successful Claude sessions

**Learning Objectives**:
- Design robust request/response workflows
- Implement streaming for better UX
- Master conversation management and portability
- Optimize the 200K context window strategically
- Build comprehensive error handling and recovery
- Use git as a checkpoint system for AI development

---

## 3.1 Request/Response Patterns

### Understanding Claude Code Workflows

Unlike traditional APIs where you send a request and receive a response, Claude Code enables conversational workflows where context builds across multiple turns.

### Synchronous vs. Asynchronous Patterns

**Synchronous (Single-Shot)**:
```markdown
# Pattern: One request, one response, done

User: "Create a login form component"
Claude: [Generates complete component]
User: [Accepts and moves on]

**Best for**:
- Simple, well-defined tasks
- One-file changes
- Clear requirements
- No iteration needed
```

**Asynchronous (Multi-Turn Conversation)**:
```markdown
# Pattern: Iterative refinement

User: "I need to add authentication to the app"
Claude: "I'll help with that. First, some questions:
          1. Which auth provider? (NextAuth, Supabase, Auth0, custom?)
          2. Social login or email/password?
          3. Where to store sessions?"

User: "NextAuth with email/password, PostgreSQL for sessions"
Claude: "Great. Let me create a plan..." [Enters plan mode]

User: [Reviews plan] "Looks good, but add 2FA support"
Claude: "Updated plan with 2FA..." [Shows revised plan]

User: "Perfect, implement it"
Claude: [Implements authentication system]

**Best for**:
- Complex features requiring clarification
- Architectural decisions
- Multiple interconnected files
- Ambiguous requirements
```

### Multi-Turn Conversation Strategy

**Pattern: Plan → Clarify → Implement → Refine**

```markdown
**Turn 1: Initial Request (Plan Mode)**
User: [Shift+Tab] "Create a plan for implementing user roles (admin, manager, user)"

**Turn 2: Clarification Questions**
Claude: "I need to understand:
         - Database or config-based roles?
         - Route-level, UI-level, or data-level permissions?
         - Can users have multiple roles?"

**Turn 3: Requirements Specification**
User: "Database roles (Prisma), route + UI level, single role per user"

**Turn 4: Plan Presentation**
Claude: [Detailed implementation plan with steps, files, risks]

**Turn 5: Plan Iteration (if needed)**
User: "Add permission groups for fine-grained control"
Claude: [Updated plan]

**Turn 6: Implementation**
User: [Shift+Tab to exit plan mode] "Implement the approved plan"
Claude: [Executes full implementation]

**Turn 7: Refinement**
User: "Add a RoleGate component to conditionally render UI"
Claude: [Adds component]

**Turn 8: Validation**
User: "Can you review for security issues?"
Claude: [Security review and recommendations]
```

### When to Start a New Conversation

**Start New Conversation When**:
- ✅ Switching to completely different feature
- ✅ Context becoming too large (approaching 100K+ tokens)
- ✅ Too many changes to track (git checkpoint first)
- ✅ Different architectural concern
- ✅ Starting fresh after major refactor

**Continue Conversation When**:
- 🔄 Iterating on same feature
- 🔄 Refining existing implementation
- 🔄 Fixing bugs in recently added code
- 🔄 Adding related functionality
- 🔄 Context is still manageable (<50K tokens)

**Tool**: Use `/clear` command to start fresh while staying in same Claude session.

---

## 3.2 Streaming Implementations

### Why Streaming Matters

Streaming provides **perceived performance improvements** even when total response time is the same.

**Without Streaming**:
```
User submits prompt → [15 seconds of blank screen] → Complete response appears
```

**With Streaming**:
```
User submits prompt → Text appears in real-time → [15 seconds total, but feels faster]
```

**User Experience Impact**:
- Users see progress immediately
- Can start reading while Claude is still generating
- Feels responsive and interactive
- Reduces abandonment

### Streaming in Claude Code

Claude Code streams by default in the CLI. For custom integrations, use the Anthropic API streaming parameter.

**API Example** (for custom tools):
```typescript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

// Streaming request
const stream = await anthropic.messages.stream({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  messages: [{
    role: 'user',
    content: 'Explain React hooks'
  }],
});

// Handle stream
for await (const chunk of stream) {
  if (chunk.type === 'content_block_delta') {
    process.stdout.write(chunk.delta.text);
  }
}
```

### Streaming Best Practices

**1. Handle Partial Responses**:
```typescript
let accumulatedResponse = '';

stream.on('data', (chunk) => {
  accumulatedResponse += chunk.text;
  // Display to user incrementally
  updateUI(accumulatedResponse);
});

stream.on('end', () => {
  // Finalize with complete response
  finalizeResponse(accumulatedResponse);
});
```

**2. Error Recovery**:
```typescript
stream.on('error', (error) => {
  // Stream interrupted
  console.error('Streaming error:', error);

  // Option 1: Retry with last complete chunk
  retryFromLastChunk(lastValidChunk);

  // Option 2: Start over
  restartRequest();
});
```

**3. Timeout Handling**:
```typescript
const STREAM_TIMEOUT = 120000; // 2 minutes

const timeoutId = setTimeout(() => {
  stream.abort();
  handleTimeout();
}, STREAM_TIMEOUT);

stream.on('end', () => {
  clearTimeout(timeoutId);
});
```

---

## 3.3 Conversation Management

### Conversation Portability

One of Claude Code's powerful features is conversation export/import, enabling cross-tool workflows.

**Export Conversations**:
```bash
# Within Claude Code CLI:
/export

# Copies full conversation history to clipboard
# Includes: all messages, tool calls, file modifications
```

**Use Cases**:
1. **Claude → Cursor workflow**:
   - Use Claude for exploration and planning (unlimited tokens)
   - Export conversation
   - Import to Cursor for final implementation and polish

2. **Resume Later**:
   - Export complex conversation
   - Close Claude
   - Resume days later with full context

3. **Share with Team**:
   - Export successful workflows
   - Share as templates
   - Team learns from effective patterns

4. **Backup Important Sessions**:
   - Export before risky changes
   - Preserve successful problem-solving approaches

**Resume Conversations**:
```bash
# Jump back to past conversation:
/resume

# Shows list of recent conversations
# Select one to continue where you left off
```

### Conversation Reversion

**Double-Tap ESC**: Revert to earlier point in current conversation

**Limitation**: Claude Code doesn't auto-restore file changes like Cursor does. You must manually revert files using git.

**Recommended Workflow**:
```bash
# Before major Claude changes:
git add . && git commit -m "Before Claude: [task]"

# Let Claude work...

# If you want to revert:
Double-tap ESC (revert conversation)
git reset --hard HEAD^ (revert file changes)
```

### Context Compression

When conversations grow too large, Claude Code automatically compresses older context.

**What Happens**:
- Recent messages: Full detail
- Mid-conversation: Summarized
- Early messages: High-level summary only

**Hook**: `compress-history` event
```python
# .claude/hooks/on_compress.py
# Triggered when history compression occurs
# Can log, notify, or take action
```

**Best Practice**: Start new conversation when reaching ~100K tokens to maintain full context quality.

---

## 3.4 Context Window Strategies

### Understanding the 200K Context Window

Claude has a **200,000-token context window**. For reference:
- Average codebase file: 200-500 tokens
- Large file: 2,000-5,000 tokens
- You can fit: ~100-400 files in context

**But**: Just because you *can* doesn't mean you *should*.

### The 30% Accuracy Boost: Document Positioning

**Critical Pattern** (Anthropic Research):

**Rule**: Large documents at **beginning**, queries at **end** = **30% accuracy improvement**

**Correct Structure**:
```markdown
<documents>
# Place ALL large documents here first
File: /app/api/users/route.ts
[... full file content]

File: /lib/database.ts
[... full file content]

File: /types/user.ts
[... full file content]
</documents>

<query>
# Your question or task goes LAST
Based on the code above, implement pagination for the users
endpoint. Use cursor-based pagination (not offset).
</query>
```

**Why This Works**:
Claude's attention mechanism gives highest weight to:
1. Beginning of context (first ~10K tokens)
2. End of context (last ~10K tokens)
3. Middle gets slightly less attention

### Extract-Then-Answer Pattern

**Problem**: Asking Claude to find information in a 50-page document often leads to missed details.

**Solution**: Two-step process

**Step 1: Extract Relevant Quotes**:
```markdown
<document>
[... 50-page API documentation]
</document>

<task>
Extract all quotes from the documentation that discuss authentication,
rate limiting, and error handling. Provide exact quotes with page/section
references.
</task>
```

**Step 2: Answer Based on Quotes**:
```markdown
Based on the quotes you extracted:

1. How do I authenticate to this API?
2. What are the rate limits?
3. What error codes should I handle?

Cite the specific quotes in your answers.
```

**Result**: Significantly better recall and accuracy on long documents.

### Sub-Agents for Context Isolation

**Problem**: Main conversation context gets polluted with details from subtasks.

**Solution**: Delegate subtasks to sub-agents with isolated contexts.

**Example Architecture**:
```markdown
**Main Agent** (orchestrator):
- Sees: High-level task, architecture, coordination
- Context: 20K tokens (clean)

**Sub-Agent 1** (backend specialist):
- Sees: Backend task only, API patterns, database
- Context: 30K tokens (focused on backend)

**Sub-Agent 2** (frontend specialist):
- Sees: Frontend task only, component patterns, UI
- Context: 30K tokens (focused on frontend)

**Sub-Agent 3** (testing specialist):
- Sees: Code to test, testing patterns, edge cases
- Context: 20K tokens (focused on testing)

Total context used: 100K
But each agent works with focused, relevant context only
```

**Detailed sub-agent patterns in Chapter 6**.

### Multi-Modal Context

Beyond text, Claude Code accepts:

**1. Screenshots**:
```bash
# Drag image into Claude Code conversation
# Use for: error messages, UI mockups, design references
```

**2. Folders from Other Repositories**:
```bash
# Drag entire folder into conversation
# Claude can read all files
# Useful for: backend context while working on frontend
# Note: Claude can modify these files if given permission
```

**3. URLs (Web Search)**:
```markdown
User: "Use the latest Next.js 14 App Router documentation
       to implement this feature"

Claude: [Fetches docs from nextjs.org automatically]
```

---

## 3.5 Error Handling & Recovery

### Self-Validation Pattern

**Technique**: Always ask Claude to validate its own work.

**Implementation**:
```markdown
# After Claude completes a task:
User: "Double-check your work. Look for:
       1. Edge cases not handled
       2. Potential bugs
       3. Security issues
       4. Performance problems
       Think step-by-step and be critical."

Claude: [Reviews own code, often finds issues missed initially]
```

**Surprising Result**: Claude frequently catches bugs on self-review that it didn't notice during implementation.

### Best-of-N Verification

**Technique**: Run the same prompt multiple times, compare outputs.

**When to Use**:
- Critical security code
- Complex algorithms
- Unfamiliar domains
- When Claude seems uncertain

**Implementation**:
```bash
# Run same prompt 3 times (different Claude sessions)
# Compare outputs
# If consistent: High confidence
# If varied: Low confidence, needs more context or human review
```

**Practical Example**:
```markdown
Prompt: "Implement JWT token validation with proper security"

Run 1: Validates signature, expiration, issuer
Run 2: Validates signature, expiration, issuer, audience
Run 3: Validates signature, expiration, issuer

Analysis: Runs 1 and 3 are identical, Run 2 adds audience check.
Investigate: Should we validate audience? (Yes, best practice)
```

### Validation Gates (Autonomous Testing)

**Pattern**: Specialized sub-agent that writes tests and iterates until they pass.

**Workflow**:
```markdown
1. Main agent implements feature
2. Validation gate sub-agent activates automatically
3. Sub-agent writes comprehensive tests
4. Sub-agent runs tests
5. If tests fail: Sub-agent fixes code and retries
6. Repeats until all tests pass
7. Reports back to main agent
```

**Configuration** (`.claude/subagents/validator.md`):
```markdown
# Validation Gate Agent

You are a testing specialist. Your job:

1. Analyze the code just written
2. Write comprehensive tests covering:
   - Happy path
   - Edge cases
   - Error conditions
   - Boundary values
3. Run the tests
4. If failures occur, fix the code (not the tests)
5. Iterate until 100% passing
6. Report test coverage and results

**Do not approve code with failing tests.**
```

### Graceful Degradation

**Pattern**: When Claude can't complete a task perfectly, provide partial success + clear explanation.

**Implementation**:
```markdown
User: "Implement feature X with requirements A, B, C, D"

Claude: "I've implemented requirements A, B, and C successfully.

Requirement D (real-time sync with WebSockets) requires:
- WebSocket server setup (not in current stack)
- Client connection management
- State synchronization strategy

Would you like me to:
1. Implement D with polling instead (simpler, works now)?
2. Set up WebSocket infrastructure first, then implement D?
3. Skip D for now and revisit later?

Here's what's working: [shows A, B, C implementation]"
```

**Key**: Deliver value while being transparent about limitations.

---

## 3.6 Git-Based Checkpointing

### The Philosophy

**Git is your safety net for AI development.** Unlike Cursor's built-in "restore to checkpoint," Claude Code requires manual git management.

### The Commit-Driven Workflow

**Basic Pattern**:
```bash
# 1. Before Claude makes changes:
git add .
git commit -m "Before: Add user roles feature"

# 2. Let Claude work...
# Claude creates/modifies files

# 3. Review changes:
git diff HEAD

# 4a. If good:
git add .
git commit -m "AI: Implement user roles with RBAC"

# 4b. If bad:
git reset --hard HEAD^  # Discard all changes
# Start over with better prompt
```

### Granular Checkpoints

**Pattern**: Commit after each significant change, not just features.

```bash
# Incremental commits:
git commit -m "AI: Add user role enum to Prisma schema"
git commit -m "AI: Create role validation middleware"
git commit -m "AI: Add RoleGate React component"
git commit -m "AI: Add role-based route protection"
git commit -m "AI: Add tests for role system"

# If role-based route protection is buggy:
git revert HEAD~2  # Revert just that commit
# Keep the rest
```

**Benefits**:
- Fine-grained rollback
- Clear audit trail
- Easy to identify which change caused issues
- Can cherry-pick successful changes

### Alternative Tools

**cc-undo**:
```bash
# Specialized tool for Claude Code checkpointing
npm install -g cc-undo

# Creates automatic snapshots
cc-undo snapshot "Before feature X"

# Restore to snapshot
cc-undo restore
```

**yoyo**:
```bash
# Lightweight undo/redo for file changes
npm install -g yoyo

# Mark checkpoint
yoyo mark

# Undo to last mark
yoyo undo
```

### Git Worktrees for Parallel Development

**Pattern**: Run multiple Claude Code instances simultaneously on different implementations.

**Use Case**: Try 3 different approaches to a complex problem, pick the best.

**Setup**:
```bash
# Create worktrees
git worktree add ../project-approach1 feature/approach1
git worktree add ../project-approach2 feature/approach2
git worktree add ../project-approach3 feature/approach3

# Open Claude Code in each
cd ../project-approach1 && claude &
cd ../project-approach2 && claude &
cd ../project-approach3 && claude &

# Give each Claude instance the same prompt
# Compare results
# Merge the best implementation
```

**Time Savings**: Feature that takes 30 minutes becomes 10 minutes (3x parallel) + 5 minutes review = 15 minutes total.

---

## 3.7 Architecture Diagrams (Markdown)

### Conversation Flow Diagram

```
┌─────────────────────────────────────────────────────┐
│                   User Request                       │
│           (Plan Mode: Shift+Tab ON)                  │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│            Claude: Clarification Questions           │
│  "Which auth provider? Social login or email/pwd?"   │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│             User: Answers Questions                  │
│        "NextAuth, email/password, PostgreSQL"        │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│          Claude: Detailed Implementation Plan        │
│   - Database changes (Prisma schema)                 │
│   - NextAuth configuration                           │
│   - API routes                                       │
│   - UI components                                    │
│   - Testing strategy                                 │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│         User: Reviews Plan, Requests Changes         │
│             "Add 2FA support"                        │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│           Claude: Updates Plan with 2FA              │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│         User: Approves Plan, Exits Plan Mode         │
│           (Shift+Tab OFF)                            │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│              Claude: Implements Feature              │
│     (Creates files, writes code, adds tests)         │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│        User: Tests, Requests Refinements            │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│           Claude: Refines Implementation             │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│                  ✅ Complete                         │
│              Git Commit Success                      │
└─────────────────────────────────────────────────────┘
```

### Context Management Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                     Main Agent (Orchestrator)                   │
│                  Context: 20K tokens (clean)                    │
│                                                                  │
│  - Overall architecture                                          │
│  - Task delegation                                               │
│  - Result coordination                                           │
└──────────┬─────────────────┬──────────────────┬────────────────┘
           │                 │                  │
           ▼                 ▼                  ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ Sub-Agent 1      │ │ Sub-Agent 2      │ │ Sub-Agent 3      │
│ Backend Expert   │ │ Frontend Expert  │ │ Test Specialist  │
│ Context: 30K     │ │ Context: 30K     │ │ Context: 20K     │
│                  │ │                  │ │                  │
│ - API routes     │ │ - React UI       │ │ - Test coverage  │
│ - Database       │ │ - Components     │ │ - Edge cases     │
│ - Business logic │ │ - Styling        │ │ - Validation     │
└──────────────────┘ └──────────────────┘ └──────────────────┘

Total: 100K tokens used
Each agent: Focused, relevant context only
Result: 3x context efficiency vs. monolithic approach
```

### Error Handling Decision Tree

```
┌─────────────────────────────────┐
│    Claude Completes Task        │
└────────────┬────────────────────┘
             │
             ▼
      ┌──────────────┐
      │ Self-Validate│◄───────┐
      └──────┬───────┘        │
             │                │
             ▼                │
     ┌──────────────┐         │
     │Issues Found? │         │
     └──────┬───────┘         │
            │                 │
        Yes │   No            │
            │   │             │
            ▼   ▼             │
    ┌────────────────────┐   │
    │  Fix Issues        │───┘
    └────────────────────┘

            │
            ▼
    ┌──────────────────┐
    │ Run Tests        │
    │ (if applicable)  │
    └────────┬─────────┘
             │
        Pass │  Fail
             │   │
             │   ▼
             │  ┌──────────────────┐
             │  │ Validation Gate  │
             │  │ Sub-Agent        │
             │  │ (Fix + Retry)    │
             │  └─────────┬────────┘
             │            │
             │            │ (Iterate until passing)
             │            │
             ▼            ▼
    ┌──────────────────────────┐
    │    Human Review          │
    │    (Final Check)         │
    └────────┬─────────────────┘
             │
        Good │  Issues
             │   │
             ▼   ▼
         ✅ Commit  ❌ Iterate
```

---

## 3.8 Key Takeaways

**Conversation Patterns**:
- ✅ Use plan mode (Shift+Tab) for complex features
- ✅ Multi-turn conversations for clarification and refinement
- ✅ Start new conversations when context gets too large (>100K tokens)
- ✅ Export conversations for portability and reuse

**Context Management**:
- ✅ **30% accuracy boost**: Documents first, queries last
- ✅ Extract-then-answer for long documents
- ✅ Sub-agents for context isolation (Chapter 6)
- ✅ Multi-modal: screenshots, folders, URLs

**Error Handling**:
- ✅ Self-validation: Always ask Claude to review its work
- ✅ Best-of-N for critical code
- ✅ Validation gates for autonomous testing
- ✅ Graceful degradation with partial success

**Git Workflow**:
- ✅ Commit before and after Claude changes
- ✅ Granular commits (one change per commit)
- ✅ Git worktrees for parallel experimentation
- ✅ Alternative tools: cc-undo, yoyo

**Quick Reference**:
```bash
# Before Claude works:
git commit -m "Before: [task]"

# Claude works...

# Review and commit:
git diff HEAD
git commit -m "AI: [description]"

# Or rollback:
git reset --hard HEAD^
```

---

## 3.9 Practice Exercises

**Exercise 1: Multi-Turn Conversation**
- Choose a complex feature (authentication, payment processing)
- Use plan mode
- Practice asking clarifying questions
- Iterate on the plan before implementing

**Exercise 2: Context Positioning**
- Take a large file (1000+ lines)
- Ask Claude to analyze it
- Try query-first (❌) vs. document-first (✅)
- Compare quality of responses

**Exercise 3: Git Checkpointing**
- Implement a feature with 5 distinct steps
- Commit after each step
- Intentionally break something in step 4
- Practice reverting just step 4, keeping 1-3

**Exercise 4: Self-Validation**
- Have Claude implement a feature
- Ask Claude to review its own work
- Note what issues it finds on self-review
- Did it catch things you missed?

**Exercise 5: Conversation Export**
- Complete a successful feature implementation
- Export the conversation
- Save as a template
- Use it for a similar feature later

---

**Next Chapter**: [Chapter 4: Tool Use & Function Calling](./04-tool-use.md) - Extend Claude's capabilities with MCP servers, external tools, and custom integrations.

---

**Word Count**: ~3,950 words
**Reading Time**: 27 minutes
**Mastery Time**: 4-6 hours

**Key Research**:
- Anthropic: 30% positioning improvement
- Community: git-based workflows (3 sources)
- Community: self-validation patterns (800+ hours)
- Armin Ronacher: agentic coding architecture

**Sources**:
- Pattern Confidence Matrix (11 sources)
- "A Complete Guide to Claude Code"
- "800+ hours Learning Claude Code"
- "I was wrong about Claude Code"
- Anthropic Prompt Engineering Documentation
