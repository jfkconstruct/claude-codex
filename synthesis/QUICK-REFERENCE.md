# Claude Code Quick Reference Cheat Sheet

**Version**: 1.0 | **Date**: 2025-11-14 | **Print**: 2 pages

---

## Top 10 Prompting Rules

| # | Rule | Impact | Example |
|---|------|--------|---------|
| **1** | **Documents First, Query Last** | +30% accuracy | `<documents>[files]</documents><query>[question]</query>` |
| **2** | **Provide 3-5 Examples** | +20% accuracy | Show input/output pairs, include edge cases |
| **3** | **Use Chain-of-Thought** | +20% accuracy | "Think step-by-step" or `<thinking>...</thinking>` |
| **4** | **Be Explicit, Not Vague** | Critical | "Add validation: email (valid format), min 20 chars" NOT "add validation" |
| **5** | **Use Plan Mode First** | Prevents waste | `Shift+Tab` before implementing complex features |
| **6** | **XML Tags for Structure** | Clarity | `<context>`, `<task>`, `<examples>`, `<constraints>`, `<format>` |
| **7** | **Temperature 0.0-0.2 for Code** | Consistency | Lower temp = less hallucination, more deterministic |
| **8** | **Commit Before & After** | Safety net | `git commit -m "Before Claude"` → work → `git commit -m "AI: [task]"` |
| **9** | **Self-Validation** | Quality | "Double-check your work, look for edge cases and bugs" |
| **10** | **Start Simple, Iterate** | Success | Break into small steps, verify each before next |

---

## Model Selection Guide

| Task Type | Model | Why |
|-----------|-------|-----|
| Feature implementation (known patterns) | **Sonnet** | Fast, cost-effective, 80% of tasks |
| Bug fixes (clear repro) | **Sonnet** | Deterministic debugging |
| Refactoring | **Sonnet** | Pattern-based, straightforward |
| Documentation | **Sonnet** | Speed matters more than depth |
| Tests | **Sonnet** | Consistent, thorough coverage |
| **Architecture decisions** | **Opus** | Complex reasoning needed |
| **Security reviews** | **Opus** | Critical accuracy required |
| **Complex algorithms** | **Opus** | Deep problem-solving |
| **Performance optimization** | **Opus** | Multi-dimensional analysis |
| **Debugging subtle bugs** | **Opus** | Advanced reasoning |

**Rule of Thumb**: Sonnet first. If stuck after 2 tries, switch to Opus.

---

## Common Parameters

| Parameter | Range | Default | Best for Code |
|-----------|-------|---------|---------------|
| **temperature** | 0.0 - 1.0 | 0.5 | **0.0 - 0.2** (consistency) |
| **max_tokens** | 1 - 4096 | Varies | 2048-4096 (complete responses) |
| **top_p** | 0.0 - 1.0 | 0.9 | 0.7-0.8 (deterministic) |

**For Production Code**: `temperature=0.0, top_p=0.8`

---

## Essential Commands

| Command | Purpose | Usage |
|---------|---------|-------|
| `/init` | Initialize project | Creates `.claude` directory, scans codebase |
| `/clear` | Start fresh | New conversation, clear context |
| `/export` | Export conversation | Copy for portability (Claude → Cursor) |
| `/resume` | Resume past session | Jump back to previous conversation |
| `/help` | Show commands | List all available commands |
| `Shift+Tab` | Toggle plan mode | Plan before executing |
| `!` | Bash mode | Run commands directly: `!npm install` |
| `#` | Memory mode | Add to claude.md: `#Use strict TypeScript` |
| `Esc Esc` | Revert conversation | Double-tap to go back |

---

## File Structure Quick Setup

```
.claude/
├── claude.md                  # Persistent project memory
├── commands/                  # Custom slash commands
│   ├── add-feature.md
│   ├── review-code.md
│   └── fix-eslint.md
├── subagents/                 # Specialized agents (advanced)
│   ├── backend-expert.md
│   ├── frontend-expert.md
│   └── testing-expert.md
└── mcp_settings.json          # MCP server config
```

**Minimal `.claude.md` Template**:
```markdown
# Project: [Name]

## Tech Stack
- [Framework, libraries, tools]

## Coding Standards
- [Style guide, patterns, naming]

## Before Every Task
1. Read relevant files first
2. Use plan mode for complex tasks
3. Ask clarifying questions
4. Follow existing patterns
```

---

## Essential MCP Servers (Priority Order)

