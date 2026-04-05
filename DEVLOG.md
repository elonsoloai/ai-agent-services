# AI Agent Development Log

> Weekly insights from building AI-powered automation

---

## Week 1 (2026-04-03 to 2026-04-09)

### What I Learned from Claude Code's Leaked System Prompt

**Source:** Anthropic accidentally published 50,000 lines of TypeScript source code with source maps in their npm package (March 2026).

**Key insights from 1,490 lines of system prompt:**

#### 1. Task Management is Survival
```
- Every action tracked with TodoWrite
- Clear state: pending → in_progress → completed
- User visibility at all times
```

#### 2. Tone Constraints
```
- No emojis unless requested
- No time estimates
- Technical accuracy > user validation
```

#### 3. Opinionated Tools
```
- Edit: requires EXACT text match (no fuzzy)
- Bash: refuses interactive commands
- Read: defaults to full file, not guessing
```

**My takeaway:** Build systems, not prompts. Constraints = reliability.

---

## Week 2 Preview

- Building a demo AI agent (open source)
- Case study: First client automation project
- Deep dive: State management in AI agents

---

*Follow for weekly technical updates.*
