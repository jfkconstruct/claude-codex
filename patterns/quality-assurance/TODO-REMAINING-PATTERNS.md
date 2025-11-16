---
status: TODO - Future Implementation
priority: Medium
estimated_effort: 4-6 hours total
date_created: 2024-11-14
---

# Remaining Security & Debugging Patterns

This document outlines the remaining patterns identified for security and debugging workflows. These patterns have been deprioritized based on Pareto analysis (80/20 rule) but remain valuable for future implementation.

---

## Pattern 1: Edge Case Discovery

**Category**: Quality Assurance
**Difficulty**: Intermediate
**Impact**: Medium
**Estimated Effort**: 2-3 hours

### Overview

A systematic approach to using Claude to identify edge cases, boundary conditions, and unusual inputs that could break your code. This pattern helps find bugs before they reach production by exploring the "what if" scenarios developers often miss.

### Why This Pattern Matters

Edge cases account for a disproportionate number of production bugs. While developers focus on the "happy path," edge cases like:
- Empty arrays/objects
- Null/undefined values
- Maximum/minimum values
- Special characters in strings
- Concurrent operations
- Network timeouts
- Race conditions

...often cause unexpected failures. Claude can systematically explore these scenarios.

### Core Concept

Ask Claude to analyze your code and generate a comprehensive list of edge cases, then help you:
1. Identify which edge cases are handled
2. Find which edge cases are missing handling
3. Generate test cases for each edge case
4. Implement defensive code for critical edge cases
5. Document assumptions and limitations

### Example Prompt Template

```markdown
Please analyze this function and identify all edge cases:

```[language]
[your code]
```

For each edge case:
1. Describe the scenario
2. Show what would happen currently
3. Indicate severity (Critical/High/Medium/Low)
4. Suggest how to handle it
5. Provide test case

Consider:
- Null/undefined inputs
- Empty collections
- Boundary values (0, negative, max int)
- Invalid types
- Concurrent access
- Network failures
- Resource exhaustion
```

### Key Use Cases

- New feature development (before writing tests)
- Code review (find missed edge cases)
- Refactoring (ensure edge cases still covered)
- Bug investigation (what edge case triggered this?)
- API design (what inputs must we handle?)

### Related Patterns

- Testing Strategies (write tests for discovered edge cases)
- Code Review (edge case coverage checklist)
- Error Handling (how to handle edge cases gracefully)
- Input Validation (prevent edge cases at boundaries)

### Example Scenarios

**Function**: User signup
**Edge Cases to Explore**:
- Email already exists
- Password too weak/strong/long
- Special characters in name
- Simultaneous signups with same email
- Database connection fails mid-transaction
- Email service unavailable
- User clicks submit button twice

**Function**: Array sorting
**Edge Cases to Explore**:
- Empty array
- Single element
- All elements identical
- Already sorted (ascending/descending)
- Contains null/undefined
- Very large array (performance)
- Floating point precision issues

### Future Implementation Notes

When implementing this pattern, include:
- Custom Claude command for edge case analysis
- Checklist of common edge case categories
- Integration with test generation
- Examples from different domains (API, UI, data processing)
- Template for documenting edge case handling decisions
- Best practices for prioritizing which edge cases to handle

---

## Pattern 2: Debugging Workflow

**Category**: Quality Assurance
**Difficulty**: Intermediate
**Impact**: Medium
**Estimated Effort**: 2-3 hours

### Overview

A structured debugging workflow that uses Claude as a debugging partner to systematically isolate, identify, and fix bugs. This pattern provides a step-by-step process for debugging complex issues, from symptom identification to root cause resolution.

### Why This Pattern Matters

Debugging is often ad-hoc and inefficient. Developers:
- Jump to conclusions without systematic analysis
- Fix symptoms instead of root causes
- Waste time on trial-and-error approaches
- Don't learn from debugging sessions
- Struggle to communicate debugging progress

A structured workflow makes debugging faster, more thorough, and educational.

### Core Concept

Follow a systematic debugging process with Claude:

1. **Symptom Identification**
   - What's the observable problem?
   - How does it manifest?
   - When does it occur?

2. **Information Gathering**
   - Relevant code
   - Error messages and stack traces
   - Application logs
   - Recent changes
   - Environment details

3. **Hypothesis Generation**
   - Ask Claude for possible causes
   - Rank hypotheses by likelihood
   - Identify evidence that would confirm/refute each

4. **Systematic Testing**
   - Test hypotheses in order
   - Collect evidence
   - Eliminate possibilities

5. **Root Cause Identification**
   - Identify the fundamental cause
   - Distinguish from symptoms

6. **Solution Implementation**
   - Fix root cause
   - Add defensive code
   - Write regression test

7. **Documentation**
   - Document the bug and fix
   - Share learnings with team
   - Update debugging knowledge base

### Example Workflow Template

```markdown
# Debugging Session

## 1. Symptom
- What: [description]
- Where: [location in app]
- When: [conditions]
- Frequency: [always/intermittent]

## 2. Gather Information
@Claude: Help me gather relevant information for debugging this issue.

- Stack trace: [paste]
- Logs: [paste relevant logs]
- Code: [relevant code]
- Changes: [recent commits]

## 3. Generate Hypotheses
@Claude: What are the most likely causes of this issue? Rank them by probability.

## 4. Test Hypotheses
Testing hypothesis #1: [description]
Evidence: [what we found]
Result: [confirmed/refuted]

## 5. Root Cause
@Claude: Based on the evidence, what's the root cause?

## 6. Solution
@Claude: Suggest a fix that addresses the root cause.

[Implement fix]

## 7. Verify & Document
- [ ] Fix verified
- [ ] Regression test added
- [ ] Documentation updated
```

