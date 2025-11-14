---
title: Pattern Relationships & Ecosystem Map
last_updated: 2024-11-14
total_patterns: 20
purpose: Understanding how patterns work together
---

# Pattern Relationships & Ecosystem Map

This document maps the relationships, dependencies, and synergies between all 20 documented Claude coding patterns.

**Purpose**: Help you understand which patterns work together, which are alternatives, and how to build effective pattern stacks for your use case.

---

## Executive Summary

### Key Insights

1. **3-Pattern Foundation**: Context Management + Claude.md + Clear Instructions form the essential baseline
2. **Optimization Multipliers**: Token Efficiency + Streaming combine for cost-effective UX
3. **Quality Stack**: Step-by-Step + Code Review + Hallucination Prevention for production
4. **Advanced Automation**: Sub-Agents + Custom Commands + MCP Servers for complex workflows

### Most Powerful Combinations

| Pattern Stack | Use Case | Combined Impact |
|---------------|----------|-----------------|
| Context + Claude.md + Plan Mode | New features | 50-80% fewer iterations |
| Few-Shot + Prefilling + System Prompts | API integrations | ~100% format consistency |
| Token Efficiency + Streaming + Caching | Production apps | 85% cost + latency wins |
| Sub-Agents + Custom Commands + MCP | Complex projects | 10x productivity on multi-domain tasks |
| Hallucination Prevention + Citations + Step-by-Step | Factual content | 15-30% accuracy improvement |

---

## Pattern Categories

### Core Foundation (Must-Have)

These 5 patterns are prerequisites for effective Claude usage:

1. **Clear Instructions** - Foundation for all other patterns
2. **Context Management** - Essential for understanding your codebase
3. **Claude.md** - Persistent memory across sessions
4. **Step-by-Step Thinking** - Improves reasoning quality
5. **Few-Shot Examples** - Format consistency and edge case handling

**Why Foundation**: Without these, all other patterns have degraded effectiveness.

**Implementation Order**: Clear Instructions → Context Management → Claude.md → Step-by-Step → Few-Shot

---

### Optimization Layer (Performance)

These patterns improve speed, cost, and user experience:

6. **Token Efficiency** - Reduces API costs
7. **Streaming** - Improves perceived latency
8. **Prefilling** - Guarantees output format
9. **System Prompts** - Consistency across conversations

**Dependency**: Requires Core Foundation first
**Best Combined With**: Token Efficiency + Streaming for cost-effective UX

---

### Advanced Techniques (Complexity Management)

These patterns handle complex, multi-step workflows:

10. **Plan Mode** - Spec before implementation
11. **Prompt Chaining** - Break complex tasks into steps
12. **Sub-Agents** - Parallel specialized execution
13. **Custom Commands** - Reusable workflows

**Dependency**: Requires Core Foundation + some Optimization patterns
**Best Combined With**: Plan Mode + Prompt Chaining + Sub-Agents for large features

---

### Quality Assurance (Production-Ready)

These patterns ensure correctness and safety:

14. **Code Review** - Security and quality validation
15. **Hallucination Prevention** - Factual accuracy
16. **Affirmative Instructions** - Positive framing
17. **Example-First Documentation** - Learning accuracy

**Dependency**: Works with any foundation
**Best Combined With**: Code Review + Hallucination Prevention for critical systems

---

### Tooling (Capability Extension)

These patterns extend Claude's native abilities:

18. **MCP Servers** - External tool access
19. **Custom Commands** - Workflow automation
20. (Custom Commands listed in both categories)

**Dependency**: Requires Core Foundation
**Best Combined With**: MCP Servers + Sub-Agents for multi-tool workflows

---

## Pattern Relationships Matrix

### Synergistic Patterns (Work Together)

Patterns that amplify each other when combined:

#### **Context Management ↔ Claude.md** ⭐⭐⭐⭐⭐
**Synergy**: Context Management structures information; Claude.md persists it
**Combined Effect**: One-time setup, permanent benefit
**Use Together**: Always - these are complementary halves of the same solution

