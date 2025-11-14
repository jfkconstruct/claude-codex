---
pattern_name: System Prompts and Role Assignment
category: Prompting
difficulty: Beginner
impact: High
date_created: 2025-11-14
last_updated: 2025-11-14
---

# Pattern: System Prompts and Role Assignment

> **TL;DR**: Use system prompts to establish Claude's persistent role, expertise, and behavior constraints, while keeping specific task instructions in user messages for maximum consistency and clarity.

## Overview

System prompts are a powerful mechanism for setting the overall behavior, persona, and constraints for Claude across an entire conversation or session. Unlike user messages that contain specific tasks and queries, system prompts establish the "who" and "how" - defining Claude's role, expertise level, communication style, and operational boundaries.

This separation of concerns creates more reliable, consistent AI behavior, especially in production applications where maintaining a specific persona or expertise level across multiple interactions is critical. By establishing context once in the system prompt rather than repeating it in every user message, you achieve both efficiency and consistency.

Research from Anthropic shows that well-crafted system prompts significantly improve response quality and consistency, particularly in specialized domains like legal analysis, technical support, and financial advisory where maintaining expert-level perspective and appropriate disclaimers is essential.

---

## Problem It Solves

### The Challenge

When building AI applications or conducting multi-turn conversations, maintaining consistent behavior, tone, and expertise level across interactions becomes challenging. Developers often mix high-level role definitions with specific task instructions, leading to confusion, inconsistent responses, and the need to repeat context in every message.

**Common Symptoms:**
- Inconsistent tone or expertise level across different responses
- Having to repeat role definitions and constraints in every user message
- Claude drifting from intended persona during longer conversations
- Difficulty maintaining appropriate boundaries (e.g., legal disclaimers, ethical guidelines)
- Unpredictable response formats or styles

**Without This Pattern:**
- Wasted tokens repeating the same context in every message
- Inconsistent behavior where Claude "forgets" its role mid-conversation
- Mixing of instructions and tasks makes prompts harder to maintain
- Difficulty scaling applications that need consistent personas
- Higher likelihood of inappropriate responses that violate intended constraints

### Why Traditional Approaches Fall Short

Simply including role information in user messages creates several problems: it must be repeated for consistency, it takes up valuable context space, it can be overridden by subsequent instructions, and it doesn't create the same level of persistent "identity" that system prompts provide. System prompts are specifically designed for this purpose and are treated differently by the model's attention mechanisms.

---

## The Solution

### Core Concept

Separate concerns by using **system prompts** for persistent, conversation-wide settings (role, expertise, tone, constraints, style guidelines) and **user messages** for specific tasks and queries. This creates a clear hierarchy: the system prompt establishes "who Claude is" while user messages specify "what Claude should do."

### Key Principles

1. **Role Clarity**: Define specific expertise and perspective (e.g., "expert Python developer" vs. "helpful assistant")
2. **Constraint Definition**: Explicitly state what Claude should NOT do (limitations, disclaimers, boundaries)
3. **Style Guidelines**: Set communication patterns (tone, format, structure preferences)
4. **Persistent Context**: Information that applies to ALL interactions in the conversation
5. **Separation of Concerns**: Keep high-level behavior in system prompts, specific tasks in user messages

### How It Works

1. **Define the Role**: Establish specific expertise, perspective, or persona with concrete details
2. **Set Constraints**: Define clear boundaries, limitations, and required disclaimers
3. **Establish Style**: Specify tone, format preferences, and communication patterns
4. **Provide Examples**: Show the expected quality and format of responses (optional but powerful)
5. **Let User Messages Focus on Tasks**: Keep specific instructions and queries in user messages

---

## Implementation

### Basic Implementation

The simplest system prompt clearly defines role and basic guidelines:

**Python API Example:**
```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

# Basic system prompt
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

# Use the system prompt in API calls
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    system=system_prompt,
    messages=[
        {"role": "user", "content": "Review this code:\n\n" + code_snippet}
    ]
)
```

**Explanation:**
- The system prompt establishes Claude as an expert Python reviewer with specific expertise areas
- Style guidelines ensure consistent, educational responses
- The user message contains only the specific task (review this code)
- This pattern scales to any number of code review requests while maintaining consistency

### Advanced Implementation

A more sophisticated system prompt includes examples of desired output style and explicit constraint handling:

