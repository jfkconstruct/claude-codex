# Pattern Quality Assessment Rubric

**Purpose**: Evaluate pattern quality and completeness for the Claude Coding Master Playbook

**Version**: 1.0
**Last Updated**: 2025-11-14

---

## 📊 Overall Scoring

Patterns are evaluated across 5 dimensions with a total possible score of **100 points**:

| Dimension | Max Points | Weight | Description |
|-----------|------------|--------|-------------|
| **Evidence Quality** | 25 | 25% | Source validation, empirical data |
| **Practical Applicability** | 25 | 25% | Real-world usefulness, scope |
| **Documentation Clarity** | 20 | 20% | Writing quality, completeness |
| **Code Example Quality** | 20 | 20% | If applicable - code quality |
| **Source Diversity** | 10 | 10% | Independent validation |

### Score Interpretation

| Total Score | Rating | Confidence Level | Action |
|-------------|--------|------------------|--------|
| 90-100 | **Excellent** | ⭐⭐⭐⭐⭐ Very High | Include in playbook, highlight |
| 75-89 | **Good** | ⭐⭐⭐⭐ High | Include in playbook |
| 60-74 | **Acceptable** | ⭐⭐⭐ Medium | Include with caveats |
| 45-59 | **Needs Improvement** | ⭐⭐ Low | Refine before including |
| 0-44 | **Insufficient** | ⭐ Very Low | Reject or major revision |

---

## 1️⃣ Evidence Quality (25 points)

### Criteria

Evidence quality measures the strength of support for the pattern's claims.

#### 1.1 Source Authority (10 points)

**10 points** - Official Anthropic documentation
- Primary source from Anthropic
- Current and maintained
- Explicitly documented

**8 points** - Recognized industry expert
- Well-known practitioner
- Demonstrated expertise
- Peer-reviewed or widely cited

**6 points** - Community consensus
- Multiple independent sources
- Consistent across sources
- Established practice

**4 points** - Individual experience
- Single practitioner
- Documented experience
- Not widely validated

**2 points** - Anecdotal
- No clear source
- Single mention
- Unverified claim

**0 points** - No source
- No attribution
- Pure speculation
- Contradicts known facts

#### 1.2 Empirical Data (10 points)

**10 points** - Rigorous quantification
- A/B tested with controls
- Statistical significance
- Reproducible methodology
- Sample size documented

**8 points** - Measured improvement
- Quantified results (e.g., "30% faster")
- Methodology described
- Multiple test cases
- Consistent results

**6 points** - Observational data
- Informal measurements
- Pattern noticed repeatedly
- General trend documented
- No formal testing

**4 points** - Qualitative assessment
- Subjective improvement noted
- No measurements
- Experience-based claim
- "Seems to work better"

**2 points** - Theoretical basis
- Logical reasoning only
- No practical testing
- Based on model architecture understanding
- Plausible but unverified

**0 points** - No data
- No evidence of effectiveness
- Untested hypothesis
- Pure conjecture

#### 1.3 Consistency Across Sources (5 points)

**5 points** - 7+ independent sources agree
- Multiple independent validations
- Consistent findings
- No contradictions

**4 points** - 5-6 sources agree
- Good validation
- Minor variations in implementation
- Core concept consistent

**3 points** - 3-4 sources agree
- Moderate validation
- Some variations
- General agreement on approach

**2 points** - 1-2 sources
- Limited validation
- May have contradictions
- Needs more research

**0 points** - Conflicting sources
- Sources disagree
- Contradictory evidence
- Unclear which approach is correct

### Evidence Quality Score: ___ / 25

---

## 2️⃣ Practical Applicability (25 points)

### Criteria

Practical applicability measures how useful the pattern is in real-world scenarios.

#### 2.1 Scope & Generality (8 points)

**8 points** - Universally applicable
- Works for all Claude Code users
- No special prerequisites
- Applies to most tasks
- Examples: XML tags, few-shot examples

**6 points** - Broadly applicable
- Works for most users
- Minimal prerequisites
- Common use case
- Examples: Streaming, error handling

**4 points** - Specific use case
- Applies to particular scenarios
- Some prerequisites
- Useful but not universal
- Examples: MCP servers, hooks

**2 points** - Narrow application
- Very specific scenario
- Significant prerequisites
- Niche use case
- Limited audience

**0 points** - Rarely applicable
- Almost never relevant
- Extreme edge case
- Very specific conditions

#### 2.2 Implementation Difficulty (8 points)

**8 points** - Trivial to implement
- No setup required
- Immediate use
- Zero learning curve
- Example: "Add 'think step-by-step' to prompt"

**6 points** - Easy to implement
- Minimal setup (5-10 minutes)
- Copy-paste ready
- Clear instructions
- Example: Using XML tags

