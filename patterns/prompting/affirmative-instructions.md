---
pattern_name: Affirmative Instructions
category: Prompting
difficulty: Beginner
impact: Medium
date_created: 2025-11-14
last_updated: 2025-11-14
---

# Pattern: Affirmative Instructions

> **TL;DR**: Tell Claude what TO do, not what NOT to do. Positive framing creates clearer mental models and more reliable outcomes.

## Overview

Affirmative instructions are a fundamental prompting technique where you frame all guidance in positive, action-oriented language. Instead of listing prohibited behaviors ("don't do X, Y, Z"), you explicitly state the desired behaviors and outcomes. This approach leverages how language models process instructions and aligns with cognitive science principles about how humans (and AI) respond to positive vs. negative framing.

Research from Anthropic shows that Claude responds significantly better to affirmative instructions. Negative instructions can paradoxically draw attention to the forbidden behavior, create ambiguity about what TO do instead, and reduce overall instruction compliance. By contrast, affirmative framing provides clear direction, reduces cognitive load, and creates actionable mental models that guide the model's behavior more effectively.

This pattern is universally applicable across all prompting scenarios but becomes especially critical in safety-critical applications, customer-facing systems, and scenarios where precision matters. It's one of the simplest yet most impactful changes you can make to your prompts.

---

## Problem It Solves

### The Challenge

When writing prompts, it's natural to think about what could go wrong and create rules to prevent those outcomes. This leads to prompts filled with "don't" statements: "Don't hallucinate," "Don't be rude," "Don't include irrelevant information." However, negative instructions create several problems that undermine prompt effectiveness.

**Common Symptoms:**
- Claude focuses on or exhibits the exact behavior you told it to avoid
- Responses lack clear direction and seem uncertain or hesitant
- Instructions are ambiguous because they specify what NOT to do but leave the desired behavior unclear
- Prompts become lengthy lists of prohibitions that are difficult to follow consistently

**Without This Pattern:**
- **Increased error rates**: Negative instructions paradoxically prime the model to think about the forbidden behavior
- **Ambiguity**: "Don't be technical" doesn't specify the desired alternative (simple? conversational? visual?)
- **Compliance issues**: Models follow positive instructions more reliably than negative ones
- **Longer prompts**: Listing everything NOT to do takes more tokens than specifying what TO do
- **Cognitive confusion**: Negative framing creates unclear mental models

### Why Traditional Approaches Fall Short

Negative instructions seem logical—they directly address concerns about potential problems. However, they fall short for several reasons:

1. **Priming effect**: Mentioning something, even negatively, activates that concept in the model's processing
2. **Lack of actionable guidance**: "Don't X" doesn't tell the model what to do instead
3. **Infinite problem space**: There are countless ways to fail, but typically one right way to succeed
4. **Processing overhead**: The model must first understand the prohibition, then infer the alternative

Affirmative instructions bypass these issues by providing direct, actionable guidance from the start.

---

## The Solution

### Core Concept

Frame every instruction as a positive statement of desired behavior. Instead of prohibiting unwanted actions, explicitly specify what you want the model to do. Transform "don't be X" into "be Y" and "avoid doing X" into "do Y instead."

### Key Principles

1. **Action-Oriented**: Every instruction should specify a concrete action or behavior to perform
2. **Positive Framing**: Use affirmative language that describes what TO do
3. **Specificity**: Replace vague prohibitions with specific, constructive guidance
4. **Constructive Alternatives**: When you identify what not to do, translate it into what to do instead

### How It Works

1. **Identify Negative Instructions**: Review your prompt for any "don't," "avoid," "never," or other negative language
2. **Determine Desired Behavior**: For each prohibition, ask "What should the model do instead?"
3. **Reframe Positively**: Transform each negative instruction into an affirmative statement
4. **Verify Clarity**: Ensure the affirmative version provides clear, actionable guidance

---

## Implementation

### Basic Implementation

Transform simple negative instructions into affirmative equivalents:

