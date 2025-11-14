---
title: Anthropic Official Prompt Engineering Patterns
source: Anthropic Documentation & Interactive Tutorial
date_extracted: 2024-11-14
type: pattern-extraction
applicability: Claude (all versions, with specific notes for Claude 4.x)
---

# Anthropic Official Prompt Engineering Patterns

This document extracts actionable patterns from Anthropic's official prompt engineering documentation. Each pattern includes context, implementation details, code examples, and practical applications.

---

## Pattern 1: Clear and Direct Instructions

### Context
Claude 4.x models have been trained for precise instruction following. Implicit or vague instructions lead to misinterpretation and poor results.

### Problem
Users often assume the model will infer intent, leading to outputs that miss the mark.

### Solution
State exactly what you want in simple, explicit language. Don't hint—tell.

### Implementation

**❌ Bad Example (Vague):**
```
Write something about customer service.
```

**✅ Good Example (Clear and Direct):**
```
Write a 500-word blog post about customer service best practices for e-commerce businesses.
Focus on response time, personalization, and proactive communication.
Use a professional but friendly tone. Include 3 specific actionable tips.
```

### Key Principles

1. **Specify format**: Length, structure, tone
2. **Define scope**: What to include/emphasize
3. **Set constraints**: What to avoid, boundaries
4. **Provide context**: Why this matters, who it's for

### When to Use
- All prompts, especially complex or high-stakes tasks
- When you need specific formatting or structure
- When working with business requirements

### Benefits
- Reduces ambiguity and misinterpretation
- Faster to good results (fewer iterations)
- More consistent outputs

---

## Pattern 2: XML Tags for Structure

### Context
Claude was specifically trained with XML tags in its training data, making it highly responsive to XML-structured prompts.

### Problem
Without clear separation, Claude may mix instructions with examples, or confuse context with tasks.

### Solution
Use XML tags to create clear boundaries between different prompt components.

### Implementation

**Basic Structure:**
```xml
<instructions>
Analyze the provided customer feedback and identify:
1. Main pain points
2. Feature requests
3. Sentiment (positive/negative/neutral)
</instructions>

<format>
Respond in JSON format with keys: pain_points, feature_requests, sentiment
</format>

<examples>
<example>
Input: "I love the app but it crashes when I upload large files"
Output: {
  "pain_points": ["App crashes with large files"],
  "feature_requests": [],
  "sentiment": "mixed"
}
</example>
</examples>

<feedback_to_analyze>
{{user's actual feedback here}}
</feedback_to_analyze>
```

### Common XML Tags

| Tag | Purpose | Example Use |
|-----|---------|-------------|
| `<instructions>` | Main task description | Define what Claude should do |
| `<context>` | Background information | Project details, constraints |
| `<examples>` | Few-shot examples | Show desired input/output |
| `<document>` | Reference material | Long texts to analyze |
| `<thinking>` | Scratchpad for reasoning | Show your work |
| `<answer>` | Final output | Separate reasoning from result |
| `<format>` | Output requirements | JSON, markdown, specific structure |

### Advanced Pattern: Thinking + Answer Separation

```xml
<instructions>
Solve this complex math problem. Show your work in <thinking> tags,
then provide the final answer in <answer> tags.
</instructions>

<problem>
If a train travels at 60 mph for 2.5 hours, then 45 mph for 1.5 hours,
what is the total distance traveled?
</problem>

<!-- Claude's response: -->
<thinking>
First segment: 60 mph × 2.5 hours = 150 miles
Second segment: 45 mph × 1.5 hours = 67.5 miles
Total: 150 + 67.5 = 217.5 miles
</thinking>

<answer>
The train traveled a total of 217.5 miles.
</answer>
```

### Benefits
- **Clarity**: Clear separation of prompt components
- **Accuracy**: Reduced misinterpretation
- **Flexibility**: Easy to modify specific sections
- **Post-processing**: Simpler to extract structured outputs

### When to Use
- Complex prompts with multiple components
- When you need structured output
- Multi-step reasoning tasks
- Document analysis with specific instructions

---

## Pattern 3: Few-Shot (Multishot) Prompting