#### **Token Efficiency ↔ Streaming** ⭐⭐⭐⭐⭐
**Synergy**: Caching reduces cost; streaming reduces perceived latency
**Combined Effect**: Fast UX at low cost
**Use Together**: Production applications where both cost and UX matter

**Implementation**:
```typescript
// Use both: cached content + streaming delivery
const stream = client.messages.stream({
  model: "claude-sonnet-4",
  system: [{
    text: CACHED_CONTEXT,
    cache_control: { type: "ephemeral" } // 90% cost savings
  }],
  messages: [...] // Streams for UX
});
```

#### **Step-by-Step Thinking ↔ Plan Mode** ⭐⭐⭐⭐
**Synergy**: Plan Mode creates spec; Step-by-Step ensures thorough reasoning during implementation
**Combined Effect**: 20% better planning quality + fewer implementation bugs
**Use Together**: Complex features requiring careful design

#### **Few-Shot Examples ↔ Prefilling** ⭐⭐⭐⭐
**Synergy**: Few-Shot shows format; Prefilling enforces it
**Combined Effect**: Near 100% format consistency
**Use Together**: API integrations requiring structured output

**Implementation**:
```python
# Combine few-shot + prefilling for guaranteed JSON
response = client.messages.create(
    messages=[
        {"role": "user", "content": f"""
Extract data from this text. Format as JSON.

Example:
Input: "Call John at 555-1234"
Output: {{"name": "John", "phone": "555-1234"}}

Text: {text}
"""},
        {"role": "assistant", "content": "{"} # Prefill forces JSON
    ]
)
```

#### **Sub-Agents ↔ Custom Commands** ⭐⭐⭐⭐
**Synergy**: Sub-Agents delegate tasks; Custom Commands standardize workflows
**Combined Effect**: Scalable team automation
**Use Together**: Large projects with repetitive multi-step tasks

#### **MCP Servers ↔ Context Management** ⭐⭐⭐⭐
**Synergy**: MCPs provide live data; Context Management structures how to use it
**Combined Effect**: Always-current understanding
**Use Together**: Projects using cutting-edge frameworks

#### **Hallucination Prevention ↔ Example-First Documentation** ⭐⭐⭐⭐
**Synergy**: Examples ground responses; hallucination prevention adds citations
**Combined Effect**: 30% accuracy + verifiable sources
**Use Together**: Documentation Q&A systems

#### **Code Review ↔ Step-by-Step Thinking** ⭐⭐⭐
**Synergy**: Step-by-Step reveals reasoning; Code Review validates security
**Combined Effect**: Transparent + secure code generation
**Use Together**: Security-critical implementations

---

### Alternative Patterns (Either/Or)

Patterns serving similar purposes with different approaches:

#### **Few-Shot Examples ⊕ Example-First Documentation**
**Similarity**: Both use examples to improve accuracy
**Difference**:
- Few-Shot: 3-5 examples inline with prompt
- Example-First: Full documentation with Q&A examples
**Choose**: Few-Shot for format control; Example-First for documentation analysis
**Can Combine**: Yes, for maximum grounding

#### **Plan Mode ⊕ Prompt Chaining**
**Similarity**: Both break complex tasks into steps
**Difference**:
- Plan Mode: Human-reviewed specification before coding
- Prompt Chaining: Automated multi-step execution
**Choose**: Plan Mode for high-stakes features; Prompt Chaining for automated pipelines
**Can Combine**: Yes - plan first, then chain execution

#### **System Prompts ⊕ Claude.md**
**Similarity**: Both provide persistent context
**Difference**:
- System Prompts: API-level, conversation-scoped
- Claude.md: File-based, project-scoped
**Choose**: Claude.md for project conventions; System Prompts for conversation roles
**Can Combine**: Yes - Claude.md for project, System Prompts for role

