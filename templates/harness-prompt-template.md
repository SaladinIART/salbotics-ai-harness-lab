# Harness Prompt Template

Use this for any AI-assisted task where you want creativity without rabbit holes.

```text
Act as my [role: build guide / writing partner / research assistant / reviewer].

GOAL
Build or produce [specific outcome] for [specific user] by [time / quality bar].

BACKGROUND / CONTEXT
Here is the domain context you must use:
- [terms, rules, definitions]
- [examples]
- [files or references]
- [what good output looks like]

INPUTS AVAILABLE
- [data, notes, screenshots, rough idea, existing files]

CONSTRAINTS
Stay within:
- tools: [allowed tools]
- scope: [what not to do]
- safety/compliance: [domain rules]
- style: [tone, format, design direction]
- time/budget: [limits]

ASK-BEFORE-ACTION RULE
Before doing the work, ask only questions that materially change the plan.
If no question is needed, state your assumptions and proceed.

PATH
Propose a short step-by-step path before implementation.
Keep the path small enough that I can review each step.

CHECKPOINT RULE
After each major step, summarize:
1. What changed
2. What remains
3. Where risk is

DONE CRITERIA
Stop when these acceptance criteria pass:
- [criterion 1]
- [criterion 2]
- [criterion 3]

Do not expand scope unless I explicitly approve it.
```