### Context
Examples are one of the most powerful ways to guide Claude's behavior, especially for complex or nuanced tasks.

### Problem
Verbal descriptions of desired output may be ambiguous or incomplete.

### Solution
Provide 3-5 diverse, realistic examples showing the exact input/output pattern you want.

### Implementation

**Basic Few-Shot Pattern:**
```xml
<instructions>
Classify customer support tickets into categories: technical, billing, feature_request, or general.
</instructions>

<examples>
<example>
<input>My payment didn't go through but I was charged</input>
<output>billing</output>
</example>

<example>
<input>How do I export my data to CSV?</input>
<output>technical</output>
</example>

<example>
<input>It would be great if you added dark mode</input>
<output>feature_request</output>
</example>

<example>
<input>What are your business hours?</input>
<output>general</output>
</example>

<example>
<input>I keep getting error 503 when I try to login</input>
<output>technical</output>
</example>
</examples>

<ticket_to_classify>
{{actual ticket text}}
</ticket_to_classify>
```

### Best Practices

1. **Include edge cases**: Show tricky examples
2. **Be diverse**: Cover different scenarios
3. **Show complete pattern**: Full input + full output
4. **3-5 examples**: Sweet spot for most tasks
5. **More for complexity**: Complex tasks benefit from additional examples

### Advanced: Few-Shot with Format Specification

```xml
<task>
Extract key information from meeting notes and create action items.
</task>

<examples>
<example>
<notes>
Discussed Q4 budget. Sarah will prepare revised forecast by Friday.
Need to review vendor contracts before renewal deadline.
</notes>
<output>
Action Items:
- [ ] Sarah: Prepare revised Q4 budget forecast (Due: Friday)
- [ ] Team: Review vendor contracts before renewal deadline (Due: TBD)
</output>
</example>

<example>
<notes>
Product launch timeline discussed. Marketing needs final assets by Nov 20.
Engineering to complete testing by Nov 15. Legal review required.
</notes>
<output>
Action Items:
- [ ] Marketing: Provide final assets for product launch (Due: Nov 20)
- [ ] Engineering: Complete product testing (Due: Nov 15)
- [ ] Legal: Review product launch materials (Due: Before Nov 20)
</output>
</example>
</examples>

<meeting_notes>
{{actual notes}}
</meeting_notes>
```

### When to Use
- Classification tasks
- Format conversion
- Tone/style matching
- Complex reasoning patterns
- Any task where "show, don't tell" is more effective

### Benefits
- Dramatically improved accuracy
- Consistent formatting
- Fewer misinterpretations
- Better handling of edge cases

---

## Pattern 4: Chain of Thought (Step-by-Step Reasoning)

### Context
Complex reasoning tasks benefit from showing intermediate steps rather than jumping to conclusions.

### Problem
Direct answers on complex tasks are more likely to be incorrect or incomplete.

### Solution
Explicitly instruct Claude to think step-by-step, showing its reasoning process.

### Implementation

**Simple Pattern:**
```
<instructions>
Solve the following problem. Think step by step and show your reasoning.
</instructions>

<problem>
A store has a 20% off sale. An item originally costs $150.
After the sale, there's an additional 10% discount for members.
What's the final price for a member?
</problem>
```

**With XML Structure:**
```xml
<instructions>
Analyze whether this code has a security vulnerability.
Use <thinking> tags to show your step-by-step analysis,
then provide your conclusion in <answer> tags.
</instructions>

<code>
def process_user_input(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)
</code>

<!-- Claude's response: -->
<thinking>
1. Examining the query construction: Uses f-string to directly interpolate user_id
2. Checking for input sanitization: No validation or sanitization visible
3. Security implications: Direct string interpolation allows SQL injection
4. Attack scenario: User could provide "1 OR 1=1" to access all records
5. Severity: High - could expose entire user database
</thinking>

<answer>
Yes, this code has a critical SQL injection vulnerability. The user_id parameter
is directly interpolated into the SQL query without sanitization or parameterization.

Recommendation: Use parameterized queries instead:
```python
query = "SELECT * FROM users WHERE id = ?"
return db.execute(query, (user_id,))
```
</answer>
```