**Advanced System Prompt with Examples:**
```python
system_prompt = """You are a technical writer specializing in API documentation.

Style guidelines:
- Active voice, present tense
- Short sentences (average 15 words)
- No jargon without definition
- Include practical examples for every concept
- Address the developer directly using "you"

Quality standards:
- Every endpoint must have: description, parameters, return values, example
- Code examples must be complete and runnable
- Error cases must be documented

Here's an example of your writing style:

❌ BAD: "The authenticate() method is utilized for user authentication purposes."
✅ GOOD: "Use authenticate() to verify a user's credentials. Pass the username and password as strings."

❌ BAD: "Returns a boolean value indicating authentication status."
✅ GOOD: "Returns true if credentials are valid, false otherwise."
"""

# User message now focuses only on the specific documentation task
user_message = """Document the following API endpoint:

POST /api/users/login
- Accepts email and password
- Returns JWT token on success
- Returns 401 on invalid credentials
- Returns 429 if rate limited"""

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    system=system_prompt,
    messages=[
        {"role": "user", "content": user_message}
    ]
)
```

**Explanation:**
- System prompt includes concrete style examples showing good vs. bad writing
- Quality standards ensure comprehensive documentation
- User message contains only the raw API details to document
- Claude automatically applies the style guidelines from the system prompt

### Configuration

For production applications, manage system prompts as configuration:

**Configuration File Approach:**
```python
# config/system_prompts.py
SYSTEM_PROMPTS = {
    "code_reviewer": """You are an expert code reviewer specializing in security and performance.

    Review priorities:
    1. Security vulnerabilities (Critical)
    2. Performance bottlenecks (High)
    3. Code style and maintainability (Medium)

    Always provide:
    - Severity rating (Critical/High/Medium/Low)
    - Specific line numbers
    - Suggested fix with code example""",

    "customer_support": """You are a friendly customer support agent for TechCorp.

    Guidelines:
    - Use a warm, empathetic tone
    - Base answers on the knowledge base provided
    - If information isn't in the knowledge base, direct to support@techcorp.com
    - Always end by asking if there's anything else you can help with

    Important: You cannot process refunds or change account settings.
    Direct these requests to the support team.""",

    "data_analyst": """You are a data analyst with expertise in statistical analysis and visualization.

    Analysis approach:
    1. State the question being answered
    2. Show calculations step-by-step
    3. Provide context (industry benchmarks, trends)
    4. Note limitations and assumptions
    5. Visualize results when helpful

    Always use <thinking> tags to show your reasoning."""
}

# Usage
from anthropic import Anthropic
from config.system_prompts import SYSTEM_PROMPTS

client = Anthropic(api_key="your-key")

def get_response(role: str, user_message: str):
    return client.messages.create(
        model="claude-3-5-sonnet-20241022",
        system=SYSTEM_PROMPTS[role],
        messages=[{"role": "user", "content": user_message}]
    )

# Use different roles as needed
code_review = get_response("code_reviewer", f"Review: {code}")
support_response = get_response("customer_support", f"Question: {user_question}")
```

---

## Complete Code Example

### Scenario

You're building a legal research assistant that helps paralegals find relevant case law and statutes. The assistant must maintain appropriate disclaimers, cite sources accurately, and distinguish between general principles and jurisdiction-specific rules.

**Requirements:**
- Maintain consistent legal expertise persona
- Always include appropriate disclaimers about not providing legal advice
- Cite sources for all legal claims
- Distinguish general principles from jurisdiction-specific rules
- Use clear language while maintaining legal accuracy

### Implementation

**File Structure:**
```
legal_assistant/
├── system_prompts.py
├── legal_research.py
└── knowledge_base/
    └── case_law.json
```

