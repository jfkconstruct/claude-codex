# Prompt Templates for Claude Code

Reusable prompt structures for common tasks. Copy-paste and customize.

Source: Claude Coding Master Playbook, Chapter 2

---

## Template 1: Feature Implementation

```markdown
<context>
Project: [Project name and description]
Tech stack: [Framework, languages, libraries]
Relevant files:
- /path/to/file1.ts (existing component/module)
- /path/to/file2.ts (related code)
</context>

<task>
Implement [feature name] with the following requirements:

**Must Have**:
- Requirement 1: [Specific, measurable]
- Requirement 2: [Clear acceptance criteria]
- Requirement 3: [Well-defined scope]

**Nice to Have**:
- Optional feature 1
- Optional feature 2

**Out of Scope** (explicitly NOT doing):
- Thing we're NOT implementing
- Another thing to avoid
</task>

<examples>
Example of similar existing code:
\`\`\`typescript
// Show how we currently handle similar features
export function ExistingFeature() {
  // Implementation pattern
}
\`\`\`
</examples>

<constraints>
- Must maintain backward compatibility with [X]
- Follow existing [pattern name] pattern
- Use [specific library/approach]
- Keep bundle size under [X KB]
- Performance: [specific metric]
</constraints>

<format>
Please provide:
1. Implementation code
2. Tests (unit + integration)
3. Brief explanation of approach
4. Any assumptions made
5. Migration guide (if breaking changes)
</format>
```

---

## Template 2: Bug Fix

```markdown
**Bug Description**:
[What's broken? Be specific]

**Reproduction Steps**:
1. Step one
2. Step two
3. Observe error

**Expected Behavior**:
[What should happen instead]

**Actual Behavior**:
[What currently happens]

**Error Message** (if applicable):
\`\`\`
[Exact error message]
\`\`\`

**Relevant Code**:
File: /path/to/file.ts
\`\`\`typescript
// Paste the buggy code section
\`\`\`

**Environment**:
- OS: [macOS/Windows/Linux]
- Browser: [Chrome 120 / Firefox 121]
- Node version: [18.17.0]
- [Other relevant environment details]

**Please**:
1. Think step-by-step to identify root cause
2. Explain why the bug occurs
3. Provide the fix
4. Suggest how to prevent similar bugs (tests, types, validation)
5. Consider edge cases
```

---

## Template 3: Code Review

```markdown
**Review This Code**:

File: /path/to/file.ts
\`\`\`typescript
// Paste code to review (up to 500 lines)
\`\`\`

**Review Checklist**:

**Security**:
- [ ] SQL injection vulnerabilities?
- [ ] XSS vulnerabilities?
- [ ] Hardcoded secrets or API keys?
- [ ] Authentication properly enforced?
- [ ] Authorization checks in place?

**Quality**:
- [ ] Edge cases handled?
- [ ] Error handling comprehensive?
- [ ] Performance issues (N+1 queries, inefficient algorithms)?
- [ ] Code style matches project standards?
- [ ] Type safety (TypeScript errors)?

**Best Practices**:
- [ ] Functions have single responsibility?
- [ ] DRY principle followed (no duplication)?
- [ ] Clear naming (variables, functions, types)?
- [ ] Adequate comments for complex logic?
- [ ] Test coverage sufficient?

**Format**:
For each issue found, provide:
- **Severity**: Critical / High / Medium / Low
- **Description**: What's the issue?
- **Location**: Line number or code section
- **Suggested fix**: How to resolve it
- **Explanation**: Why this is an issue
```

---

## Template 4: Refactoring

```markdown
**Current Code**:
\`\`\`typescript
// Paste code to refactor
\`\`\`

**Refactoring Goals**:
- [ ] Improve type safety
- [ ] Reduce code duplication
- [ ] Better error handling
- [ ] Enhance readability
- [ ] Optimize performance
- [ ] [Other specific goals]

**Constraints**:
- Must maintain same public API
- Cannot introduce breaking changes
- Must improve or maintain test coverage
- Keep or reduce bundle size

**Provide**:
1. Refactored code
2. Side-by-side comparison (before/after)
3. Explanation of changes and benefits
4. Migration guide (if API changes slightly)
5. Updated tests (if needed)
```