### Business Use Case: Insurance Claims

```xml
<role>
You are an insurance claims analyst. Evaluate claims systematically.
</role>

<instructions>
Review the claim and determine if it should be approved.
Think step by step in <thinking> tags, then provide your decision in <decision> tags.
</instructions>

<evaluation_criteria>
- Policy coverage matches claim type
- Claim amount within policy limits
- Required documentation provided
- No exclusions apply
</evaluation_criteria>

<claim>
Policy: Auto Insurance, $500 deductible, $50K coverage
Incident: Rear-ended at stoplight, repair estimate $3,200
Documentation: Police report, repair estimate, photos
</claim>
```

### Benefits
- **Accuracy**: 20%+ improvement in complex reasoning (per Anthropic case study)
- **Transparency**: See the reasoning process
- **Debugging**: Identify where logic goes wrong
- **Trust**: Auditable decision-making

### When to Use
- Mathematical calculations
- Code review and debugging
- Multi-criteria decisions
- Legal/compliance analysis
- Troubleshooting scenarios

---

## Pattern 5: Prefilling for Format Control

### Context
You can guide Claude's output by starting its response for it—a technique called "prefilling."

### Problem
Claude might choose an unexpected format or structure for its response.

### Solution
Begin Claude's response with the desired format, forcing it to continue in that pattern.

### Implementation

**Force JSON Output:**
```
User: Analyze this data and provide summary statistics in JSON format.

Data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

Assistant (prefilled): {
```

Claude will then continue the JSON: `"mean": 5.5, "median": 5.5, "min": 1, "max": 10}`

**Force Step-by-Step Thinking:**
```
User: Explain how photosynthesis works.

Assistant (prefilled): Let me break this down step by step:

1.
```

Claude continues with structured, numbered explanation.

**Maintain Character Voice:**
```
User: You are Sherlock Holmes. What do you observe about this crime scene?

Assistant (prefilled): Elementary, my dear Watson. Upon careful observation, I note
```

### Practical Applications

**API Integration (Force JSON):**
```python
# Prefill ensures valid JSON output every time
response = anthropic.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=[
        {"role": "user", "content": "Extract: Name, Email, Phone from: 'John Doe, john@example.com, 555-1234'"},
        {"role": "assistant", "content": "{"}  # Prefill
    ]
)
```

### Benefits
- **Format guarantee**: Force specific output structures
- **Consistency**: Same format every time
- **Efficiency**: Fewer tokens explaining format requirements
- **Control**: Direct Claude's approach from the start

### When to Use
- API responses requiring JSON/XML
- Maintaining consistent tone/voice
- Enforcing specific output structures
- Starting responses in a particular direction

---

## Pattern 6: Long Context Optimization

### Context
Claude 3 models support 200K token context windows, but performance varies based on how information is structured.

### Problem
Simply dumping large documents into prompts leads to poor recall and accuracy.

### Solution
Strategic positioning of documents and queries dramatically improves performance.

### Implementation

**Document Positioning (20K+ tokens):**
```xml
<!-- ✅ GOOD: Document first, query last -->
<document>
[Large document: 50,000 tokens of legal contract text]
</document>

<instructions>
Review the contract above and identify:
1. All liability limitations
2. Termination clauses
3. Any unusual or non-standard terms
</instructions>
```

**❌ Bad: Query before document:**
```xml
<instructions>
Identify liability limitations, termination clauses, and unusual terms.
</instructions>

<document>
[Large document...]
</document>
```

**Result**: Up to **30% accuracy improvement** by placing query at the end.

### Extract-Then-Answer Pattern

```xml
<instructions>
First, extract all relevant quotes from the document that pertain to the question.
Then, answer the question based solely on those quotes.
</instructions>

<document>
[50-page technical specification document]
</document>

<question>
What are the system's performance requirements under peak load?
</question>

<response_format>
Step 1 - Relevant Quotes:
<quotes>
[Extracted quotes here]
</quotes>

Step 2 - Answer:
<answer>
[Answer based on quotes]
</answer>
</response_format>
```

### Multi-Document Pattern

