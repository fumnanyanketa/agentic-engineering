# Module 2 · Lesson 3: The Prompting Playbook

> **Course:** Building with Claude, a self-paced course
> **Module 2:** Core skills, working with the model
> **Speaker:** Margo van Laar, Applied AI Engineer, Anthropic (London)
> **Source talk:** [The prompting playbook](https://www.youtube.com/watch?v=G2B0YWuJUgI) · [full transcript](../../transcripts/code-with-claude-2026-london-2026/05_the-prompting-playbook.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

Prompting is a debugging skill, not a writing skill. You improve a prompt by making changes one at a time and checking each change against a set of tests, you tidy the prompt up first, and you reach for the right fix (clearer structure, a tool, a stronger model, or a multi step process) instead of just adding more instructions.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you build a small tool called **PromptLab** and use it to take a real assistant from broken to working. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project: build PromptLab"** section near the end, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Prompt engineering overview (Anthropic docs)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)** (docs). The official, durable method: define success and evals first, structure the prompt, and recognize when a different lever (model, tool) is the real fix rather than more instructions.
> - **[Language Models are Few-Shot Learners (GPT-3)](https://arxiv.org/abs/2005.14165)** (paper). The seminal paper establishing why in-context prompting and examples work at all.

## A few plain-language basics first

This lesson uses some everyday AI terms. Here they are in simple words, so nothing below is confusing:

- **LLM (Large Language Model):** the kind of AI that reads and writes text. "Claude" is an LLM. Think of it as a very capable text assistant.
- **Model:** one specific version of that AI, for example "Sonnet 4.6" or "Opus 4.7." Different models have different strengths, speeds, and prices, much like different car engines.
- **Prompt:** the text instructions you give the model to tell it what to do and how to behave. Writing good prompts is called **prompt engineering**.
- **Token:** the unit the model reads and writes in. A token is roughly three quarters of a word. You are billed per token, so "using more tokens" means "costing more and taking longer."
- **Latency:** how long the model takes to respond, measured in seconds. Lower is faster.
- **API (Application Programming Interface):** the connection your code uses to send a prompt to the model and get its answer back. An "API call" is one such request.
- **Eval (evaluation):** a set of test cases you run a prompt against to measure whether it works. This is the single most important idea in the lesson.
- **Harness:** all the code and settings around the model (the API call, the tools you give it, the loop that runs it). The prompt is what you say to the model; the harness is everything else that surrounds it.

You do not need to memorise these. Every term is also explained again the first time it appears below.

## Why this lesson matters

Prompting was, in Margo's words, "arguably the first skill we had to learn as engineers working with LLMs, and it continues to be one of the most critical." In real jobs you are usually not writing a prompt from a blank page. More often you are maintaining a prompt that several people have edited over time, that mixes rules, tone, and old fixes together, and that suddenly works worse after you switch to a newer model. This lesson gives you a repeatable method for that exact situation, and then shows how to start a brand new assistant the right way.

## Learning objectives

By the end of this lesson you will be able to:

1. Build a small **eval** (a set of test cases) with the three kinds of cases every prompt needs.
2. Apply basic **prompt cleanup** (clear structure, removing junk, defining the output) before chasing specific problems.
3. Work out *why* a prompt is failing and pick the correct fix: rewrite an instruction, give the model a **tool**, switch model or reasoning effort, or split the work into a **multi step loop**.
4. Spot and avoid the most common trap: leftover instructions from older models that quietly make newer models behave worse.

## Prerequisites

- Module 2 · Lesson 1 (this lesson assumes you know the basics of sending a message to Claude and getting a reply).
- Helpful but optional: Module 3 (Evals for taste). This lesson leans on evals, and Module 3 goes deeper on them. You can do them in either order.

---

## Part 1: the setup, a prompt in trouble

Picture a customer support chatbot for a made up phone company called **Meridian Mobile**. ("Customer support chatbot" just means an assistant that answers customer questions about their account.) The prompt behind it has, in Margo's description, "no clear owner," it covers "policy, tone, processes," and it carries "patches for previous models all mixed together." A **patch** here means a small instruction someone added in the past to fix a specific problem with an older model. After the team switches to a newer model, several of their tests start failing.

> 🔑 **Key idea: you cannot fix what you cannot measure.** When a prompt gets worse after a model change, there are only two possible reasons, and you must tell them apart:
> 1. The new model is just as capable but **behaves differently**. You can fix this by adjusting the prompt.
> 2. The new model is **less capable** at this task. No amount of prompting will fix that, and you need a different model.
> An **eval** (your set of test cases) is what lets you tell which situation you are in, and it proves whether a change actually helped or not.

### The three kinds of test cases every eval needs

An **eval** is just a collection of **test cases**. A test case is one example input plus the answer you expect. The demo uses only five test cases to stay simple (a real one would have many more), but they cover three essential kinds:

| Kind of case | What it checks | Meridian example |
|---|---|---|
| **Control case** | Something that should *always* work. It is clear cut and the model handles it well. It is your "nothing is on fire" signal. | "What is the data limit on the basic plan?" |
| **Edge case** | Something the model has gotten wrong before. The prompt should stop that mistake from coming back. | Doing the billing maths; not hiding information it actually has. |
| **Capability or handoff case** | Does the model know the limits of its job: when to pass the customer to a human, or when to refuse? | Sending billing disputes to a human. |

> 💡 The capability or handoff case is the one teams most often forget. A model that confidently answers something it should have passed to a human is more dangerous than one that simply fails and says so.

### The method

Here is the loop you will repeat for the rest of Part 1, 2, and 3:

```text
1. Run the eval on version 0 of the prompt   -> see what is failing
2. Clean up the prompt first                 -> often an easy win on its own
3. Fix failing cases ONE AT A TIME           -> so cause and effect are clear
4. Re-run the eval after every change         -> keep what helps, undo what does not
```

On the first run, the control case passes but the bot "performs pretty poorly in the other areas." Before zooming in on any single problem, clean the prompt up.

---

## Part 2: prompt cleanup (do this first, every time)

The original prompt has obvious problems. It tells the bot it is a human, "which just isn't true." It contains text that was clearly copied straight off a web page: the giveaway is "a reference to a hero image" (a "hero image" is the big banner picture at the top of a website) and even "references to cookies at the bottom" (website "cookies" are unrelated to a support bot). And everything is crammed "into one big paragraph" with no separation between rules, tone, and data.

### Fix 2.1: add structure with XML tags

**XML tags** are labels written in angle brackets, like `<role>` and `</role>`, that mark where a section starts and ends. They are an easy way to show the model which part of the prompt is which. A messy, unlabelled prompt looks like this:

```text
You are a friendly human support rep for Meridian Mobile. Our hero image
shows... [website junk] ... Always be polite. Never give wrong plan
details, point them to the URL. Plans: basic 10GB... We use cookies to...
Always calculate prorated amounts correctly.
```

Restructure it so each kind of information is clearly separated:

```text
<role>
You are a customer support assistant for Meridian Mobile, a mobile network operator.
</role>

<guidelines>
- Be concise, warm, and conversational.
- Answer using the customer's account data as the source of truth.
</guidelines>

<policy>
- Plan data allowances are listed in <plan_data>.
- Customers on grandfathered or legacy plans may have different allowances.
  These are captured in the customer's account context.
</policy>

<tone>
Friendly and professional. Avoid jargon.
</tone>

<plan_data>
...
</plan_data>
```

Just doing this, with no other change, already improves the results. (A **grandfathered** or **legacy** plan means an old plan a customer is still on even though the company stopped offering it to new customers. More on that in Part 3.)

> 🔑 **Rule of thumb (quote):** "If you're reading a prompt and you can't tell guidelines from policy from data, most likely the model isn't able to either." (Margo van Laar)

### Fix 2.2: define the output, and enforce it in the harness

An **output contract** is simply a clear statement of the exact format you want the answer in. If your answers come back in inconsistent shapes, define the format and then back it up in the **harness** (the code around the model) rather than hoping the prompt alone is enough.

```text
<output_format>
Respond with your message wrapped in <response>...</response> tags.
</output_format>
```

```python
# Enforce the format in the harness, not just in the prompt text.
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,                  # the most tokens (text) the reply may use
    system=system_prompt,
    messages=messages,
    stop_sequences=["</response>"],   # stop generating the moment this text appears
)
```

A **stop sequence** is a piece of text that tells the model "stop writing as soon as you produce this." Here it makes the model stop right after it closes the `</response>` tag, which keeps the output tidy.

> 💡 If your output is more complicated (for example **JSON**, a common machine readable text format that uses braces and quotes), use a feature called **structured outputs**, which forces the answer into a fixed shape automatically. As Margo puts it, the prompt "is not always the most effective way of handling issues," so change the harness too.

After cleanup, two of the five cases pass reliably. Three problems remain: **hotspot**, **proration**, and **billing error**. Now fix them one at a time.

---

## Part 3: fixing failures one at a time

### Failure 3.1: the model hides information it actually has (the "hotspot" case)

"Hotspot" here means using your phone as a wireless internet source for other devices, and plans include a data allowance for it.

**Question:** "How much hotspot data is on my unlimited plan?"
**The customer's reality:** they are on a grandfathered (old) plan, and their account record clearly says **5 GB**.
**The bug:** the bot ignores that and answers with the generic "4 GB," then tells the customer to "go check this out yourself" by sending them to a web link, instead of giving the answer it already has.

The instruction causing this:

```text
We changed our plans recently. The policy doc shows current plan data, and
customers on grandfathered plans have different rates. NEVER give a customer
the wrong plan details, instead point them to the URL.
```

That "never give wrong details, send them to the URL" line is an old patch written for a weaker model. Newer models follow instructions more literally, so the patch is now **overfitted**. (**Overfitting** means following a rule so rigidly that it backfires. Here the bot suppresses the correct answer just to avoid any risk of being "wrong.") The fix is to state the balanced truth and trust the data:

```text
Customers on grandfathered plans may have different allowances. The customer's
account context is the accurate source of truth, so use it to answer directly.
```

> 🔑 **Lesson:** everyone worries about the model **inventing** facts (this is called **hallucination**, when an AI states something untrue as if it were true). But the opposite also happens: the model **withholds** information it genuinely has, usually because of a defensive patch like this one.
> ✅ **Best practice: keep a record of your defensive changes.** **Version control** (a system like Git that tracks every edit and why it was made) lets you note why each patch was added. A newer model can turn an old patch harmful, and you will want to find it and remove it.

### Failure 3.2: doing maths in its head (the "proration" case)

**Proration** means charging only for the part of a billing period you actually used. If you upgrade your plan halfway through the month, proration works out the fair amount for the remaining days.

**Question:** "What if I upgrade to the 30 GB plan? What will my next bill be?"
**The bug:** the model "reasons through it, does a little mental math" (works the sum out in its head), but never gives a concrete, trustworthy number.

The instruction causing this only *nags* the model:

```text
Don't ever give a customer a vague answer. CRITICAL: always calculate any
prorated amounts correctly.
```

> 🔑 **Lesson (quote):** "Instructions don't add capability. Telling the model it's critical to do a calculation right doesn't make it better at mental maths."

The right fix is to give the model a **tool**. A **tool** is a small function (a piece of code) that the model can choose to run when it needs to, for example to do exact maths or look something up. **Tool use** is the general name for this ability. There are three steps.

```text
# 1. In the prompt: tell it when to use the tool
Whenever a calculation is required, use the calculate_proration tool. Do not
do arithmetic yourself.
```

```python
# 2. Describe the tool so the model knows what it does and when to call it.
#    This description is called the "tool schema".
calculate_proration_tool = {
    "name": "calculate_proration",
    "description": "Calculate a prorated charge when a customer changes plan "
                   "partway through a billing cycle. Use this for ANY billing math.",
    "input_schema": {                       # the inputs the tool expects
        "type": "object",
        "properties": {
            "old_plan_price": {"type": "number"},
            "new_plan_price": {"type": "number"},
            "days_remaining":  {"type": "integer"},
            "days_in_cycle":   {"type": "integer"},
        },
        "required": ["old_plan_price", "new_plan_price",
                     "days_remaining", "days_in_cycle"],
    },
}

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system=system_prompt,
    tools=[calculate_proration_tool],       # hand the tool to the model
    messages=messages,
)
```

```python
# 3. Write the actual maths the tool runs.
def calculate_proration(old_plan_price, new_plan_price, days_remaining, days_in_cycle):
    daily_old = old_plan_price / days_in_cycle
    daily_new = new_plan_price / days_in_cycle
    credit  = daily_old * days_remaining    # money owed back for the unused old plan
    charge  = daily_new * days_remaining    # cost of the new plan for the remaining days
    return round(charge - credit, 2)
```

(A **tool schema** is the written description of a tool: its name, what it does, and what inputs it needs. The model reads the schema to decide when and how to use the tool.) With the tool connected, the case passes. The model "does the maths using the tool in the background and returns the correct response."

### Failure 3.3: only telling one side of the story (the "billing error" case)

**Scenario:** a genuine billing dispute that should be **escalated** (passed up) to a human staff member.
**The bug:** the bot tries to diagnose and explain the problem itself instead of escalating.

The instruction causing this tells only one side:

```text
Avoid escalating or transferring to a care specialist unless absolutely
necessary, as it costs ~$8 and counts against our fast-resolution contract.
```

Because the prompt mentions only the *cost* of escalating, the model leans hard toward never escalating. State **both** sides so it can weigh them:

```text
Escalating to a care specialist costs ~$8 and counts against our fast-resolution
target, so do not escalate trivially. However, if you get a billing error wrong,
it can cost a refund AND the customer's trust. When there is a genuine billing
conflict, escalate.
```

> 🔑 **Lesson:** the model "optimizes for a goal." (To **optimise for** something means to push as hard as possible toward it.) If you give it only one side of a **trade-off** (a choice where you gain one thing but give up another), it will overdo that side. As models get smarter they weigh trade-offs themselves, so state both sides and let the model balance them. This is the same shape of mistake as the hotspot patch.

All five cases now pass. ✅

---

## Part 4: building a new assistant from scratch

The second scenario is starting fresh. The goal is an assistant that builds a **week long staff schedule** for 8 retail employees while satisfying hard rules (enough people on each shift, only scheduling people when they are available, and so on). When you build from zero you choose three things, not one: the **prompt**, the **model**, and the **harness**.

Because the rules are strict, you do not need another AI to judge the output. You can grade it with a plain **Python function** (a small block of code) that counts rule breaks. This is called a **deterministic grader**, where "deterministic" means it always gives the same answer for the same input, with no AI judgement involved.

```python
def count_violations(schedule, employees, requirements):
    """Return how many hard rules a generated schedule breaks."""
    violations = 0
    for shift in requirements:
        assigned = schedule.get(shift.id, [])
        if len(assigned) < shift.required_headcount:     # not enough people on this shift
            violations += 1
        for emp_id in assigned:
            if not employees[emp_id].is_available(shift): # person scheduled when unavailable
                violations += 1
    return violations
```

This kind of "satisfy a set of strict rules" problem has a name: **constraint satisfaction**. A **constraint** is just a rule that must hold.

The talk then climbs a ladder of approaches, getting better each time. Watch which lever changes at each step:

| Step | Approach | Result | Cost and latency |
|--:|---|---|---|
| 1 | **Sonnet 4.6**, simple prompt | All 5 fail. Burns tokens and does not check its work. | baseline |
| 2 | **Opus 4.7**, same prompt | Still fails, but **far fewer rule breaks**. More reasoning power helps. | similar |
| 3 | **Opus 4.7 with adaptive thinking** (a harness change only) | **Passes reliably** | about 3x the tokens, about 3x the latency (~100 seconds) |
| 4 | **Sonnet 4.6 with a better prompt** ("check your work before answering") | Passes 2 of 5. The failures are now answers cut off by the length limit, not rule breaks. | even more tokens if you raise the limit |
| 5 | **A generate, evaluate, repair loop** (3 small prompts working together) | **All 5 pass** | **lower** tokens and latency than step 4 |

**Adaptive thinking** (step 3) means letting the model decide for itself how much private "scratch work" to do before answering. More thinking usually means a better answer, but it costs more tokens and time. It is just a harness change:

```python
# Same prompt as before. Just let Opus decide how much to think.
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    thinking={"type": "adaptive"},   # the model chooses its own reasoning depth
    system=system_prompt,
    messages=messages,
)
```

Step 5 splits one big prompt into **three small prompts**, each with a single job. Running smaller, focused steps in sequence is what people mean by an **agentic loop** (an "agent" is an AI that takes a series of actions on its own toward a goal, rather than answering in one shot).

```python
def schedule_agent(problem, max_rounds=3):
    schedule = generate(problem)                  # 1. draft a schedule
    for _ in range(max_rounds):
        violations = evaluate(schedule, problem)  # 2. another prompt lists exactly what is broken
        if not violations:
            break
        schedule = repair(schedule, violations)   # 3. a third prompt fixes only those problems
    return schedule
```

> 🔑 **Two good winners:** "Opus 4.7 with adaptive thinking," or the "generate, evaluate, repair loop." The loop has a bonus: you can add **soft constraints** at run time. (A **soft constraint** is a nice to have preference rather than a strict rule, for example "try to keep Harry and Sally on different shifts" or "add a third shift on Wednesday.") You add these in the evaluate step in plain English, without touching the deterministic grader.

> 💡 **Design principle:** when steps are "easy and repeatable to separate out," split them into their own prompts instead of asking one giant prompt to do everything.

---

## Key takeaways

1. **Evals first.** A set of test cases is the only honest way to know whether a change helped or just got lucky. Cover control, edge, and capability or handoff cases.
2. **Clean up before anything clever.** Add structure with tags, delete copied in junk, and define the output. This is often a free win.
3. **Change one thing at a time.** Isolate each failing case so you can see exactly what your change did.
4. **Instructions do not add capability.** If the model genuinely cannot do a task, give it a **tool**, a **stronger model**, more **thinking**, or a **multi step loop**. Do not just tell it to "be careful."
5. **Watch out for old patches and one sided rules.** Leftover "never do X" or "always do Y" instructions can make a smarter model hide information or refuse to act. State both sides of a trade-off and let the model decide.
6. **Record your defensive changes** with version control, so you can find and remove them when a new model makes them harmful.

## Common pitfalls

- ❌ Telling the model to "do better" instead of giving it the means to do better.
- ❌ Long lists of "never do this" rules that the next model will over apply.
- ❌ Stating only the cost of an action and never the cost of doing nothing.
- ❌ Leaving website boilerplate (hero images, cookie notices) in a prompt.
- ❌ Changing several things at once, so you cannot tell what actually helped.
- ❌ Trusting the prompt alone for output format when a stop sequence or structured outputs would be more reliable.

---

## 🛠️ Capstone Project: build PromptLab

> This is the main hands on project for the lesson, and the best way to make everything above stick. You are going to build the very tool Margo used in the talk. In her words: "I five-coded this web app so that we can iterate on the prompt together... I can run my evals on all five test cases and inspect the results." We will build this out together, so do not worry about size. Start as small as a single script and grow it as far as you like.

### What you will build

**PromptLab** is a small workbench for improving prompts the eval driven way, plus the assistant you develop inside it. It has two halves that line up exactly with the two halves of this lesson:

1. **The harness:** a way to define test cases, run a prompt against all of them, and see a simple pass or fail grid (green and red), just like Margo's web app.
2. **The assistant:** a support assistant for a company you choose, which you take from a broken first version to all green by applying every technique in this lesson.

> 🎯 **Pick your world.** Reuse **Meridian Mobile** (the phone company) so it matches the lesson, or swap in something you find fun, such as a **gym chain**, a **streaming service**, or a **co-working space**. You just need a world that has: tiered plans, an upgrade partway through the month (so you need proration maths), an old "grandfathered" plan (an edge case), and a dispute that must go to a human (a handoff case). That one world naturally exercises every skill below.

### Why this is the perfect practice

| Lesson skill | Where you use it in PromptLab |
|---|---|
| Building an eval (control, edge, capability) | Milestone 1, you cannot move on without it |
| Prompt cleanup (tags, output contract) | Milestone 3, measure the free win |
| Removing overfitted patches | Milestone 4a, the "hidden information" bug |
| Tools beat instructions | Milestone 4b, the proration tool |
| Stating both sides of a trade-off | Milestone 4c, the escalation bug |
| Choosing model and thinking effort | Milestone 5, the from scratch feature |
| The generate, evaluate, repair loop | Milestone 5, solving the schedule |

### Milestones (build them in order, each one works on its own)

1. **Scaffold.** Set up a project, connect the Anthropic SDK (the official code library for calling Claude), and create a `cases.json` file with 5 test cases: 1 control, 2 edge, 1 capability or handoff, and 1 of your own. (Smallest version: a single Python script. Bigger version: a small web page with a results grid.)
2. **Eval runner.** Write code that runs the current prompt against every test case and prints a **pass or fail grid**. This is your dashboard for everything that follows.
3. **The broken version 0.** Write a deliberately messy prompt on purpose (one big paragraph, copied in junk, and an old "never give wrong info, send them to the URL" patch). Run the eval to get a red baseline.
4. **Clean up.** Restructure with `<role>`, `<guidelines>`, `<policy>`, and `<tone>` tags, delete the junk, and add an output contract plus a stop sequence. Re-run and record the improvement.
5. **Fix the failures one at a time.**
   - **(a)** Fix the hidden information bug by removing the old patch and trusting the account data.
   - **(b)** Add a `calculate_proration` tool (schema plus the maths) so the model stops doing sums in its head.
   - **(c)** Fix the escalation bug by stating both sides of the cost versus benefit.
6. **Add a from scratch feature.** Give the assistant a second skill: a **weekly staff scheduler** with hard rules. Write a deterministic `count_violations` grader, then climb the ladder yourself: simple prompt, then a stronger model, then adaptive thinking, then the generate, evaluate, repair loop. Note the tokens and latency at each step.
7. **Stretch goals.** Save every prompt version and show a leaderboard of them. Add an AI based grader for tone. Allow soft constraints at run time ("keep Harry and Sally on different shifts") without changing the deterministic grader.

### How you will know you are done

- ✅ Every test case passes **consistently** (run each a few times, since results vary slightly).
- ✅ You can point to **each change** and show, from the grid, the exact failure it fixed.
- ✅ At least one case is fixed by a **tool**, and one by **stating both sides of a trade-off**, proving you did not just "add more instructions."
- ✅ The scheduler passes using the **loop** at lower cost and latency than forcing one giant prompt to do it all.

> 💡 **Keep yourself honest:** change one thing at a time and re-run. If you cannot say which change caused an improvement, you changed too much at once.

---

## Practice exercises (optional extra reps)

> **What these are:** five small, self contained coding tasks. Each one asks you to *do* one specific thing (they are not quiz questions), so you get focused practice on a single skill. They are optional and independent of each other. The **Capstone Project above is the main build**, and it already includes all of these skills in one place, so feel free to skip straight to it if you would rather build one bigger thing. Each exercise is labelled by difficulty. A tiny test setup is enough, even a single notebook with 5 test cases that prints pass or fail.

### Exercise 1: build the eval first (foundational)
Write a 5 case eval for a support assistant in a topic you know well (for example a software billing assistant). Make sure you include **one control case, two edge cases, and one capability or handoff case** (where the assistant must pass the user to a human or refuse). Write down the answer you expect for each case before you write any prompt.

### Exercise 2: cleanup pass (foundational)
Take this deliberately messy prompt and restructure it with `<role>`, `<guidelines>`, `<policy>`, and `<output_format>` tags, removing anything that does not belong:

```text
You are a helpful human agent. Our homepage hero banner says "Switch & Save!".
Be nice. Never quote a wrong price, send them to /pricing instead. We accept
cookies. Plans: Lite $10/10GB, Pro $30/50GB. Always get the math right.
```
Run your eval before and after. What changed, and why?

### Exercise 3: tool versus instruction (intermediate)
Your assistant keeps doing arithmetic in its head and getting it slightly wrong. Without changing the model: (a) write the prompt instruction that points it to a tool, (b) write the tool schema, and (c) write the tool's code. Confirm the failing case flips to passing. Then answer: why could a stronger instruction alone never fix this?

### Exercise 4: fix a one sided rule (intermediate)
Find a "never / always / avoid unless absolutely necessary" line in one of your real prompts. Rewrite it to state **both sides of the trade-off**. Predict how a smarter model would behave under the old wording versus the new wording, then test it.

### Exercise 5: climb the ladder on a from scratch assistant (advanced)
Pick a constraint satisfaction task (scheduling, a seating chart, packing a bag). Build a deterministic grader, then climb the ladder yourself: simple prompt, then stronger model, then adaptive thinking, then the generate, evaluate, repair loop. Record rule breaks, tokens, and latency at each step. Which approach is best for *your* budget? Finally, add a soft constraint at run time in the evaluate step and confirm you did not have to touch the grader.

---

## Cheat sheet

```text
WHEN A PROMPT GETS WORSE
  1. Do you have an eval? If not, build one (control + edge + capability).
  2. Clean up: structure with tags, delete junk, define the output (+ stop sequence).
  3. Fix ONE failure at a time, and re-run after each change.

CHOOSE THE RIGHT FIX (not "more instructions")
  Wrong or hidden facts ....... remove the old patch; trust the data source
  Bad maths / unreliable step . give it a TOOL
  Will not act / too cautious . state BOTH sides of the trade-off
  Not capable enough .......... stronger model OR adaptive thinking
  One prompt doing too much ... split into generate -> evaluate -> repair

ALWAYS REMEMBER
  - Instructions do not add capability.
  - Record your defensive patches so you can remove them later.
  - Smarter models weigh their own trade-offs, so give them both sides.
```

## How this connects to the rest of the course

- **Earlier, Module 2 · Lesson 4 (Picking the right model):** the "stronger model versus adaptive thinking" choices here are made rigorously, with evals, there.
- **Earlier, Module 2 · Lesson 5 (The thinking lever):** a deeper look at adaptive thinking and reasoning effort, the lever used in Part 4.
- **Next, Module 3 (Evals for taste):** builds out the eval idea this whole lesson rests on, including AI based graders versus code based graders.
- **Later, Module 5 (Claude Managed Agents):** the generate, evaluate, repair pattern grows into multi agent systems and a feature called "outcomes."

---

*Source: "The prompting playbook" by Margo van Laar (Anthropic), Code with Claude 2026, London. Code snippets are illustrative reconstructions of the approaches shown in the talk. Adapt the model names and API details to the current SDK.*
