# The Checkpoint Rule: Stop Rabbit Holes Early

## Goal

Use checkpoints so AI work stays visible and correctable.

## Plain-English Idea

A rabbit hole starts when work keeps moving but you stop understanding what changed.

The checkpoint rule is simple:

```text
After each major step, summarize:
1. What changed
2. What remains
3. Where risk is
```

This turns hidden movement into visible progress.

## Fake Example

You ask AI to help plan a simple volunteer signup tracker.

Without checkpoints, AI might jump from spreadsheet fields to website design to database setup.

With checkpoints, the work stops after each useful step:

```text
Checkpoint 1:
Changed: Defined fields for volunteer name, role, date, contact permission, and notes.
Remains: Decide whether this stays as a spreadsheet or becomes a small app.
Risk: Contact details are sensitive. Use fake data in examples.
```

Now you can correct direction before the project grows.

## Try It

Add this line to any multi-step AI request:

```text
After each major step, stop and summarize what changed, what remains, and where risk is. Wait for my confirmation before continuing.
```

Use it especially when AI is:

- writing many files
- changing a plan
- reviewing sensitive material
- debugging with repeated attempts
- turning a rough idea into a product

## Prompt Card

```text
Act as my project guide.

Goal:
Help me complete this task in small reviewable steps:
[task]

Context:
I am non-technical and need to understand each major change before the next one.

Constraints:
Use fake data.
Keep the task small.
Do not skip review checkpoints.

Path:
Propose 3 to 5 steps.
After each step, stop.

Checkpoint rule:
For every stop, summarize:
1. What changed
2. What remains
3. Where risk is

Done criteria:
I can see the final output, understand what changed, and know what still needs human review.
```

## Common Failures And Fixes

| Failure | Why it happens | Fix |
|---|---|---|
| AI continues after a checkpoint | Stop rule is weak | Say "wait for my confirmation before continuing" |
| Checkpoint is too vague | AI reports effort, not outcome | Ask for changed/remains/risk |
| Risk is hidden | AI avoids uncertainty | Require one risk note per checkpoint |
| Too many checkpoints | Steps are too tiny | Use checkpoints after major steps only |
| Human review is skipped | Done criteria are unclear | Define acceptance criteria before work starts |

## Recap

- Checkpoints are review gates, not paperwork.
- The risk line is often the most valuable line.
- Waiting before the next step protects attention, privacy, and scope.
- A checkpoint can save hours of cleanup.

## Worksheet

Use the [checkpoint review sheet](worksheets/checkpoint-review-sheet.md).