```xml
<!-- Documents at the beginning -->
<document id="contract_2023">
[Contract text...]
</document>

<document id="contract_2024">
[Contract text...]
</document>

<document id="amendment">
[Amendment text...]
</document>

<!-- Query at the end for best performance -->
<instructions>
Compare the 2023 and 2024 contracts, noting any changes in:
- Payment terms
- Deliverables
- Timelines

Then review the amendment and explain how it modifies the 2024 contract.
</instructions>
```

### Example Supplementation for Long Docs

```xml
<document>
[200-page product manual]
</document>

<example_questions>
<example>
Q: What is the warranty period for Model X?
A: According to page 47, Model X has a 2-year limited warranty covering manufacturing defects.
</example>

<example>
Q: How do I reset the device to factory settings?
A: Page 112 provides reset instructions: Hold the power button for 10 seconds while pressing the reset button.
</example>
</example_questions>

<actual_question>
What are the troubleshooting steps for error code E-23?
</actual_question>
```

### Benefits
- **30% accuracy boost**: From strategic positioning
- **Better recall**: Extract-then-answer grounds responses
- **Reduced hallucination**: Quotes ensure accuracy
- **Scalable**: Works with very large documents

### When to Use
- Documents over 20K tokens
- Multiple document analysis
- Technical specification review
- Legal/compliance document analysis
- Any task requiring precise citations

---

## Pattern 7: Avoiding Hallucinations

### Context
AI models can generate plausible-sounding but incorrect information when uncertain.

### Problem
Hallucinations erode trust and can have serious consequences in business contexts.

### Solution
Multiple techniques to ground responses and minimize fabrication.

### Implementation

**1. Permission to Say "I Don't Know"**
```xml
<instructions>
Answer the user's question based on the provided documentation.

IMPORTANT: If you cannot find the answer in the documentation,
say "I don't know" or "This information is not in the provided documentation."
Do not guess or use your general knowledge.
</instructions>

<documentation>
[Company's internal docs]
</documentation>

<question>
What is the company's policy on remote work?
</question>
```

**2. Restrict to Provided Sources**
```xml
<instructions>
You are a customer support agent. Answer questions using ONLY the information
in the knowledge base below. Do not use your general knowledge about the product.

If the answer is not in the knowledge base, direct the user to contact support@company.com.
</instructions>

<knowledge_base>
[Company KB articles]
</knowledge_base>
```

**3. Require Citations**
```xml
<instructions>
Analyze the research paper and answer the question.
For each claim in your answer, cite the specific section and page number.

Format: [Section X.Y, p. Z]
</instructions>

<paper>
[Academic paper text]
</paper>

<question>
What methodology did the researchers use?
</question>
```

**4. Post-Hoc Verification**
```xml
<instructions>
This is a two-step process:

Step 1: Answer the question based on the document.
Step 2: For each claim in your answer, find and quote the supporting text from the document.
If you cannot find supporting text for a claim, mark it as [UNVERIFIED] and retract it.
</instructions>

<document>
[Source document]
</document>

<question>
What are the key findings?
</question>
```

**5. Chain-of-Thought Verification**
```xml
<instructions>
Answer the question and show your reasoning step-by-step.
At each step, cite your source. If you realize you're making an unsupported assumption,
stop and indicate you don't have enough information.
</instructions>
```

### Temperature Adjustment

**Low Temperature (0.0-0.3)**: More consistent, less creative, fewer hallucinations
**High Temperature (0.7-1.0)**: More creative, varied, higher hallucination risk

```python
# For factual tasks, use low temperature
response = anthropic.messages.create(
    model="claude-3-5-sonnet-20241022",
    temperature=0.0,  # Most consistent
    messages=[...]
)
```

### Citations API Pattern

```python
# Using Anthropic's Citations API (Claude 3.5 Sonnet/Haiku)
response = anthropic.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {
                    "type": "text",
                    "text": document_content
                }
            },
            {
                "type": "text",
                "text": "What are the main conclusions?"
            }
        ]
    }]
)

# Response includes citations to specific document passages
# Up to 15% more accurate than manual citation methods
```

### Benefits
- **Trust**: Auditable, verifiable responses
- **Accuracy**: Grounded in actual sources
- **Compliance**: Critical for regulated industries
- **Debugging**: Easy to check where information came from

