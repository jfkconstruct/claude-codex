---
title: Claude Coding Patterns - Complete Index
last_updated: 2024-11-14
total_patterns: 20
status: Active
---

# Claude Coding Patterns - Complete Index

This directory contains comprehensive, production-ready patterns for coding with Claude. All patterns follow a standardized template with code examples, metrics, and real-world case studies.

**Total Patterns**: 20 documented patterns
**Last Updated**: November 14, 2024
**Template Version**: 1.0

---

## Quick Navigation

- [Context Management](#context-management) (3 patterns)
- [Prompting Techniques](#prompting-techniques) (10 patterns)
- [Architecture](#architecture) (2 patterns)
- [Workflow](#workflow) (1 pattern)
- [Tooling](#tooling) (2 patterns)
- [Optimization](#optimization) (2 patterns)
- [Quality Assurance](#quality-assurance) (1 pattern)

---

## Context Management

Patterns for managing how Claude understands and processes your codebase.

### 1. **Context Management & Codebase Understanding** ⭐ CRITICAL
**File**: [`context-management.md`](./context-management.md)
**Impact**: High (30% accuracy improvement)
**Difficulty**: Intermediate
**Sources**: 7+ sources

Strategic document positioning and context optimization for Claude to understand large codebases.

**Key Techniques**:
- Document positioning (30% accuracy improvement)
- MCP servers (Context7, Serena)
- XML structuring
- .claudeignore configuration

**When to Use**: Large codebases (>10K lines), unfamiliar projects, complex architectures

---

### 2. **Claude.md / Persistent Memory** ⭐ CRITICAL
**File**: [`claude-md-persistent-memory.md`](./claude-md-persistent-memory.md)
**Impact**: High (5-10 min saved per session)
**Difficulty**: Beginner
**Sources**: 5 sources

Store project context, conventions, and patterns that Claude automatically reads in every session.

**Key Techniques**:
- Tech stack documentation
- Coding conventions with examples
- Project-specific patterns
- Anti-patterns and constraints

**When to Use**: All projects, especially team projects and long-running codebases

---

### 3. **Plan Mode / Spec-Driven Development** ⭐ CRITICAL
**File**: [`plan-mode-spec-driven-development.md`](./plan-mode-spec-driven-development.md)
**Impact**: High (50-80% reduction in rework)
**Difficulty**: Beginner
**Sources**: 5 sources

Separate planning from execution using Shift+Tab to create detailed specifications before coding.

**Key Techniques**:
- Shift+Tab workflow
- Clarifying questions
- Iterative plan refinement
- Fix plan errors (cheap) vs. code errors (expensive)

**When to Use**: New features (3+ files), architectural decisions, security-critical tasks

---

## Prompting Techniques

Fundamental patterns for how you communicate with Claude.

### 4. **Clear, Explicit, Direct Instructions** ⭐ CRITICAL
**File**: [`prompting/clear-instructions.md`](./prompting/clear-instructions.md)
**Impact**: High (foundation of all prompting)
**Difficulty**: Beginner
**Sources**: 4+ sources (foundational)

State exactly what you want in simple, unambiguous language. Treat Claude like an intern on their first day.

**Key Techniques**:
- Explicit context provision
- Specific requirements
- Clear boundaries
- Acceptance criteria

**When to Use**: All tasks, especially complex requirements

---

### 5. **Step-by-Step Thinking / Chain of Thought** ⭐ CRITICAL
**File**: [`prompting/step-by-step-thinking.md`](./prompting/step-by-step-thinking.md)
**Impact**: High (20% accuracy improvement)
**Difficulty**: Beginner
**Sources**: 5 sources

Explicitly instruct Claude to show its reasoning and break down complex problems.

**Key Techniques**:
- "think step by step"
- "show your work"
- "ultrathink" keyword
- `<thinking>` tags

**When to Use**: Complex tasks, debugging, learning, architecture decisions

---

### 6. **Few-Shot Examples**
**File**: [`prompting/few-shot-examples.md`](./prompting/few-shot-examples.md)
**Impact**: High (20% accuracy improvement)
**Difficulty**: Beginner
**Sources**: 3 sources (including Anthropic official)

Provide 3-5 diverse examples showing exact input/output pattern you want.

**Key Techniques**:
- 3-5 diverse examples
- Edge case demonstrations
- Format consistency
- Input/output pairs

**When to Use**: Format consistency, edge cases, complex patterns

---

### 7. **Prefilling**
**File**: [`prompting/prefilling.md`](./prompting/prefilling.md)
**Impact**: High (near 100% format consistency)
**Difficulty**: Intermediate
**Sources**: Anthropic official documentation

Force specific output formats by setting the first few words of Claude's response.

**Key Techniques**:
- JSON mode (start with `{`)
- XML mode (start with `<`)
- Character voice enforcement
- Preamble elimination

**When to Use**: API integrations, structured output, consistent formatting

---

### 8. **Hallucination Prevention** ⚠️ CRITICAL FOR PRODUCTION
**File**: [`prompting/hallucination-prevention.md`](./prompting/hallucination-prevention.md)
**Impact**: High (15% citation accuracy improvement)
**Difficulty**: Intermediate
**Sources**: Anthropic official documentation

Prevent fabricated information through citations, source restrictions, and verification.

**Key Techniques**:
- Permission to say "I don't know"
- Restrict to provided sources
- Require citations
- Post-hoc verification
- Temperature control (0.0-0.3)

**When to Use**: Customer support, medical/legal/financial, user-facing content

---

### 9. **System Prompts**
**File**: [`prompting/system-prompts.md`](./prompting/system-prompts.md)
**Impact**: High (consistency across sessions)
**Difficulty**: Beginner
**Sources**: Anthropic official documentation

Establish persistent role, expertise, and behavioral constraints separate from user messages.

**Key Techniques**:
- Role definition
- Expertise specification
- Tone setting
- Boundary establishment

**When to Use**: Chatbots, multi-turn conversations, specialized tasks

---

### 10. **Prompt Chaining**
**File**: [`prompting/prompt-chaining.md`](./prompting/prompt-chaining.md)
**Impact**: High (20-40% quality improvement)
**Difficulty**: Advanced
**Sources**: Anthropic official documentation

Break complex tasks into sequential prompts with validation gates between steps.

**Key Techniques**:
- Sequential workflows
- State management
- Validation gates
- Modular prompt design

**When to Use**: Complex workflows, large documents, validation requirements

---

### 11. **Affirmative Instructions**
**File**: [`prompting/affirmative-instructions.md`](./prompting/affirmative-instructions.md)
**Impact**: Medium (improved compliance)
**Difficulty**: Beginner
**Sources**: Anthropic official documentation

Tell Claude what TO do, not what NOT to do (positive framing).

**Key Techniques**:
- Positive framing
- Action-oriented guidance
- Concrete specifications
- Avoid prohibitions

**When to Use**: All prompts, especially safety-critical scenarios

---

### 12. **Example-First Documentation**
**File**: [`prompting/example-first-documentation.md`](./prompting/example-first-documentation.md)
**Impact**: High (30% accuracy improvement)
**Difficulty**: Intermediate
**Sources**: Anthropic official documentation

Provide example Q&A pairs before asking questions to improve documentation analysis.

**Key Techniques**:
- 2-4 example Q&A pairs
- Format demonstration
- Citation patterns
- Document-first positioning

**When to Use**: Learning new libraries, documentation chatbots, technical Q&A

---

### 13. **Anthropic Official Patterns** 📚 REFERENCE
**File**: [`prompting/anthropic-official.md`](./prompting/anthropic-official.md)
**Type**: Source Document
**Patterns**: 11 patterns documented

Raw extraction from Anthropic's official prompt engineering documentation. All patterns from this document have been extracted into individual pattern files (see patterns 4-12 above).

---

## Architecture

Patterns for structuring complex systems with Claude.

### 14. **Sub-Agents / Parallel Task Delegation**
**File**: [`architecture/sub-agents.md`](./architecture/sub-agents.md)
**Impact**: High (10x faster on multi-part tasks)
**Difficulty**: Advanced
**Sources**: 5 sources

Define specialized sub-agents with focused responsibilities for parallel execution.

**Key Techniques**:
- Domain-isolated sub-agents
- Parallel execution
- Specialized expertise
- Clean context boundaries

**When to Use**: Complex projects, parallel tasks, domain separation

---

### 15. **GitHub Examples (Agency Swarm)** 📚 REFERENCE
**File**: [`architecture/github-examples.md`](./architecture/github-examples.md)
**Type**: Source Document
**Patterns**: 10 architecture patterns

Production patterns extracted from the Agency Swarm codebase with 30+ code snippets.

---

## Workflow

Patterns for development processes and methodologies.

*See Pattern #3: Plan Mode / Spec-Driven Development above*

---

## Tooling

Patterns for extending Claude's capabilities with custom tools.

### 16. **Custom Commands / Reusable Workflows**
**File**: [`tooling/custom-commands.md`](./tooling/custom-commands.md)
**Impact**: High (60-80% time savings)
**Difficulty**: Intermediate
**Sources**: 3 sources

Create slash commands for repetitive tasks and multi-step workflows.

**Key Techniques**:
- `.claude/commands/` directory
- Multi-step workflow automation
- Team standardization
- Executable documentation

**When to Use**: Repetitive tasks, team sharing, standardized workflows

---

### 17. **MCP Servers / External Tool Integration**
**File**: [`tooling/mcp-servers.md`](./tooling/mcp-servers.md)
**Impact**: High (always-current docs, database access)
**Difficulty**: Intermediate
**Sources**: 3 sources

Extend Claude with Model Context Protocol servers for documentation, databases, browsers, and more.

**Key Techniques**:
- Context7 (live documentation)
- Serena (semantic code search)
- Filesystem, Browser, Database access
- `.claude/mcp_settings.json` configuration

**When to Use**: Documentation needs, database access, external integrations

---

## Optimization

Patterns for improving performance and reducing costs.

### 18. **Token Efficiency & Cost Optimization** 💰 COST SAVINGS
**File**: [`optimization/token-efficiency.md`](./optimization/token-efficiency.md)
**Impact**: High (60-90% cost reduction)
**Difficulty**: Intermediate
**Sources**: Web research (6+ sources)

Reduce API costs through caching, compression, batching, and model selection.

**Key Techniques**:
- Prompt caching (90% savings)
- Compression (20-76% reduction)
- Batching (30% savings)
- Model selection (4-60x cheaper)
- Output control

**When to Use**: API costs >$100/month, large contexts, batch operations

---

### 19. **Streaming Responses & Latency Optimization** ⚡ UX CRITICAL
**File**: [`optimization/streaming-patterns.md`](./optimization/streaming-patterns.md)
**Impact**: High (85% perceived latency reduction)
**Difficulty**: Intermediate
**Sources**: Web research (6+ sources)

Improve perceived responsiveness through progressive streaming using Server-Sent Events.

**Key Techniques**:
- Server-Sent Events (SSE)
- Time-to-first-token (TTFT) optimization
- Progressive rendering
- Error handling and retry logic

**When to Use**: Interactive chat, content generation, user-facing applications

---

## Quality Assurance

Patterns for ensuring code quality and correctness.

### 20. **Code Review & Validation**
**File**: [`quality-assurance/code-review.md`](./quality-assurance/code-review.md)
**Impact**: High (prevents vulnerabilities)
**Difficulty**: Beginner
**Sources**: 3 sources

Always review Claude's code output with systematic checklists and self-review.

**Key Techniques**:
- Claude self-review
- Comprehensive checklist (security, errors, validation, etc.)
- Custom command: `/review-code`
- Human final approval

**When to Use**: Production code, security-critical, before deployment

---

## Pattern Template

**File**: [`PATTERN_TEMPLATE.md`](./PATTERN_TEMPLATE.md)

Standardized template for documenting new patterns. Use this when creating additional patterns.

**Sections Include**:
- Overview and TL;DR
- Problem/Solution/Implementation
- When to Use / When NOT to Use
- Complete code examples
- Common pitfalls and best practices
- Real-world examples
- Quick reference and FAQ
- Sources and metrics

---

## Usage Guide

### Getting Started

**1. Start with Critical Patterns** (⭐):
- Context Management
- Claude.md
- Plan Mode
- Clear Instructions
- Step-by-Step Thinking

**2. Add Domain-Specific Patterns**:
- Hallucination Prevention (if factual accuracy matters)
- Token Efficiency (if API costs matter)
- Streaming (if UX matters)
- Sub-Agents (if complexity is high)

**3. Advanced Optimization**:
- Custom Commands (for team standardization)
- MCP Servers (for external integrations)
- Prompt Chaining (for complex workflows)

### Pattern Selection Matrix

| Use Case | Recommended Patterns |
|----------|---------------------|
| **New Project Setup** | Claude.md, Context Management, Plan Mode |
| **Team Collaboration** | Claude.md, Custom Commands, Code Review |
| **Large Codebase** | Context Management, MCP Servers (Serena), Sub-Agents |
| **Cost-Conscious** | Token Efficiency, Model Selection, Batching |
| **User-Facing Product** | Streaming, Hallucination Prevention, System Prompts |
| **Learning/Exploration** | Step-by-Step Thinking, Example-First Documentation |
| **Production Deployment** | Code Review, Hallucination Prevention, Testing |
| **Complex Workflows** | Plan Mode, Prompt Chaining, Sub-Agents |

---

## Contributing New Patterns

When discovering new patterns:

1. **Use the Template**: Start with `PATTERN_TEMPLATE.md`
2. **Include Metrics**: Quantitative improvements if available
3. **Provide Examples**: Complete, working code examples
4. **Show Real Usage**: Case studies or production examples
5. **Cite Sources**: Properly attribute where patterns came from
6. **Follow Structure**: Maintain consistency with existing patterns

---

## Pattern Statistics

### By Category
- **Prompting Techniques**: 10 patterns (50%)
- **Context Management**: 3 patterns (15%)
- **Optimization**: 2 patterns (10%)
- **Architecture**: 2 patterns (10%)
- **Tooling**: 2 patterns (10%)
- **Quality Assurance**: 1 pattern (5%)

### By Difficulty
- **Beginner**: 9 patterns (45%)
- **Intermediate**: 9 patterns (45%)
- **Advanced**: 2 patterns (10%)

### By Impact
- **High Impact**: 18 patterns (90%)
- **Medium Impact**: 2 patterns (10%)

### By Source
- **Anthropic Official**: 7 patterns
- **Community Synthesis**: 7 patterns
- **Web Research**: 2 patterns
- **Production Codebases**: 2 patterns
- **Multi-Source**: 2 patterns

---

## Related Resources

### Synthesis Documents
- [`synthesis/top-10-practices.md`](../synthesis/top-10-practices.md) - Original top 10 synthesis
- [`synthesis/research-priorities.md`](../synthesis/research-priorities.md) - Gap analysis and roadmap

### Source Materials
- [`sources/docs/`](../sources/docs/) - Official documentation
- [`sources/youtube/`](../sources/youtube/) - Tutorial transcripts
- [`patterns/architecture/github-examples.md`](./architecture/github-examples.md) - Production code patterns

---

## Version History

| Version | Date | Patterns | Changes |
|---------|------|----------|---------|
| 1.0 | 2024-11-14 | 20 | Initial comprehensive index |

---

## Maintenance

**Last Review**: 2024-11-14
**Next Review**: 2024-12-14
**Maintainer**: Claude Coding Knowledge Base Project

**To Add New Pattern**:
1. Create pattern using `PATTERN_TEMPLATE.md`
2. Update this index with new entry
3. Update pattern statistics
4. Update version history
5. Commit with descriptive message

---

**Index Complete** | 20 Patterns Documented | Production-Ready
