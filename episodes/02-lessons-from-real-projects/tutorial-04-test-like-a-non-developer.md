# Test Like a Non-Developer

## Goal

Check AI-assisted output with simple evidence before trusting it.

## Plain-English Idea

Testing does not always mean writing code.

For a non-technical builder, testing means:

1. Decide what should happen.
2. Try the smallest realistic action.
3. Compare expected vs actual.
4. Record evidence.
5. Fix one thing at a time.

This works for documents, spreadsheets, small apps, local demos, and prompt workflows.

## Fake Example

You asked AI to design a tiny stock checklist for a community pantry.

Expected:

- Add an item.
- Mark quantity.
- Flag low stock.
- Export a simple list.

Test with fake rows:

| Item | Quantity | Low-stock limit | Expected result |
|---|---:|---:|---|
| Rice | 4 | 5 | low stock |
| Tea | 12 | 5 | ok |
| Soap | 0 | 3 | low stock |

If the output marks tea as low stock, the logic is wrong.

You do not need to know programming to catch that.

## Try It

Before accepting an AI result, write this:

```text
Expected:
Actual:
Evidence:
Next fix:
```

Only ask for one fix at a time.

## Prompt Card

```text
Act as my testing helper.

Goal:
Create a plain-English test plan for this output:
[describe output]

Context:
I am not a developer. I can click, read, compare rows, and record what happened.

Constraints:
Use fake data only.
No private files.
No technical setup unless absolutely needed.
Each test must have expected result and actual result.

Path:
1. List the most important 5 things to test.
2. Give fake test data.
3. Tell me what success looks like.
4. Give me an evidence note template.

Checkpoint rule:
After the test plan, summarize what changed, what remains, and where risk is.

Done criteria:
I can test the output without guessing what "working" means.
```

## Common Failures And Fixes

| Failure | Why it happens | Fix |
|---|---|---|
| "Looks fine" replaces testing | No expected result | Write expected vs actual |
| Too many fixes at once | Panic after first bug | Fix one cause at a time |
| Real data used too early | Fake data was not prepared | Build fake rows before testing |
| Evidence is missing | No notes were kept | Save a short test log |
| AI says done too soon | Done criteria are weak | Define what must pass |

## Recap

- Testing is comparison, not magic.
- Fake data protects privacy and makes bugs easier to see.
- Evidence beats panic.
- One fix at a time keeps the work understandable.

## Worksheet

Use the [checkpoint review sheet](worksheets/checkpoint-review-sheet.md) and the test-note section inside it.
