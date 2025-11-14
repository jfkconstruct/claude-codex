---
description: Review code for quality, security, and correctness
---

# Code Review Checklist

Review the recently modified files and check ALL of the following:

## Security
- [ ] No SQL injection vulnerabilities (use parameterized queries)
- [ ] No XSS vulnerabilities (sanitize user input)
- [ ] No hardcoded secrets or API keys
- [ ] Authentication properly enforced
- [ ] Authorization checks in place
- [ ] Sensitive data properly encrypted
- [ ] CSRF protection where needed
- [ ] Cryptographically secure random tokens

## Error Handling
- [ ] All async operations have try/catch
- [ ] Errors logged with sufficient context
- [ ] User-friendly error messages (no stack traces)
- [ ] Graceful degradation on failures
- [ ] Proper HTTP status codes
- [ ] Database errors properly handled
- [ ] Network failures handled

## Data Validation
- [ ] All user inputs validated
- [ ] Type checking with TypeScript
- [ ] Zod schemas for runtime validation
- [ ] Null/undefined checks where needed
- [ ] Array bounds checking
- [ ] Input sanitization

## Edge Cases
- [ ] Empty arrays/objects handled
- [ ] Null/undefined inputs handled
- [ ] Very large inputs handled (pagination?)
- [ ] Concurrent requests handled (race conditions?)
- [ ] Network failures handled
- [ ] Multiple simultaneous operations

## Performance
- [ ] No N+1 queries
- [ ] Database queries optimized
- [ ] Appropriate caching
- [ ] No unnecessary re-renders (React)
- [ ] Efficient algorithms (no O(n²) unless necessary)
- [ ] Resource cleanup (connections, timers)

## Code Quality
- [ ] Follows project coding standards
- [ ] Functions are single responsibility
- [ ] No code duplication
- [ ] Clear variable/function names
- [ ] Adequate comments for complex logic
- [ ] TypeScript types are explicit
- [ ] No magic numbers or strings

## Testing
- [ ] Unit tests exist and pass
- [ ] Integration tests if needed
- [ ] Edge cases covered by tests
- [ ] Happy path tested
- [ ] Error paths tested
- [ ] Test coverage acceptable

## Accessibility (if UI)
- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] ARIA labels where needed
- [ ] Color contrast sufficient
- [ ] Focus indicators visible

## Final Checks
- [ ] No console.log() or debugging code
- [ ] No commented-out code
- [ ] All TODOs have issue numbers
- [ ] Dependencies are necessary
- [ ] Breaking changes documented

---

After reviewing, provide:
1. List of issues found (with severity: CRITICAL, HIGH, MEDIUM, LOW)
2. Recommended fixes for each issue
3. Overall quality score (1-10)
4. Go/No-Go recommendation