#### **Prefilling ⊕ Few-Shot Examples**
**Similarity**: Both enforce output format
**Difference**:
- Prefilling: Physically start response (100% guarantee)
- Few-Shot: Show examples (60-80% compliance)
**Choose**: Prefilling for API integrations; Few-Shot for learning
**Can Combine**: Yes - maximum format consistency

---

### Prerequisite Dependencies

Patterns requiring other patterns first:

#### **Sub-Agents → Claude.md**
**Dependency**: Sub-agents need consistent context across all agents
**Why**: Without Claude.md, each sub-agent may interpret project differently
**Implementation Order**: Set up Claude.md → define sub-agents

#### **Prompt Chaining → Step-by-Step Thinking**
**Dependency**: Chain steps benefit from explicit reasoning
**Why**: Each step should show its work for debugging
**Implementation Order**: Master step-by-step → build chains

#### **Token Efficiency → Context Management**
**Dependency**: Must understand what to cache before optimizing
**Why**: Caching wrong content wastes effort
**Implementation Order**: Optimize context → apply caching

#### **Streaming → System Prompts** (optional)
**Dependency**: Streaming works better with consistent role/tone
**Why**: Partial responses should maintain voice throughout
**Implementation Order**: Define system prompt → add streaming

#### **Code Review → Clear Instructions**
**Dependency**: Can only review what was clearly requested
**Why**: Review against explicit requirements
**Implementation Order**: Write clear requirements → review implementation

#### **MCP Servers → Context Management**
**Dependency**: Need structured context to use MCP data effectively
**Why**: MCPs provide raw data; context structures how to apply it
**Implementation Order**: Set up context patterns → integrate MCPs

---

### Enhancer Patterns (Amplifiers)

Patterns that make other patterns more effective:

#### **Step-by-Step Thinking** → Enhances ALL patterns
**Amplification**: +20% accuracy across all tasks
**Mechanism**: Reveals reasoning, catches errors early
**Apply To**: Plan Mode, Code Review, Hallucination Prevention, Prompt Chaining

#### **Clear Instructions** → Enables ALL patterns
**Amplification**: Foundation for everything
**Mechanism**: Reduces ambiguity, improves compliance
**Apply To**: Every single pattern benefits

#### **Token Efficiency** → Enhances Context Management + Claude.md
**Amplification**: Makes large contexts sustainable
**Mechanism**: Caching expensive context
**Apply To**: Large documentation, multi-turn conversations

#### **Custom Commands** → Enhances Sub-Agents + Code Review
**Amplification**: Standardizes sub-agent tasks and review processes
**Mechanism**: Codifies best practices
**Apply To**: Team workflows, quality gates

#### **MCP Servers** → Enhances Context Management + Hallucination Prevention
**Amplification**: Always-current data prevents stale knowledge
**Mechanism**: Live documentation and database access
**Apply To**: Rapidly evolving frameworks, fact-checking

---

## Pattern Stacks for Common Use Cases

### Stack 1: New Project Setup
**Scenario**: Starting a greenfield project with Claude

**Pattern Stack**:
1. **Clear Instructions** - Establish baseline
2. **Context Management** - Structure codebase understanding
3. **Claude.md** - Document tech stack and conventions
4. **Plan Mode** - Spec before building
5. **Code Review** - Validate implementations

**Expected Results**:
- 50-80% fewer implementation iterations
- Consistent code quality from day one
- New developers productive in hours

**Implementation Order**: 1 → 2 → 3 → 4 → 5

---

### Stack 2: Production API Development
**Scenario**: Building customer-facing APIs requiring reliability

**Pattern Stack**:
1. **Clear Instructions** - Explicit requirements
2. **Few-Shot Examples** - Show expected formats
3. **Prefilling** - Guarantee JSON structure
4. **Hallucination Prevention** - Factual accuracy
5. **Code Review** - Security validation
6. **Token Efficiency** - Reduce costs

**Expected Results**:
- Near 100% format consistency
- 15% better factual accuracy
- 60-90% cost reduction
- Production-ready security

