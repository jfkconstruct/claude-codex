---
pattern_name: Test-Driven Development (TDD) with Claude
category: Testing
difficulty: Intermediate
impact: High
date_created: 2025-11-14
last_updated: 2025-11-14
---

# Pattern: Test-Driven Development (TDD) with Claude

> **TL;DR**: Write tests before implementation by having Claude generate tests from specifications, then implement code to pass those tests—resulting in better design, fewer bugs, and living documentation.

## Overview

Test-Driven Development (TDD) with Claude transforms the traditional TDD workflow by leveraging AI to rapidly generate comprehensive test suites from specifications. Instead of manually writing every test, you describe expected behavior to Claude, review the generated tests, then implement code to make them pass.

This pattern follows the classic Red-Green-Refactor cycle:
1. **Red**: Claude generates failing tests from specifications
2. **Green**: You (or Claude) implement code to pass tests
3. **Refactor**: Improve code while tests ensure behavior is maintained

According to **Anthropic's official agentic coding best practices (April 2025)**, TDD with Claude is significantly more powerful than manual TDD because:
- Claude generates comprehensive test suites in minutes (not hours)
- Tests cover edge cases systematically (humans often forget)
- Explicit about TDD prevents Claude from creating mock implementations
- Tests serve as precise specifications for implementation
- Catches misunderstandings early (in tests, before code exists)

Research shows teams using TDD produce 40-80% fewer bugs and have more maintainable code. Adding Claude to TDD accelerates the process while maintaining quality.

---

## Problem It Solves

### The Challenge

Traditional TDD is powerful but time-consuming and often abandoned because:
- Writing tests first feels slower than diving into code
- Developers skip TDD under deadline pressure
- Manual test writing is tedious and error-prone
- Hard to write comprehensive tests without implementation insight
- TDD discipline is difficult to maintain consistently