**4 points** - Moderate effort
- Some setup required (30-60 minutes)
- Configuration needed
- Learning curve exists
- Example: Setting up MCP servers

**2 points** - Significant effort
- Substantial setup (2+ hours)
- Complex configuration
- Steep learning curve
- Example: Advanced sub-agent architecture

**0 points** - Impractical difficulty
- Extremely complex
- High risk
- Not worth the effort
- Better alternatives exist

#### 2.3 Impact vs. Effort Ratio (9 points)

**9 points** - High impact, low effort
- Significant improvement (20%+)
- Easy to implement
- Quick wins
- Examples: Document positioning, few-shot examples

**7 points** - High impact, moderate effort
- Significant improvement (20%+)
- Some setup required
- Worth the investment
- Examples: Context7 MCP, prompt caching

**5 points** - Moderate impact, low effort
- Modest improvement (10-20%)
- Easy to implement
- Nice to have
- Examples: Specific phrasing patterns

**3 points** - Moderate impact, moderate effort
- Modest improvement (10-20%)
- Some setup required
- Marginal value
- Use case dependent

**1 point** - Low impact, any effort
- Minimal improvement (<10%)
- Not worth the time
- Better alternatives exist

**0 points** - No impact
- Doesn't improve results
- Wasted effort
- Anti-pattern

### Practical Applicability Score: ___ / 25

---

## 3️⃣ Documentation Clarity (20 points)

### Criteria

Documentation clarity measures how well the pattern is explained.

#### 3.1 Writing Quality (5 points)

**5 points** - Excellent writing
- Clear and concise
- No ambiguity
- Professional tone
- Error-free grammar
- Logical flow

**4 points** - Good writing
- Mostly clear
- Minor ambiguities
- Good structure
- Few grammatical errors

**3 points** - Adequate writing
- Generally understandable
- Some confusion
- Acceptable structure
- Several grammatical errors

**2 points** - Poor writing
- Often unclear
- Significant ambiguity
- Weak structure
- Many errors

**0 points** - Incomprehensible
- Cannot understand
- Incoherent
- Unusable

#### 3.2 Completeness (10 points)

**Pattern includes all essential components:**

- [ ] **Clear title** (1 point): Descriptive, specific name
- [ ] **Description** (2 points): What the pattern is, why it works
- [ ] **When to use** (2 points): Specific scenarios and conditions
- [ ] **How to implement** (2 points): Step-by-step instructions
- [ ] **Example** (2 points): Concrete before/after demonstration
- [ ] **Troubleshooting** (1 point): Common issues and solutions

**Scoring**:
- 10 points: All 6 components present and well-developed
- 8 points: 5 components present
- 6 points: 4 components present
- 4 points: 3 components present
- 2 points: 2 components present
- 0 points: 1 or fewer components

#### 3.3 Structure & Organization (5 points)

**5 points** - Excellent structure
- Follows playbook template exactly
- Logical section order
- Easy to scan
- Proper heading hierarchy
- Good use of formatting (bold, code blocks, lists)

**4 points** - Good structure
- Mostly follows template
- Logical organization
- Scannable
- Minor formatting issues

**3 points** - Adequate structure
- Basic organization
- Somewhat hard to scan
- Inconsistent formatting

**2 points** - Poor structure
- Disorganized
- Hard to follow
- Formatting problems

**0 points** - No structure
- Random organization
- Unusable layout

### Documentation Clarity Score: ___ / 20

---

## 4️⃣ Code Example Quality (20 points)

### Criteria

Code example quality measures the quality of code provided (if applicable).

**Note**: If pattern doesn't require code examples (e.g., conceptual prompting patterns), redistribute these 20 points to other categories or score N/A.

#### 4.1 Code Correctness (8 points)

**8 points** - Production-ready code
- Compiles/runs without errors
- Handles all edge cases
- No security vulnerabilities
- Follows best practices
- Type-safe

**6 points** - Good code
- Works correctly
- Handles common cases
- Minor issues
- Mostly type-safe

**4 points** - Functional code
- Works for basic cases
- Some edge cases missed
- Has issues but usable

**2 points** - Buggy code
- Errors present
- Missing key functionality
- Needs significant fixes

**0 points** - Broken code
- Doesn't work
- Major errors
- Unusable

#### 4.2 Code Clarity & Style (7 points)

**7 points** - Excellent code
- Self-documenting
- Well-commented
- Follows language conventions
- Consistent style
- Easy to understand
- Proper naming

**5 points** - Good code
- Mostly clear
- Some comments
- Generally good style
- Minor inconsistencies

**3 points** - Acceptable code
- Understandable with effort
- Few comments
- Style issues
- Inconsistent

**1 point** - Poor code
- Hard to understand
- No comments
- Bad naming
- Style problems