**Implementation Order**: 1 → 2 → 3 → 6 → 4 → 5

---

### Stack 3: Interactive Chat Application
**Scenario**: Building chatbot with good UX and low costs

**Pattern Stack**:
1. **System Prompts** - Define personality/role
2. **Context Management** - Structure knowledge base
3. **Token Efficiency** - Cache documentation (90% savings)
4. **Streaming** - Progressive responses (85% perceived latency reduction)
5. **Hallucination Prevention** - Grounded answers
6. **Claude.md** - Persistent bot configuration

**Expected Results**:
- <500ms time-to-first-token
- 90% cost savings on repeated context
- Verifiable, grounded responses
- Consistent personality

**Implementation Order**: 1 → 2 → 6 → 3 → 4 → 5

---

### Stack 4: Complex Multi-Domain Project
**Scenario**: Large system with frontend, backend, testing, DevOps

**Pattern Stack**:
1. **Claude.md** - Project-wide conventions
2. **Context Management** - Organize codebase
3. **Sub-Agents** - Domain specialists (frontend, backend, testing)
4. **Custom Commands** - Standardized workflows
5. **MCP Servers** - External tools (database, browser)
6. **Plan Mode** - Architecture decisions
7. **Prompt Chaining** - Multi-step features

**Expected Results**:
- 10x faster on multi-domain tasks
- Clean separation of concerns
- Scalable to large teams
- Automated complex workflows

**Implementation Order**: 1 → 2 → 6 → 3 → 4 → 5 → 7

---

### Stack 5: Learning New Framework
**Scenario**: Quickly becoming productive with unfamiliar technology

**Pattern Stack**:
1. **MCP Servers** (Context7) - Always-current docs
2. **Example-First Documentation** - Learn from Q&A
3. **Step-by-Step Thinking** - Understand reasoning
4. **Few-Shot Examples** - See patterns in action
5. **Code Review** - Catch anti-patterns

**Expected Results**:
- 30% faster learning curve
- Fewer beginner mistakes
- Understanding "why" not just "what"
- Production-quality code from start

**Implementation Order**: 1 → 2 → 3 → 4 → 5

---

### Stack 6: Team Standardization
**Scenario**: Ensuring consistency across team members

**Pattern Stack**:
1. **Claude.md** - Shared conventions
2. **Custom Commands** - Reusable workflows
3. **Code Review** - Quality gates
4. **System Prompts** - Consistent "voice"
5. **Few-Shot Examples** - Style guide

**Expected Results**:
- 50% faster onboarding
- Consistent code style
- Reduced review cycles (30-40%)
- Shared best practices

**Implementation Order**: 1 → 2 → 5 → 4 → 3

---

### Stack 7: Cost-Optimized Development
**Scenario**: Minimizing API costs while maintaining quality

**Pattern Stack**:
1. **Token Efficiency** - Caching, compression, batching
2. **Context Management** - Minimal necessary context
3. **Claude.md** - Cache project knowledge
4. **Model Selection** - Haiku for simple tasks
5. **Clear Instructions** - Reduce iterations

**Expected Results**:
- 60-90% cost reduction
- Maintained output quality
- Faster development (fewer retries)
- Sustainable economics

**Implementation Order**: 2 → 3 → 1 → 4 → 5

---

## Anti-Combinations

Patterns that conflict or don't work well together:

### ❌ Prefilling + Verbose Instructions
**Conflict**: Prefilling works best with concise prompts
**Why**: Verbose instructions waste tokens when format is guaranteed
**Solution**: Use prefilling + minimal instruction

### ❌ Over-Caching + Dynamic Context
**Conflict**: Caching static content, but treating it as dynamic
**Why**: Cached content can't change per request
**Solution**: Cache truly static portions only

### ❌ Too Many Sub-Agents
**Conflict**: 10+ sub-agents create coordination overhead
**Why**: Diminishing returns, hard to orchestrate
**Solution**: Limit to 3-5 specialized sub-agents