### Key Debugging Scenarios

**Scenario 1: Intermittent Failures**
- Collect multiple failure instances
- Look for patterns in timing, data, environment
- Use Claude to correlate patterns
- Identify race conditions, timing issues, resource contention

**Scenario 2: "It Works on My Machine"**
- Document environment differences
- Ask Claude to identify which differences matter
- Reproduce in similar environment
- Fix environment-specific assumptions

**Scenario 3: Performance Degradation**
- Gather performance metrics
- Identify when degradation started
- Use Claude to analyze profiler data
- Find O(n²) algorithms, N+1 queries, memory leaks

**Scenario 4: Integration Issues**
- Isolate which system is failing
- Test each integration point independently
- Use Claude to analyze API responses, contracts
- Identify version mismatches, schema changes

### Debugging Techniques to Include

- Binary search (comment out code sections)
- Rubber duck debugging (explain to Claude)
- Time-travel debugging (use git bisect)
- Differential debugging (working vs. broken)
- Logging instrumentation (strategic log placement)
- Breakpoint strategies (conditional, exception)

### Related Patterns

- Error Interpretation (understand error messages)
- Testing Strategies (write test that reproduces bug)
- Code Review (catch bugs before they exist)
- Logging Patterns (what to log for debugging)

### Future Implementation Notes

When implementing this pattern, include:
- Custom Claude command for guided debugging
- Debugging session template (markdown)
- Common debugging patterns (race conditions, memory leaks, etc.)
- Integration with git bisect for regression finding
- Examples from different bug categories
- Debugging checklists for different scenarios
- Best practices for documenting debugging sessions

---

## Prioritization Rationale (Pareto Analysis)

These patterns were deprioritized because:

### Edge Case Discovery
- **High value** but **overlaps** with existing patterns:
  - Testing Strategies (covers test case generation)
  - Code Review (includes edge case checking)
  - Input Validation (handles boundary conditions)
- **Specialized use case**: Most valuable during new feature development
- **Medium frequency**: Used less often than daily debugging/security review

### Debugging Workflow
- **High value** but **overlaps significantly** with Error Interpretation:
  - Error Interpretation covers 80% of debugging scenarios
  - Debugging Workflow is more comprehensive but also more complex
  - Error Interpretation is faster for common cases
- **Higher complexity**: Requires more structure and discipline
- **Learning curve**: Teams need training to follow systematic process

### Why Completed Patterns Were Higher Priority

1. **Security Review (OWASP)**: Universal, prevents critical production issues
2. **Input Validation**: Foundational, prevents most common vulnerabilities
3. **Error Interpretation**: Daily use, immediate productivity impact

These three patterns deliver 80% of the value in security and debugging workflows.

---

## Recommended Implementation Timeline

**Phase 1 (Completed)**:
- ✅ Security Review (OWASP Top 10)
- ✅ Input Validation & Sanitization
- ✅ Error Interpretation

**Phase 2 (Next Sprint - 4-6 hours)**:
- ⏸ Edge Case Discovery
- ⏸ Debugging Workflow

**Phase 3 (Future)**:
- Performance Debugging
- Integration Testing Patterns
- Security Regression Testing
- Log Analysis Patterns

---

## How to Contribute

If you'd like to implement these patterns:

1. Follow the pattern template at `/patterns/PATTERN_TEMPLATE.md`
2. Include real-world examples from actual debugging sessions
3. Add custom Claude commands for automation
4. Provide checklists and quick reference guides
5. Link to related patterns
6. Submit PR with completed pattern

---

## Notes for Future Implementation

### Edge Case Discovery Pattern

**Key sections to include**:
- Comprehensive edge case checklist (by category: nulls, boundaries, concurrency, errors, performance)
- Examples from different domains (API, UI, data processing, async operations)
- Integration with test generation (turn edge cases into test cases)
- Prioritization framework (which edge cases must be handled vs. can be documented)

**Custom command idea**:
```bash
/find-edge-cases [function-name]
# Analyzes function and generates comprehensive edge case list
```

### Debugging Workflow Pattern

**Key sections to include**:
- Step-by-step debugging process with Claude
- Templates for different bug types (crash, performance, integration, concurrency)
- Integration with git bisect for regression hunting
- Log analysis techniques
- Performance profiling interpretation

**Custom command idea**:
```bash
/debug-session
# Starts guided debugging session with structured questions
```

---

## Related Research

From `/synthesis/research-priorities.md`:
- Testing Strategies are Priority 2 (High) - Edge Case Discovery fits here
- Error Handling Patterns are Priority 3 (High) - Debugging Workflow relates

From `/synthesis/pattern-index.md`:
- Pattern #10: Double-Check / Self-Validation - Related to edge case discovery
- Pattern #24: Validation Gates - Automated testing of edge cases

---

**Status**: Ready for implementation when team capacity allows
**Last Updated**: 2024-11-14
**Maintainer**: Claude Coding Knowledge Base Project
