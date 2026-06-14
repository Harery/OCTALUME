# Stage 1 — Brain Dump Intake
Layer: Macro | Enhancements: E2 (classifier), E7 (language)
Output: docs/product-spec.md

---

## Step 0 — Open with one message, ask for the raw idea

Send this before anything else:

> "Tell me about your idea — don't worry about structure, don't worry about details.
> Just write it the way you'd explain it to a friend. I'll read everything you give me
> and come back with the right questions."

Do not ask anything else. Wait.

---

## Step 1 — Analyze the dump internally (never show this work)

After the dump arrives:

1. **E7** — detect language. If non-English:
   - Note the language internally
   - Prepend a single line to the top of your Q1–Q9 message: *"Your idea is in [language] — should I deliver all outputs in [language] or in English?"*
   - This is part of the same message as the 9 questions — NOT a separate round-trip
   - Wait for all 9 answers + language preference together before proceeding
2. **E2** — classify the product type:
   - Marketplace → payment split + provider/consumer SEO path
   - SaaS → subscription logic + feature comparison SEO
   - Content platform → content schema priority
   - Service portal → booking logic + LocalBusiness schema
   - Education platform → Course schema + teacher/student logic
   - Community/social → moderation logic mandatory
3. Build your internal picture:
   - What is this? (one sentence)
   - Who uses it?
   - What is the core job?
   - What is clearly stated vs what you are inferring vs what is missing?
4. List the real gaps — these become your 9 questions

---

## Step 2 — Generate 9 dynamic questions

Each question targets a real gap from this specific project.
Not a template. Not a checklist. Based on what was actually in the dump.

**Cover these gap areas — pick the 9 most relevant to this project:**
- Who actually uses this (if vague or assumed)
- The one core action the product must do (if unclear)
- What success looks like in real numbers (if not stated)
- Why existing tools aren't good enough (if not explained)
- A hard limit — something this must never do (always ask if absent)
- Budget reality (always ask if not mentioned)
- Timeline or launch pressure (ask if there's any hint of urgency)
- Who runs it after launch (if not mentioned)
- Any locked-in tools, platforms, or legal constraints (if not mentioned)

**Format — strict:**

```
Q[N]. [Question — one sentence, plain words, conversational tone]

  A. [Short option]
  B. [Short option]
  C. [Short option]  ← I'd go with this based on what you shared
  D. [Short option]
  E. Something else — tell me

```

Rules:
- One recommended option per question — based on the dump, not a generic default
- Never recommend the same option (A/B/C/D) twice in a row across all 9 questions
- Option text: one line, no jargon, no compound sentences
- Question text: how a person talks, not how a document reads
- No AI writing. No corporate tone. Nothing that sounds like a survey form.

**Send all 9 questions in one message. Wait for all 9 answers.**

---

## Step 3 — After all 9 answers

1. Merge the dump + all answers into one complete picture
2. Flag anything still unclear as an assumption — do not ask again
3. Run a web search on the product domain before writing the output
4. Write docs/product-spec.md

---

## Output — docs/product-spec.md

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRODUCT SPEC — [Project Name]
docs/product-spec.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Product type
[type from E2 classifier + preset path activated]

## Language
[detected + output language confirmed]

## What this does
[1–2 sentences. A non-technical person must understand it immediately.]

## Who it's for
[Real people. Specific. Not personas. Not "SMBs".]

## The core job
[The one action above all else.]

## Success definition
[From the answers — include a real number if one was given]

## Primary keyword universe
[5–10 search terms real users would type — search-verified]

## Signal inventory
[Every distinct idea from the dump + answers, numbered, unsorted]

## Hard constraints
[Locked-in tools, legal limits, red lines — from answers]

## Budget model
[What was stated]

## Operator model
[Who runs it and how]

## Timeline
[What was stated, or "none stated"]

## Not building yet
[Deferred ideas + one-line reason each]

## My assumptions
[What I inferred but wasn't stated — operator corrects if wrong]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Gate → Stage 2 sub-skill: `stages/s02-brd.md`