### ❌ Streaming + Prefilling (sometimes)
**Conflict**: Prefilling may delay first token
**Why**: Must generate prefilled content before streaming
**Solution**: Minimal prefill (1-2 characters) or skip for TTFT optimization

### ❌ Plan Mode + Rapid Prototyping
**Conflict**: Planning slows iteration speed
**Why**: Spec overhead not worth it for throwaway code
**Solution**: Skip plan mode for experiments, use for production

---

## Learning Progression

Recommended order for learning and implementing patterns:

### Phase 1: Foundations (Week 1)
**Focus**: Essential patterns for basic productivity

1. **Clear Instructions** (Day 1) - Master explicit communication
2. **Context Management** (Day 2-3) - Structure codebase understanding
3. **Claude.md** (Day 4) - Set up persistent memory
4. **Step-by-Step Thinking** (Day 5) - Improve reasoning quality
5. **Few-Shot Examples** (Day 6-7) - Format consistency

**Milestone**: Productive with Claude on simple tasks

---

### Phase 2: Optimization (Week 2)
**Focus**: Improve speed, cost, and quality

6. **Token Efficiency** (Day 1-2) - Reduce API costs
7. **Streaming** (Day 3-4) - Improve UX
8. **System Prompts** (Day 5) - Conversation consistency
9. **Code Review** (Day 6-7) - Quality validation

**Milestone**: Production-ready applications

---

### Phase 3: Advanced Techniques (Week 3)
**Focus**: Complex workflows and automation

10. **Plan Mode** (Day 1-2) - Spec-driven development
11. **Custom Commands** (Day 3-4) - Workflow automation
12. **MCP Servers** (Day 5) - External tool integration
13. **Prompt Chaining** (Day 6-7) - Multi-step workflows

**Milestone**: Automated complex processes

---

### Phase 4: Mastery (Week 4)
**Focus**: Specialized techniques and edge cases

14. **Sub-Agents** (Day 1-3) - Parallel specialized execution
15. **Hallucination Prevention** (Day 4-5) - Factual accuracy
16. **Prefilling** (Day 6) - Format guarantees
17. **Specialized Patterns** (Day 7) - Affirmative Instructions, Example-First

**Milestone**: Expert-level Claude usage

---

## Visual Dependency Graph

```
Core Foundation (Layer 1)
┌─────────────────────────────────────────────────────────┐
│  Clear Instructions ──────────────────────────────┐     │
│         │                                         │     │
│         ▼                                         ▼     │
│  Context Management ◄──► Claude.md        Step-by-Step │
│         │                     │                  │     │
│         └─────────┬───────────┘                  │     │
│                   ▼                              │     │
│            Few-Shot Examples ◄────────────────────┘     │
└─────────────────────────────────────────────────────────┘
                      │
                      ▼
Optimization Layer (Layer 2)
┌─────────────────────────────────────────────────────────┐
│  Token Efficiency ◄──► Streaming                        │
│         │                   │                            │
│         │                   │                            │
│    Prefilling        System Prompts                     │
└─────────────────────────────────────────────────────────┘
                      │
                      ▼
Advanced Techniques (Layer 3)
┌─────────────────────────────────────────────────────────┐
│  Plan Mode ──► Prompt Chaining                          │
│      │               │                                   │
│      └───────┬───────┘                                   │
│              ▼                                           │
│        Sub-Agents ◄──► Custom Commands                  │
└─────────────────────────────────────────────────────────┘
                      │
                      ▼
Quality & Tooling (Layer 4)
┌─────────────────────────────────────────────────────────┐
│  Code Review    Hallucination Prevention                │
│         │                   │                            │
│         │                   │                            │
│  MCP Servers ◄────────┬────┘                            │
│                       │                                  │
│         Affirmative Instructions                         │
│         Example-First Documentation                      │
└─────────────────────────────────────────────────────────┘

Legend:
──► Prerequisite dependency
◄──► Synergistic combination
```