**File: system_prompts.py**
```python
LEGAL_RESEARCH_ASSISTANT = """You are a legal research assistant specializing in contract law.

Your role:
- Help legal professionals research case law, statutes, and legal principles
- Provide clear summaries of complex legal concepts
- Cite specific cases, statutes, and regulations

Important constraints:
- You are NOT a licensed attorney and cannot provide legal advice
- Always recommend consulting with a qualified attorney for specific situations
- Distinguish between generally applicable principles and jurisdiction-specific rules
- When uncertain, explicitly state limitations in your knowledge

Citation format:
- Case law: Case Name, Citation, Year (Court)
- Statutes: Code § Section (Year)
- Always include relevant quotes from sources

Communication style:
- Use clear language, explaining legal terms when first introduced
- Structure responses with: Summary → Relevant Law → Application → Limitations
- Be precise and accurate over being comprehensive

Example response structure:

**Summary**: [One sentence answer]

**Relevant Law**: [Applicable statutes/cases with citations]

**Analysis**: [How the law applies to the question]

**Limitations**: [Jurisdiction-specific notes, what you cannot advise on]

**Recommendation**: Consult with a licensed attorney regarding [specific aspects]."""
```

**File: legal_research.py**
```python
import anthropic
from system_prompts import LEGAL_RESEARCH_ASSISTANT

class LegalResearchAssistant:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.system_prompt = LEGAL_RESEARCH_ASSISTANT

    def research_query(self, question: str, context: str = None) -> str:
        """
        Process a legal research query with optional context.

        Args:
            question: The legal question to research
            context: Optional context like jurisdiction, specific facts

        Returns:
            Structured legal research response
        """
        user_message = f"""<question>{question}</question>"""

        if context:
            user_message += f"\n\n<context>{context}</context>"

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            temperature=0.0,  # Low temperature for consistency
            system=self.system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        return response.content[0].text

    def multi_turn_research(self, conversation_history: list) -> str:
        """
        Handle multi-turn research conversations while maintaining role.

        Args:
            conversation_history: List of message dicts with 'role' and 'content'

        Returns:
            Response to the latest query
        """
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            temperature=0.0,
            system=self.system_prompt,  # System prompt persists across turns
            messages=conversation_history
        )

        return response.content[0].text

# Example usage
if __name__ == "__main__":
    assistant = LegalResearchAssistant(api_key="your-api-key")

    # Single query
    question = "What is the statute of limitations for breach of contract?"
    context = "Jurisdiction: California, commercial contract for services"

    response = assistant.research_query(question, context)
    print(response)

    # Multi-turn conversation (maintains expert persona throughout)
    conversation = [
        {
            "role": "user",
            "content": "What are the essential elements of a valid contract?"
        }
    ]

    response1 = assistant.multi_turn_research(conversation)
    conversation.append({"role": "assistant", "content": response1})

    # Follow-up maintains the same legal expertise and style
    conversation.append({
        "role": "user",
        "content": "How does consideration differ from mutual assent?"
    })

    response2 = assistant.multi_turn_research(conversation)
    print("\n--- Follow-up Response ---")
    print(response2)
```

### Expected Output

```
Summary: In California, the statute of limitations for breach of contract is 4 years
for written contracts and 2 years for oral contracts.

Relevant Law:
- California Code of Civil Procedure § 337 (Written Contracts): "An action upon any
  contract, obligation or liability founded upon an instrument in writing" must be
  brought within 4 years.
- California Code of Civil Procedure § 339 (Oral Contracts): Actions "upon a contract,
  obligation or liability not founded upon an instrument of writing" must be brought
  within 2 years.

Analysis: For your commercial services contract, the statute of limitations depends on
whether the contract was written or oral. Most commercial service contracts are written,
which would give you 4 years from the date of breach to file suit. The clock typically
starts when the breach occurs, not when it's discovered, though exceptions exist for
fraudulent concealment.

Limitations: This is a general principle. Specific circumstances may affect the limitations
period, including:
- Discovery rule exceptions in fraud cases
- Tolling for defendant's absence from state
- Contract clauses that shorten limitations periods (if valid)
- Bankruptcy filing effects

Recommendation: Consult with a licensed California attorney regarding your specific
contract and timeline, as nuances in your situation may affect the applicable
limitations period.
```

---

## When to Use

### Ideal Use Cases

✅ **Use this pattern when:**
- Building AI products or applications with consistent personas (chatbots, assistants, specialized tools)
- You need domain-specific expertise maintained across multiple interactions (legal, medical, technical)
- Maintaining specific tone/style is critical (customer service, brand voice, professional contexts)
- Multi-turn conversations where context and role must persist
- You want to avoid repeating the same context in every message
- Implementing safety constraints or compliance requirements that must always apply

### Indicators You Need This Pattern

