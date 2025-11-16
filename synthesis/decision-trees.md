# Claude Code Decision Trees

**Purpose**: Quick decision-making guides for common Claude Code scenarios
**Version**: 1.0
**Date**: 2025-11-14

---

## Decision Tree 1: Which Claude Model Should I Use?

```
START: What type of task are you doing?
│
├─ Simple feature implementation with known patterns?
│  └─ Is this your first attempt at this task?
│     ├─ YES → Use Sonnet ✅
│     └─ NO (tried already, stuck) → Use Opus 🎯
│
├─ Bug fix?
│  └─ Do you have clear reproduction steps?
│     ├─ YES → Use Sonnet ✅
│     └─ NO (subtle/intermittent bug) → Use Opus 🎯
│
├─ Refactoring existing code?
│  └─ Is the pattern straightforward?
│     ├─ YES → Use Sonnet ✅
│     └─ NO (complex architectural changes) → Use Opus 🎯
│
├─ Documentation or tests?
│  └─ Use Sonnet ✅ (speed matters more)
│
├─ Architecture decision?
│  └─ Use Opus 🎯 (needs deep reasoning)
│
├─ Security review?
│  └─ Use Opus 🎯 (critical accuracy required)
│
├─ Complex algorithm or data structure?
│  └─ Use Opus 🎯 (advanced problem-solving)
│
├─ Performance optimization?
│  └─ Use Opus 🎯 (multi-dimensional analysis)
│
└─ Debugging race conditions or subtle issues?
   └─ Use Opus 🎯 (deep reasoning needed)

COST OPTIMIZATION TIP:
If on Max plan ($200/month), default to Opus. You rarely hit limits.
If watching costs closely, start Sonnet, escalate to Opus if needed.

RULE OF THUMB:
- 75-80% of tasks: Sonnet
- 20-25% of tasks: Opus
- Savings: 40-50% vs. Opus-only approach
```

---

## Decision Tree 2: How Should I Structure My Prompt?

```
START: What information do you have?
│
├─ Is this a complex task (multi-step, many files)?
│  ├─ YES → Enter Plan Mode (Shift+Tab)
│  │        └─ Ask Claude to create a detailed plan
│  │           └─ Review plan
│  │              ├─ Plan unclear? → Ask clarifying questions, iterate
│  │              └─ Plan good? → Exit plan mode, execute
│  │
│  └─ NO (simple, single-file change)
│     └─ Continue to next check
│
├─ Do you have the tech stack and context documented?
│  ├─ NO → Add <context> section
│  │      - Tech stack (framework, libraries, database)
│  │      - Relevant file paths
│  │      - Existing patterns to follow
│  │
│  └─ YES → Continue
│
├─ Is the desired output format complex or specific?
│  ├─ YES → Add 3-5 <examples>
│  │      - Show exact input/output pairs
│  │      - Include edge cases
│  │      - Show error handling
│  │
│  └─ NO (standard code format) → Continue
│
├─ Are there constraints or things to avoid?
│  ├─ YES → Add <constraints> section
│  │      - What to follow (coding standards, libraries)
│  │      - What to avoid (breaking changes, certain patterns)
│  │
│  └─ NO → Continue
│
└─ How complex is the reasoning required?
   ├─ Complex (multi-step logic, debugging)
   │  └─ Add "Think step-by-step" or <thinking> tags
   │
   └─ Simple → Direct task description

FINAL STRUCTURE:
<context>[Background info]</context>
<task>[Clear, specific task]</task>
<examples>[2-5 input/output pairs]</examples>
<constraints>[What to follow/avoid]</constraints>
<format>
Please provide:
1. [Expected output 1]
2. [Expected output 2]
</format>

OPTIMIZATION:
- Long documents? → Place at BEGINNING (30% accuracy boost)
- Query? → Place at END
- Both? → <documents>...</documents> first, <query>...</query> last
```

---

## Decision Tree 3: When Should I Use Streaming?

