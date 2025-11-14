# Test Project Plan: Validating Top 15 Claude Code Patterns

**Project**: Build a Task Management API with AI-Powered Features
**Duration**: 2-3 days (8-12 hours development time)
**Validation Goal**: Systematically test our top 15 patterns in a real-world scenario
**Success Metric**: Document measurable improvements vs. baseline approach

---

## 🎯 Project Overview

### What We're Building

A production-ready REST API for task management with AI-powered features:
- Task CRUD operations (Create, Read, Update, Delete)
- AI-powered task prioritization
- Natural language task parsing
- Smart deadline suggestions
- Task description enhancement

### Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript (strict mode)
- **Database**: PostgreSQL via Prisma
- **API Client**: Anthropic Claude SDK
- **Testing**: Jest + Supertest
- **MCP**: Context7 for live documentation
- **Hooks**: Type checking, linting, security scanning

### Why This Project?

This project naturally exercises all 15 patterns:
- Complex enough to require structured prompting
- AI integration tests MCP and API patterns
- Multiple files test git workflow patterns
- Production requirements test monitoring/security
- Cost considerations test optimization patterns

---

## 📋 Top 15 Patterns to Validate

### Tier 1: High Impact (Tested First)

| # | Pattern | Confidence | Expected Impact | How We Test It |
|---|---------|------------|-----------------|----------------|
| 1 | Document Positioning | ⭐⭐⭐⭐⭐ | +30% accuracy | Large schema docs first, then queries |
| 2 | Few-Shot Examples | ⭐⭐⭐⭐⭐ | +25% task completion | Provide 3-5 examples per prompt |
| 3 | XML Tag Structure | ⭐⭐⭐⭐⭐ | +20% response quality | Use `<context>`, `<task>`, `<constraints>` |
| 4 | Context7 MCP | ⭐⭐⭐⭐⭐ | Current docs | Reference Next.js, Prisma, TypeScript |
| 5 | Sonnet-First Strategy | ⭐⭐⭐⭐ | 40-50% cost | Use Sonnet for iterations, Opus for critical |

### Tier 2: Architecture & Workflow

| # | Pattern | Confidence | Expected Impact | How We Test It |
|---|---------|------------|-----------------|----------------|
| 6 | Chain-of-Thought | ⭐⭐⭐⭐⭐ | +15% reasoning | Ask Claude to think step-by-step |
| 7 | 5-Component Prompt | ⭐⭐⭐⭐ | Consistency | Context, Task, Examples, Constraints, Format |
| 8 | Git Checkpoint | ⭐⭐⭐⭐ | 100% rollback | Checkpoint before each AI-generated change |
| 9 | Sub-Agents | ⭐⭐⭐ | 70-80% cost savings | Isolate schema, API, tests in separate contexts |
| 10 | Streaming Responses | ⭐⭐⭐⭐ | Better UX | Stream AI prioritization results |

### Tier 3: Production & Optimization

| # | Pattern | Confidence | Expected Impact | How We Test It |
|---|---------|------------|-----------------|----------------|
| 11 | Prompt Caching | ⭐⭐⭐⭐ | Cost reduction | Cache system prompt, schema definitions |
| 12 | Retry Logic | ⭐⭐⭐⭐ | Reliability | Exponential backoff on rate limits |
| 13 | Error Handling | ⭐⭐⭐⭐⭐ | Production-ready | Try/catch all API calls with logging |
| 14 | Type Check Hooks | ⭐⭐⭐⭐ | 50% less debugging | Auto-run `tsc` after file changes |
| 15 | Security Scanning | ⭐⭐⭐⭐ | OWASP compliance | Scan for API keys, SQL injection, XSS |

---

## 🏗️ Project Phases

### Phase 1: Setup & Schema (Test Patterns 1-5, 8)

**Duration**: 2 hours

#### Tasks

1. **Initialize Project**
   - Set up Next.js with TypeScript
   - Configure Prisma with PostgreSQL
   - Install Claude SDK
   - Set up git repository