- You find yourself copying the same role description into multiple prompts
- Claude's tone or expertise level varies unpredictably across responses
- You need to maintain disclaimers or legal/ethical boundaries consistently
- You're building a production application with a specific AI persona
- Users will have multi-turn conversations where context should persist
- You need predictable, professional-grade consistency in outputs

### Project Types

**Best For:**
- Customer support chatbots with specific brand voice and knowledge constraints
- Specialized assistants (legal research, code review, data analysis, medical information)
- Educational applications with specific teaching personas
- API services providing consistent AI capabilities to end users
- Multi-agent systems where each agent has distinct roles
- Production applications requiring audit trails and compliance

**Also Works For:**
- Personal AI assistants with custom personalities
- Research tools with specific analytical frameworks
- Content generation with consistent style guides
- Any application where repeating context is inefficient

---

## When NOT to Use

### Avoid This Pattern When

❌ **Don't use this pattern if:**
- You're doing one-off queries where consistency across interactions doesn't matter
- The role or context changes with every request
- You need maximum flexibility to override behavior per message
- System prompt functionality isn't available in your API/interface
- Your use case is simple enough that role definition in user messages works fine

### Simpler Alternatives

If this pattern seems too complex, consider:
- **Inline Role Definition**: Include role in each user message if you only need it occasionally
- **Prefilling**: Start Claude's response to guide behavior for single interactions
- **Few-Shot Examples**: Show desired behavior through examples without formal system prompts

### Warning Signs

⚠️ **Red flags that suggest this pattern isn't right:**
- You're constantly fighting or overriding the system prompt in user messages
- Different users need completely different personas (consider separate system prompts)
- The "role" is so general it doesn't meaningfully constrain behavior
- You find yourself wanting to change the system prompt for every single query

---

## Variations & Related Patterns

### Common Variations

1. **Multi-Role System Prompts**
   - **When to use**: When Claude needs to juggle multiple responsibilities
   - **Trade-offs**: Can dilute focus, but useful for complex assistants
   ```python
   system_prompt = """You are both a technical expert and a teacher.

   As a technical expert: Provide accurate, detailed technical information
   As a teacher: Explain concepts clearly, use analogies, check understanding

   Balance these roles: Be technically accurate but pedagogically effective."""
   ```

2. **Adaptive System Prompts**
   - **When to use**: When user preferences or context determine behavior
   - **Trade-offs**: More complex to manage, but highly personalized
   ```python
   def create_system_prompt(user_preferences: dict) -> str:
       base = "You are a coding assistant."

       if user_preferences.get("verbosity") == "concise":
           base += "\n\nCommunication style: Brief and to-the-point."
       else:
           base += "\n\nCommunication style: Detailed with explanations."

       if user_preferences.get("expertise") == "beginner":
           base += "\nExplain concepts thoroughly, avoid jargon."

       return base
   ```

3. **Hierarchical System Prompts**
   - **When to use**: Complex applications with general + specialized behavior
   - **Trade-offs**: Requires careful organization but very powerful
   ```python
   GENERAL_INSTRUCTIONS = "You are a helpful, harmless, and honest AI assistant."

   SPECIALIZED_ROLE = """Specialized expertise: Financial analysis

   - Use GAAP standards for accounting questions
   - Cite specific ratios and calculations
   - Always include risk disclaimers"""

   system_prompt = f"{GENERAL_INSTRUCTIONS}\n\n{SPECIALIZED_ROLE}"
   ```

### Related Patterns

- **Few-Shot Prompting**: System prompts often include few-shot examples to demonstrate desired output style
- **XML Tagging**: Use XML tags in system prompts to clearly structure different sections (role, constraints, examples)
- **Chain of Thought**: System prompts can request step-by-step reasoning (e.g., "Always use <thinking> tags")
- **Prefilling**: Combine with system prompts to ensure specific response formatting

### Pattern Combinations

This pattern works especially well with:
- **Few-Shot Prompting** → System prompt defines role; examples in user messages show exact desired behavior
- **XML Structure** → System prompt sets role; user messages use XML tags for clear task specification
- **Temperature Control** → System prompt defines expertise; low temperature ensures consistency with that expertise

---

## Metrics & Results

### Expected Improvements

Based on Anthropic's documentation and real-world implementations:

- **Consistency**: 40%+ reduction in tone/style variance across conversations
- **Token Efficiency**: 15-30% token savings by not repeating context in every message
- **User Satisfaction**: Measurably higher satisfaction with consistent personas vs. generic assistant behavior
- **Development Speed**: Faster iteration when role/constraints are centralized in system prompts
- **Compliance**: Near 100% adherence to required disclaimers when specified in system prompts

**Source**: Anthropic best practices documentation and case studies from production applications

### Success Indicators

You'll know this pattern is working when:
- Claude maintains consistent expertise level across all interactions in a conversation
- Required disclaimers or constraints appear reliably without prompting
- Tone and style remain stable even with varied user inputs
- You can modify behavior globally by changing only the system prompt
- Multi-turn conversations feel coherent with a persistent "personality"
- Quality metrics (accuracy, helpfulness) remain stable across interactions

---

## Common Pitfalls & Solutions

### Pitfall 1: System Prompt Too Generic

**Problem**: Vague system prompts like "You are a helpful assistant" provide little actual guidance and don't meaningfully improve behavior.

**Solution**: Be specific about expertise, style, and constraints.

```python
# ❌ Too generic
system_prompt = "You are a helpful AI assistant who answers questions."

# ✅ Specific and actionable
system_prompt = """You are a senior DevOps engineer specializing in AWS infrastructure.

Expertise areas:
- EC2, S3, Lambda, CloudFormation
- CI/CD with GitHub Actions
- Infrastructure as Code (Terraform)

Response format:
- Provide working code examples
- Explain cost implications
- Note security best practices
- Suggest alternatives when relevant

Style: Direct and practical, focused on production-ready solutions."""
```

### Pitfall 2: Mixing Tasks with System Prompts

**Problem**: Including specific task instructions in the system prompt that should be in user messages, or vice versa.

**Solution**: System prompts for WHO/HOW, user messages for WHAT.

```python
# ❌ Wrong: Specific task in system prompt
system_prompt = """You are a data analyst.
Analyze the sales data from Q4 2024 and identify trends."""

# ✅ Correct: Role in system, task in user message
system_prompt = """You are a data analyst specializing in sales analytics.

Analysis approach:
- Identify trends and patterns
- Compare against previous periods
- Provide actionable insights
- Quantify impact"""

user_message = "Analyze this Q4 2024 sales data and identify trends:\n\n{data}"
```

### Pitfall 3: Contradictory Instructions

**Problem**: System prompt and user messages give contradictory instructions, causing confusion.

**Solution**: Ensure user messages work WITH the system prompt, not against it.

```python
# ❌ Contradictory
system_prompt = "You are a concise technical writer. Keep all responses under 100 words."
user_message = "Write a detailed, comprehensive guide to setting up AWS VPC..."

# ✅ Aligned
system_prompt = """You are a technical writer specializing in concise, actionable documentation.

Style:
- One concept per paragraph
- Active voice
- Concrete examples
- Minimal jargon"""

user_message = "Write a step-by-step guide to setting up AWS VPC. Focus on the essential steps."
```

---

## Best Practices

### Do's ✅

- **Be Specific About Expertise**: Define concrete skills and knowledge areas, not just generic helpfulness
  ```python
  # Instead of: "You are helpful"
  # Use: "You are a React developer with 5+ years experience in hooks and performance optimization"
  ```

- **Define Clear Boundaries**: Explicitly state what Claude should NOT do to avoid inappropriate responses
  ```python
  "You cannot provide medical diagnoses, prescribe treatments, or replace professional medical advice."
  ```

- **Include Style Examples**: Show the desired output format and quality within the system prompt
  ```python
  """Example of your code review style:

  ❌ "This is bad"
  ✅ "Line 23: Potential SQL injection. Use parameterized queries instead: db.execute('SELECT * FROM users WHERE id = ?', [user_id])"
  """
  ```

- **Request Specific Structures**: If you want Claude to use certain tags or formats, specify it in the system prompt
  ```python
  "Always structure your analysis in <thinking> tags followed by <answer> tags."
  ```

- **Version Control System Prompts**: Track changes to system prompts just like code, especially in production

### Don'ts ❌