---

## Template 5: Testing

```markdown
**Code to Test**:
File: /path/to/file.ts
\`\`\`typescript
// Function, component, or module to test
\`\`\`

**Testing Requirements**:

**Unit Tests**:
- [ ] Happy path (normal usage)
- [ ] Edge cases (boundary values)
- [ ] Error conditions
- [ ] Invalid inputs

**Integration Tests** (if applicable):
- [ ] API endpoint behavior
- [ ] Database operations
- [ ] External service calls

**E2E Tests** (if applicable):
- [ ] Critical user flows
- [ ] Multi-step processes

**Coverage Target**: 80% minimum

**Test Framework**: [Jest / Vitest / Mocha]

**Provide**:
1. Comprehensive test suite
2. Test descriptions that serve as documentation
3. Mock strategies for external dependencies
4. Test data/fixtures
5. Coverage report interpretation
```

---

## Template 6: Documentation

```markdown
**Code to Document**:
\`\`\`typescript
// Paste code
\`\`\`

**Documentation Requirements**:

**Function/Method Documentation**:
- Purpose and responsibility
- Parameter descriptions (types, constraints)
- Return value description
- Examples showing typical usage
- Examples showing edge cases
- Throws/Errors documentation

**Format** (JSDoc):
\`\`\`typescript
/**
 * Brief one-line description
 *
 * Longer description if needed, explaining:
 * - When to use this
 * - How it works internally (if complex)
 * - Performance considerations
 *
 * @param paramName - Description, constraints
 * @returns Description of return value
 * @throws {ErrorType} When and why this error occurs
 *
 * @example
 * // Basic usage
 * const result = functionName(arg);
 * // => expected output
 *
 * @example
 * // Edge case
 * const result = functionName(edgeCaseArg);
 * // => expected output
 *
 * @see Related documentation or functions
 */
\`\`\`

**Also Provide**:
- README section (if this is a new module)
- Usage guide for common scenarios
- Troubleshooting section (common issues)
```

---

## Template 7: API Endpoint

```markdown
**API Endpoint Specification**:

**Route**: [HTTP Method] /path/to/endpoint

**Description**: [What this endpoint does]

**Authentication**: [Required / Optional / Public]

**Request**:
\`\`\`typescript
// Request body schema
{
  field1: string;
  field2: number;
  // ...
}
\`\`\`

**Response** (Success):
\`\`\`typescript
// 200 OK
{
  success: true,
  data: {
    // Response data structure
  }
}
\`\`\`

**Response** (Error):
\`\`\`typescript
// 400/401/404/500
{
  success: false,
  error: "Error message",
  details: { /* optional */ }
}
\`\`\`

**Validation Rules**:
- field1: Required, email format
- field2: Required, positive integer
- [List all validation rules]

**Business Logic**:
1. Step one (e.g., validate input)
2. Step two (e.g., check permissions)
3. Step three (e.g., update database)
4. Step four (e.g., send notification)

**Error Cases**:
- 400: Invalid input (validation failed)
- 401: Unauthorized (no/invalid auth token)
- 403: Forbidden (insufficient permissions)
- 404: Resource not found
- 500: Server error

**Provide**:
1. Route handler implementation
2. Validation schema (Zod)
3. Tests for happy path + error cases
4. OpenAPI/Swagger documentation (optional)
```

---

## Template 8: Database Schema