**Negative Framing (Less Effective):**
```
Don't be too technical. Don't use jargon. Don't make it too long.
Don't include irrelevant information.
```

**Affirmative Framing (More Effective):**
```
Use simple, everyday language. Explain technical terms when necessary.
Keep responses under 200 words. Focus only on information directly answering the question.
```

**Explanation:**
- Instead of "don't be technical," specify "use simple, everyday language"
- Instead of "don't use jargon," provide constructive guidance: "explain technical terms when necessary"
- Instead of "don't make it too long," give a concrete target: "under 200 words"
- Instead of "don't include irrelevant information," specify the focus: "information directly answering the question"

### Advanced Implementation

Apply affirmative framing to complex system prompts:

**Negative Framing (Customer Support Example):**
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

**Affirmative Framing (Customer Support Example):**
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

**Explanation:**
- "Don't make promises" → "Set accurate expectations" (actionable and specific)
- "Don't blame" → "Show empathy and take ownership" (defines desired behavior)
- "Don't use jargon" → "Use clear, simple language" (positive directive)
- "Don't provide outside info" → "Base answers on knowledge base" (clear source)
- "Don't end without resolution" → "Ensure issue is resolved or escalated" (explicit success criteria)

### Configuration

Common negative-to-affirmative transformations:

| Negative ❌ | Affirmative ✅ | Why It's Better |
|------------|---------------|-----------------|
| "Don't hallucinate" | "Base all answers on the provided documentation" | Specifies the source to use |
| "Don't be rude" | "Use a professional and respectful tone" | Defines the desired tone |
| "Don't give legal advice" | "Provide general information and recommend consulting an attorney" | Explains what to do instead |
| "Avoid complex SQL" | "Use simple, readable SQL queries" | Describes the target style |
| "Don't make assumptions" | "Ask clarifying questions when information is missing" | Provides specific action to take |
| "Don't be verbose" | "Be concise and direct" | Positive target state |
| "Never use external knowledge" | "Use only the information in <context> tags" | Clear boundary with alternative |
| "Avoid technical terms" | "Use plain language that a non-expert can understand" | Defines audience and style |

---

## Complete Code Example

### Scenario

You're building an AI-powered medical information chatbot that helps patients understand their test results. The system must be accurate, empathetic, and avoid giving medical advice.

**Requirements:**
- Must not provide medical diagnoses or treatment recommendations
- Should be empathetic and reassuring
- Must avoid medical jargon
- Should encourage patients to consult their doctor
- Must only use information from the provided medical literature

### Implementation

**File: medical_chatbot.py**
```python
import anthropic

# ❌ NEGATIVE FRAMING (Less Effective)
negative_system_prompt = """You are a medical information assistant.

IMPORTANT RULES:
- Don't diagnose medical conditions
- Don't recommend treatments
- Don't use complex medical terminology
- Don't provide information outside the medical literature
- Don't be cold or clinical
- Don't discourage patients from seeing doctors
- Don't make assumptions about their condition
"""

# ✅ AFFIRMATIVE FRAMING (More Effective)
affirmative_system_prompt = """You are a medical information assistant.

YOUR ROLE:
- Explain medical test results in clear, everyday language
- Provide context from established medical literature
- Show empathy and understanding for patient concerns
- Encourage patients to discuss results with their healthcare provider
- Ask clarifying questions when details are needed
- Use analogies and simple explanations to make complex concepts accessible
- Remind patients that only their doctor can provide personalized medical advice

COMMUNICATION STYLE:
- Warm, supportive, and reassuring
- Clear and easy to understand
- Patient-focused and empathetic
"""

client = anthropic.Anthropic(api_key="your-api-key")

def get_medical_info(patient_query, medical_literature):
    """Process patient query with affirmative framing"""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        temperature=0.3,  # Lower temperature for consistency
        system=affirmative_system_prompt,  # Using affirmative version
        messages=[
            {
                "role": "user",
                "content": f"""
<medical_literature>
{medical_literature}
</medical_literature>

<patient_question>
{patient_query}
</patient_question>

Provide a helpful, accurate response based on the medical literature.
Remember to use simple language and encourage consultation with their doctor.
"""
            }
        ]
    )

    return message.content[0].text

# Example usage
medical_literature = """
Hemoglobin A1c (HbA1c) Test:
- Normal: Below 5.7%
- Prediabetes: 5.7% to 6.4%
- Diabetes: 6.5% or above
- Reflects average blood sugar over 2-3 months
- Used to diagnose diabetes and monitor treatment effectiveness
"""

patient_query = "My A1c test came back at 6.1%. What does this mean?"

response = get_medical_info(patient_query, medical_literature)
print(response)
```