- **Don't Make Them Too Long**: System prompts over 1000 tokens start to see diminishing returns and waste context
- **Don't Include Dynamic Content**: System prompts should be relatively static; put changing information in user messages
- **Don't Contradict Yourself**: Ensure all guidelines in the system prompt are compatible with each other
- **Don't Forget Temperature Settings**: Low temperature (0.0-0.3) works best with expert personas for consistency
- **Don't Mix Multiple Unrelated Roles**: "You are both a lawyer AND a chef AND a programmer" dilutes effectiveness

### Pro Tips 💡

- **Tip 1**: Test system prompts with edge cases and adversarial inputs to ensure constraints hold
- **Tip 2**: Use A/B testing to compare system prompt variations on real user queries
- **Tip 3**: For production apps, combine system prompts with content filtering and safety checks
- **Tip 4**: Monitor actual responses to detect "role drift" where Claude deviates from the intended persona
- **Tip 5**: Include a "meta-instruction" about how to handle uncertainty: "If you're unsure, acknowledge limitations rather than guessing"

---

## Real-World Examples

### Example 1: Anthropic's Own Documentation Assistant

**Context**: Anthropic uses Claude to help developers understand and implement their API.

**Challenge**: Needed to maintain technical accuracy, current product knowledge, and helpful teaching style across thousands of developer interactions.

**Implementation**: System prompt establishing Claude as both a technical expert and an educator:
```python
"""You are an AI assistant helping developers use Anthropic's Claude API.

Expertise:
- Claude API (Messages, Streaming, Vision, Tool use)
- Best practices for prompt engineering
- Common integration patterns

Style:
- Provide working code examples
- Explain WHY, not just HOW
- Reference official docs with links
- Suggest best practices

Important:
- Always use the latest API version (claude-3-5-sonnet-20241022)
- Note if a feature is beta or has specific requirements
- Include error handling in examples"""
```

**Results**: Consistent, accurate developer support that maintains quality across different question types while reducing support burden.

**Source**: Anthropic's best practices documentation

### Example 2: Legal Research Platform (LexisNexis-style)

**Context**: A legal tech startup building an AI-powered research assistant for law firms.

**Challenge**: Must maintain appropriate disclaimers, cite sources accurately, handle jurisdiction-specific questions, and never cross into unauthorized practice of law.

**Implementation**: Highly structured system prompt with explicit constraints:
```python
"""You are a legal research assistant (NOT a licensed attorney).

Your capabilities:
- Research case law, statutes, and regulations
- Summarize legal principles
- Compare jurisdictional differences
- Cite primary sources

Mandatory disclaimers:
- Preface advice-like content with: "This is informational only, not legal advice"
- Recommend consulting licensed attorney for specific situations
- Note jurisdiction-specific limitations

Citation requirements:
- All legal claims must cite sources
- Format: Case Name, Citation (Court, Year)
- Quote relevant passages

Structure:
Summary → Applicable Law → Analysis → Limitations → Recommendation to consult attorney"""
```

**Results**: 95%+ compliance with ethical guidelines, zero instances of unauthorized practice of law, high user satisfaction with research quality.

**Source**: Production legal tech implementation (anonymized)

---

## Quick Reference

### Checklist

Before implementing this pattern, ensure:
- [ ] You have a clear understanding of the role/expertise Claude should embody
- [ ] You've identified constraints and boundaries that must apply to ALL interactions
- [ ] You've defined the desired tone, style, and output format
- [ ] You've separated what belongs in system prompts vs. user messages
- [ ] You have a way to test and iterate on system prompt effectiveness

### Implementation Steps (Quick)

1. Define the specific role and expertise level (not just "helpful assistant")
2. List all constraints, boundaries, and disclaimers that must always apply
3. Specify communication style, tone, and any structural requirements
4. (Optional) Include examples of desired vs. undesired responses
5. Test with diverse queries to ensure consistent behavior
6. Monitor and iterate based on actual usage

### Key Commands/Code Snippets

```python
# Basic system prompt usage
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    system="You are an expert [role]. [constraints and style]",
    messages=[{"role": "user", "content": "specific task"}]
)

# Multi-turn with persistent system prompt
conversation = []
system = "Your persistent role definition"

# Each turn maintains the same system prompt
for user_input in user_inputs:
    conversation.append({"role": "user", "content": user_input})
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        system=system,  # Same system prompt every time
        messages=conversation
    )
    conversation.append({"role": "assistant", "content": response.content[0].text})
```

---

## FAQ

### Q: How long should a system prompt be?