2. **Design Database Schema with Claude**
   - **Test Pattern 1 (Document Positioning)**:
     ```markdown
     <large_document>
     [Paste full Prisma schema documentation]
     </large_document>

     <query>
     Design a database schema for task management with:
     - Users table
     - Tasks table with priority, deadline, status
     - AI suggestions history
     </query>
     ```

   - **Test Pattern 2 (Few-Shot Examples)**:
     Provide 3 examples of good Prisma schemas

   - **Test Pattern 3 (XML Tags)**:
     Use structured tags for context, task, constraints

   - **Test Pattern 4 (Context7 MCP)**:
     Reference latest Prisma docs automatically

   - **Test Pattern 5 (Sonnet-First)**:
     Use Sonnet for initial schema design

3. **Git Checkpoint**
   - **Test Pattern 8 (Git Checkpoint)**:
     ```bash
     claude_checkpoint "Design database schema"
     # Work with Claude...
     git diff HEAD  # Review changes
     claude_commit "Add Prisma schema for task management"
     ```

**Success Criteria**:
- Schema compiles without errors
- All relationships properly defined
- Migration runs successfully
- Checkpoint allows clean rollback if needed

**Measurements**:
- Time to complete: Target 2 hours
- Accuracy: Schema matches requirements on first try
- Cost: Track Sonnet tokens used

---

### Phase 2: API Implementation (Test Patterns 6-7, 11-13)

**Duration**: 3-4 hours

#### Tasks

1. **Create CRUD Endpoints**

   - **Test Pattern 6 (Chain-of-Thought)**:
     ```markdown
     <task>
     Implement POST /api/tasks endpoint.
     Think step-by-step:
     1. What validation is needed?
     2. What database operations?
     3. What error cases to handle?
     4. What to return?
     </task>
     ```

   - **Test Pattern 7 (5-Component Prompt)**:
     ```markdown
     <context>
     Next.js 14 App Router project
     Prisma for database
     TypeScript strict mode
     </context>

     <task>
     Create POST /api/tasks endpoint
     </task>

     <examples>
     [Show 3 similar endpoint examples]
     </examples>

     <constraints>
     - Validate with Zod
     - Return 201 on success
     - Include error handling
     </constraints>

     <format>
     - Route handler code
     - Validation schema
     - Types
     </format>
     ```

2. **Implement AI Integration**

   - **Test Pattern 11 (Prompt Caching)**:
     ```typescript
     const systemPrompt = `
     You are a task management assistant.
     [Long system instructions...]
     `;
     // Cache this in Claude API call with cache_control
     ```

   - **Test Pattern 12 (Retry Logic)**:
     ```typescript
     async function callClaudeWithRetry(prompt: string) {
       let attempt = 0;
       while (attempt < 4) {
         try {
           return await anthropic.messages.create({...});
         } catch (error: any) {
           if (error.code === 'rate_limit_exceeded') {
             await sleep(2 ** attempt * 1000);
             attempt++;
           } else throw error;
         }
       }
     }
     ```

   - **Test Pattern 13 (Error Handling)**:
     ```typescript
     try {
       const result = await callClaude(prompt);
       return NextResponse.json({ success: true, data: result });
     } catch (error) {
       logger.error('AI prioritization failed', { error, userId });
       return NextResponse.json(
         { success: false, error: 'Failed to prioritize tasks' },
         { status: 500 }
       );
     }
     ```

**Success Criteria**:
- All CRUD endpoints working
- AI features functional
- Proper error handling
- Type-safe throughout
- Caching reduces costs
- Retries handle rate limits

**Measurements**:
- API response times: Target <500ms
- Type errors: 0
- Cached tokens vs. uncached: 50%+ reduction
- Retry success rate: 100%

---

### Phase 3: Sub-Agents & Streaming (Test Patterns 9-10)

**Duration**: 2-3 hours

#### Tasks

1. **Refactor with Sub-Agents**

   - **Test Pattern 9 (Sub-Agents)**:
     ```typescript
     // Instead of one large context:

     // Sub-agent 1: Schema queries
     const schemaAgent = createSubAgent({
       systemPrompt: "You help with database queries",
       context: prismaSchema
     });

     // Sub-agent 2: API logic
     const apiAgent = createSubAgent({
       systemPrompt: "You help with API endpoints",
       context: apiPatterns
     });

     // Sub-agent 3: AI features
     const aiAgent = createSubAgent({
       systemPrompt: "You help with AI integration",
       context: claudePatterns
     });
     ```

   - **Measure**: Cost reduction from context isolation
   - **Target**: 70-80% savings on repeated queries