**Common Symptoms:**
- Tests written after implementation (test-last, not TDD)
- Tests that don't catch bugs (written to pass existing code)
- Incomplete test coverage (edge cases skipped)
- Code that's hard to test (not designed with testability in mind)
- Refactoring fear (tests don't provide safety net)

**Without This Pattern:**
- TDD feels too slow, gets abandoned
- Tests don't drive design (written after implementation)
- Missing edge cases discovered in production
- Code tightly coupled (not designed for testability)
- Technical debt accumulates (hard to refactor without tests)

### Why Traditional Approaches Fall Short

**Manual TDD**: Slow, test-writing bottleneck prevents momentum

**Test-Last**: Tests validate existing code, don't drive better design

**Skip Testing**: Fast initially, but bugs and refactoring fears slow everything later

**Partial TDD**: Inconsistently applied, loses design benefits

---

## The Solution

### Core Concept

Use Claude to **generate comprehensive test suites from specifications** before any implementation exists. This combines the design benefits of TDD with the speed of AI-assisted test generation.

The workflow:
1. **Specify**: Describe what the code should do (requirements, API contract, behavior)
2. **Generate Tests**: Claude creates comprehensive failing tests
3. **Review Tests**: Verify tests match your intent
4. **Implement**: Write (or Claude writes) code to pass tests
5. **Refactor**: Improve code, tests ensure behavior preserved

Claude's role:
- Generates tests from specifications (Red phase)
- Can implement code to pass tests (Green phase)
- Suggests refactorings (Refactor phase)
- Ensures tests don't create mock implementations

### Key Principles

1. **Test-First Always**: Tests exist before implementation, no exceptions
2. **Specification-Driven**: Tests are generated from clear behavior specifications
3. **Comprehensive Coverage**: Claude systematically considers edge cases
4. **Explicit About TDD**: Tell Claude "we're doing TDD" to avoid mock implementations
5. **Red-Green-Refactor**: Follow classic TDD cycle with AI acceleration

### How It Works

**Traditional TDD** (manual):
```
Specify → Write Tests (slow) → Implement → Refactor
```

**TDD with Claude** (accelerated):
```
Specify → Claude Generates Tests (fast) → Review → Implement → Refactor
```

---

## Implementation

### Basic Implementation

**Scenario**: Building a shopping cart total calculator

#### Step 1: Specify Behavior

Create a clear specification:

```markdown
## Shopping Cart Total Calculator

Function: calculateCartTotal(items, taxRate)

Behavior:
- Input: Array of items (each has price, quantity), taxRate (decimal)
- Output: Object with { subtotal, tax, total }
- Business Rules:
  - subtotal = sum of (price * quantity) for all items
  - tax = subtotal * taxRate
  - total = subtotal + tax
  - All amounts rounded to 2 decimal places

Edge Cases:
- Empty cart should return { subtotal: 0, tax: 0, total: 0 }
- Negative prices/quantities should throw error
- Invalid taxRate should throw error
```

#### Step 2: Generate Tests with Claude

**Prompt**:
```
We're doing Test-Driven Development. Please generate Jest tests for the calculateCartTotal function based on this specification:

[paste specification]

Important: We're following TDD, so:
- Generate tests that will FAIL initially (no implementation exists yet)
- Do NOT create mock implementations
- Cover all specified behaviors and edge cases
- Tests should precisely specify expected behavior

Please generate comprehensive tests.
```

#### Step 3: Review Generated Tests

Claude generates:

```javascript
// tests/calculateCartTotal.test.js
import { calculateCartTotal } from '../src/calculateCartTotal';

describe('calculateCartTotal', () => {
  describe('Basic calculations', () => {
    test('should calculate total for single item', () => {
      const items = [{ price: 10.00, quantity: 2 }];
      const result = calculateCartTotal(items, 0.08);

      expect(result).toEqual({
        subtotal: 20.00,
        tax: 1.60,
        total: 21.60
      });
    });

    test('should calculate total for multiple items', () => {
      const items = [
        { price: 10.00, quantity: 2 },
        { price: 5.50, quantity: 3 }
      ];
      const result = calculateCartTotal(items, 0.10);

      expect(result).toEqual({
        subtotal: 36.50,
        tax: 3.65,
        total: 40.15
      });
    });

    test('should round amounts to 2 decimal places', () => {
      const items = [{ price: 10.99, quantity: 3 }];
      const result = calculateCartTotal(items, 0.085);

      expect(result).toEqual({
        subtotal: 32.97,
        tax: 2.80,  // 32.97 * 0.085 = 2.80245, rounded to 2.80
        total: 35.77
      });
    });
  });

  describe('Edge cases', () => {
    test('should return zeros for empty cart', () => {
      const result = calculateCartTotal([], 0.08);

      expect(result).toEqual({
        subtotal: 0,
        tax: 0,
        total: 0
      });
    });

    test('should handle zero tax rate', () => {
      const items = [{ price: 10.00, quantity: 1 }];
      const result = calculateCartTotal(items, 0);

      expect(result).toEqual({
        subtotal: 10.00,
        tax: 0,
        total: 10.00
      });
    });
  });

  describe('Error handling', () => {
    test('should throw error for negative price', () => {
      const items = [{ price: -10.00, quantity: 2 }];

      expect(() => calculateCartTotal(items, 0.08))
        .toThrow('Price cannot be negative');
    });

    test('should throw error for negative quantity', () => {
      const items = [{ price: 10.00, quantity: -2 }];

      expect(() => calculateCartTotal(items, 0.08))
        .toThrow('Quantity cannot be negative');
    });

    test('should throw error for invalid tax rate (negative)', () => {
      const items = [{ price: 10.00, quantity: 2 }];

      expect(() => calculateCartTotal(items, -0.08))
        .toThrow('Tax rate must be between 0 and 1');
    });

    test('should throw error for invalid tax rate (> 1)', () => {
      const items = [{ price: 10.00, quantity: 2 }];

      expect(() => calculateCartTotal(items, 1.5))
        .toThrow('Tax rate must be between 0 and 1');
    });
  });
});
```

**Review**: Tests look good! They cover:
- ✅ Basic calculations (single item, multiple items, rounding)
- ✅ Edge cases (empty cart, zero tax)
- ✅ Error cases (negative values, invalid tax rate)
- ✅ No mock implementation (tests will fail until we write real code)

#### Step 4: Run Tests (Red Phase)

```bash
npm test

# All tests fail (expected!):
# FAIL tests/calculateCartTotal.test.js
# ● calculateCartTotal › Basic calculations › should calculate total for single item
#   Cannot find module '../src/calculateCartTotal'
```

**Perfect!** Tests are red (failing) as expected in TDD.

#### Step 5: Implement Code (Green Phase)

Now implement to make tests pass:

**Option A: Write Code Yourself**
```javascript
// src/calculateCartTotal.js
export function calculateCartTotal(items, taxRate) {
  // Validate tax rate
  if (taxRate < 0 || taxRate > 1) {
    throw new Error('Tax rate must be between 0 and 1');
  }

  // Validate items
  for (const item of items) {
    if (item.price < 0) {
      throw new Error('Price cannot be negative');
    }
    if (item.quantity < 0) {
      throw new Error('Quantity cannot be negative');
    }
  }

  // Calculate subtotal
  const subtotal = items.reduce((sum, item) => {
    return sum + (item.price * item.quantity);
  }, 0);

  // Calculate tax
  const tax = subtotal * taxRate;

  // Calculate total
  const total = subtotal + tax;

  // Round to 2 decimal places
  return {
    subtotal: Math.round(subtotal * 100) / 100,
    tax: Math.round(tax * 100) / 100,
    total: Math.round(total * 100) / 100
  };
}
```

**Option B: Ask Claude to Implement**
```
Here are the tests we generated:

[paste tests]

Please implement the calculateCartTotal function to make all tests pass.
Do NOT create a mock implementation. Write the real business logic.
```

#### Step 6: Run Tests (Green Phase)

```bash
npm test

# PASS tests/calculateCartTotal.test.js
# ✓ All 10 tests passing
```

**Success!** All tests pass (green).

#### Step 7: Refactor (Refactor Phase)

Now that tests pass, refactor for better code quality:

**Prompt to Claude**:
```
The calculateCartTotal function works (all tests pass), but could it be improved?

Please suggest refactorings for:
- Readability
- Performance
- Maintainability
- Code organization

Ensure all tests still pass after refactoring.
```

**Claude suggests**:
```javascript
// src/calculateCartTotal.js (refactored)

// Extract validation
function validateTaxRate(taxRate) {
  if (taxRate < 0 || taxRate > 1) {
    throw new Error('Tax rate must be between 0 and 1');
  }
}

function validateItem(item) {
  if (item.price < 0) {
    throw new Error('Price cannot be negative');
  }
  if (item.quantity < 0) {
    throw new Error('Quantity cannot be negative');
  }
}

// Extract rounding
function roundToTwoDecimals(value) {
  return Math.round(value * 100) / 100;
}

// Main function (cleaner)
export function calculateCartTotal(items, taxRate) {
  validateTaxRate(taxRate);
  items.forEach(validateItem);

  const subtotal = items.reduce((sum, item) =>
    sum + (item.price * item.quantity), 0
  );

  const tax = subtotal * taxRate;
  const total = subtotal + tax;

  return {
    subtotal: roundToTwoDecimals(subtotal),
    tax: roundToTwoDecimals(tax),
    total: roundToTwoDecimals(total)
  };
}
```

Run tests again:
```bash
npm test
# ✓ All tests still pass (tests ensure refactoring didn't break anything)
```

**TDD Cycle Complete!** ✅ Red → Green → Refactor

---

### Advanced Implementation

**Scenario**: Building a user authentication API endpoint

#### Step 1: Create Detailed Specification

```markdown
## POST /api/auth/login

### Request Body
{
  "email": "string (required)",
  "password": "string (required)"
}

### Behavior
1. Validate email format
2. Validate password not empty
3. Check user exists in database
4. Verify password hash matches
5. Create JWT token with user ID
6. Return token + user info

### Success Response (200)
{
  "token": "jwt-token-string",
  "user": {
    "id": "user-id",
    "email": "user@example.com",
    "name": "User Name"
  }
}

### Error Responses
- 400: Missing email or password, invalid email format
- 401: Invalid credentials (user not found or password wrong)
- 429: Rate limit exceeded (5 attempts per 15 minutes per IP)
- 500: Server error

### Security Requirements
- Never reveal whether email exists (always say "invalid credentials")
- Log failed login attempts
- Implement rate limiting per IP
- No password in response
- JWT expires in 24 hours
```

#### Step 2: Generate Comprehensive Tests

**Prompt**:
```
We're doing TDD for a user authentication endpoint. Generate comprehensive integration tests based on this spec:

[paste specification]

Framework: Jest + Supertest
Use mocks for: User database, bcrypt, JWT, rate limiter

This is TDD: generate FAILING tests, no mock implementation.
Be thorough with security scenarios.
```

**Claude generates** 20+ tests covering success, validation, security, rate limiting, and error cases.

#### Step 3-7: Follow Red-Green-Refactor Cycle

Same process as basic implementation, but with more complex scenarios.

---

## When to Use

### Ideal Use Cases

✅ **Use this pattern when:**
- Building new features from scratch
- Requirements are clear and well-specified
- Code quality and testability are priorities
- Working on critical business logic
- Building public APIs (tests = contract)
- Refactoring legacy code (tests = safety net)
- Teaching TDD to team (Claude accelerates learning)

### Indicators You Need This Pattern

- You often discover bugs after implementation
- Refactoring is scary (no test safety net)
- Code is tightly coupled (hard to test)
- Requirements are misunderstood after implementation
- Your test coverage is low (<70%)
- Code reviews find logic errors frequently

### Project Types

**Best For:**
- Business logic (payment processing, inventory, pricing)
- API endpoints (REST, GraphQL)
- Data transformations (ETL, validation)
- Security-critical code (authentication, authorization)
- Algorithmic code (calculations, parsing)

---

## When NOT to Use

### Avoid This Pattern When

❌ **Don't use this pattern if:**
- Prototyping/spike solutions (speed over quality)
- Requirements are vague or rapidly changing
- Code is UI-heavy with visual requirements
- Simple CRUD operations (TDD overhead not worth it)
- Throwaway code or experiments

### Simpler Alternatives

If TDD seems too heavyweight:
- **Test After**: Write implementation, then tests (faster but less design benefit)
- **Behavior-Driven Development (BDD)**: Higher-level specifications
- **Property-Based Testing**: For complex input spaces

---

## Best Practices

### Do's ✅

- **Be explicit**: Tell Claude "We're doing TDD" to prevent mock implementations
- **Start with specifications**: Clear requirements before tests
- **Review generated tests**: Ensure they match your intent
- **Run tests (Red)**: Verify tests fail before implementation
- **One cycle at a time**: Red → Green → Refactor, repeat
- **Small iterations**: Test one behavior, implement, test next behavior
- **Refactor confidently**: Tests ensure nothing breaks

### Don'ts ❌

- **Don't skip Red phase**: If tests pass immediately, they're testing nothing
- **Don't implement before tests**: Defeats TDD's design benefits
- **Don't skip Refactor**: Technical debt accumulates
- **Don't write tests that test implementation**: Test behavior, not internals
- **Don't generate tests from existing code**: That's not TDD, it's retrofitting tests

### Pro Tips 💡

**Tip 1: Start with API Contract**
```
Before any code, define the API contract:

Function signature:
processOrder(order: Order): OrderResult

Then generate tests from this contract.
```

**Tip 2: Use Specification-by-Example**
```
Generate TDD tests for user registration based on these examples:

Example 1: Valid registration
Input: { email: "test@example.com", password: "Secure123!" }
Output: { id: 1, email: "test@example.com" }

Example 2: Duplicate email
Input: { email: "existing@example.com", password: "..." }
Output: Error "Email already registered"

[more examples]
```

**Tip 3: Incremental TDD**
```
We're doing TDD in small steps:

Step 1: Generate tests for basic success case only
Step 2: Implement to pass basic tests
Step 3: Generate tests for edge case X
Step 4: Extend implementation for edge case X
...
```

**Tip 4: Test One Thing at a Time**
```
Generate a SINGLE test for: user login with valid credentials

Once that passes, we'll add the next test (invalid password).
```

---

## Metrics & Results

### Expected Improvements

Based on TDD research and Claude acceleration:

- **Bug Reduction**: 40-80% fewer defects (TDD research)
- **Design Quality**: Better modularity and testability
- **Refactoring Safety**: Tests enable fearless refactoring
- **Test Generation Speed**: 10x faster with Claude vs. manual
- **Edge Case Coverage**: 30-50% more edge cases caught
- **Documentation**: Tests serve as living documentation

**Source**: TDD studies + Anthropic agentic coding best practices

### Success Indicators

You'll know TDD with Claude is working when:
- Tests exist before implementation (every time)
- Test coverage is 80%+ consistently
- Refactoring doesn't break functionality (tests catch it)
- Fewer bugs discovered in QA/production
- New team members understand code via tests
- Code is modular and loosely coupled (testable design)

---

## Real-World Examples

### Example 1: Anthropic Engineering - TDD Best Practice

**Source**: Anthropic "Claude Code: Best practices for agentic coding" (April 2025)

**Recommendation**:
> "Test-driven development becomes even more powerful with agentic coding. Ask Claude to write tests based on expected input/output pairs. Be explicit about doing test-driven development, so it avoids creating mock implementations."

**Key Insights**:
- Anthropic engineers use TDD with Claude internally
- Explicit "we're doing TDD" prevents mock implementations
- Tests from specifications (input/output pairs) work best
- Significantly more powerful than traditional manual TDD

---

### Example 2: Fintech Startup - Payment Processing

**Context**: Building payment processing logic with strict correctness requirements

**Challenge**:
- Complex business rules (fees, currency conversion, refunds)
- Zero tolerance for calculation errors
- Multiple edge cases (partial refunds, failed payments, retries)

**Implementation**:
1. Created detailed specifications with examples
2. Used Claude to generate comprehensive test suites (Red)
3. Implemented payment logic to pass tests (Green)
4. Refactored for performance while tests ensured correctness (Refactor)

**Results**:
- 95% test coverage achieved
- Zero calculation bugs in production (6 months)
- Refactored twice confidently (tests caught regressions)
- Passed financial audits with test documentation
- Test generation time: 2 hours (vs. estimated 16 hours manual)

---

## Common Pitfalls & Solutions

### Pitfall 1: Tests Pass Immediately (Not TDD)

**Problem**: Generated tests pass right away, meaning they're not testing anything new.

**Solution**: Ensure tests are written before implementation exists.

```
// ❌ Wrong: Implementing first, then tests
implement calculateDiscount()
generate tests for calculateDiscount() // Tests pass immediately (test-last)

// ✅ Correct: Tests first (TDD)
generate tests for calculateDiscount() // Tests fail (no implementation)
implement calculateDiscount() // Now tests pass
```

---

### Pitfall 2: Claude Creates Mock Implementation

**Problem**: Claude generates tests with mock/stub implementations instead of real tests.

**Example**:
```javascript
// ❌ Mock implementation (not real TDD)
test('should calculate total', () => {
  const mockTotal = 100; // Just returns a mock value
  expect(calculateTotal()).toBe(mockTotal);
});
```

**Solution**: Be explicit with Claude.
```
Important: We're doing TDD. Do NOT create mock implementations.
Generate tests that will FAIL until we write the real code.
Tests should verify actual behavior, not mocks.
```

---

### Pitfall 3: Over-Testing Implementation Details

**Problem**: Tests are brittle, breaking when implementation changes even if behavior doesn't.

**Solution**: Test behavior, not implementation.
```
// ❌ Testing implementation (brittle)
test('should call database.query exactly once', () => {
  // Breaks if we optimize to cache results
});

// ✅ Testing behavior (robust)
test('should return user data for valid ID', () => {
  const user = getUserById(123);
  expect(user.id).toBe(123);
});
```

---

## Quick Reference

### TDD Cycle with Claude

```
1. SPECIFY
   ↓
   Write clear behavior specification

2. RED (Claude generates failing tests)
   ↓
   Prompt: "Generate TDD tests for [spec]. No mock implementations."
   ↓
   Review tests, run (should fail)

3. GREEN (Implement to pass)
   ↓
   Write code OR prompt: "Implement to pass these tests"
   ↓
   Run tests (should pass)

4. REFACTOR (Improve code)
   ↓
   Prompt: "Suggest refactorings while keeping tests passing"
   ↓
   Apply refactorings, run tests (should still pass)

5. REPEAT
   ↓
   Next behavior/feature
```

### Key Prompt Templates

**Generate Tests (Red Phase)**:
```
We're doing TDD. Generate [framework] tests for [function/feature] based on this specification:

[paste specification]

Important:
- Generate FAILING tests (no implementation exists)
- Do NOT create mock implementations
- Cover happy path, edge cases, and errors
- Follow TDD principles
```

**Implement Code (Green Phase)**:
```
Here are the TDD tests we generated:

[paste tests]

Please implement [function/feature] to make all tests pass.
Write real business logic, not mock implementations.
```

**Refactor (Refactor Phase)**:
```
All tests are passing. Please suggest refactorings to improve:
- Code readability
- Performance
- Maintainability

Ensure all tests still pass after refactoring.
```

---

## Further Reading

### Books
- "Test-Driven Development: By Example" by Kent Beck
- "Growing Object-Oriented Software, Guided by Tests" by Freeman & Pryce

### Articles
- [Anthropic: Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) - Official TDD guidance
- [Martin Fowler: Is TDD Dead?](https://martinfowler.com/articles/is-tdd-dead/) - TDD debate and nuances

### Related Patterns
- [Test Generation](/patterns/testing/test-generation.md) - Generate tests for existing code
- [Edge Case Discovery](/patterns/testing/edge-case-discovery.md) - Systematic edge case identification

---

## Sources & References

### Primary Sources

1. **Anthropic Official Best Practices (April 2025)**
   - Direct recommendation: "Test-driven development becomes even more powerful with agentic coding"
   - Key insight: "Be explicit about doing test-driven development, so it avoids creating mock implementations"
   - Source: anthropic.com/engineering/claude-code-best-practices

2. **TDD Research**
   - 40-80% defect reduction with TDD (Microsoft Research, IBM studies)
   - Better design modularity
   - Reduced debugging time

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-14 | Initial documentation based on Anthropic official best practices and TDD principles |

---

## Metadata

**Tags**: `tdd`, `test-driven-development`, `testing`, `red-green-refactor`, `agentic-coding`, `anthropic-best-practices`

**Prerequisites**:
- Understanding of TDD principles (Red-Green-Refactor)
- Familiarity with a testing framework
- Ability to write clear specifications

**Estimated Time to Learn**: 2-4 hours (basic TDD cycle)

**Skill Level**: Intermediate (TDD requires discipline and practice)

---

## Contributing

Found an improvement? Please contribute:
1. Share your TDD with Claude experiences
2. Add language-specific examples (Python, Go, Ruby, etc.)
3. Document TDD patterns for different domains
4. Add more refactoring patterns

---

**Pattern Template Version**: 1.0
**Last Updated**: 2025-11-14
**Maintainer**: Claude Coding Knowledge Base Project
