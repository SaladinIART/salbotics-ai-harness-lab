# Speaker Notes: Implement Harness Engineering

Target: 15-20 minutes, casual English, slides-only.

## 1. Implement Harness Engineering

Open with audience pain, not theory.

"This talk is for people who already have expertise. Doctors, chemical engineers, 3D artists, builders. You have been playing with AI. Sometimes it feels magical. Sometimes it becomes a rabbit hole.

My claim is simple: vibing is not the problem. Unmanaged vibing is. Harness engineering is how we keep exploration useful."

## 2. Rabbit Holes

"You ask AI to build something simple. Then it asks you to install a thing. Then it changes framework. Then it creates files you did not ask for. Then it explains an error using words that sound confident. Thirty minutes later: 12 files, 6 errors, no idea what happened."

Define rabbit hole:

- Goal drift
- Missing context
- No stop rule
- No review loop

## 3. Harness Engineering

"A harness is not a cage. It is the thing that lets power move safely. In AI work, the harness is reusable structure around the conversation."

Formula:

`Goal + Context + Path + Checkpoints + Done Criteria`

Punchline: "Do not prompt harder. Harness better."

## 4. Before / After

Bad prompt: "Build me an app for tracking patients / chemicals / animation assets."

"This is not a bad human. This is a naked prompt."

Harnessed prompt:

"Act as my build guide. First ask 3 scoping questions. Then propose a 3-step path. After each step, summarize changes, remaining work, and risk."

## 5. Harness Prompt Template

"You can use this tomorrow. Replace the bracketed bits. If you are a doctor, your domain terms go into background. If you are a chemical engineer, safety constraints go into constraints. If you are a 3D animator, art style and pipeline constraints go there."

## 6. Context Is The New Code

"Patrick Debois described context as something we engineer, not something we randomly paste. The lifecycle is simple: generate context, evaluate it, distribute it, observe what happens."

Do not dwell on the acronym. Use it as validation that prompt libraries are part of a bigger operating loop.

## 7. Context Pack

"A context pack is a little folder of reusable knowledge. It is not tool lock-in. It can be markdown. It can travel across AI tools."

Open standard posture:

- `AGENTS.md`
- `GEMINI.md`
- `SKILL.md`
- reusable prompt packs
- examples and checkpoints

## 8. Library Ladder

"Do not start with a huge library. Start with one prompt you use twice. Turn it into a checklist. Add domain rules. Add examples. Share it with one person. Then improve based on what breaks."

## 9. Checkpoint Rule

"This rule is the cheapest anti-rabbit-hole tool I know. After each major step, make AI summarize what changed, what remains, and where risk is."

Why it works: it converts hidden movement into visible progress.

Optional bridge to future labs:

"This also applies to fun work like game design. A small snake game can become multiplayer, skins, leaderboard, story mode, and asset pipeline very quickly. The harness protects version one so the game becomes playable before it becomes huge."

## 10. Next Stage

"Pick one task you repeat often. Build one context pack. Use it three times. Improve it once. Share it with one person."

Closing line:

"Your expertise is the context. Harness engineering is how you make AI use it without dragging you into the hole."