### When to Use
- Customer support (knowledge base answers)
- Legal/compliance work
- Medical/healthcare applications
- Financial advice
- Any high-stakes factual task

---

## Pattern 8: System Prompts and Role Assignment

### Context
System prompts set the overall behavior, persona, and constraints for Claude.

### Problem
Mixing high-level role definition with specific task instructions can be confusing.

### Solution
Use system prompts for broad role-setting; put specific instructions in user messages.

### Implementation

**System Prompt (High-Level Role):**
```python
system_prompt = """You are an expert Python code reviewer with 10+ years of experience.

Your focus areas:
- Security vulnerabilities (OWASP Top 10)
- Performance optimization
- Code maintainability and readability
- Best practices and design patterns

Your style:
- Constructive and educational
- Specific with examples
- Prioritize issues by severity
- Provide actionable recommendations

Always explain WHY something is a problem, not just WHAT is wrong."""

response = anthropic.messages.create(
    model="claude-3-5-sonnet-20241022",
    system=system_prompt,
    messages=[
        {"role": "user", "content": "Review this code:\n\n" + code_snippet}
    ]
)
```

**User Message (Specific Task):**
```python
user_message = """Review the following code for security issues.
Focus especially on input validation and SQL injection risks.

<code>
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)
</code>

Provide:
1. List of identified issues
2. Severity rating (Critical/High/Medium/Low)
3. Specific fix for each issue"""
```

### Advanced: Role with Examples

```python
system_prompt = """You are a technical writer specializing in API documentation.

Style guidelines:
- Active voice, present tense
- Short sentences (avg 15 words)
- No jargon without definition
- Include practical examples
- Address the developer directly ("you")

Here's an example of your writing style:

BAD: "The authenticate() method is utilized for user authentication purposes."
GOOD: "Use authenticate() to verify a user's credentials. Pass the username and password as strings."
"""
```

### Domain-Specific System Prompts

**Legal Assistant:**
```python
system_prompt = """You are a legal research assistant specializing in contract law.

Important constraints:
- You are NOT a licensed attorney and cannot provide legal advice
- Always recommend consulting with a qualified attorney for specific situations
- Cite specific laws, cases, or regulations when possible
- Distinguish between generally applicable principles and jurisdiction-specific rules
- Use clear language, explaining legal terms when first introduced
"""
```

**Financial Analyst:**
```python
system_prompt = """You are a financial analyst with expertise in equity valuation and risk assessment.

Analysis framework:
1. Always start with the specific numbers/data provided
2. Show your calculations explicitly
3. State assumptions clearly
4. Provide context (industry benchmarks, historical trends)
5. Note limitations of the analysis

Disclaimers:
- This is analytical commentary, not investment advice
- Past performance doesn't guarantee future results
- Multiple factors affect financial outcomes
"""
```

### Best Practices

1. **Be specific about expertise**: "Expert Python developer" not just "helpful assistant"
2. **Define constraints**: What Claude should NOT do
3. **Set tone/style**: Professional, friendly, concise, etc.
4. **Request specific structures**: "Always use <thinking> tags", "Cite sources"
5. **Include examples**: Show desired output style

### Benefits
- **Consistency**: Same behavior across conversations
- **Quality**: Expert-level responses
- **Safety**: Clear boundaries and disclaimers
- **Efficiency**: Don't repeat context in every message

### When to Use
- Building AI products (consistent persona)
- Domain-specific applications
- When you need specific tone/style
- Multi-turn conversations

---

## Pattern 9: Prompt Chaining for Complex Tasks

### Context
Complex workflows are often better handled as a sequence of focused prompts rather than one mega-prompt.

### Problem
Single prompts handling multiple complex steps can produce poor results or miss important details.

### Solution
Break tasks into sequential prompts, each handling one focused step, with outputs flowing to the next.

### Implementation

**Basic Chain Pattern:**