---

## Pattern Selection Decision Tree

```
Start: What's your primary goal?
│
├─ NEW PROJECT
│  └─ Use: Context Management + Claude.md + Plan Mode
│     └─ High quality? → Add: Code Review + Step-by-Step
│     └─ Team project? → Add: Custom Commands
│
├─ REDUCE COSTS
│  └─ Use: Token Efficiency + Context Management
│     └─ Chat app? → Add: Streaming + System Prompts
│     └─ API integration? → Add: Prefilling + Few-Shot
│
├─ IMPROVE UX
│  └─ Use: Streaming + System Prompts
│     └─ Real-time? → Optimize: TTFT with Haiku model
│     └─ Consistency? → Add: Claude.md + Few-Shot
│
├─ COMPLEX WORKFLOW
│  └─ Use: Plan Mode + Prompt Chaining
│     └─ Multiple domains? → Add: Sub-Agents
│     └─ Repetitive? → Add: Custom Commands
│     └─ External tools? → Add: MCP Servers
│
├─ FACTUAL ACCURACY
│  └─ Use: Hallucination Prevention + Step-by-Step
│     └─ Documentation? → Add: Example-First + MCP
│     └─ Citations? → Add: Grounding techniques
│
└─ LEARNING / EXPLORATION
   └─ Use: Step-by-Step + Few-Shot Examples
      └─ New framework? → Add: MCP (Context7)
      └─ Understanding code? → Add: Context Management
```

---

## Integration Checklist

When combining multiple patterns, ensure:

- [ ] **Clear Instructions** is foundation for all
- [ ] **Dependencies respected** (prerequisites implemented first)
- [ ] **No anti-combinations** (check conflicts above)
- [ ] **Synergies leveraged** (combine complementary patterns)
- [ ] **Layer ordering** (Core → Optimization → Advanced → Quality)
- [ ] **Budget allocated** (some combinations require more tokens initially)
- [ ] **Team aligned** (everyone understands the pattern stack)

---

## Maintenance & Evolution

### As Project Grows

**Weeks 1-4**: Core Foundation only
**Months 2-3**: Add Optimization Layer
**Months 4-6**: Introduce Advanced Techniques
**Months 6+**: Full Quality & Tooling stack

### As Team Grows

**Solo developer**: Core + basic optimization
**2-5 developers**: Add Custom Commands + Code Review
**5+ developers**: Full stack with Sub-Agents

### As Costs Grow

**<$50/month**: Basic patterns fine
**$50-500/month**: Implement Token Efficiency
**$500+/month**: Full optimization stack required

---

## Summary: Most Important Relationships

1. **Context + Claude.md** = Essential baseline (implement together always)
2. **Token Efficiency + Streaming** = Cost-effective UX (production requirement)
3. **Step-by-Step + Code Review** = Quality + transparency (security-critical)
4. **Sub-Agents + Custom Commands** = Scalable automation (large projects)
5. **Few-Shot + Prefilling** = Format guarantees (API integrations)

---

## Quick Reference: Pattern Pairs

| Need | Pattern Pair | Combined Effect |
|------|-------------|-----------------|
| Reliable Format | Few-Shot + Prefilling | ~100% consistency |
| Low Cost UX | Token Efficiency + Streaming | 85% latency + 90% cost savings |
| Factual Content | Hallucination Prevention + Citations | 15-30% accuracy |
| Complex Features | Plan Mode + Prompt Chaining | 20-40% quality improvement |
| Team Consistency | Claude.md + Custom Commands | 50% faster onboarding |
| Multi-Domain | Sub-Agents + MCP Servers | 10x productivity |
| Production Quality | Step-by-Step + Code Review | Transparent + secure |

---

**Version**: 1.0
**Last Updated**: 2024-11-14
**Maintainer**: Claude Coding Knowledge Base Project

**Next Review**: After implementing 5+ new patterns (expand relationship matrix)