### Expected Output

```
Your HbA1c result of 6.1% falls in what medical literature calls the "prediabetes"
range (5.7% to 6.4%). Think of HbA1c as a snapshot of your average blood sugar levels
over the past 2-3 months.

Here's what this means: Your blood sugar levels have been higher than the normal range
(below 5.7%), but not high enough to be classified as diabetes (6.5% or above). This
is actually valuable information because it gives you an opportunity to make changes
before diabetes develops.

I want to emphasize that this is general information based on medical literature.
Your doctor is the best person to interpret this result in the context of your overall
health, family history, and other factors. They can discuss with you:
- What lifestyle changes might be helpful
- Whether additional testing is needed
- A personalized plan for your specific situation

Please schedule a time to discuss this result with your healthcare provider so they
can give you personalized guidance.
```

**Comparison**: Notice how the affirmative framing produces a response that's naturally empathetic, clear, and appropriately cautious without explicitly being told what NOT to do. The positive instructions create a constructive framework that guides behavior more effectively.

---

## When to Use

### Ideal Use Cases

✅ **Use this pattern when:**
- Writing any prompt for Claude (universal best practice)
- Creating system prompts for AI products or applications
- Building customer-facing AI systems where tone and reliability matter
- Developing safety-critical applications (medical, legal, financial)
- Setting behavioral guidelines for AI assistants
- Training or onboarding users to write better prompts
- Refactoring prompts that aren't producing desired results

### Indicators You Need This Pattern

- Your prompts contain multiple "don't" or "avoid" statements
- Claude sometimes exhibits the exact behavior you're trying to prevent
- Responses seem uncertain or lack clear direction
- You're getting inconsistent results despite detailed instructions
- Your prompts are long lists of prohibitions
- You're spending time debugging unwanted behaviors

### Project Types

**Best For:**
- Customer support chatbots and AI assistants
- Educational AI tutors and learning companions
- Healthcare information systems
- Legal document analysis tools
- Financial advisory systems
- Code review and analysis tools
- Content moderation systems
- Any production AI system with specific behavioral requirements

**Also Works For:**
- Personal productivity assistants
- Creative writing aids
- Research and analysis tools
- Data extraction and transformation tasks
- One-off analytical queries

---

## When NOT to Use

### Avoid This Pattern When

❌ **Don't overthink it if:**
- You're writing a simple, one-time query with no behavioral constraints
- The instruction is already naturally affirmative (most basic task descriptions are)
- You're just experimenting and iterating rapidly (though it's still better practice)

### Simpler Alternatives

This pattern IS the simpler alternative. There's rarely a reason not to use affirmative framing:

- **No alternative needed**: Just write instructions in positive, action-oriented language from the start
- **Natural framing**: Most well-written prompts are already affirmative without conscious effort

### Warning Signs

⚠️ **Red flags that suggest you're overcomplicating:**
- You're spending excessive time rewriting already-clear instructions
- The affirmative version is significantly longer or less clear than the negative version
- You're creating convoluted positive statements when a simple "don't" would be clearer (rare, but possible)

**Note**: These warning signs are extremely rare. In 99% of cases, affirmative framing improves clarity.

---