| MCP | Purpose | Install |
|-----|---------|---------|
| **1. Context7** | Latest docs (Priority #1) | `npm install -g @context7/mcp-server` |
| **2. Supabase** | Database queries | `npm install -g @supabase/mcp-server` |
| **3. Playwright** | Browser automation | Uses `npx`, no install needed |

**Config** (`.claude/mcp_settings.json`):
```json
{
  "mcpServers": {
    "context7": {
      "command": "context7-mcp",
      "args": ["--libraries", "nextjs,react,typescript,tailwindcss"]
    }
  }
}
```

---

## Cost Optimization Tips

| Strategy | Savings | How |
|----------|---------|-----|
| **Sonnet over Opus** | 40-50% | Use Sonnet default, Opus only for complex tasks |
| **Sub-agents** | 33% | Isolated contexts prevent pollution |
| **Clear prompts** | 66% | Reduce iterations, be explicit upfront |
| **Context cleanup** | 15-20% | `/clear` between unrelated tasks |
| **Plan mode** | 30-50% | Cheap planning prevents expensive rework |

**Token Budget Alert**: Set daily limit alerts at 80% threshold.

---

## Common Error Codes & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `RATE_LIMIT_EXCEEDED` | Too many requests | Exponential backoff: 2s, 4s, 8s, 16s |
| `CONTEXT_LENGTH_EXCEEDED` | Too much context | Use sub-agents, `/clear`, or shorten prompt |
| `INVALID_API_KEY` | Auth failure | Check `ANTHROPIC_API_KEY` environment variable |
| `MCP_SERVER_NOT_FOUND` | MCP not installed | Verify install: `which [mcp-command]` |
| `TIMEOUT` | Response too slow | Increase timeout, optimize query, use streaming |
| `CONTENT_FILTER` | Blocked content | Rephrase prompt, avoid sensitive topics |

---

## Security Checklist (OWASP Top 10)

```markdown
- [ ] SQL Injection: Queries parameterized? No string interpolation?
- [ ] XSS: User input sanitized? Avoid dangerouslySetInnerHTML?
- [ ] Authentication: Sessions server-side? No user-provided auth?
- [ ] Secrets: Environment variables? Not hardcoded?
- [ ] Authorization: RBAC enforced? Access controls checked?
- [ ] CSRF: POST/PUT/DELETE protected with tokens?
- [ ] Rate Limiting: Auth endpoints rate-limited?
- [ ] Input Validation: All user input validated (zod, joi)?
- [ ] Error Messages: No stack traces exposed?
- [ ] Dependencies: npm audit clean?
```

**Command**: `/review-security` (create custom command)

---

## Debugging Workflow

```
1. Reproduce Issue
   ↓
2. Ask Claude to Analyze Step-by-Step
   "Think step-by-step: What might cause [error]?"
   ↓
3. Claude Proposes Solutions
   ↓
4. Implement Fix
   ↓
5. Self-Validation
   "Double-check: Did this fix the root cause? Any edge cases?"
   ↓
6. Test Thoroughly
   ↓
7. Git Commit
```

---

## Testing Requirements

| Coverage | Requirement |
|----------|-------------|
| **Minimum** | 80% for new code |
| **Critical paths** | 100% + E2E tests |
| **Utility functions** | 100% |

**Test Pyramid**:
- **70%** Unit tests (fast, isolated)
- **20%** Integration tests (API + DB)
- **10%** E2E tests (critical user flows)

---

## Git Workflow for AI Development

```bash
# 1. Before Claude works
git add . && git commit -m "Before: [task]"

# 2. Claude generates code
# [Work happens...]

# 3. Review changes
git diff HEAD

# 4a. Accept changes
git add . && git commit -m "AI: [description]"

# 4b. Reject changes
git reset --hard HEAD^  # Discard everything
```

**Granular Commits**: One logical change per commit for easy rollback.

---

## Performance Benchmarks

| Metric | Target | Action if Exceeded |
|--------|--------|-------------------|
| **API P95 latency** | < 200ms | Add caching, optimize queries |
| **Page load** | < 2s | Code splitting, lazy loading |
| **Bundle size** | < 500KB | Tree shaking, analyze bundle |
| **Test suite** | < 30s | Parallel execution, mock optimization |

---

## Quick Wins

**5-Minute Improvements**:
1. ✅ Install Context7 MCP (always up-to-date docs)
2. ✅ Create basic `.claude.md` (persistent context)
3. ✅ Set temperature to 0.0 for code (consistency)
4. ✅ Use plan mode (Shift+Tab) for next task
5. ✅ Add git pre-commit checkpoint

**30-Minute Improvements**:
1. ✅ Create 3 custom commands for repetitive tasks
2. ✅ Set up basic monitoring dashboard
3. ✅ Configure security review command
4. ✅ Implement validation gates (auto-testing)
5. ✅ Establish sub-agent structure

---

## Prompt Template (Copy-Paste)

```markdown
<context>
Tech stack: [Framework, libraries, database]
Relevant files: [File paths]
</context>

<task>
[Clear, specific task description]

Requirements:
- [Requirement 1]
- [Requirement 2]
</task>

<examples>
Example 1: [Show input/output]
Example 2: [Show edge case]
</examples>

<constraints>
- [What to follow]
- [What to avoid]
</constraints>

<format>
Please provide:
1. [What you want to see]
2. [How to structure response]
</format>
```

---

## Emergency Rollback

```bash
# If Claude made breaking changes:
git log --oneline -5           # Find last good commit
git reset --hard [commit-sha]  # Hard reset
git push --force origin [branch]  # If already pushed

# If you just need to undo last commit:
git reset --hard HEAD^

# If you want to keep changes but uncommit:
git reset --soft HEAD^
```

---

## Resources

**Official**:
- Anthropic Docs: docs.anthropic.com
- API Reference: docs.anthropic.com/claude/reference
- Console: console.anthropic.com

**Community**:
- GitHub Discussions: github.com/anthropics/claude-code
- Pattern Library: [This repository]

**Support**:
- Issues: github.com/anthropics/claude-code/issues
- Status: status.anthropic.com

---

## Success Metrics

**Week 1 Goals**:
- [ ] 3+ successful features with Claude
- [ ] `.claude.md` created and maintained
- [ ] Context7 MCP installed and used
- [ ] Plan mode used consistently

**Month 1 Goals**:
- [ ] 10+ custom commands created
- [ ] Sub-agents configured
- [ ] Monitoring dashboard active
- [ ] Team workflow established

**Efficiency Targets**:
- 50% faster feature development
- 80%+ test coverage maintained
- Zero security vulnerabilities in AI code
- 90%+ code review approval rate

---

**Remember**: AI generates code, humans own it. Always review, test, and validate.

---

**Print**: This cheat sheet is designed to fit on 2 pages when printed. Keep it handy!
