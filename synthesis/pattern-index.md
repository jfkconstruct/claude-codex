# Claude Coding Patterns - Comprehensive Index
## Extracted from 11 Source Documents

**Analysis Date**: 2024-11-14
**Sources Reviewed**: 11 files (10 markdown, 1 JSON)
**Already Documented Patterns**: 18
**New Patterns Identified**: 27

---

## Executive Summary

This index catalogs NEW patterns and techniques found in source materials that are NOT yet documented in the `/patterns/` directory. The analysis reveals a rich ecosystem of advanced techniques spanning workflow automation, performance optimization, quality assurance, and mobile-specific development patterns.

**Key Findings**:
- **Automation patterns** (hooks, GitHub CLI) are heavily emphasized but undocumented
- **Performance optimization** techniques (document positioning, token management) have quantified benefits
- **Mobile/app development** has distinct patterns separate from web development
- **Quality assurance** patterns (validation gates, type checking) are sophisticated but missing
- **Context engineering** represents an emerging methodology worth deep documentation

---

## NEW PATTERNS IDENTIFIED

### 1. XML Tag Structuring
**Sources**: anthropic-prompt-engineering.md (extensive coverage)
**Frequency**: 4 sources

**Description**: 
Using XML tags to structure prompts and responses for clarity and parseability. Common tags include `<thinking>`, `<answer>`, `<document>`, `<example>`, `<instructions>`, `<context>`. Claude was specifically trained with XML in training data.

**Why Valuable**:
- **Clarity**: Separates different parts of prompts (instructions, examples, context)
- **Accuracy**: Reduces errors from misinterpretation  
- **Flexibility**: Easy to find, add, remove, or modify sections
- **Post-processing**: Makes extracting specific parts of responses easier
- **Quantified Impact**: Improves structured output reliability

**Key Techniques**:
- Combine with multishot prompting using `<examples>` wrapper
- Use `<thinking>` + `<answer>` separation for chain of thought
- Structure prompt chaining with clear XML handoffs

---

### 2. Git Checkpointing Workflow
**Sources**: "I was wrong about Claude Code.md", "A Complete Guide to Claude Code.md"
**Frequency**: 3 sources

**Description**:
Using Git as a checkpoint/restore system specifically for AI coding sessions. Commit frequently (every successful change) to create restore points. Use git revert/discard when AI goes wrong direction instead of relying on built-in undo.

**Why Valuable**:
- Claude Code lacks Cursor's "restore to chat point" feature
- Provides rollback capability for AI-generated changes
- Enables experimentation without risk
- Creates audit trail of AI changes
- Allows testing different approaches on same codebase state

**Implementation**:
```bash
# After each successful AI change
git add .
git commit -m "AI: [description of change]"

# When AI goes wrong direction
git reset --hard HEAD  # or specific commit
```

**Best Practices**:
- Commit after every accepted AI change
- Use descriptive commit messages noting it's AI-generated
- Don't wait for "features" - commit incremental changes
- Alternative tools: cc-undo, yoyo for snapshot management

---

### 3. Hooks (Event-Driven Automation)
**Sources**: "A Complete Guide to Claude Code.md", "I was using Claude Code wrong.md"
**Frequency**: 2 sources (but extensively covered)

**Description**:
Programmatic automation triggered at specific points in the development lifecycle. Can run custom scripts before/after tool use, on conversation start/stop, after sub-agent completion, etc.