```
START: What's your use case?
│
├─ Building a user-facing application?
│  └─ Is response time important for UX?
│     ├─ YES (users waiting for results)
│     │  └─ Use Streaming ✅
│     │     - Perceived faster response
│     │     - Users see progress immediately
│     │     - Can start reading while generating
│     │
│     └─ NO (background processing, batch jobs)
│        └─ Non-streaming is fine
│           - Simpler implementation
│           - Wait for complete response
│
├─ Using Claude Code CLI?
│  └─ Streaming enabled by default ✅
│     (You get streaming automatically)
│
├─ Building custom integration with Anthropic API?
│  └─ What's the expected response size?
│     ├─ Large (2000+ tokens)
│     │  └─ Use Streaming ✅
│     │     - Better UX for long responses
│     │     - Handle partial responses incrementally
│     │
│     ├─ Medium (500-2000 tokens)
│     │  └─ Your choice
│     │     - Streaming: Better UX
│     │     - Non-streaming: Simpler code
│     │
│     └─ Small (< 500 tokens)
│        └─ Non-streaming is fine
│           - Overhead not worth it
│           - Simpler implementation
│
└─ Need to process response in real-time?
   ├─ YES (display to user, log incrementally)
   │  └─ Use Streaming ✅
   │
   └─ NO (process complete response only)
      └─ Non-streaming is fine

IMPLEMENTATION NOTES:
- Streaming adds complexity (handle partial chunks)
- Must handle errors mid-stream
- Need timeout management
- But: Dramatically improves perceived performance

RECOMMENDATION:
Default to streaming for user-facing apps, skip for batch processing.
```

---

## Decision Tree 4: How Do I Optimize Costs?

```
START: Where are most of your tokens going?
│
├─ Don't know? → Set up monitoring first
│  └─ Track: tokens per task, tokens per model, tokens per developer
│     └─ Come back to this tree after 1 week of data
│
└─ Know your usage patterns? → Continue
   │
   ├─ Using Opus for everything?
   │  └─ OPTIMIZATION: Switch to Sonnet-first strategy
   │     - Saves 40-50% immediately
   │     - Start with Sonnet
   │     - Escalate to Opus only when stuck
   │
   ├─ Large context sizes (100K+ tokens per conversation)?
   │  └─ Are you working on complex multi-part features?
   │     ├─ YES → Use sub-agents
   │     │  - Main agent: 20K tokens (orchestration)
   │     │  - Sub-agents: 20-30K each (focused tasks)
   │     │  - Savings: 33% via context isolation
   │     │
   │     └─ NO → Use /clear between unrelated tasks
   │        - Prevents context pollution
   │        - Savings: 15-20%
   │
   ├─ Many iterations per task (back-and-forth)?
   │  └─ Root cause?
   │     ├─ Vague prompts → Be more explicit
   │     │  - Add context, examples, constraints
   │     │  - Potential savings: 66% (fewer iterations)
   │     │
   │     ├─ Skipping plan mode → Use Shift+Tab
   │     │  - Planning is cheap (few tokens)
   │     │  - Prevents expensive rework
   │     │  - Potential savings: 30-50%
   │     │
   │     └─ Unclear requirements → Clarify upfront
   │        - Ask all questions at start
   │        - Reduces back-and-forth
   │
   ├─ High token usage per task (even with good prompts)?
   │  └─ Is task complexity appropriate for AI?
   │     ├─ YES → Consider if Opus provides value
   │     │  - If stuck on Sonnet, Opus justified
   │     │  - If completing successfully, cost is ROI
   │     │
   │     └─ NO → Break into smaller subtasks
   │        - Smaller tasks = smaller contexts
   │        - More focused, less token waste
   │
   └─ Already optimized prompts and model selection?
      └─ Advanced optimizations:
         ├─ Conversation portability
         │  - Use Claude for exploration (unlimited)
         │  - Export to Cursor for refinement (efficient)
         │
         ├─ MCP server optimization
         │  - Remove unused MCPs (reduce overhead)
         │  - Optimize slow MCPs (reduce timeouts)
         │
         └─ Token budget alerts
            - Set daily limits
            - Alert at 80% threshold
            - Review high-token sessions

COST BREAKDOWN:
Max Plan: $200/month
- Supports 40-60 hours/week intensive use
- Effective cost: $3-5/hour
- vs. Developer cost: $50-200/hour
- ROI: If saves 2 hours/week = $800/month savings

TARGET SAVINGS:
- Sonnet-first: 40-50% reduction
- Sub-agents: 33% reduction
- Clear prompts: 66% potential reduction
- Combined: 70-80% optimization possible
```