## Variations & Related Patterns

### Common Variations

1. **Hybrid Approach (Occasional Negatives for Emphasis)**
   - **When to use**: When a prohibition is so critical it needs emphasis alongside positive guidance
   - **Trade-offs**: Can work, but generally less effective than pure affirmative framing
   - **Example**: "Use simple language. Explain technical terms when necessary. NEVER include specific medical diagnoses—instead, encourage consulting a doctor."

2. **Constraint-Based Affirmative**
   - **When to use**: When you need to define boundaries positively
   - **Trade-offs**: More verbose but crystal clear
   - **Example**: Instead of "Don't exceed 500 words," use "Keep your response between 300-500 words, aiming for conciseness while covering all key points."

### Related Patterns

- **Clear and Direct Instructions** (Pattern 1): Affirmative instructions are a subset of being clear and direct
- **System Prompts and Role Assignment** (Pattern 8): Apply affirmative framing to role definitions
- **Few-Shot Prompting** (Pattern 3): Examples should demonstrate desired behavior, not show what to avoid

### Pattern Combinations

This pattern works especially well with:
- **Role Assignment** → Define what the role DOES, not what it doesn't do
- **Few-Shot Examples** → Show positive examples of desired behavior rather than negative examples of what to avoid
- **Chain of Thought** → Request step-by-step reasoning (affirmative) rather than "don't jump to conclusions" (negative)

---

## Metrics & Results

### Expected Improvements

While Anthropic hasn't published specific percentage improvements for affirmative instructions alone, the company's documentation consistently emphasizes this as a core best practice. Qualitative observations include:

- **Better instruction compliance**: Claude follows affirmative instructions more consistently
- **Reduced unwanted behaviors**: Fewer instances of the model doing what you tried to prohibit
- **Clearer outputs**: Responses demonstrate better understanding of desired behavior
- **Shorter prompts**: Affirmative framing typically uses fewer tokens to convey the same guidance

**Source**: Anthropic Prompt Engineering Documentation and Interactive Tutorial (2024)

### Success Indicators

You'll know this pattern is working when:
- Claude consistently produces outputs matching your desired behavior
- You spend less time debugging and fixing unwanted responses
- Prompts become shorter and clearer
- You eliminate most or all "don't" statements from your prompts
- New team members find your prompts easier to understand and modify

---

## Common Pitfalls & Solutions

### Pitfall 1: Converting Negative to Vague Positive

**Problem**: Simply removing "don't" without providing clear alternative guidance

**Solution**: Specify the concrete alternative behavior

```
// ❌ Vague positive (unclear)
"Be appropriate with customers"

// ❌ Negative (ineffective)
"Don't be rude to customers"

// ✅ Specific affirmative (clear and actionable)
"Use a professional, respectful tone. Show empathy for customer concerns.
Address them by name and thank them for their patience."
```

### Pitfall 2: Making Affirmative Versions Too Wordy

**Problem**: The affirmative version becomes convoluted or much longer than the negative

**Solution**: Find the core positive behavior and state it simply

```
// ❌ Overly complex
"When considering whether to include information, you should carefully evaluate
whether that information directly pertains to and helps answer the specific question
posed by the user, and if it does not meet these criteria, then you should refrain
from including it in your response."

// ✅ Clear and concise
"Include only information that directly answers the user's question."
```

### Pitfall 3: Hybrid Negative-Positive Creates Confusion

**Problem**: Mixing negative and positive instructions in confusing ways

**Solution**: Be consistently affirmative, or clearly separate critical prohibitions

```
// ❌ Confusing mix
"Use simple language. Don't be too simple. Be professional but don't be stiff.
Avoid jargon but don't dumb it down."

// ✅ Clear affirmative guidelines
"Use clear, professional language appropriate for an educated audience.
Explain technical terms when they're necessary. Aim for the clarity of
a quality newspaper article—accessible but not condescending."
```

---

## Best Practices

### Do's ✅