**Why Valuable**:
- Enables deterministic control over Claude's behavior
- Automates quality checks (linting, type checking, testing)
- Provides notifications and logging
- Can inject additional context automatically
- Replicates features from other tools (e.g., Cursor's auto-lint)

**Available Hook Points**:
- `stop`: When Claude finishes a task
- `post-tool-use`: After any tool execution (can filter by tool type)
- `pre-message`: Before user sends message
- `compress-history`: When conversation history is compressed
- `sub-agent-complete`: After sub-agent finishes

**Example Use Cases**:
1. **Type Checking Hook**: Auto-run TypeScript type checker after file edits
2. **Notification Hook**: Play sound when task completes
3. **Documentation Hook**: Auto-update docs when code changes
4. **Test Hook**: Run tests after code modifications
5. **Critic Agent Hook**: Review code quality after writes

**Exit Codes**:
- `0`: Success, continue
- `2`: Blocking error (Claude must fix before continuing)
- Other: Non-blocking feedback

---

### 4. Parallel Agent Execution
**Sources**: "A Complete Guide to Claude Code.md", "800+ hours.md"
**Frequency**: 2 sources

**Description**:
Running multiple Claude Code instances simultaneously, either on different parts of codebase OR on same feature to pick best implementation. Uses git worktrees for isolation.

**Why Valuable**:
- Dramatically reduces development time
- Allows "best-of-N" approach for complex features
- Isolated environments prevent conflicts
- Can work on frontend/backend simultaneously
- Hedges against AI making mistakes (run 3x, pick best)

**Two Approaches**:

**A. Different Features in Parallel**
- Agent 1: Frontend UI
- Agent 2: Backend API
- Agent 3: Database migrations
- Merge all when complete

**B. Same Feature Multiple Times**
- All agents implement same feature
- Review all implementations
- Pick best one to merge
- Faster than serial retry

**Implementation**:
```bash
# Create worktrees
git worktree add ../project-feature1 feature/feature1
git worktree add ../project-feature2 feature/feature2

# Open Claude in each
cd ../project-feature1 && claude
cd ../project-feature2 && claude
```

**Time Savings**: Feature that would take 30+ min can run 3 parallel instances in 10 min each, pick best

---

### 5. Permission Management Patterns
**Sources**: "A Complete Guide to Claude Code.md", "I was using Claude Code wrong.md"
**Frequency**: 2 sources

**Description**:
Strategic configuration of which commands Claude can run autonomously vs. requiring approval. Critical for balancing automation with safety.

**Why Valuable**:
- Enables autonomous operation while maintaining safety
- Reduces babysitting overhead
- Prevents dangerous operations (file deletion)
- Customizable per project needs

**Best Practices**:

**Always Allow**:
- `grep`, `ls`, `find` (search/navigation)
- `cd`, `mkdir` (directory operations)
- `python`, `node`, `npm` (language commands)
- `git status`, `git diff` (read-only git)

**Never Allow**:
- `rm` (file deletion - always require approval)
- `bash *` (wildcard permissions - too dangerous)
- Deployment commands without review
- Database destructive operations

**YOLO Mode**: 
- Run with `--dangerously-skip-permissions`
- ONLY safe inside dev containers
- Container provides isolation + firewall
- Allows fully autonomous operation

---

### 6. Extract-Then-Answer Pattern
**Sources**: anthropic-prompt-engineering.md
**Frequency**: 1 source (official Anthropic technique)

**Description**:
For long document analysis: (1) First ask Claude to extract relevant word-for-word quotes, (2) Then answer the question based on those quotes.

**Why Valuable**:
- **Significantly improves recall** over long contexts
- Grounds responses in actual text
- Prevents hallucinations
- Creates auditable responses
- **Quantified Impact**: Major accuracy improvement for long documents

**Implementation**:
```
Step 1: "Extract all quotes from the document that discuss [topic]"
Step 2: "Based on the quotes you extracted, answer: [question]"
```

**Variations**:
- Post-hoc verification: Generate answer, then find supporting quotes
- Combined approach: Extract + answer in structured XML response

---

### 7. Document Positioning Optimization
**Sources**: anthropic-prompt-engineering.md
**Frequency**: 1 source (official Anthropic research)

**Description**:
Strategic placement of documents and queries in prompts based on Claude's 200K context window characteristics.

**Why Valuable**:
- **30% accuracy improvement** (per Anthropic internal tests)
- Simple to implement
- Free performance boost
- Especially important for multi-document prompts

**Rules**:
1. **Large documents (20K+ tokens)**: Place at BEGINNING of prompt
2. **Queries**: Place at END after documents
3. **Critical details**: Beginning or end (avoid middle)

**Example Structure**:
```
<documents>
[Large document 1]
[Large document 2]
</documents>

<examples>
[Example Q&As about other sections]
</examples>

<query>
What is [specific question]?
</query>
```

---

### 8. Plan-First Workflow (Spec-Driven Development)
**Sources**: "I was using Claude Code wrong.md", "A Complete Guide.md", Peter Yang tutorial
**Frequency**: 5 sources

**Description**:
ALWAYS use plan mode before execution. Have Claude create detailed spec/plan, review it, align on approach, THEN execute. Save plans to `.claude/tasks/` for tracking.

**Why Valuable**:
- Prevents wasted work from misaligned implementation
- Allows course correction before coding
- Creates documentation of intent
- Similar to Amazon's Kiero workflow (proven at scale)
- Transparency into AI's approach

**Workflow**:
1. **Enter Plan Mode**: `Shift+Tab` twice in Claude Code
2. **Request Plan**: "Create detailed plan for [feature]"
3. **Claude Plans**: Uses limited toolset (web search, research)
4. **Review**: Human reviews plan thoroughly
5. **Align**: Iterate on plan until perfect
6. **Execute**: Switch to normal mode, implement plan
7. **Update**: Claude updates plan as work progresses

**Plan Mode Characteristics**:
- Special system prompt for planning
- Limited tool access (no code editing)
- Focus on research, architecture, task breakdown
- Web search for latest docs/patterns

**Anti-Pattern**: Starting to code immediately without planning

---

### 9. Cost/Token Optimization Patterns
**Sources**: "I was wrong about Claude Code.md"
**Frequency**: 1 source (detailed analysis)

**Description**:
Understanding and managing token consumption for cost efficiency and performance. Claude Code uses 10-100x more tokens than Cursor.

**Why Valuable**:
- Claude Code on Max plan ($200/month): Can use $3000+ in tokens/week
- Understanding usage prevents bill shock
- Strategic model selection saves money
- Cursor optimizes aggressively; Claude doesn't

**Key Insights**:
- **Claude Code strategy**: Not optimized, uses full context, eats cost
- **Cursor strategy**: Heavy compression, minimizes tokens
- **Trade-off**: More tokens = better output quality
- **Sustainability**: Claude's approach may not last as user base grows

**Model Selection**:
- **Opus 4**: Most powerful, highest cost, best for complex tasks
- **Sonnet 4**: Good balance, sometimes better than Opus
- **Auto-select**: Let Claude choose based on task
- Recommendation: Use Opus on Max plan (rarely hit limits)

**Token Tracking**:
- Tools exist to monitor token consumption
- Can reveal actual cost if on API pricing
- Helps identify inefficient patterns

---

### 10. Double-Check / Self-Validation Pattern
**Sources**: "I was wrong about Claude Code.md"
**Frequency**: 1 source

**Description**:
After Claude completes a task, explicitly ask it to verify its own work, look for edge cases, and confirm everything is working.

**Why Valuable**:
- Claude often finds issues it initially missed
- Catches edge cases before testing
- Provides peace of mind
- Acts as first-pass QA
- Minimal time investment for safety boost

**Implementation**:
```
"Can you double-check your work and make sure you didn't break anything else?"

"Try to find edge cases and confirm everything is working correctly."

"Review the code you just wrote for potential issues."
```

**Surprising Finding**: Claude frequently finds and fixes issues on self-review

---

### 11. Multi-Modal Context (Screenshots, Folders, URLs)
**Sources**: "I was wrong about Claude Code.md", multiple tutorials
**Frequency**: 4 sources

**Description**:
Providing context through multiple modalities beyond text: drag screenshots, entire folders from other codebases, and URLs for documentation.

**Why Valuable**:
- Screenshots: Show exact errors, design references, UI issues
- Folders: Cross-codebase context (frontend sees backend)
- URLs: Claude fetches latest docs automatically
- Richer context = better output

**Techniques**:

**Screenshots**:
- Drag error screenshots directly into chat
- Show design mockups for UI implementation
- Display browser rendering issues

**Folders**:
- Drag folders from OTHER codebases
- "Here's the backend structure" while working on frontend
- Claude can make changes to dragged folders if given permission
- Workaround for multi-repo limitation

**URLs**:
- Claude Code has web browser access
- Paste documentation links directly
- OR: "Use the latest Google Calendar API" (Claude searches)
- Reduces manual doc copying

---

### 12. Best-of-N Verification
**Sources**: anthropic-prompt-engineering.md
**Frequency**: 1 source (official technique)

**Description**:
Run the same prompt multiple times, compare outputs for consistency. Inconsistencies may indicate hallucinations or uncertainty.

**Why Valuable**:
- Reveals when Claude is "guessing"
- Higher confidence when outputs align
- Identifies hallucination risk
- Useful for critical code sections

**Implementation**:
1. Run same prompt 3-5 times
2. Compare outputs
3. Consistent = high confidence
4. Inconsistent = investigate further, may need more context

**Best Used For**:
- Complex algorithms
- Security-critical code
- Unfamiliar domains
- When stakes are high

---

### 13. Temperature Adjustment Strategy
**Sources**: anthropic-prompt-engineering.md
**Frequency**: 1 source

**Description**:
Adjusting temperature parameter (0-1) to control output consistency vs. creativity. Lower temperature reduces hallucinations.

**Why Valuable**:
- Direct control over consistency
- Reduces hallucinations for factual tasks
- Increases creativity for brainstorming
- Simple parameter with big impact

**Guidelines**:
- **0-0.3**: Maximum consistency, minimal hallucination (use for code)
- **0.4-0.7**: Balanced (default for most tasks)
- **0.8-1.0**: Maximum creativity (brainstorming, alternatives)

**Recommendation**: Use lower temperatures for production code

---

### 14. Bash Mode & Memory Mode Shortcuts
**Sources**: "I was using Claude Code wrong.md"
**Frequency**: 1 source

**Description**:
Quick keyboard shortcuts for common operations:
- `!` enters bash mode (run commands directly)
- `#` enters memory mode (add to claude.md)

**Why Valuable**:
- Faster than switching contexts
- Commands stay in conversation history (Claude learns from them)
- Memory additions are immediately saved
- Reduces friction in workflow

**Bash Mode (!)**:
```
!npm install package-name
!git status
!python script.py
```
- Executes immediately
- Output added to conversation
- Claude aware of commands run

**Memory Mode (#)**:
```
#I prefer TypeScript strict mode
#Always use Tailwind for styling
```
- Choose project or global scope
- Saved to claude.md instantly
- Persists across sessions

---

### 15. Conversation Portability (Export/Resume)
**Sources**: "I was using Claude Code wrong.md", tutorials
**Frequency**: 2 sources

**Description**:
Export conversation history to move between tools (Claude Code ↔ Cursor ↔ Windsurf), or resume past conversations.

**Why Valuable**:
- Not locked into single tool
- Use Claude for exploration, Cursor for final implementation
- Preserve context across tool switches
- Resume work from days/weeks ago

**Commands**:
- `/export`: Copy full conversation history
- `/resume`: Jump back to past conversation
- Double-tap `ESC`: Revert to earlier point in current conversation

**Workflow**:
1. Explore/plan in Claude Code (unlimited tokens)
2. Export conversation
3. Paste into Cursor for final edits
4. No context loss

**Limitation**: Claude Code doesn't auto-restore file changes when reverting (unlike Cursor)

---

### 16. TDD for Mobile Apps (Build-Market-Iterate)
**Sources**: mobile-app-monetization-guide-transcript.md
**Frequency**: 1 source (extensive coverage)

**Description**:
Distinct pattern for mobile app development focused on rapid iteration and TikTok-first marketing. Build simple, ship fast, market heavily, iterate based on what hits.

**Why Valuable**:
- Mobile apps have different economics than web
- iOS users pay more than Android users
- TikTok drives mobile app discovery
- Volume strategy: ship many apps, one will hit
- Proven examples: Candle (hundreds of thousands users), Jack's app (5K MRR in 15 days)

**Tech Stack**:
- **Frontend**: React Native + Expo
- **Backend**: Convex (real-time database critical for mobile UX)
- **Auth**: Clerk / WorkOS / BetterAuth
- **Platform Focus**: iOS first (paying customers)

**Marketing Strategy**:
1. **TikTok is #1**: Create one video per day minimum
2. **Partner Up**: If you can't create content, find someone who can
3. **Follow Trends**: Build apps around trending behaviors (e.g., "raw dogging boredom" → Timeout app)
4. **Normies ≠ Devs**: Twitter devs won't pay; TikTok normies will

**Development Process**:
1. Watch TikTok for trends (market research)
2. Build simple app matching trend (1-2 days)
3. Create TikTok content showing app
4. Ship to App Store
5. Repeat until one hits

**Key Insight**: "Throw many shots from three-point line. One will hit."

---

### 17. Context Engineering / PRP Framework
**Sources**: "A Complete Guide to Claude Code.md"
**Frequency**: 1 source (extremely detailed)

**Description**:
Structured three-step methodology: (1) Create Initial MD describing feature, (2) Generate comprehensive Product Requirement Prompt (PRP), (3) Execute PRP to build feature. Includes validation gates.

**Why Valuable**:
- Ensures complete context before building
- Produces production-ready code in one shot
- Self-validating with validation gates
- Scales to complex features
- Reproducible methodology

**Three Steps**:

**Step 1: Initial MD**
- Describe feature to build
- List relevant examples
- Reference documentation
- Note special considerations

**Step 2: Generate PRP**
```
/generate-prp path/to/initial.md
```
- Claude researches all references
- Reads examples and docs
- Creates comprehensive prompt with:
  - Core principles
  - Do's and don'ts
  - Step-by-step tasks
  - Validation loops
  - Anti-patterns
  - Final checklist

**Step 3: Execute PRP**
```
/clear  # Start fresh
/execute-prp path/to/generated-prp.md
```
- Claude implements full feature
- Follows validation gates
- Tests itself
- Iterates until passing

**Validation Gates**:
- Specialized sub-agent for testing
- Writes tests autonomously
- Iterates until tests pass
- Ensures production quality

**Success Metrics**: Can build complex features (AI agents, full apps) in single shot

---

### 18. IDE Deep Integration
**Sources**: "I was using Claude Code wrong.md"
**Frequency**: 1 source

**Description**:
Using VSCode extension for deep integration vs. terminal-only usage. Auto-detects current file, selected lines, and provides "Run Claude Code" button.

**Why Valuable**:
- Contextual awareness (knows current file)
- Selection-aware (works on highlighted code)
- Tighter workflow than switching to terminal
- Works across IDEs (VSCode, Cursor, Windsurf)

**Setup**: Install Claude Code extension

**Features**:
- Button in IDE to launch Claude
- Auto-detects open file
- Auto-detects selected lines
- `/ide` command to switch between IDEs

---

### 19. Prompting Keywords (Magic Words)
**Sources**: "A Complete Guide to Claude Code.md"
**Frequency**: 1 source

**Description**:
Specific keywords built into Claude's model that trigger different behaviors: "important", "proactively", "ultra think".

**Why Valuable**:
- Direct access to model capabilities
- Increases effort on critical tasks
- Can dramatically increase token usage for deeper thinking
- Built into training data

**Keywords**:

**"important"**: Flags task as high priority
**"proactively"**: Claude anticipates needs, does extra work
**"ultra think"**: Massively increases reasoning tokens

**Anti-Keywords** (avoid these):
**"production ready"**: Causes over-engineering, adds unnecessary backward compatibility

**Best Practice**: Use sparingly for truly critical sections

---

### 20. Grounding with Citations
**Sources**: anthropic-prompt-engineering.md
**Frequency**: 1 source

**Description**:
Requiring Claude to cite sources for claims, extract quotes, and provide auditable responses. Anthropic has Citations API for enhanced accuracy.

**Why Valuable**:
- Makes responses auditable
- Prevents hallucinations
- **15% accuracy improvement** with Citations API
- Builds trust in AI output
- Essential for critical decisions

**Techniques**:

**Require Citations**:
"Cite your sources for each claim"

**Extract Quotes First**:
"First extract relevant quotes, then answer based on those quotes"

**Post-hoc Verification**:
"Find supporting quotes for your previous answer"

**Citations API**:
- Upload documents directly
- Claude references exact passages
- 15% better than manual citation methods

---

### 21. GitHub CLI Integration (End-to-End Automation)
**Sources**: "A Complete Guide to Claude Code.md", Simon Willison summary
**Frequency**: 2 sources

**Description**:
Using GitHub CLI (`gh`) to enable Claude to read issues, create branches, push code, and create PRs entirely from terminal. Full workflow automation from issue to PR.

**Why Valuable**:
- Complete automation of GitHub workflows
- No context switching to browser
- Claude handles entire issue → fix → PR flow
- Scales to managing multiple issues in parallel

**Setup**:
```bash
gh auth login
gh repo list  # Verify setup
```

**Capabilities**:
- `gh issue view [number]`: Read issue details
- `gh issue create`: Create new issues
- `gh pr create`: Create pull requests
- `gh pr list`: List PRs
- Git operations: branch, commit, push

**Example Workflow**:
```
/fix-github-issue 123

Claude:
1. Reads issue #123 via gh cli
2. Analyzes codebase
3. Implements fix
4. Writes tests
5. Creates branch
6. Commits changes
7. Pushes to GitHub
8. Creates pull request
```

**One-Command Fix**: `/fix-github-issue [number]` does entire flow

---

### 22. Mobile App Niche Selection
**Sources**: mobile-app-monetization-guide-transcript.md
**Frequency**: 1 source

**Description**:
Strategic selection of app niches based on market trends and monetization potential. Couples niche particularly successful.

**Why Valuable**:
- Some niches monetize 10x better than others
- First-mover advantage on trends
- Reduces risk through trend-following

**Hot Niches** (as of content date):
1. **Couples apps**: Proven monetization, large market
2. **Productivity/focus**: "Raw dogging boredom" trend
3. **Wellness/mental health**: Gen Z healing trends
4. **Content creation tools**: TikTok ecosystem

**Selection Criteria**:
- Trending on TikTok (normies talking about it)
- Willingness to pay (iOS users)
- Simple to build (1-2 day MVP)
- Viral potential (shareable on social)

**Validation**: Build in 1-2 days, ship, measure TikTok response

---

### 23. Codebase Onboarding Pattern
**Sources**: "Claude Code is the Best.md", tutorials
**Frequency**: 3 sources

**Description**:
Using Claude to understand and explain existing codebases when joining projects or working with unfamiliar code.

**Why Valuable**:
- Dramatically faster onboarding (hours vs. days)
- Understand architecture without reading all code
- Ask "why" questions about design decisions
- Essential for contractors/consultants

**Questions to Ask**:
```
"Explain how this codebase is structured"
"How does the authentication flow work?"
"What are the key components and their relationships?"
"Explain the data flow from frontend to backend"
"What are the main patterns used here?"
```

**Workflow**:
1. Run `/init` to have Claude scan codebase
2. Ask architecture questions
3. Request flow diagrams (code → explanation)
4. Dive into specific modules
5. Understand dependencies and patterns

**Time Savings**: Hours of reading → 10-15 minutes of Q&A

---

### 24. Validation Gates (Autonomous Testing)
**Sources**: "A Complete Guide to Claude Code.md"
**Frequency**: 1 source (detailed coverage)

**Description**:
Specialized sub-agent that autonomously writes tests, runs them, and iterates until all tests pass. Part of PRP framework but can be used standalone.

**Why Valuable**:
- Autonomous quality assurance
- Catches bugs before manual testing
- Ensures production readiness
- Frees developer from writing tests
- Iterates until confident

**How It Works**:
1. Main agent completes feature
2. Validation gates sub-agent activates
3. Sub-agent:
   - Writes comprehensive tests
   - Runs tests
   - Fixes failing tests
   - Repeats until all pass
4. Reports back to main agent

**Configuration**:
- Special system prompt for testing
- Access to testing tools
- Isolated context window
- Autonomous operation mode

**Integration**: Trigger with "validation gate" keyword in prompts

---

### 25. Type Checking Hook (Proactive Linting)
**Sources**: "I was using Claude Code wrong.md"
**Frequency**: 1 source

**Description**:
Post-tool-use hook that automatically runs TypeScript type checker after Claude edits/creates files. Returns blocking errors to Claude for immediate fixing.

**Why Valuable**:
- Replicates Cursor's auto-lint feature
- Catches type errors before running code
- Proactive fixing vs. reactive debugging
- Maintains type safety
- Zero manual effort

**Implementation**:
```python
# .claude/hooks/type_check.py
import subprocess, json, sys

data = json.loads(sys.stdin.read())
file_path = data['tool_input']['path']

if file_path.endswith(('.ts', '.tsx')):
    result = subprocess.run(['tsc', '--noEmit'], capture_output=True)
    if result.returncode != 0:
        print(result.stderr.decode(), file=sys.stderr)
        sys.exit(2)  # Exit code 2 = blocking error
```

**Hook Configuration**:
```json
{
  "hooks": [{
    "event": "post-tool-use",
    "matcher": "edit|multi_file_edit|write_to_file",
    "command": "python .claude/hooks/type_check.py"
  }]
}
```

**Exit Code 2**: Blocking error - Claude must fix before continuing

---

### 26. Web Search for Latest Docs
**Sources**: "I was wrong about Claude Code.md", tutorials
**Frequency**: 3 sources

**Description**:
Claude Code has built-in web browser access. Can search for and read latest documentation without manual copy-paste.

**Why Valuable**:
- Always uses latest docs (not training cutoff)
- Reduces manual documentation lookup
- Works with new libraries/APIs
- Can search when you don't have exact URL

**Usage**:

**Direct URL**:
```
"Use the API docs at [URL]"
```
Claude fetches and reads

**Search**:
```
"Make sure to use the latest Google Calendar API"
```
Claude searches, finds docs, reads them

**Best For**:
- New/updated libraries
- API integrations
- Framework updates
- Unfamiliar technologies

---

### 27. Task-Based vs. Role-Based Sub-Agents
**Sources**: "800+ hours of Learning.md"
**Frequency**: 1 source (important anti-pattern)

**Description**:
**ANTI-PATTERN**: Assigning sub-agents roles (frontend dev, PM, designer).
**BEST PRACTICE**: Assign sub-agents specific tasks (optimize code, gather research, review UI).

**Why Valuable**:
- Role-based agents underperform vs. task-based
- Prevents wasted time on ineffective patterns
- Learned from 800+ hours of trial/error
- Goes against common intuition

**Don't Do This** (Role-Based):
```
Sub-agent: "You are a senior frontend developer"
Sub-agent: "You are a product manager"
Sub-agent: "You are a UI/UX designer"
```
Results: Poor quality, doesn't work like human roles

**Do This Instead** (Task-Based):
```
Sub-agent: "Clean up and optimize the code just written"
Sub-agent: "Generate documentation for new API endpoints"
Sub-agent: "Gather research on best practices for [topic]"
Sub-agent: "Review UI components using Playwright MCP"
```
Results: High quality, specific, measurable

**Key Insight**: Current AI agents excel at tasks, not roles

---

## PATTERN COVERAGE ANALYSIS

### Well-Covered Areas
✅ **Core Prompting**: Clear instructions, step-by-step, examples - extensively documented
✅ **Tool Integration**: MCP servers mentioned across many sources
✅ **Plan Mode**: Multiple sources emphasize planning-first approach
✅ **Context Management**: Claude.md usage well understood

### Significant Gaps

❌ **Workflow Automation** (HIGH PRIORITY)
- Hooks barely documented but extremely powerful
- GitHub CLI integration missing
- Event-driven patterns absent

❌ **Quality Assurance Patterns** (HIGH PRIORITY)
- Validation gates not documented
- Type checking automation missing
- Double-check patterns absent
- Best-of-N verification not covered

❌ **Performance Optimization** (MEDIUM PRIORITY)
- Document positioning (30% improvement!) not documented
- Token management patterns missing
- Cost optimization absent
- Temperature strategies not covered

❌ **Mobile-Specific Development** (MEDIUM PRIORITY)
- Mobile app tech stacks not covered
- TikTok-first marketing missing
- Niche selection patterns absent
- Monetization strategies not documented

❌ **Advanced Techniques** (MEDIUM PRIORITY)
- Parallel agent execution missing
- Git worktree patterns absent
- Context engineering/PRP not documented
- Conversation portability not covered

❌ **Grounding & Accuracy** (MEDIUM PRIORITY)
- Extract-then-answer pattern missing
- Citations strategies not documented
- Best-of-N verification absent
- Explicit uncertainty permission not covered

---

## QUANTIFIED IMPACTS

Several patterns have measured performance improvements:

1. **Document Positioning**: **+30% accuracy** (Anthropic research)
2. **Extract-Then-Answer**: **Significant recall improvement** for long docs
3. **Citations API**: **+15% citation accuracy** vs. manual methods
4. **Few-Shot Examples**: **+20% accuracy** (Fortune 500 case study)
5. **Plan-First Workflow**: Prevents wasted work, reduces iteration cycles

---

## RECOMMENDATIONS

### Immediate Documentation Priorities

**Tier 1 - High Impact, Not Documented**:
1. **Hooks System** - Event-driven automation
2. **Validation Gates** - Autonomous testing pattern
3. **GitHub CLI Integration** - End-to-end automation
4. **Document Positioning** - 30% accuracy boost
5. **Extract-Then-Answer** - Grounding pattern

**Tier 2 - Valuable, Currently Missing**:
6. **Parallel Agent Execution** - Worktree workflows
7. **Context Engineering/PRP** - Structured methodology
8. **Permission Management** - Safety patterns
9. **Git Checkpointing** - AI-specific workflow
10. **Mobile App Development** - Complete stack + marketing

**Tier 3 - Nice to Have**:
11. **Conversation Portability** - Export/resume patterns
12. **Prompting Keywords** - Magic words
13. **Type Checking Hooks** - Specific automation
14. **Cost/Token Optimization** - Financial management
15. **Onboarding Patterns** - Codebase understanding

### Pattern Gaps by Category

**Automation & Workflow** (5 patterns):
- Hooks, GitHub CLI, Bash/Memory shortcuts, Conversation portability, IDE integration

**Quality & Testing** (5 patterns):
- Validation gates, Type checking, Double-check, Best-of-N, Temperature adjustment

**Performance** (4 patterns):
- Document positioning, Token optimization, Extract-then-answer, Cost management

**Mobile/App Dev** (3 patterns):
- TDD cycle, Niche selection, Tech stack patterns

**Advanced Techniques** (7 patterns):
- Parallel agents, Context engineering, Git checkpointing, Permission management, XML structuring, Grounding, Anti-patterns

**Context & Discovery** (3 patterns):
- Multi-modal context, Web search, Onboarding, Prompting keywords

---

## METHODOLOGY NOTES

**Sources Analyzed**:
1. anthropic-prompt-engineering.md (official docs)
2. armin-ronacher-agentic-coding-summary.md
3. simon-willison-github-actions-summary.md
4. peter-yang-movie-app-summary.md
5. mobile-app-monetization-guide-transcript.md
6. top-tutorials.json
7. I was wrong about Claude Code UPDATED AI workflow.md
8. Claude Code Is The Best AI Coding Agent.md
9. A Complete Guide to Claude Code Here are ALL the.md
10. 7wGE I was using Claude Code wrong... The Ultimate Work.md
11. 800+ hours of Learning Claude Code in 8 minutes 2.md

**Analysis Approach**:
- Read all 11 files completely
- Identified techniques and patterns
- Cross-referenced against existing documentation
- Noted frequency across sources
- Extracted quantified benefits where available
- Categorized by type and priority

**Pattern Validation**:
- Patterns mentioned in multiple sources weighted higher
- Official Anthropic guidance prioritized
- Quantified results noted separately
- Anti-patterns explicitly flagged

---

## NEXT STEPS

1. **Review this index** with team/community
2. **Prioritize patterns** for documentation
3. **Create pattern documents** using PATTERN_TEMPLATE.md
4. **Add examples** from source materials
5. **Test patterns** in real projects
6. **Measure impact** of documented patterns
7. **Iterate** based on community feedback

---

**Document Status**: Draft v1.0
**Author**: Pattern Analysis Agent
**Review Status**: Pending
**Last Updated**: 2024-11-14