---

## Decision Tree 5: Should I Use Plan Mode?

```
START: What are you about to do?
│
├─ Is this a trivial task (< 5 minutes)?
│  ├─ YES (add comment, rename variable)
│  │  └─ Skip plan mode ⏩
│  │     - Direct implementation faster
│  │
│  └─ NO (non-trivial task) → Continue
│
├─ Does the task involve multiple files?
│  ├─ YES (3+ files)
│  │  └─ Use Plan Mode ✅
│  │     - Coordinate changes across files
│  │     - Ensure consistency
│  │
│  └─ NO (1-2 files) → Continue
│
├─ Are the requirements unclear or ambiguous?
│  ├─ YES
│  │  └─ Use Plan Mode ✅
│  │     - Claude asks clarifying questions
│  │     - You align on approach before coding
│  │
│  └─ NO (crystal clear) → Continue
│
├─ Does this involve architecture decisions?
│  ├─ YES (choosing patterns, libraries, structure)
│  │  └─ Use Plan Mode ✅
│  │     - Discuss trade-offs
│  │     - Validate approach
│  │     - Document decisions
│  │
│  └─ NO → Continue
│
├─ Will this take more than 30 minutes to implement?
│  ├─ YES
│  │  └─ Use Plan Mode ✅
│  │     - Plan is cheap (low tokens)
│  │     - Implementation is expensive
│  │     - Catch issues early
│  │
│  └─ NO (quick implementation) → Continue
│
├─ Is this a new feature (vs. bug fix)?
│  ├─ YES (new functionality)
│  │  └─ Use Plan Mode ✅
│  │     - Ensure completeness
│  │     - Consider edge cases
│  │     - Plan testing strategy
│  │
│  └─ NO (bug fix with known solution)
│     └─ Skip plan mode ⏩
│        - Direct fix is faster
│
└─ When in doubt?
   └─ Use Plan Mode ✅
      - Cost: 30 seconds of your time
      - Benefit: Prevents hours of rework
      - ROI: Massive

WORKFLOW:
1. Shift+Tab (enter plan mode)
2. "Create a plan for [task]"
3. Claude asks questions + creates plan
4. Review plan thoroughly
5. Iterate if needed
6. Shift+Tab (exit plan mode)
7. "Implement the approved plan"

ANTI-PATTERN:
Starting to code immediately without planning
Result: Misaligned implementation, wasted tokens, rework
```

---

## Decision Tree 6: Should I Use Sub-Agents?

