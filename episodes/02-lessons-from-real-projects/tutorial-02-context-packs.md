# Context Packs: Give AI Enough Memory Without Sharing Secrets

## Goal

Build a small context pack for one repeated workflow without exposing sensitive information.

## Plain-English Idea

AI performs better when it understands the job.

That does not mean you should paste everything.

A context pack is a small folder of reusable notes:

```text
context-pack/
  README.md
  DOMAIN.md
  PROMPTS.md
  EXAMPLES.md
  CHECKPOINTS.md
  GEMINI.md
```

It tells AI what matters, what is forbidden, what good output looks like, and when to stop.

## Fake Example

Imagine a student club that prepares event announcements every month.

The context pack could include:

- `README.md`: "This pack helps draft event announcements."
- `DOMAIN.md`: audience, tone, required event details, forbidden claims.
- `PROMPTS.md`: draft announcement, shorten announcement, check clarity.
- `EXAMPLES.md`: one good fake announcement and one weak fake announcement.
- `CHECKPOINTS.md`: review gate before posting.
- `GEMINI.md`: language notes, audience notes, continuation notes.

The pack should not include real student phone numbers, private chat exports, payment records, or personal details.

## Try It

Choose one workflow you repeat at least twice a month.

Create only three files first:

```text
README.md
DOMAIN.md
PROMPTS.md
```

Add examples later after you see what breaks.

## Prompt Card

```text
Act as my context-pack designer.

Goal:
Help me create a small context pack for this repeated workflow:
[workflow]

Context:
The user is [audience].
The output should be [output].
The workflow repeats [how often].

Constraints:
Use fake examples only.
Do not ask for private records.
Do not include names, phone numbers, account details, or local paths.

Path:
1. Propose the minimum context-pack file list.
2. Draft short starter content for each file.
3. Add a safety section that says what must not be included.

Checkpoint rule:
After drafting the pack, summarize what changed, what remains, and where risk is.

Done criteria:
The pack can be reused next time without re-explaining the whole workflow.
```

## Common Failures And Fixes

| Failure | Why it happens | Fix |
|---|---|---|
| Context pack becomes a diary | Too much raw history | Keep only reusable rules and examples |
| Sensitive data slips in | Real examples were copied | Replace with fake examples |
| AI still misses domain terms | Terms are not defined | Add a short glossary to `DOMAIN.md` |
| Pack gets too large | It tries to cover every job | One pack per repeated workflow |
| Future sessions forget decisions | No handoff file | Add `GEMINI.md` with continuation notes |

## Recap

- Context is not a data dump.
- A good context pack is small, reusable, and safe.
- Fake examples are usually enough for teaching AI the shape of work.
- A handoff file helps future sessions continue without private memory.

## Worksheet

Use the [handoff checklist](worksheets/handoff-checklist.md).