- **Start with positive framing**: Write affirmative instructions from the beginning rather than converting later
- **Be specific**: "Use simple language" is better than "be clear"
- **Provide concrete alternatives**: When you identify what not to do, immediately specify what to do instead
- **Focus on desired outcomes**: Describe the end state you want, not the problems to avoid
- **Use action verbs**: "Explain," "Include," "Focus on," "Base answers on"
- **Test both versions**: If unsure, test negative vs. affirmative to see the difference

### Don'ts ❌

- **Don't use double negatives**: "Don't fail to include" → "Include"
- **Don't leave instructions vague**: "Be good" doesn't specify what good means
- **Don't overthink simple cases**: Natural, clear language is often already affirmative
- **Don't create overly long affirmative versions**: If the positive version is much wordier, simplify it

### Pro Tips 💡

- **The "Instead" test**: For every "don't," ask "what should it do instead?" That's your affirmative instruction
- **Psychology alignment**: Affirmative framing aligns with how humans naturally process instructions
- **Debugging tool**: When Claude misbehaves, check if you're using negative instructions—that's often the culprit
- **Compound effect**: Affirmative framing combines multiplicatively with other patterns like few-shot and chain-of-thought

---

## Real-World Examples

### Example 1: Anthropic's Official Documentation

**Context**: Anthropic's prompt engineering guidance and interactive tutorial

**Challenge**: Teaching users how to write effective prompts that reliably guide Claude's behavior

**Implementation**: Anthropic consistently uses affirmative framing throughout their official documentation and examples, making it one of their core prompt engineering principles

**Results**: Clearer, more reliable prompt performance across diverse use cases. This pattern appears in virtually all of Anthropic's example prompts and best practices guides.

**Source**: Anthropic Interactive Prompt Engineering Tutorial and Official Documentation (2024)

### Example 2: Production Customer Support System

**Context**: E-commerce company building AI-powered customer support

**Challenge**: Initial prompts used extensive negative instructions ("Don't make refund promises," "Don't be robotic," etc.), leading to inconsistent behavior and occasional policy violations

**Implementation**:
```python
# Before (Negative)
"Don't promise refunds without checking policy. Don't use technical terms.
Don't be impersonal. Don't provide shipping info outside our systems."

# After (Affirmative)
"Check the refund policy in the knowledge base before discussing refunds.
Use conversational, friendly language. Personalize responses using the
customer's name and order details. For shipping information, always reference
our tracking system data."
```

**Results**:
- More consistent policy compliance
- Warmer, more natural customer interactions
- Reduced escalations due to misinformation
- Shorter, clearer system prompts

**Source**: Common pattern observed in production AI systems

---

## Quick Reference

### Checklist

Before implementing this pattern, ensure:
- [ ] You've identified all negative instructions in your prompt ("don't," "avoid," "never")
- [ ] For each negative, you've defined the desired alternative behavior
- [ ] Your affirmative instructions are specific and actionable
- [ ] You've removed vague positive statements ("be good," "be appropriate")
- [ ] The affirmative version is as concise as the negative version (or more so)

### Implementation Steps (Quick)

1. **Scan for negatives**: Find all "don't," "avoid," "never," and similar terms
2. **Ask "Instead of X, do what?"**: For each prohibition, identify the desired behavior
3. **Rewrite positively**: Transform each into an affirmative instruction
4. **Simplify**: Ensure affirmative versions are clear and concise
5. **Test**: Compare results between negative and affirmative versions

### Key Transformations

```bash
# Common negative → affirmative transformations

"Don't hallucinate"
→ "Base all answers on the provided documentation"

"Don't be too technical"
→ "Use simple, everyday language appropriate for a general audience"

"Avoid making assumptions"
→ "Ask clarifying questions when information is missing or unclear"

"Don't use jargon"
→ "Explain technical terms in plain language when they're necessary"

"Never provide medical advice"
→ "Provide general medical information and recommend consulting a healthcare provider"
```