```
START: What's the scope of your task?
│
├─ Single, focused task (one concern)?
│  └─ Skip sub-agents ⏩
│     - Main agent is sufficient
│     - Sub-agents add overhead
│
└─ Complex, multi-faceted project?
   │
   ├─ Can the task be broken into independent subtasks?
   │  ├─ NO (highly interdependent)
   │  │  └─ Skip sub-agents ⏩
   │  │     - Coordination overhead too high
   │  │     - Use main agent with clear structure
   │  │
   │  └─ YES (parallelizable) → Continue
   │
   ├─ How many distinct concerns?
   │  ├─ 2 concerns
   │  │  └─ Maybe use sub-agents
   │  │     - Benefit: Context isolation
   │  │     - Cost: Setup overhead
   │  │     - Evaluate if context is polluted
   │  │
   │  ├─ 3-5 concerns
   │  │  └─ Use sub-agents ✅
   │  │     - Clear value from isolation
   │  │     - Examples:
   │  │       * Backend + Frontend + Testing
   │  │       * API + Database + Validation + Tests
   │  │
   │  └─ 6+ concerns
   │     └─ Use sub-agents, but review architecture
   │        - May indicate task is too large
   │        - Consider breaking into smaller features
   │
   ├─ Is context bleeding between concerns?
   │  ├─ YES (main conversation polluted with details)
   │  │  └─ Use sub-agents ✅
   │  │     - Isolate frontend details from backend
   │  │     - Keep main agent focused on orchestration
   │  │
   │  └─ NO → May not need sub-agents yet
   │
   └─ Do you want to try multiple approaches in parallel?
      ├─ YES (experimental, compare implementations)
      │  └─ Use parallel sub-agents ✅
      │     - Run 2-3 implementations simultaneously
      │     - Git worktrees for isolation
      │     - Pick best result
      │     - Time savings: 3x (for 3 parallel)
      │
      └─ NO → Standard sub-agents or main agent

SUB-AGENT ARCHETYPES:
- Backend expert (API, database, business logic)
- Frontend expert (UI, components, styling)
- Testing specialist (unit, integration, E2E tests)
- Documentation generator (docs, README, comments)
- Code reviewer (security, quality, best practices)

ASSIGNMENT STRATEGY:
✅ Task-based: "Implement authentication API"
❌ Role-based: "You are a senior backend developer"
Reason: Task-based outperforms role-based

WHEN SUB-AGENTS SHINE:
- Full-stack features (backend + frontend)
- Large refactors (multiple modules)
- Parallel development (speed critical)
- Context isolation (main agent staying clean)
```

---

## Decision Tree 7: When Should I Use MCP Servers?

```
START: What capability do you need?
│
├─ Access to latest documentation?
│  └─ Install Context7 MCP ✅
│     - Priority #1 recommendation
│     - Always valuable
│     - Universally recommended (10/11 sources)
│
├─ Database queries or analytics?
│  └─ Do you have a database (Supabase, Postgres, etc.)?
│     ├─ YES → Install Database MCP ✅
│     │  - Direct data access
│     │  - Analytics queries
│     │  - Debugging data issues
│     │
│     └─ NO → Not applicable
│
├─ Browser automation or testing?
│  └─ Need E2E tests or web scraping?
│     ├─ YES → Install Playwright MCP ✅
│     │  - Automated testing
│     │  - Screenshot generation
│     │  - Web research
│     │
│     └─ NO → Not needed
│
├─ GitHub operations (issues, PRs)?
│  └─ Use GitHub CLI (gh) via bash commands
│     - No separate MCP needed
│     - Claude can use `gh` directly
│
├─ External API integration?
│  └─ Can you accomplish this with bash + curl?
│     ├─ YES → Use bash commands
│     │  - Simpler than MCP
│     │  - Less overhead
│     │
│     └─ NO (complex integration, frequent use)
│        └─ Consider custom MCP
│           - Worth it if used regularly (weekly+)
│           - Evaluate cost/benefit
│           - Simpler alternatives first
│
└─ Niche or specialized tool?
   └─ Ask these questions:
      1. Will I use this weekly or more?
      2. Can bash commands accomplish this?
      3. Does the value justify setup complexity?

      ├─ All YES → Build custom MCP
      ├─ Mixed → Try bash first, MCP if needed
      └─ Mostly NO → Skip MCP, use bash or manual

MCP PRIORITY ORDER:
1. ✅ Context7 (install immediately, always valuable)
2. ✅ Database MCP (if using database, high value)
3. ✅ Playwright (if testing/automation needs)
4. ⚠️ Niche MCPs (evaluate carefully)

ARMIN RONACHER'S WARNING:
Some MCPs add unnecessary complexity without value.
"Code is all you need" for many scenarios.
Evaluate cost/benefit before adding MCPs.

ESSENTIAL vs. NICE-TO-HAVE:
Essential:
- Context7 (documentation)
- Database (if applicable)
- Browser (if testing/research)

Nice-to-have (evaluate):
- Stripe (if frequent payment operations)
- AWS (if frequent cloud operations)
- Slack (if frequent messaging)
- [Custom for your domain]
```

---

## Decision Tree 8: How Should I Handle Errors?

