# Advanced Agentic Patterns with Claude

> Comprehensive guide to multi-agent systems, task decomposition, memory patterns, orchestration strategies, and autonomous agent architectures using Claude

**Last Updated**: 2025-11-25
**Status**: Production-Ready Patterns
**Sources**: Anthropic Engineering, Claude-Flow, Community Frameworks

---

## Table of Contents

1. [Multi-Agent System Architectures](#multi-agent-system-architectures)
2. [Task Decomposition Patterns](#task-decomposition-patterns)
3. [Agent Memory & State Management](#agent-memory--state-management)
4. [Orchestration Strategies](#orchestration-strategies)
5. [Autonomous Agent Architectures](#autonomous-agent-architectures)
6. [Production Frameworks & Examples](#production-frameworks--examples)
7. [Performance Metrics & Benchmarks](#performance-metrics--benchmarks)
8. [Implementation Best Practices](#implementation-best-practices)

---

## Multi-Agent System Architectures

### Orchestrator-Worker Pattern

The primary architectural pattern used in production Claude systems.

**Architecture**:
- **Lead Agent** (typically Claude Opus 4): Coordinates strategy and orchestrates subagents
- **Subagents** (typically Claude Sonnet 4): Specialized workers operating in parallel
- **Isolated Contexts**: Each subagent maintains its own context window
- **Lightweight Communication**: Subagents return condensed findings to orchestrator

**Key Benefits**:
- Context management within 200K token limits (each subtask has separate context)
- True parallel processing without memory conflicts
- 90.2% performance improvement over single-agent systems
- Scales to 10+ concurrent subagents

**Implementation Pattern**:
```
Orchestrator analyzes query
    ↓
Decomposes into subtasks
    ↓
Spawns specialized subagents in parallel
    ↓
Subagents act as "intelligent filters"
    ↓
Return findings to orchestrator
    ↓
Orchestrator synthesizes results
```

### The "3 Amigo Agents" Development Pattern

**Specialized trio for AI-driven development**:
- **PM Agent**: Product strategy and requirements
- **UX Designer Agent**: Interface and experience design
- **Claude Code Agent**: Implementation and engineering

**Use Case**: Developing multi-agent orchestration patterns where AI specialists collaborate in real-time

### Agent Loop Architecture

**Four-stage feedback cycle** (from Claude Agent SDK):

1. **Gather Context** – Fetch and update information
2. **Take Action** – Execute tasks through tools
3. **Verify Work** – Evaluate and improve outputs
4. **Repeat** – Iterate until objectives met

**Context Gathering Methods**:
- **Agentic Search**: File system navigation with bash commands (`grep`, `tail`)
- **Semantic Search**: Fast but less accurate than agentic search
- **Subagents**: Parallel exploration with context isolation
- **Compaction**: Auto-summarization as context limits approach

---

## Task Decomposition Patterns

### Decomposition Strategy by Task Size

**Huge Tasks**: 15-25 subtasks
**Large Tasks**: 8-15 subtasks
**Medium Tasks**: 3-8 subtasks
**Small Tasks**: Direct implementation (no decomposition)

### Effective Delegation Principles

**Each subagent requires**:
1. **Clear objective** – Specific goal and success criteria
2. **Output format** – Expected structure of results
3. **Tool guidance** – Which tools to use and how
4. **Task boundaries** – Explicit scope to prevent duplication/gaps

**Effort Scaling**:
- Simple fact-finding: 1 agent, 3-10 tool calls
- Complex research: 10+ subagents with divided responsibilities

### Tool Matching Strategy

Agents should select appropriate tools based on user intent:
- Prefer specialized tools over generic options
- Match tool capabilities to task requirements
- Consider performance trade-offs (speed vs accuracy)

### Best Practices for Planning

**Before Implementation**:
1. Ask Claude to create a plan before coding
2. Provide explicit steps including which will be delegated to subagents
3. Explicitly request user confirmation of the plan
4. Only then proceed with implementation

**Avoiding Failure**:
- Prevent duplication through clear task boundaries
- Avoid gaps by ensuring complete coverage
- Minimize context switching through logical grouping

---

## Agent Memory & State Management

### Memory Architecture Patterns

**Isolated Memory Spaces with Controlled Exchange**:
- Each agent maintains own working memory for task execution
- Orchestrator holds global memory (task state, results aggregation, coordination metadata)
- Prevents memory conflicts and lock contention
- Enables true parallel processing

### Hierarchical Memory Structure

Claude Code offers **four memory locations** in hierarchical structure:

1. **Session Memory** – Current conversation context
2. **Project Memory** – Persistent across sessions for project
3. **Global Memory** – User-wide knowledge base
4. **External Memory** – File-based storage outside context

**All memory files automatically loaded into context when Claude Code launches**

### Official Memory Tools

**File-Based Memory System**:
- Create, read, update, delete files in dedicated memory directory
- Persists across conversations
- Enables knowledge base building over time
- Maintains project state across sessions
- References previous learnings

**Performance Impact**:
- Memory tool + context editing: **39% improvement** over baseline
- Context editing alone: **29% improvement**

### Persistent State Management (Claude-Flow)

**SQLite-Based Infrastructure**:
- Location: `.swarm/memory.db`
- Cross-session state management
- Agent coordination support
- 12 specialized tables for memory operations

**Hybrid Memory Approaches**:

**AgentDB v1.3.9**:
- 96x faster vector search (9.6ms → <0.1ms)
- 125x faster batch operations
- 164x faster large queries
- 4-32x memory reduction via quantization
- HNSW semantic indexing with O(log n) complexity
- 9 reinforcement learning algorithms (Q-Learning, PPO, MCTS, Decision Transformer)
- Reflexion memory for learning from experiences

**ReasoningBank (Legacy SQLite)**:
- Hash-based embeddings (1024 dimensions)
- 2-3ms average query latency
- Pattern matching with similarity scoring
- Namespace isolation for domain organization

### Long-Running Task Patterns

**Context Window Management**:
- Standard context windows become insufficient for extended conversations
- Intelligent compression mechanisms required
- Agents summarize completed work phases
- Essential information stored in external memory before proceeding

**Strategy**:
1. Lead agents save plans to external memory
2. Maintain context when windows exceed 200K tokens
3. Fresh subagents receive clean contexts
4. Continuity preserved through handoffs
5. Retrieved stored context prevents information loss

---

## Orchestration Strategies

### Core Orchestration Patterns

#### 1. Orchestrator-Worker with Parallel Execution

**Pattern**:
```
Lead Agent (Opus 4) coordinates
    ↓
Multiple Subagents (Sonnet 4) work in parallel
    ↓
Each subagent has isolated context
    ↓
Results aggregated by orchestrator
```

**Supports**: Up to 10+ parallel tasks confirmed

#### 2. Sequential Coordination

**Pattern**:
```
Sonnet (planning) → Haiku (execution) → Sonnet (review)
```

**Example - Full-Stack Feature**:
```
backend-architect
    → database-architect
    → frontend-developer
    → test-automator
    → security-auditor
    → deployment-engineer
    → observability-engineer
```

**7+ agents coordinate sequentially for complex features**

#### 3. Swarm Intelligence (Claude-Flow)

**Two Primary Modes**:

**Swarm Mode**:
- Instant setup for quick tasks
- Task-scoped memory
- Lightweight coordination

**Hive-Mind Mode**:
- Interactive wizard setup
- Complex projects with project-wide persistent SQLite storage
- Resumable sessions
- Queen-led coordination with specialized workers

**Key Features**:
- Dynamic Agent Architecture (DAA): Self-organizing agents with fault tolerance
- Mesh topology: Configurable up to 5+ agents
- Semantic search: Contextual understanding vs keyword matching
- Skill library consolidation: Auto-consolidation of successful patterns

### MCP Integration for Orchestration

**100+ Specialized Tools** across:
- Swarm orchestration (`swarm_init`, `agent_spawn`, `task_orchestrate`)
- Memory operations (`memory_usage`, `memory_search`)
- Neural pattern training
- GitHub repository analysis and PR management
- Performance benchmarking and analysis

### Progressive Disclosure Pattern

**Three-tier skill architecture** (wshobson/agents):

1. **Metadata** – Always loaded (~300 tokens average)
2. **Instructions** – Activated on demand
3. **Resources** – Examples/templates loaded as needed

**Benefits**:
- Minimal context overhead
- Knowledge packages with progressive disclosure
- Specialized expertise activated only when needed
- Average 3.4 components per plugin maintains efficiency

---

## Autonomous Agent Architectures

### Claude Agent SDK Architecture

**Core Concept**: Give agents tools to "write files, run commands, and iterate on work"

**Action Execution Tools**:
- **Tools**: Primary building blocks for frequent, high-value actions
- **Bash & Scripts**: Flexible computer operations
- **Code Generation**: Agents excel at creating precise, reusable code
- **MCP (Model Context Protocol)**: Standardized integrations with automatic auth

### Work Verification Approaches

**1. Rules-Based Feedback**:
- Define explicit validation criteria
- Code linting provides layered feedback
- TypeScript offers more validation points than JavaScript

**2. Visual Feedback**:
- Screenshots or renders for UI verification
- Validates layout, styling, hierarchy, responsiveness

**3. LLM-as-Judge**:
- Separate model evaluates outputs against fuzzy criteria
- Trade-off: Performance gains vs latency costs

### Specialized Agent Categories

**From awesome-claude-code-subagents (100+ agents)**:

**Core Development**:
- API designers, backend/frontend developers
- Fullstack specialists, microservices architects

**Language Specialists**:
- TypeScript, Python, Rust, Go, Java, C++, PHP, Ruby
- Framework-specific experts

**Infrastructure**:
- Cloud architects, DevOps engineers
- Kubernetes specialists, SRE engineers

**Quality & Security**:
- Code reviewers, security auditors
- QA experts, penetration testers

**Data & AI**:
- Data scientists, ML engineers
- LLM architects, NLP specialists

**Developer Experience**:
- Build engineers, refactoring specialists
- Documentation experts

**Meta & Orchestration**:
- Multi-agent coordinators
- Workflow orchestrators

### Agent Implementation Structure

**Standard YAML Configuration**:
```yaml
name: agent-name
description: Clear role description
tools:
  - Read
  - Write
  - Bash
  - Grep
  # Granular permissions
role: |
  Domain-specific instructions
  Workflow guidelines
  Success criteria
```

**Deployment**:
- Project-level: `.claude/agents/`
- Global: `~/.claude/agents/`

### Resilience Engineering Patterns (claude-007-agents)

**Production-Grade Features**:
- **Fault Tolerance**: Circuit breakers, retry mechanisms, graceful degradation
- **Structured Logging**: JSON logging with contextual information
- **Self-Healing**: Automatic recovery patterns
- **Automated Quality**: Trunk.io integration for linting/security

**Coordination Intelligence**:
- Codebase-aware autonomous development
- Dynamic agent selection based on tech stack
- Multi-agent parallel execution with dependency management
- Organizational memory support

---

## Production Frameworks & Examples

### Claude-Flow v2.7.0

**Repository**: https://github.com/ruvnet/claude-flow

**Architecture**: Enterprise-grade AI orchestration platform

**Key Features**:
- 64 specialized agents across multiple domains
- Hive-mind swarm intelligence
- Persistent memory with SQLite storage
- 100+ advanced MCP tools
- 25 Claude Skills with natural language activation

**Performance**:
- 32.3% token reduction through efficient context management
- 2.8-4.4x speed improvement via parallel coordination
- >90% test coverage (180 AgentDB tests)
- 84.8% SWE-Bench solve rate

**Use Cases**:

**Single Feature Development**:
```bash
hive-mind spawn  # Initialize once per feature
swarm --continue-session  # Continue with persistent memory
```

**Multi-Feature Projects**:
```bash
init --project-name myproject
# Spawn separate hive-minds per feature
--namespace auth
--namespace users
# Enables parallel development with isolation
```

**Research & Analysis**:
```bash
# Launch multi-agent sessions
--agents researcher,analyst --claude
# Query learned knowledge through memory system
```

### wshobson/agents

**Repository**: https://github.com/wshobson/agents

**Architecture**: Intelligent automation and multi-agent orchestration

**Components**:
- 85 specialized AI agents
- 15 multi-agent workflow orchestrators
- 47 agent skills
- 44 development tools
- 63 focused, single-purpose plugins

**Agent Distribution**:
- 47 Haiku agents: Fast, deterministic execution
- 97 Sonnet agents: Complex reasoning and architectural decisions

**Plugin System**:
- Granular architecture: Each plugin loads only relevant components
- Average 3.4 components per plugin
- Single-responsibility principle
- Composable design: Mix and match for complex workflows

**Installation Pattern**:
```bash
/plugin marketplace add wshobson/agents  # Register 63 plugins
/plugin install python-development       # Load only 3 agents + tools
```

### VoltAgent/awesome-claude-code-subagents

**Repository**: https://github.com/VoltAgent/awesome-claude-code-subagents

**Description**: Definitive collection of Claude Code subagents

**Scale**: 100+ production-ready agents across 10 major categories

**Key Features**:
- Domain-specific instructions for superior performance
- Granular tool permissions
- Standardized YAML-based configuration
- Isolated context spaces per agent
- Clarity in primary conversation thread

### claude-007-agents

**Repository**: https://github.com/avivl/claude-007-agents

**Architecture**: Unified AI agent orchestration system

**Specialized Orchestrators**:
- **Vibe Coding Coordinator**: 15-20 minute autonomous preparation phases
- **Exponential Planner**: Strategic planning with AI capability scaling awareness
- **Parallel Coordinator**: Multi-agent execution with coordinated tool calling
- **Sequential Thinking**: Complex multi-step reasoning with adaptive planning
- **Safety Specialists**: Pre-deployment validation and architectural analysis

**Critical Requirement**: Bootstrap setup mandatory per project

```bash
claude "Use @bootstrap-orchestrator to analyze and setup this project"
```

**Bootstrap Process**:
1. Analyzes codebase
2. Selects optimal agents
3. Creates configuration files with commit attribution
4. Validates system readiness

### Anthropic's Multi-Agent Research System

**Official Implementation**: https://www.anthropic.com/engineering/multi-agent-research-system

**Production System Architecture**:
- Lead agent (Opus 4) with specialized subagents (Sonnet 4)
- Parallel tool calling
- Intelligent filtering through iterative information gathering
- External memory for plan storage

**Performance**:
- 90.2% improvement over single-agent Opus 4
- 90% time reduction for complex queries via parallel tool calling
- Token usage explains 80% of performance variance

**Production Reliability Features**:
- Checkpoint systems and retry logic
- Agents adapt when tools fail (no full restart)
- Rainbow deployments to avoid disrupting running agents
- Decision pattern monitoring without content inspection

---

## Performance Metrics & Benchmarks

### Token Usage Patterns

**Baseline Comparisons**:
- Standard chat: 1x tokens (baseline)
- Single agent: 4x tokens vs chat
- Multi-agent: 15x tokens vs standard chat

**Efficiency Gains**:
- Claude-Flow: 32.3% token reduction through context management
- Progressive disclosure: ~300 tokens average per plugin (wshobson/agents)

### Speed & Performance

**Time Improvements**:
- Parallel tool calling: Up to 90% time reduction for complex queries
- Claude-Flow coordination: 2.8-4.4x speed improvement
- AgentDB vector search: 96x faster (9.6ms → <0.1ms)
- Batch operations: 125x faster
- Large queries: 164x faster

**Query Latency**:
- ReasoningBank: 2-3ms average
- AgentDB: <0.1ms vector search

### Accuracy & Quality

**Task Performance**:
- Multi-agent vs single-agent: 90.2% improvement (Anthropic research)
- Token volume explains: 80% of success variance
- Memory + context editing: 39% improvement over baseline
- Context editing alone: 29% improvement
- Claude-Flow SWE-Bench: 84.8% solve rate

**Test Coverage**:
- Claude-Flow: >90% coverage with 180 AgentDB tests

### Memory & Storage

**Memory Efficiency**:
- AgentDB quantization: 4-32x memory reduction
- HNSW indexing: O(log n) complexity

---

## Implementation Best Practices

### Prompt Engineering for Agents

**Build Simulations**:
- Understand agent behavior before production
- Reveal failure modes early
- Test edge cases systematically

**Thinking Strategies**:
- Extended thinking for planning phases
- Interleaved thinking for evaluation steps
- Encode human research heuristics (decomposition, source evaluation, adaptive search)

**Tool Guidance**:
- Teach orchestrator how to delegate effectively
- Provide clear tool selection criteria
- Match tools to agent capabilities

### Evaluation & Testing

**Start Small**:
- Begin with ~20 query samples
- Identify high-impact improvements
- Iterate based on real patterns

**LLM Judge Criteria**:
- Factual accuracy
- Citation accuracy
- Completeness
- Source quality
- Tool efficiency

**Combine Methods**:
- Automated evaluation for scale
- Human testing for edge cases and biases
- Monitor decision patterns for diagnosis

### Production Deployment

**Reliability Patterns**:
- Implement checkpoint systems
- Add retry logic for transient failures
- Enable agent adaptation to tool failures
- Use rainbow deployments for zero-disruption updates

**Monitoring**:
- Track decision patterns (not content)
- Monitor interaction structures
- Measure token efficiency
- Benchmark completion times

**Error Handling**:
- Circuit breakers for fault tolerance
- Graceful degradation strategies
- Self-healing recovery patterns
- Structured logging with context

### Cost-Benefit Analysis

**When to Use Multi-Agent**:
- Tasks where value justifies 15x token cost
- Complex research requiring parallel exploration
- Large codebases exceeding single context limits
- Problems benefiting from specialized expertise

**When to Avoid**:
- Simple, single-step tasks
- Low-value operations
- Tight latency requirements
- Cost-sensitive applications

### Architecture Trade-offs

**Synchronous Execution**:
- ✅ Simpler coordination
- ✅ Easier debugging
- ❌ Bottlenecks at single-agent completion
- ❌ Subagents can't coordinate with each other

**Asynchronous Execution** (Future):
- ✅ Additional parallelism opportunities
- ✅ Better resource utilization
- ❌ Coordination complexity increases
- ❌ Debugging becomes harder

### Development Workflow Recommendations

**Performance Assessment**:
1. Check if missing context causes misunderstanding
2. Identify repeated failures needing formal validation
3. Provide better tools for difficult problems
4. Build representative test sets for feature additions

**Context Engineering**:
- Folder and file structure is a form of context engineering
- File system as structured information storage
- Use bash commands for intelligent data loading
- Balance between agentic search (accurate) and semantic search (fast)

**Agent Model Selection**:
- Haiku: Fast, deterministic tasks
- Sonnet: Complex reasoning, architectural decisions
- Opus: Orchestration, strategic planning
- Match model capabilities to task requirements

### Getting Started Checklist

**For New Projects**:
1. Define clear objectives and success criteria
2. Identify tasks suitable for decomposition
3. Choose appropriate framework (Claude-Flow, wshobson/agents, custom)
4. Set up bootstrap/initialization per framework requirements
5. Start with simple delegation before complex orchestration
6. Build evaluation suite early
7. Monitor token usage and performance

**For Existing Codebases**:
1. Run bootstrap analysis (if using claude-007-agents)
2. Map existing architecture to agent capabilities
3. Identify high-value automation targets
4. Gradually introduce agents for specific workflows
5. Validate performance improvements with metrics
6. Iterate based on real-world usage patterns

---

## References & Resources

### Official Documentation

- **Anthropic Multi-Agent Research System**: https://www.anthropic.com/engineering/multi-agent-research-system
- **Building Agents with Claude Agent SDK**: https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk
- **Claude Code Best Practices**: https://www.anthropic.com/engineering/claude-code-best-practices
- **Claude Agent SDK**: https://docs.claude.com

### Production Frameworks

- **Claude-Flow**: https://github.com/ruvnet/claude-flow
- **wshobson/agents**: https://github.com/wshobson/agents
- **awesome-claude-code-subagents**: https://github.com/VoltAgent/awesome-claude-code-subagents
- **claude-007-agents**: https://github.com/avivl/claude-007-agents
- **awesome-claude-agents**: https://github.com/rahulvrane/awesome-claude-agents

### Community Resources

- **Claude Subagents Guide**: https://www.cursor-ide.com/blog/claude-subagents
- **ClaudeLog Documentation**: https://claudelog.com
- **Multi-Agent Orchestration Tutorial**: https://dev.to/bredmond1019/multi-agent-orchestration-running-10-claude-instances-in-parallel-part-3-29da

---

## Conclusion

Advanced agentic patterns with Claude enable unprecedented automation and intelligence in software development and research tasks. The orchestrator-worker architecture, combined with sophisticated memory management and parallel execution, delivers 90%+ performance improvements over single-agent approaches.

Key success factors:
- **Clear task decomposition** with explicit boundaries
- **Appropriate model selection** (Haiku for speed, Sonnet for reasoning, Opus for orchestration)
- **Effective context management** through memory systems and progressive disclosure
- **Production-grade reliability** with fault tolerance and self-healing
- **Cost-benefit awareness** (15x token usage justified by value)

The ecosystem of production frameworks (Claude-Flow, wshobson/agents, claude-007-agents) provides battle-tested implementations ready for immediate deployment, while Anthropic's official patterns offer validated architectural guidance.

As multi-agent systems continue evolving toward asynchronous execution and enhanced coordination, the potential for autonomous AI agents will expand dramatically while maintaining the reliability and predictability required for production systems.

---

**Pattern Status**: ✅ Production-Ready
**Adoption Level**: Enterprise
**Maintenance**: Active Development
**Community Support**: Strong