2. **Add Streaming for AI Features**

   - **Test Pattern 10 (Streaming)**:
     ```typescript
     export async function POST(req: Request) {
       const stream = await anthropic.messages.stream({
         model: 'claude-sonnet-4',
         messages: [{ role: 'user', content: prompt }],
         max_tokens: 1024,
       });

       return new Response(
         stream.toReadableStream(),
         { headers: { 'Content-Type': 'text/event-stream' } }
       );
     }
     ```

   - **Measure**: Time to first byte (TTFB)
   - **Target**: <200ms vs. 2-3s for full response

**Success Criteria**:
- Sub-agents isolate context successfully
- Streaming provides progressive results
- Cost reduced from context management
- User experience improved with streaming

**Measurements**:
- Context tokens before/after: 70%+ reduction
- TTFB: <200ms
- User-perceived latency: 50%+ improvement
- Total cost: 70-80% reduction

---

### Phase 4: Testing & Hooks (Test Patterns 14-15)

**Duration**: 2-3 hours

#### Tasks

1. **Set Up Hooks**

   - **Test Pattern 14 (Type Check Hook)**:

     Create `.claude/hooks/type-check.py`:
     ```python
     #!/usr/bin/env python3
     import subprocess, sys, json

     event_data = json.loads(sys.stdin.read())
     file_path = event_data.get('tool_input', {}).get('path', '')

     if file_path.endswith(('.ts', '.tsx')):
         result = subprocess.run(['tsc', '--noEmit'], capture_output=True)
         if result.returncode != 0:
             print(result.stderr, file=sys.stderr)
             sys.exit(2)  # Blocking error
     sys.exit(0)
     ```

   - **Test Pattern 15 (Security Scan Hook)**:

     Create `.claude/hooks/security-scan.py`:
     ```python
     #!/usr/bin/env python3
     import re, sys, json

     event_data = json.loads(sys.stdin.read())
     file_path = event_data.get('tool_input', {}).get('path', '')

     with open(file_path, 'r') as f:
         content = f.read()

     issues = []

     # Check for hardcoded API keys
     if re.search(r'api[_-]?key\s*=\s*["\'][^"\']+["\']', content, re.I):
         issues.append("Hardcoded API key found")

     # Check for SQL injection
     if re.search(r'SELECT.*\$\{', content):
         issues.append("Possible SQL injection")

     if issues:
         for issue in issues:
             print(f"❌ {issue}", file=sys.stderr)
         sys.exit(2)  # Blocking

     sys.exit(0)
     ```

2. **Write Tests**

   Create comprehensive test suite:
   - Unit tests for each endpoint
   - Integration tests for AI features
   - Mock external API calls
   - Test error handling paths

3. **Validate Hooks Work**

   - Introduce a type error → Hook should block commit
   - Add hardcoded API key → Security hook should block
   - Fix issues → Hooks should pass
   - Commit successfully

**Success Criteria**:
- Type check hook catches TypeScript errors
- Security hook catches vulnerabilities
- All tests pass
- CI/CD ready

**Measurements**:
- Type errors caught before commit: 100%
- Security issues caught: 100%
- Test coverage: >80%
- False positive rate: <5%

---

## 📊 Validation Methodology

### A/B Comparison

We'll build the project **twice** to compare:

#### Approach A: Without Patterns (Baseline)
- Vague prompts
- No structure
- No MCP
- No hooks
- Random model selection
- No checkpoints

#### Approach B: With All 15 Patterns
- Structured prompts
- XML tags
- Context7 MCP
- Type check + security hooks
- Sonnet-first strategy
- Git checkpoints

### Metrics to Track

| Metric | Baseline | With Patterns | Target Improvement |
|--------|----------|---------------|-------------------|
| Development Time | ? | ? | 30% faster |
| First-Try Accuracy | ? | ? | 40% better |
| Type Errors | ? | ? | 80% fewer |
| Security Issues | ? | ? | 100% caught |
| Total Cost | ? | ? | 50% reduction |
| Code Quality (linting) | ? | ? | 90%+ pass rate |
| Test Coverage | ? | ? | 80%+ |
| Rollback Needed | ? | 0 | 100% safety |