```python
# Step 1: Extract information
extraction_prompt = """
<document>
{research_paper}
</document>

Extract the following information:
- Research question
- Methodology
- Key findings
- Limitations

Format as JSON.
"""

extraction_result = claude(extraction_prompt)

# Step 2: Analyze extracted information
analysis_prompt = f"""
<extracted_info>
{extraction_result}
</extracted_info>

Analyze this research:
1. Assess methodology strength
2. Evaluate validity of conclusions
3. Identify potential biases
4. Rate overall quality (1-10)
"""

analysis_result = claude(analysis_prompt)

# Step 3: Generate recommendations
recommendation_prompt = f"""
<analysis>
{analysis_result}
</analysis>

Based on this analysis, provide:
1. Whether we should implement these findings in our product
2. What additional research is needed
3. Potential risks of implementation
"""

final_result = claude(recommendation_prompt)
```

**XML-Structured Chaining:**

```python
# Chain Step 1: Data collection
step1 = """
<task>Review customer feedback from Q4 and categorize complaints</task>

<feedback>
{customer_feedback_data}
</feedback>

Output format:
<categories>
  <category name="..." count="..." severity="...">
    <examples>...</examples>
  </category>
</categories>
"""

categories = claude(step1)

# Chain Step 2: Root cause analysis
step2 = f"""
<categorized_complaints>
{categories}
</categorized_complaints>

For each major category:
1. Identify root causes
2. Find patterns or common threads
3. Estimate business impact

<output_format>
<root_cause_analysis>
  <category name="...">
    <causes>...</causes>
    <patterns>...</patterns>
    <business_impact>...</business_impact>
  </category>
</root_cause_analysis>
</output_format>
"""

root_causes = claude(step2)

# Chain Step 3: Solution proposals
step3 = f"""
<root_causes>
{root_causes}
</root_causes>

For each identified root cause:
1. Propose 2-3 potential solutions
2. Estimate implementation effort (S/M/L)
3. Estimate impact (Low/Medium/High)
4. Identify dependencies

Prioritize by impact/effort ratio.
"""

solutions = claude(step3)
```

### Real-World Example: Code Review Chain

```python
# Stage 1: Security scan
security_check = """
<code>{code}</code>

Scan for security vulnerabilities:
- SQL injection
- XSS
- Command injection
- Path traversal
- Authentication issues

List ONLY the issues found, with line numbers.
"""

security_issues = claude(security_check)

# Stage 2: Performance analysis (if security passes)
if "No security issues" in security_issues:
    performance_check = f"""
    <code>{code}</code>

    Analyze performance:
    - O(n) complexity of algorithms
    - Database query efficiency
    - Memory usage patterns
    - Caching opportunities

    Focus on bottlenecks.
    """

    performance_analysis = claude(performance_check)

# Stage 3: Maintainability review
maintainability = f"""
<code>{code}</code>

<security_notes>{security_issues}</security_notes>
<performance_notes>{performance_analysis}</performance_notes>

Review code maintainability:
- Naming clarity
- Function size and complexity
- Documentation completeness
- Test coverage needs

Provide specific recommendations.
"""

final_review = claude(maintainability)
```

### Benefits
- **Quality**: Each step gets focused attention
- **Debugging**: Easy to identify which step failed
- **Flexibility**: Can adjust based on intermediate results
- **Modularity**: Reuse individual steps across workflows
- **Clarity**: Simpler prompts are more reliable

### When to Use
- Multi-step analysis workflows
- Decision trees (next step depends on previous result)
- Complex transformations (extract → transform → summarize)
- Quality gates (security check → performance check → approval)
- Research tasks (gather → analyze → synthesize)

---

## Pattern 10: Affirmative Instructions

