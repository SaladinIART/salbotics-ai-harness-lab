# Turn a Vague Idea Into an AI Work Order

## Goal

Turn a loose idea into a clear AI work order that a non-technical builder can review.

## Plain-English Idea

A vague prompt gives AI too much room to wander.

A work order gives the task a shape:

```text
Goal + Context + Path + Checkpoints + Done Criteria
```

This does not make the work boring. It makes the work easier to inspect.

## Fake Example

Vague prompt:

```text
Build me a tracker for my weekend food stall.
```

Better work order:

```text
Build a simple first version of a food stall tracker for one owner.

Context:
The owner sells 12 menu items. Each sale has item, quantity, payment method,
and note. Use fake data only.

Path:
First propose fields and screen flow. Then propose a tiny test plan.
Do not write code until the plan is approved.

Checkpoints:
After each major step, summarize what changed, what remains, and where risk is.

Done:
The first version can add a sale, list today's sales, show total revenue,
and export a simple CSV.
```

The second version tells AI what "good enough" means.

## Try It

Pick one task you repeat often:

- cleaning a spreadsheet
- planning social posts
- sorting receipts
- tracking study notes
- preparing a workshop checklist

Write one work order before asking AI to help.

## Prompt Card

```text
Act as my build guide.

Goal:
Help me turn this rough idea into a small first version:
[write idea here]

Context:
The user is [who uses it].
The task happens when [real-life situation].
Important terms:
- [term 1]
- [term 2]

Constraints:
Use fake data only.
Keep the first version small.
Do not add extra features unless I approve them.

Path:
1. Restate the goal.
2. Ask up to 3 questions only if they change the plan.
3. Propose fields, screen flow, and done criteria.
4. Wait before implementation.

Checkpoint rule:
After each major step, summarize what changed, what remains, and where risk is.

Done criteria:
I can explain the plan to another person in 2 minutes.
The first version has clear inputs, outputs, and test steps.
```

## Common Failures And Fixes

| Failure | Why it happens | Fix |
|---|---|---|
| AI builds too much | Goal is too broad | Ask for a "small first version" |
| AI asks endless questions | No question limit | Say "ask up to 3 questions only if they change the plan" |
| AI invents data | No data rule | Say "use fake data only" |
| Output cannot be checked | No done criteria | Define what must work before the task starts |
| Work drifts | No checkpoints | Add the checkpoint rule |

## Recap

- A prompt is a request.
- A work order is a request with review boundaries.
- Good AI work starts smaller than your ambition.
- If you cannot check the result, the prompt is not ready.

## Worksheet

Use the [prompt brief worksheet](worksheets/prompt-brief-worksheet.md).