**0 points** - Incomprehensible
- Cannot understand
- Unmaintainable

#### 4.3 Completeness & Usability (5 points)

**5 points** - Complete & copy-paste ready
- All imports included
- Dependencies documented
- Configuration specified
- Error handling included
- Can use immediately

**4 points** - Nearly complete
- Most imports included
- Minor gaps
- Mostly copy-paste ready

**3 points** - Partial
- Missing some imports
- Requires adaptation
- Usable with work

**2 points** - Incomplete
- Many gaps
- Significant work needed
- Proof-of-concept only

**0 points** - Unusable
- Too many gaps
- Can't use as-is

### Code Example Quality Score: ___ / 20

---

## 5️⃣ Source Diversity (10 points)

### Criteria

Source diversity measures independent validation across different origins.

#### 5.1 Number of Independent Sources (6 points)

**6 points** - 7+ independent sources
- Highly validated
- Consensus pattern
- Very high confidence

**5 points** - 5-6 independent sources
- Well validated
- Strong confidence

**4 points** - 3-4 independent sources
- Moderate validation
- Medium confidence

**3 points** - 2 independent sources
- Limited validation
- Needs more research

**2 points** - 1 source
- Single source
- Low confidence
- Unverified

**0 points** - 0 sources or same source repeated
- No validation
- Cannot verify

#### 5.2 Source Type Diversity (4 points)

**Award 1 point for each different source type (max 4)**:

- [ ] Official Anthropic documentation
- [ ] Community expert (blog, video)
- [ ] Open source code examples
- [ ] Research paper or study
- [ ] Production case study
- [ ] Community discussion (Reddit, forums)

**Scoring**:
- 4 points: 4+ different source types
- 3 points: 3 source types
- 2 points: 2 source types
- 1 point: 1 source type
- 0 points: No sources or all same type

### Source Diversity Score: ___ / 10

---

## 📋 Complete Rubric Score Sheet

### Pattern Information

- **Pattern Name**: ___________________________
- **Category**: ___________________________
- **Evaluator**: ___________________________
- **Date**: ___________________________

### Dimension Scores

| Dimension | Points Earned | Max Points | Percentage |
|-----------|---------------|------------|------------|
| 1. Evidence Quality | ___ | 25 | ___% |
| 2. Practical Applicability | ___ | 25 | ___% |
| 3. Documentation Clarity | ___ | 20 | ___% |
| 4. Code Example Quality | ___ | 20 | ___% |
| 5. Source Diversity | ___ | 10 | ___% |
| **TOTAL** | **___** | **100** | **___%** |

### Final Rating

Based on total score:

- [ ] **Excellent (90-100)**: ⭐⭐⭐⭐⭐ Very High Confidence
- [ ] **Good (75-89)**: ⭐⭐⭐⭐ High Confidence
- [ ] **Acceptable (60-74)**: ⭐⭐⭐ Medium Confidence
- [ ] **Needs Improvement (45-59)**: ⭐⭐ Low Confidence
- [ ] **Insufficient (0-44)**: ⭐ Very Low Confidence

### Recommendation

- [ ] **Include in playbook** - Ready as-is
- [ ] **Include with revisions** - Minor improvements needed
- [ ] **Major revision required** - Significant work needed
- [ ] **Reject** - Does not meet minimum standards

### Detailed Feedback

**Strengths**:
-
-
-

**Weaknesses**:
-
-
-

**Improvement Suggestions**:
-
-
-

**Overall Assessment**:


---

## 🎯 Example Evaluations

### Example 1: Document Positioning Pattern

#### Pattern Information
- **Pattern Name**: Document Positioning (Large Docs First)
- **Category**: Prompting Techniques
- **Evaluator**: Playbook Team
- **Date**: 2025-11-14

#### Detailed Scores

**1. Evidence Quality: 24/25**
- Source Authority (10/10): Official Anthropic documentation
- Empirical Data (9/10): 30% improvement quantified, methodology clear
- Consistency (5/5): 6 sources agree

**2. Practical Applicability: 24/25**
- Scope & Generality (8/8): Universal - all users benefit
- Implementation Difficulty (8/8): Trivial - just reorder prompt
- Impact vs. Effort (8/9): High impact, zero effort (perfect ROI)

**3. Documentation Clarity: 19/20**
- Writing Quality (5/5): Clear, concise, professional
- Completeness (9/10): All components present, could add more examples
- Structure (5/5): Perfect template adherence

**4. Code Example Quality: 18/20**
- Correctness (8/8): Perfect example code
- Clarity (6/7): Very clear, minor improvements possible
- Completeness (4/5): Slightly incomplete imports

**5. Source Diversity: 10/10**
- Number of Sources (6/6): 6 independent sources
- Type Diversity (4/4): Official docs, experts, case studies, discussions