```
START: Claude encountered an error or produced incorrect code
│
├─ Is this a runtime error in generated code?
│  └─ Ask Claude to review step-by-step:
│     "Double-check your work. Think step-by-step:
│      1. What might be causing this error?
│      2. What edge cases did we miss?
│      3. How should we fix it?"
│
│     └─ Claude often finds issues on self-review
│
├─ Is this an API error (Anthropic API)?
│  └─ What's the error code?
│     ├─ RATE_LIMIT_EXCEEDED
│     │  └─ Implement exponential backoff
│     │     - Wait: 2s, 4s, 8s, 16s
│     │     - Max 4 retries
│     │     - Then fail gracefully
│     │
│     ├─ CONTEXT_LENGTH_EXCEEDED
│     │  └─ Options:
│     │     1. Use /clear and start fresh
│     │     2. Use sub-agents (context isolation)
│     │     3. Shorten your prompt
│     │     4. Split into smaller tasks
│     │
│     ├─ TIMEOUT
│     │  └─ Diagnose cause:
│     │     - Slow MCP server? → Optimize or increase timeout
│     │     - Large response? → Use streaming
│     │     - Complex query? → Simplify or break down
│     │
│     └─ INVALID_API_KEY
│        └─ Check environment:
│           - Is ANTHROPIC_API_KEY set?
│           - Is it correct?
│           - Has it expired?
│
├─ Is this an MCP server error?
│  └─ What type of error?
│     ├─ MCP_SERVER_NOT_FOUND
│     │  └─ Verify installation:
│     │     - which [mcp-command]
│     │     - npm list -g [mcp-package]
│     │     - Check .claude/mcp_settings.json
│     │
│     ├─ MCP_AUTHENTICATION_FAILED
│     │  └─ Check credentials:
│     │     - Environment variables set?
│     │     - API keys valid?
│     │     - Permissions correct?
│     │
│     └─ MCP_TIMEOUT
│        └─ Optimize:
│           - Add pagination to queries
│           - Increase timeout setting
│           - Break into smaller operations
│
├─ Is the code quality poor (not meeting standards)?
│  └─ Prevention strategies:
│     ├─ Add to .claude.md:
│     │  - Coding standards
│     │  - Quality requirements
│     │  - Example patterns to follow
│     │
│     ├─ Use validation gates:
│     │  - Auto-run linter
│     │  - Auto-run type checker
│     │  - Auto-run tests
│     │  - Block on failures
│     │
│     └─ Code review workflow:
│        - /review-security
│        - /review-code
│        - Manual human review
│
└─ Is Claude hallucinating or providing inaccurate info?
   └─ Mitigation strategies:
      ├─ Lower temperature (0.0-0.2)
      ├─ Require citations: "Cite your sources"
      ├─ Extract-then-answer pattern for docs
      ├─ Provide more context and examples
      ├─ Use MCP for live docs (Context7)
      └─ Best-of-N verification (critical code)

EMERGENCY ROLLBACK:
If Claude made breaking changes:
1. git log --oneline -5
2. git reset --hard [last-good-commit]
3. Start over with better prompt
```

---

## Quick Reference: Decision Flowchart Symbols

```
Symbol Guide:
├─ Branch point (decision)
└─ Final outcome
✅ Recommended action
⏩ Skip/Not needed
🎯 Advanced/Complex path
⚠️ Warning/Caution
❌ Anti-pattern
```

---

## Using These Decision Trees

**How to Navigate**:
1. Start at the top
2. Answer each question honestly
3. Follow the branch that matches your answer
4. Reach a recommendation
5. Implement the recommended action

**When to Revisit**:
- Every few weeks (as you gain experience)
- When stuck on a decision
- When reviewing team workflows
- When onboarding new team members

**Customization**:
These trees are starting points. Customize based on:
- Your team's workflows
- Your specific tech stack
- Your organization's constraints
- Lessons learned from experience

---

**Related Resources**:
- Quick Reference Cheat Sheet: `QUICK-REFERENCE.md`
- Full Playbook: `playbook/01-foundation-setup.md` through `05-production-readiness.md`
- Pattern Confidence Matrix: `pattern-confidence-matrix.md`

**Version History**:
- v1.0 (2025-11-14): Initial decision trees based on 11-source analysis