---

## ✅ Success Criteria

### Pattern-Specific Success

Each pattern must demonstrate:

1. **Document Positioning**:
   - ✅ Prompts with docs first have 30%+ better accuracy
   - ✅ Measure: Compare response quality scores

2. **Few-Shot Examples**:
   - ✅ Prompts with 3-5 examples complete tasks 25%+ faster
   - ✅ Measure: Time to acceptable solution

3. **XML Tag Structure**:
   - ✅ Structured prompts get 20%+ better responses
   - ✅ Measure: Quality scoring by independent reviewer

4. **Context7 MCP**:
   - ✅ No outdated API recommendations
   - ✅ All suggestions match current docs

5. **Sonnet-First Strategy**:
   - ✅ 40-50% cost reduction vs. Opus-only
   - ✅ Quality difference: <10%

6. **Chain-of-Thought**:
   - ✅ Complex tasks have 15%+ better reasoning
   - ✅ Fewer logical errors

7. **5-Component Prompt**:
   - ✅ Consistent response format
   - ✅ All requirements addressed

8. **Git Checkpoint**:
   - ✅ 100% ability to rollback bad changes
   - ✅ Zero lost work

9. **Sub-Agents**:
   - ✅ 70-80% token cost reduction
   - ✅ Same quality as monolithic approach

10. **Streaming Responses**:
    - ✅ TTFB <200ms (vs. 2-3s for complete)
    - ✅ Better perceived performance

11. **Prompt Caching**:
    - ✅ 50%+ token reduction on repeated prompts
    - ✅ Zero quality loss

12. **Retry Logic**:
    - ✅ 100% rate limit recovery
    - ✅ All requests eventually succeed

13. **Error Handling**:
    - ✅ No unhandled exceptions
    - ✅ User-friendly error messages

14. **Type Check Hooks**:
    - ✅ 100% of type errors caught before commit
    - ✅ <5% false positives

15. **Security Scanning**:
    - ✅ 100% of test vulnerabilities caught
    - ✅ OWASP compliance

### Overall Project Success

- ✅ All CRUD operations working
- ✅ AI features functional and accurate
- ✅ Test coverage >80%
- ✅ Zero type errors in production code
- ✅ Zero security vulnerabilities
- ✅ Documentation complete
- ✅ Deployment-ready

---

## 📈 Expected Outcomes

### Quantified Improvements

Based on our pattern validation:

| Metric | Expected Outcome |
|--------|------------------|
| **Development Speed** | 30-40% faster than baseline |
| **Code Accuracy** | 35-40% better first-try success |
| **Total Cost** | 50-60% reduction (Sonnet + caching + sub-agents) |
| **Type Safety** | 80% fewer runtime type errors |
| **Security** | 100% of common vulnerabilities caught |
| **Debugging Time** | 50% reduction (hooks catch early) |
| **Rollback Safety** | 100% (git checkpoints) |
| **Documentation Quality** | 40% improvement (Context7 MCP) |

### Qualitative Improvements

- **Confidence**: High confidence in generated code quality
- **Maintainability**: Type-safe, well-structured code
- **Security**: Production-ready security posture
- **Developer Experience**: Smooth workflow with immediate feedback
- **Reliability**: Error handling ensures stability

---

## 📋 Testing Checklist

Before declaring validation complete:

### Pattern Validation

- [ ] All 15 patterns tested in real scenarios
- [ ] Metrics collected for each pattern
- [ ] A/B comparison completed
- [ ] Results documented with evidence

### Code Quality

- [ ] All tests passing
- [ ] Type checking passes
- [ ] Linting passes
- [ ] Security scan passes
- [ ] Code review completed

### Documentation

- [ ] README with setup instructions
- [ ] API documentation
- [ ] Pattern usage documented
- [ ] Metrics and results recorded

### Deployment

- [ ] Builds successfully
- [ ] Environment variables documented
- [ ] Database migrations work
- [ ] Health checks implemented

---

