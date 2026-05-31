# Public Lessons From Private Projects

## Goal

Share useful lessons from real work without exposing private details.

## Plain-English Idea

Not every lesson should become a case study.

Sometimes the safe public version is a pattern:

```text
Private story -> general lesson -> fake example -> checklist
```

The public lesson should help the reader even when all private details are removed.

## Fake Example

Private version:

```text
We built a tool for [real organization] that handled [real data] and solved [specific internal problem].
```

Public-safe version:

```text
From building local tools, one lesson became clear: AI work needs fake sample data before testing with real records. A safe first test uses 3 to 5 invented rows that cover normal, empty, and edge cases.
```

The public version teaches the method without exposing the organization, data, or internal workflow.

## Try It

Before sharing any project lesson, write two versions:

1. Private truth: what actually happened.
2. Public lesson: what others can safely learn.

Then delete the private truth from the publishable draft.

## Prompt Card

```text
Act as my public-safety editor.

Goal:
Turn this private project note into a safe public lesson:
[paste note only after removing obvious sensitive details]

Context:
The audience is non-technical builders who need practical AI workflow advice.

Constraints:
Do not include client names, local paths, private repo names, account details,
commercial strategy, operational numbers, or personal notes.
Use fake data and generic labels.
If the lesson depends on private detail, say it should not be published.

Path:
1. Identify sensitive details.
2. Extract the general lesson.
3. Rewrite as a fake example.
4. Add a checklist readers can reuse.

Checkpoint rule:
Summarize what changed, what remains, and where risk is.

Done criteria:
The result is useful without exposing the original project.
```

## Common Failures And Fixes

| Failure | Why it happens | Fix |
|---|---|---|
| Case study reveals too much | Specifics feel more convincing | Teach the pattern, not the private event |
| Fake data looks real | Values are too detailed | Mark examples as fake and keep them simple |
| Private path remains | Draft copied from local notes | Search for drive letters and folder separators |
| Strategy leaks | "Why we built it" reveals advantage | Share user-facing lesson only |
| Lesson becomes vague | Too much was removed | Add a fake example and worksheet |

## Recap

- A public lesson does not need private proof.
- Patterns, checklists, and fake examples travel better than confidential stories.
- If redaction removes the lesson, do not publish it.
- The safest useful unit is often a prompt card or worksheet.

## Worksheet

Use the [redaction checklist](worksheets/redaction-checklist.md).