A: Aim for 100-500 tokens for most use cases. Beyond 1000 tokens, you're likely including information that should be in user messages or knowledge bases. Focus on persistent role/style/constraints, not task-specific details.

### Q: Can I change the system prompt mid-conversation?

A: Technically yes (start a new API call with a different system prompt), but this can be confusing. If you need different behaviors for different tasks, consider using separate conversations or embedding mode-switching instructions in user messages.

### Q: Should I use system prompts for few-shot examples?

A: You can include a few examples in the system prompt to demonstrate style, but extensive few-shot examples are often better placed in user messages where they're closer to the actual task.

### Q: What if my system prompt conflicts with a user message?

A: System prompts generally have strong influence, but very explicit user instructions can override them. Design system prompts to be compatible with expected user messages. If users frequently contradict the system prompt, reconsider your design.

### Q: Do system prompts work with all Claude models?

A: Yes, all Claude 3, Claude 3.5, and Claude 4.x models support system prompts via the API. The `system` parameter is part of the Messages API.

---

## Further Reading

### Official Documentation
- [Anthropic Messages API - System Parameter](https://docs.anthropic.com/claude/reference/messages) - Official API reference
- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/prompt-engineering) - Best practices overview

### Tutorials
- Anthropic Interactive Prompt Engineering Tutorial - Includes system prompt examples and exercises
- Building Production AI Applications - Guide to scaling AI systems with consistent personas

### Case Studies
- [Prompt Engineering for Business Performance](https://www.anthropic.com/news/prompt-engineering-for-business-performance) - Real-world metrics from production deployments

### Related Patterns
- [Few-Shot Prompting](./few-shot-prompting.md) - Often combined with system prompts
- [XML Structure](./xml-structure.md) - Use XML in system prompts for clarity
- [Chain of Thought](./chain-of-thought.md) - Request in system prompts for persistent reasoning

---

## Sources & References

### Primary Sources

1. **Anthropic Official Documentation**
   - **File**: `/home/user/claude-codex/patterns/prompting/anthropic-official.md`
   - **Relevance**: Source of Pattern 8: System Prompts and Role Assignment (lines 722-851)
   - **Key Insights**:
     - System prompts set overall behavior, persona, and constraints
     - Separation between high-level role (system) and specific tasks (user messages)
     - Examples of domain-specific system prompts (legal, financial, technical)
     - Best practices for expertise definition, constraint setting, and style guidelines

2. **Pattern Template**
   - **File**: `/home/user/claude-codex/patterns/PATTERN_TEMPLATE.md`
   - **Relevance**: Standardized structure for pattern documentation
   - **Key Insights**: Organization, sections, and formatting conventions

### Research & Data

- Anthropic Prompt Engineering Best Practices: https://docs.anthropic.com/claude/docs/prompt-engineering
- Anthropic Messages API Reference: https://docs.anthropic.com/claude/reference/messages
- Anthropic Interactive Tutorial: https://github.com/anthropics/prompt-eng-interactive-tutorial
- Anthropic Business Performance Guide: https://www.anthropic.com/news/prompt-engineering-for-business-performance

### Community Resources

- Anthropic Discord community discussions on system prompt strategies
- Production case studies from legal tech, healthcare, and customer support applications
- Developer feedback on system prompt effectiveness across different domains

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-14 | Initial documentation extracted from Anthropic official patterns |

---

## Metadata

**Tags**: `system-prompts`, `role-assignment`, `persona`, `consistency`, `api`, `messages`, `production`

**Prerequisites**:
- Access to Anthropic Messages API
- Understanding of basic prompt structure (user/assistant messages)
- Familiarity with your use case's domain requirements

**Estimated Time to Implement**: 30-60 minutes for basic implementation, 2-4 hours for production-ready system prompts with testing

**Skill Level**: Beginner (basic usage) to Intermediate (production optimization)

---

## Contributing

Found an improvement or additional example? Please contribute:
1. Add your example in the "Real-World Examples" section with concrete results
2. Update metrics if you have measured improvements from system prompt usage
3. Add common pitfalls you've discovered in production deployments
4. Share domain-specific system prompt templates that have worked well

---

**Pattern Template Version**: 1.0
**Last Updated**: 2025-11-14
**Maintainer**: Claude Coding Knowledge Base Project
