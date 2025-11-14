# Contributing to Claude Coding Knowledge Base

Thank you for your interest in contributing to this knowledge base! This guide will help you add valuable content to our collection.

## How to Contribute

### Adding New Sources

1. **Create a new file** in the appropriate `/sources/` subdirectory:
   - `/sources/docs` - Official documentation
   - `/sources/youtube` - Video transcripts or summaries
   - `/sources/github` - Code examples and discussions
   - `/sources/blogs` - Blog posts and articles
   - `/sources/reddit` - Reddit discussions
   - `/sources/twitter` - Twitter threads and insights

2. **File naming convention**: Use descriptive names with dates
   - Example: `2024-01-anthropic-prompt-engineering.md`
   - Example: `2024-02-hamel-husain-effective-prompting.md`

3. **Include metadata** at the top of each source file:
   ```markdown
   ---
   title: [Title of the source]
   author: [Author name]
   url: [Original URL]
   date: [Publication date]
   type: [docs/video/article/discussion]
   ---
   ```

### Extracting Patterns

1. Read through collected sources
2. Identify reusable patterns or principles
3. Create a new file in the appropriate `/patterns/` subdirectory
4. Use the pattern template (see below)

### Pattern Template

```markdown
# [Pattern Name]

## Context
When does this pattern apply?

## Problem
What problem does this solve?

## Solution
How to implement this pattern

## Examples
Real-world examples

## Anti-patterns
Common mistakes to avoid

## Sources
- Link to source files that support this pattern
```

## Quality Standards

- **Accuracy**: All information must be verifiable from sources
- **Clarity**: Write clear, concise explanations
- **Citations**: Always link back to source material
- **Examples**: Include practical code examples where applicable

## Review Process

1. Create a branch for your changes
2. Submit a pull request with a clear description
3. Address any feedback from reviewers
4. Once approved, changes will be merged

## Questions?

Open an issue for any questions or discussions about contributions.