**TOTAL: 95/100 - Excellent ⭐⭐⭐⭐⭐**

**Recommendation**: Include in playbook - Highlight as top pattern

---

### Example 2: Hypothetical Low-Quality Pattern

#### Pattern Information
- **Pattern Name**: "Always Use Haikus in Prompts"
- **Category**: Prompting Techniques
- **Evaluator**: Playbook Team
- **Date**: 2025-11-14

#### Detailed Scores

**1. Evidence Quality: 4/25**
- Source Authority (2/10): Single blog post
- Empirical Data (0/10): No measurements
- Consistency (2/5): Only one source

**2. Practical Applicability: 8/25**
- Scope & Generality (2/8): Very narrow use case
- Implementation Difficulty (6/8): Easy to implement
- Impact vs. Effort (0/9): No demonstrated impact

**3. Documentation Clarity: 12/20**
- Writing Quality (3/5): Adequate writing
- Completeness (6/10): Missing troubleshooting, when to use
- Structure (3/5): Acceptable structure

**4. Code Example Quality: N/A**
- No code needed for this pattern

**5. Source Diversity: 2/10**
- Number of Sources (2/6): One source
- Type Diversity (0/4): Single blog post

**TOTAL: 26/80* - Insufficient ⭐**
(*Code quality not applicable, scored out of 80)

**Recommendation**: Reject - Insufficient evidence, no demonstrated value

---

## 📊 Batch Evaluation Template

For evaluating multiple patterns at once:

| Pattern | Evidence | Practical | Docs | Code | Sources | Total | Rating | Action |
|---------|----------|-----------|------|------|---------|-------|--------|--------|
| Pattern 1 | /25 | /25 | /20 | /20 | /10 | /100 | ⭐ | Include/Revise/Reject |
| Pattern 2 | /25 | /25 | /20 | /20 | /10 | /100 | ⭐ | Include/Revise/Reject |
| Pattern 3 | /25 | /25 | /20 | /20 | /10 | /100 | ⭐ | Include/Revise/Reject |
| Pattern 4 | /25 | /25 | /20 | /20 | /10 | /100 | ⭐ | Include/Revise/Reject |
| Pattern 5 | /25 | /25 | /20 | /20 | /10 | /100 | ⭐ | Include/Revise/Reject |

**Average Score**: ___ / 100
**Patterns Included**: ___
**Patterns Needing Revision**: ___
**Patterns Rejected**: ___

---

## 🔄 Continuous Improvement

### Re-evaluation Triggers

Patterns should be re-evaluated when:

1. **New Evidence Emerges**
   - New sources validate or contradict
   - Quantified measurements become available
   - Official documentation changes

2. **Community Feedback**
   - Users report issues
   - Edge cases discovered
   - Better implementations found

3. **Claude Updates**
   - New model versions
   - API changes
   - Feature additions/removals

4. **Time-Based**
   - Every 6 months for all patterns
   - Every 3 months for medium confidence
   - Monthly for low confidence

### Version History

Track pattern quality over time:

| Date | Version | Score | Changes | Evaluator |
|------|---------|-------|---------|-----------|
| 2025-11-14 | 1.0 | 95/100 | Initial | Team |
| 2025-XX-XX | 1.1 | XX/100 | Updated evidence | Name |

---

## 🎓 Evaluator Guidelines

### Before Evaluating

1. **Read the pattern completely**
2. **Check all cited sources**
3. **Test code examples** (if applicable)
4. **Review related patterns**
5. **Consider your own experience**

### During Evaluation

1. **Be objective**: Base scores on criteria, not personal preference
2. **Be consistent**: Use same standards for all patterns
3. **Be thorough**: Check all dimensions carefully
4. **Be fair**: Give credit where due, note weaknesses honestly
5. **Document**: Explain scores in feedback section

### After Evaluating

1. **Review scores**: Do they reflect overall quality?
2. **Write feedback**: Provide constructive comments
3. **Make recommendation**: Clear action item
4. **Submit evaluation**: Add to tracking sheet

### Common Pitfalls to Avoid

- **Halo effect**: Don't let one dimension influence others
- **Leniency bias**: Don't inflate scores
- **Strictness bias**: Don't be overly harsh
- **Central tendency**: Use full range (not everything is 60-70)
- **Recency bias**: Don't favor recently discovered patterns

---

## 📞 Questions & Support

- **Rubric Questions**: Open GitHub issue
- **Scoring Disputes**: Request second evaluation
- **Rubric Improvements**: Submit PR with proposed changes

---

**Rubric Version**: 1.0
**Last Updated**: 2025-11-14
**Maintained By**: Claude Coding Playbook Team

[Back to README](../README.md) | [Contributing Guidelines](../CONTRIBUTING.md) | [Pattern Index](../synthesis/pattern-index.md)