```markdown
**Database Schema**:

**Table Name**: [table_name]

**Purpose**: [What this table stores]

**Fields**:
- id: UUID, primary key
- field1: VARCHAR(255), required, unique
- field2: INTEGER, required
- created_at: TIMESTAMP, default NOW()
- updated_at: TIMESTAMP, auto-update
- deleted_at: TIMESTAMP, nullable (soft delete)

**Relationships**:
- Belongs to: [other_table] (foreign key: [field])
- Has many: [other_table] (via [join_field])
- Has one: [other_table] (via [join_field])

**Indexes**:
- Primary: id
- Unique: field1
- Index: field2 (frequently queried)
- Composite: (field1, field2) for [specific query]

**Constraints**:
- field1 must be unique
- field2 must be positive
- [Other business rules]

**Provide** (Prisma):
1. Prisma schema definition
2. Migration file
3. Seed data (example records)
4. Query examples (common operations)
5. Type definitions (generated types)
```

---

## Template 9: Performance Optimization

```markdown
**Performance Issue**:
[What's slow? Specific metrics]

**Current Performance**:
- Metric 1: [e.g., API response time: 5s]
- Metric 2: [e.g., Page load: 8s]
- Metric 3: [e.g., Database query: 3s]

**Target Performance**:
- Metric 1: [e.g., < 500ms]
- Metric 2: [e.g., < 2s]
- Metric 3: [e.g., < 100ms]

**Profiling Data** (if available):
\`\`\`
// Paste profiler output or metrics
\`\`\`

**Current Implementation**:
\`\`\`typescript
// Code that needs optimization
\`\`\`

**Please**:
1. Identify bottlenecks (step-by-step analysis)
2. Propose optimization strategies
3. Implement optimizations
4. Explain trade-offs (complexity vs. performance)
5. Provide benchmarks (before/after)
6. Suggest monitoring approach
```

---

## Template 10: Architecture Decision

```markdown
**Decision Context**:
[What are we trying to accomplish?]

**Problem Statement**:
[What problem does this solve?]

**Constraints**:
- Constraint 1 (e.g., must support 10K concurrent users)
- Constraint 2 (e.g., budget: $500/month infrastructure)
- Constraint 3 (e.g., team has 2 backend developers)

**Options Considered**:

**Option 1: [Name]**
- Pros:
  - Benefit 1
  - Benefit 2
- Cons:
  - Drawback 1
  - Drawback 2
- Estimated cost: [$X/month]
- Estimated effort: [X developer-weeks]

**Option 2: [Name]**
- [Same structure as Option 1]

**Option 3: [Name]**
- [Same structure as Option 1]

**Evaluation Criteria**:
- Performance
- Cost
- Maintainability
- Team expertise
- Time to implement
- [Other relevant criteria]

**Please**:
1. Analyze each option against criteria
2. Provide recommendation with reasoning
3. Identify risks for recommended option
4. Suggest mitigation strategies
5. Propose proof-of-concept plan (if needed)
```

---

## Quick Reference: Prompt Components

Every effective prompt should include:

1. **Context**: What Claude needs to know
   - Tech stack
   - File paths
   - Existing patterns

2. **Task**: What you want accomplished
   - Clear, specific instructions
   - Success criteria
   - Scope (what's in, what's out)

3. **Examples**: What good looks like
   - 2-5 input/output pairs
   - Include edge cases
   - Show desired format

4. **Constraints**: What to follow/avoid
   - Coding standards
   - Performance requirements
   - Compatibility requirements

5. **Format**: How to structure response
   - What sections to include
   - Level of detail
   - Additional context needed

---

## Tips for Effective Prompts

**Be Explicit**:
- ✅ "Add email validation: must be valid email format, required field"
- ❌ "Add validation"

**Provide Context**:
- ✅ "This Next.js 14 app uses App Router, TypeScript, and Tailwind"
- ❌ "Fix the styling"

**Use Examples**:
- ✅ Show 3 examples of desired output
- ❌ Describe what you want in words only

**Think Step-by-Step**:
- ✅ "Think step-by-step: analyze, propose, implement"
- ❌ "Just fix it"

**Document Position**:
- ✅ `<documents>[big file]</documents><query>[question]</query>`
- ❌ `[question]<documents>[big file]</documents>`

---

**Related Resources**:
- Quick Reference Cheat Sheet: `../QUICK-REFERENCE.md`
- Decision Trees: `../decision-trees.md`
- Full Playbook: `../playbook/`
