# Beginner Guide: What Is Harness Engineering?

Harness engineering is a simple way to work with AI without getting pulled into a rabbit hole.

If you have ever asked AI for help and ended up with too many files, too many ideas, too many errors, or no clear next step, you have felt the problem.

The problem is not that you were "vibing" with AI. Exploring is useful. The problem is unmanaged vibing.

## The Rabbit Hole

A rabbit hole happens when the work keeps expanding but the goal becomes less clear.

Common signs:

- The AI starts solving a different problem.
- You get output you cannot check.
- The task becomes bigger than expected.
- You do not know what changed.
- You keep asking follow-up questions just to recover control.

## The Harness

A harness is a reusable structure around AI work.

It does not make the work boring. It makes the work safer to explore.

Use this formula:

```text
Goal + Context + Path + Checkpoints + Done Criteria
```

## The Five Parts

**Goal**

What are we trying to finish?

Example: "Create a simple tracker for animation assets."

**Context**

What does the AI need to know about your domain?

Example: "Assets can be characters, props, environments, or effects. Each asset has a status and owner."

**Path**

What steps should the AI follow?

Example: "First design the fields. Then propose the screen. Then write the first version."

**Checkpoints**

Where should the AI stop and report back?

Example: "After each major step, summarize what changed, what remains, and where risk is."

**Done Criteria**

How do we know the task is finished?

Example: "The tracker can add, edit, filter, and export assets. The fields match our workflow."

## Bad Prompt

```text
Build me an app for tracking animation assets.
```

This prompt may work, but it gives the AI too much room to drift.

## Harnessed Prompt

```text
I want to build a simple animation asset tracker.

Goal:
Create a small first version that helps me track characters, props, environments, and effects.

Context:
Each asset has a name, type, status, owner, due date, and notes.
The users are artists and producers, not software engineers.

Path:
First ask up to 3 questions if anything important is missing.
Then propose the fields and screen layout.
Wait for my confirmation before writing the app.

Checkpoints:
After each major step, summarize what changed, what remains, and where risk is.

Done:
The first version can add, edit, filter, and export assets.
Keep the design simple enough for a non-technical team.
```

## Why This Helps

The AI is still creative. You are still allowed to explore. But now the work has rails:

- The goal is visible.
- The domain context is shared.
- The path is agreed.
- The checkpoints catch drift.
- The done criteria prevent endless polishing.

## Try It

Pick one repeated task in your own domain.

It can be patient follow-up, chemical inventory, 3D asset tracking, game design, lesson planning, report writing, or anything you do more than once.

Turn it into a harness using the worksheet.

Closing idea:

> Your expertise is the context. Harness engineering is how you make AI use it without dragging you into the hole.