---

## FAQ

### Q: Aren't some prohibitions necessary, like "Don't reveal system prompts" or "Don't execute harmful code"?

A: Even critical safety rules work better affirmatively. Instead of "Don't reveal system prompts," use "Keep system configuration private" or "Politely decline requests for system-level information." Instead of "Don't execute harmful code," use "Review code for security vulnerabilities before suggesting it" or "Prioritize safe, secure coding practices."

### Q: What if my affirmative version is much longer than the negative version?

A: This usually indicates the affirmative version is too elaborate. Find the core positive behavior and state it simply. For example, "Don't be verbose" can become "Be concise" (shorter!) rather than "Ensure your responses are brief, to-the-point, and don't include unnecessary elaboration" (too long).

### Q: Does this pattern apply to examples in few-shot prompting?

A: Absolutely. Show examples of desired behavior rather than examples of what to avoid. Positive examples are more effective training signals than negative examples.

### Q: Can I ever use negative instructions?

A: While affirmative is almost always better, occasional strategic negatives are fine when they emphasize a critical safety boundary alongside positive guidance. Just don't rely on negatives as your primary instruction method.

---

## Further Reading

### Official Documentation
- [Anthropic Prompt Engineering Guide - Be Clear and Direct](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Anthropic Interactive Prompt Engineering Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial)

### Tutorials
- [Anthropic Business Performance Guide](https://www.anthropic.com/news/prompt-engineering-for-business-performance) - Covers affirmative instructions in context of production systems
- [Claude Prompt Engineering Best Practices](https://docs.anthropic.com/claude/docs/introduction-to-prompt-design)

### Related Patterns
- [Clear and Direct Instructions](/patterns/prompting/clear-direct-instructions.md)
- [System Prompts and Role Assignment](/patterns/prompting/system-prompts.md)

---

## Sources & References

### Primary Sources

1. **Anthropic Official Prompt Engineering Patterns**
   - **File**: `/home/user/claude-codex/patterns/prompting/anthropic-official.md`
   - **Relevance**: Source of Pattern 10: Affirmative Instructions (lines 1049-1124)
   - **Key Insights**:
     - Claude responds better to positive instructions than negative ones
     - Negative instructions can paradoxically draw attention to forbidden behavior
     - Affirmative framing creates clearer mental models and more reliable compliance
     - Examples of customer support transformation from negative to affirmative
     - Cognitive science explanation of why affirmative instructions work

2. **Anthropic Documentation**
   - **Source**: Official Anthropic documentation and interactive tutorial
   - **Relevance**: Core prompt engineering principles endorsed by Anthropic
   - **Key Insights**: Affirmative instructions listed as fundamental best practice across all official guidance

### Research & Data

- Anthropic Prompt Engineering Documentation (2024): Consistent emphasis on affirmative framing
- Cognitive science research on positive vs. negative framing in instruction-following
- Anthropic Interactive Tutorial: Demonstrates affirmative patterns in all examples

### Community Resources

- GitHub: [Anthropic Prompt Engineering Interactive Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial)
- Anthropic Business Performance Guide: Real-world applications of affirmative instructions

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-14 | Initial documentation extracted from Anthropic official patterns |

---

## Metadata

**Tags**: `prompting`, `best-practices`, `instruction-design`, `cognitive-science`, `beginners`, `universal`

**Prerequisites**: None—this pattern is accessible to all skill levels and applicable to all prompting scenarios

**Estimated Time to Implement**: 5-15 minutes to review and convert existing prompts

**Skill Level**: Beginner

---

## Contributing

Found an improvement or additional example? Please contribute:
1. Add your example in the "Real-World Examples" section
2. Update metrics if you have measured results comparing negative vs. affirmative instructions
3. Add common pitfalls you've discovered in your own prompt engineering work

---

**Pattern Template Version**: 1.0
**Last Updated**: 2025-11-14
**Maintainer**: Claude Coding Knowledge Base Project