### Context
Claude responds better to positive instructions (do this) than negative ones (don't do that).

### Problem
Negative instructions can confuse the model or paradoxically draw attention to the forbidden behavior.

### Solution
Frame instructions affirmatively, specifying desired behavior rather than forbidden behavior.

### Implementation

**❌ Negative (Less Effective):**
```
Don't be too technical. Don't use jargon. Don't make it too long.
Don't include irrelevant information.
```

**✅ Affirmative (More Effective):**
```
Use simple, everyday language. Explain technical terms when necessary.
Keep responses under 200 words. Focus only on information directly answering the question.
```

**More Examples:**

| Negative ❌ | Affirmative ✅ |
|------------|---------------|
| "Don't hallucinate" | "Base all answers on the provided documentation" |
| "Don't be rude" | "Use a professional and respectful tone" |
| "Don't give legal advice" | "Provide general information and recommend consulting an attorney" |
| "Avoid complex SQL" | "Use simple, readable SQL queries" |
| "Don't make assumptions" | "Ask clarifying questions when information is missing" |

### Real Example: Customer Support

**❌ Negative Framing:**
```python
system_prompt = """You are a customer support agent.

Rules:
- Don't make promises you can't keep
- Don't blame the customer
- Don't use technical jargon
- Don't provide information not in the knowledge base
- Don't end conversations without resolution
"""
```

**✅ Affirmative Framing:**
```python
system_prompt = """You are a customer support agent.

Guidelines:
- Set accurate expectations based on our capabilities
- Show empathy and take ownership of issues
- Use clear, simple language
- Base answers on our knowledge base
- Ensure the customer's issue is resolved or escalated before ending
"""
```

### Why It Works

1. **Cognitive framing**: Positive framing creates clearer mental models
2. **Reduces ambiguity**: "Do X" is clearer than "Don't do Y, Z, A, B..."
3. **Avoids priming**: Mentioning something (even negatively) can trigger it
4. **Action-oriented**: Gives Claude clear direction on what TO do

### Benefits
- **Clarity**: Less ambiguous instructions
- **Better compliance**: Model follows positive instructions more reliably
- **Simpler prompts**: Fewer edge cases to specify
- **Mental model alignment**: How humans naturally think about tasks

---

## Pattern 11: Example-First Documentation Analysis

### Context
When analyzing long documents with specific questions, providing relevant examples improves accuracy.

### Problem
Without examples, Claude may miss the expected format or level of detail in answers.

### Solution
Include examples of correctly answered questions about other parts of the document.

### Implementation

```xml
<document>
[100-page technical manual]
</document>

<example_qa>
<example>
<question>What is the maximum operating temperature?</question>
<answer>According to Section 3.2 (page 15), the maximum operating temperature
is 85°C (185°F). Operating above this temperature may cause thermal shutdown
or permanent damage.</answer>
<citation>Section 3.2, page 15</citation>
</example>

<example>
<question>How often should maintenance be performed?</question>
<answer>Section 7.1 (page 45) specifies that routine maintenance should be
performed quarterly, with detailed procedures listed in Appendix C.</answer>
<citation>Section 7.1, page 45; Appendix C</citation>
</example>
</example_qa>

<actual_question>
What are the safety requirements for installation?
</actual_question>

<expected_format>
Provide a comprehensive answer with:
- Specific requirements from the manual
- Section references and page numbers
- Any warnings or cautions mentioned
</expected_format>
```

### Benefits
- **Format consistency**: Claude sees expected answer structure
- **Citation style**: Learns how to reference the document
- **Detail level**: Understands expected thoroughness
- **Improved recall**: Up to 30% better with examples (Anthropic testing)

---

## Key Metrics and Expected Improvements

Based on Anthropic's published research and case studies:

| Technique | Measured Improvement | Use Case |
|-----------|---------------------|----------|
| Few-shot prompting | 20%+ accuracy | Fortune 500 insurance claims |
| Query-last positioning | Up to 30% | Multi-document long-context tasks |
| Citations API | 15% citation accuracy | vs. manual citation methods |
| Step-by-step reasoning | 20%+ accuracy | Complex reasoning tasks |
| Extract-then-answer | Significant recall boost | Long document Q&A |
| Claude 3 Opus vs 2.1 | 2x accuracy | Difficult open-ended questions |

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Vague Instructions
```
❌ "Write something about our product"
✅ "Write a 300-word product description highlighting [features], targeting [audience], in [tone]"
```

### Anti-Pattern 2: Mixing Instructions and Data
```
❌ Analyze this data: [data]. Make sure to calculate mean and median. [more data]
✅ <instructions>Calculate mean and median</instructions>
     <data>[all data here]</data>
```

### Anti-Pattern 3: Assuming Knowledge
```
❌ "Fix the bug" (assuming Claude knows which bug)
✅ "The app crashes when users upload files >10MB. Fix the file upload handler."
```

### Anti-Pattern 4: Over-Reliance on Model Knowledge
```
❌ "What is our company's refund policy?"
✅ <policy>[paste policy]</policy>
     "Explain our refund policy based on the above."
```

### Anti-Pattern 5: No Examples for Complex Formats
```
❌ "Output as JSON" (Claude might choose any JSON structure)
✅ Provide example JSON + "Output in this exact format"
```

---

## Quick Reference: Pattern Selection Guide

| Your Task | Best Patterns | Why |
|-----------|--------------|-----|
| Classification | Few-shot prompting + XML tags | Examples show exact categories |
| Analysis | Chain of thought + XML structure | Show reasoning, separate sections |
| Long document Q&A | Document-first + Extract-then-answer | Maximizes recall and accuracy |
| Code review | System prompt + Chain of thought | Consistent expertise + transparency |
| Creative writing | System prompt + Prefilling | Set voice/style + start direction |
| Fact extraction | Hallucination prevention + Citations | Accuracy and auditability |
| Multi-step workflow | Prompt chaining | Focused attention at each step |
| Format enforcement | Prefilling + Examples | Guarantee structure |
| Complex reasoning | CoT + Few-shot + XML tags | Maximum accuracy and structure |

---

## Integration Examples

### Python SDK Integration

```python
import anthropic

client = anthropic.Anthropic(api_key="your-key")

# Pattern: Few-shot + XML + Prefilling
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    temperature=0,  # Low temp for consistency
    system="""You are an expert data analyst. Always structure your responses
    with <analysis> tags for reasoning and <result> tags for final answers.""",
    messages=[
        {
            "role": "user",
            "content": """
            <examples>
            <example>
              <data>Sales: [100, 150, 200]</data>
              <output>
                <analysis>Computing statistics: mean=(100+150+200)/3=150, trend=increasing</analysis>
                <result>{"mean": 150, "trend": "increasing"}</result>
              </output>
            </example>
            </examples>

            <data>Sales: [300, 280, 320, 310]</data>
            Output following the example format.
            """
        },
        {
            "role": "assistant",
            "content": "<analysis>"  # Prefill
        }
    ]
)

print(message.content[0].text)
```

### Multi-Turn Conversation

```python
conversation_history = []

# Turn 1: Extract
conversation_history.append({
    "role": "user",
    "content": f"<doc>{document}</doc>\n\nExtract key facts as bullet points."
})

response1 = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=conversation_history
)

conversation_history.append({
    "role": "assistant",
    "content": response1.content[0].text
})

# Turn 2: Analyze (builds on extraction)
conversation_history.append({
    "role": "user",
    "content": "Based on those facts, what are the 3 most important insights?"
})

response2 = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=conversation_history
)
```

---

## Summary

Anthropic's prompt engineering patterns emphasize:

1. **Clarity**: Be explicit, not implicit
2. **Structure**: Use XML tags for complex prompts
3. **Examples**: Show, don't just tell
4. **Reasoning**: Request step-by-step thinking
5. **Grounding**: Minimize hallucinations with citations
6. **Positioning**: Strategic document placement for long contexts
7. **Chaining**: Break complex tasks into focused steps
8. **Affirmative**: Say what to do, not what to avoid
9. **Role-setting**: Use system prompts for consistent behavior
10. **Testing**: Iterate scientifically

These patterns, often combined, create powerful prompts that reliably produce high-quality outputs.

---

## Sources

- Anthropic Interactive Prompt Engineering Tutorial: https://github.com/anthropics/prompt-eng-interactive-tutorial
- Anthropic Business Performance Guide: https://www.anthropic.com/news/prompt-engineering-for-business-performance
- Claude Documentation: https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview
- Official best practices and case studies from Anthropic (2024)

**Pattern Extraction Date**: November 14, 2024
**Applicable Models**: Claude 3 (Haiku, Sonnet, Opus), Claude 3.5 (Sonnet, Haiku), Claude 4.x
**Status**: Validated against official Anthropic documentation and published case studies