## 🔬 Data Collection Template

For each pattern, collect:

```markdown
## Pattern: [Name]

### Test Scenario
[What we tested]

### Methodology
[How we tested it]

### Baseline Measurement
- Metric 1: [Value]
- Metric 2: [Value]

### With Pattern Measurement
- Metric 1: [Value]
- Metric 2: [Value]

### Improvement
- Metric 1: +[X]% improvement
- Metric 2: +[X]% improvement

### Observations
**What worked well**:
- [Observation]

**What didn't work**:
- [Issue]

**Edge cases**:
- [Edge case]

### Confidence Assessment
- [ ] Pattern validated as documented
- [ ] Pattern needs refinement
- [ ] Pattern not validated

### Evidence
- Screenshots: [Link]
- Metrics CSV: [Link]
- Code diff: [Commit hash]
```

---

## 🎯 Next Steps After Validation

### If Patterns Validate Successfully

1. **Update Confidence Levels**: Promote patterns to "Verified in Production"
2. **Document Learnings**: Add insights to playbook
3. **Create Case Study**: Document this validation as case study
4. **Share Results**: Publish metrics and findings
5. **Update Pattern Index**: Mark patterns as production-validated

### If Patterns Need Refinement

1. **Document Issues**: Record what didn't work
2. **Adjust Patterns**: Refine based on learnings
3. **Re-test**: Validate adjustments
4. **Update Playbook**: Improve documentation
5. **Add Caveats**: Document limitations

### If Patterns Don't Validate

1. **Root Cause Analysis**: Why didn't it work?
2. **Alternative Approaches**: Research other methods
3. **Update Confidence**: Lower confidence level
4. **Document Failure**: Transparency about limitations
5. **Mark for Removal**: Consider deprecating pattern

---

## 📁 Project Deliverables

At project completion, deliver:

1. **Source Code**
   - Complete working API
   - All tests
   - Configuration files
   - Git history with checkpoints

2. **Validation Report**
   - Metrics for all 15 patterns
   - A/B comparison results
   - Screenshots and evidence
   - Lessons learned

3. **Documentation**
   - README with setup
   - API documentation
   - Pattern usage examples
   - Troubleshooting guide

4. **Case Study** (using template from CONTRIBUTING.md)
   - Project overview
   - Patterns used
   - Results
   - Recommendations

---

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- PostgreSQL 14+
- Anthropic API key
- Context7 MCP installed
- Git configured

### Setup Steps

1. **Clone and Initialize**
   ```bash
   git clone [repo]
   cd task-management-api
   npm install
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Add ANTHROPIC_API_KEY
   # Add DATABASE_URL
   ```

3. **Set Up Database**
   ```bash
   npx prisma migrate dev
   ```

4. **Install Hooks**
   ```bash
   chmod +x .claude/hooks/*.py
   # Configure in Claude Code settings
   ```

5. **Start Development**
   ```bash
   claude_checkpoint "Project setup complete"
   npm run dev
   ```

---

## 📞 Questions & Support

- **Pattern Questions**: See `synthesis/pattern-index.md`
- **Code Examples**: See `synthesis/code-snippets/`
- **Troubleshooting**: See playbook chapters
- **Issues**: Open GitHub issue

---

## 📊 Timeline Summary

| Phase | Duration | Patterns Tested | Key Deliverable |
|-------|----------|-----------------|-----------------|
| Phase 1: Setup & Schema | 2 hours | 1-5, 8 | Database schema |
| Phase 2: API Implementation | 3-4 hours | 6-7, 11-13 | CRUD endpoints |
| Phase 3: Sub-Agents & Streaming | 2-3 hours | 9-10 | Optimized architecture |
| Phase 4: Testing & Hooks | 2-3 hours | 14-15 | Production-ready code |
| **Total** | **9-12 hours** | **All 15** | **Complete validation** |

---

**Status**: 🟡 Ready for execution
**Validation Team**: TBD
**Start Date**: TBD
**Expected Completion**: TBD

**Last Updated**: 2025-11-14
**Version**: 1.0

[Back to README](../README.md) | [Pattern Index](../synthesis/pattern-index.md) | [Contributing](../CONTRIBUTING.md)
