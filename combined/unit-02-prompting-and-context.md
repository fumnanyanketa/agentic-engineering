# Unit 2: Prompting and Context Engineering

> **Course:** Agentic Engineering, a model-agnostic self-paced path *(working title)*
> **Unit 2 of 11:** Learn to talk to a model so it does what you want, and learn to give it the right information in the smallest high-signal form, then write your first versioned system prompt for an AtlasOS agent
> **Principle (vendor-neutral):** Agentic Engineering Module 2 (Prompt engineering fundamentals) and Module 3 (Context engineering I)
> **The how, across models:** Claude (Anthropic), Gemini (Google), GPT (OpenAI), current practice verified June 2026
> **AtlasOS build:** your `prompts/` library, with the first real system prompt for Scout (the research agent), committed and tested
> **Estimated time:** 90 to 120 minutes

---

## In one sentence

A **prompt** is the text you send a model, and a model is only as good as what you put in front of it, so this unit teaches you the two linked crafts that decide whether you get a useful answer or a confident mess: writing clear, structured, example-backed instructions (prompting), and curating the smallest high-signal set of information the model sees while it works (context engineering), shown the same way across Claude, Gemini, and GPT, and finished by writing a real, versioned system prompt for your first AtlasOS agent.

> 🎯 **Where this unit is heading.** The payoff is a **Build** where you create a `prompts/` folder in the `atlasos` repo you made in Unit 1, write a real, versioned **system prompt** for **Scout** (the research-and-synthesis agent), give it a worked **few-shot example** and a strict **output contract**, test it against a couple of inputs, and commit it to git as a real artifact. Jump to **"The Build"** to see the finish line, then come back and we will get you there.

## First-principles companion

> 💡 **The durable ideas behind this unit.** The tools change monthly; these do not. Optional, read them any time:
>
> - **[Prompt engineering overview (Anthropic docs)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)** (docs). The durable method: define success and tests first, structure the prompt, and recognise when a different lever (a tool, a stronger model) is the real fix rather than more instructions.
> - **[Language Models are Few-Shot Learners (GPT-3)](https://arxiv.org/abs/2005.14165)** (paper). The seminal paper establishing why in-context prompting and examples work at all.
> - **[Effective context engineering for AI agents (Anthropic)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)** (essay). The principle-level case for "find the smallest set of high-signal tokens," covering curation and compaction as ideas, not buttons.
> - **[Prompt caching (Anthropic docs)](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)** (docs). How caching works and where its large cost saving comes from, from first principles.

## A few plain-language basics first

New terms, in plain words. You do not need to memorise these; each is explained again the moment it matters.

- **Model:** the AI itself, one specific version of it (for example Claude's Sonnet, Google's Gemini, OpenAI's GPT). Different models have different strengths, speeds, and prices.
- **Prompt:** the text you send the model. **Prompt engineering** is shaping that text so the model does what you want, consistently, not just once by luck.
- **Token:** the unit a model reads and writes in, roughly three quarters of a word. You are billed per token, so "more tokens" means "more cost and more wait."
- **Context window:** the maximum amount of text (in tokens) a model can hold in mind at once for a single request. Today's largest windows are very big (hundreds of thousands to a million tokens), but, as you will see, big does not mean you should fill it.
- **Context:** everything the model can see in one request: the system prompt, your message, any reference documents, examples, past conversation, and the results of any tools it used.
- **Context engineering:** deciding what goes into that limited space and what stays out, so the model sees the *best* set of information, not the *most*.
- **System prompt:** a separate, higher-priority instruction that sets the model's role and standing rules for the whole conversation. It frames everything the user then says.
- **Few-shot:** a prompt that includes a few worked examples of input and the desired output, so the model copies the pattern. ("Zero-shot" means no examples.)
- **Structured output:** a response that follows a fixed shape (for example JSON, a common machine-readable text format) so your program can read it reliably instead of scraping free text.
- **Latency:** how long the model takes to respond. Lower is faster.
- **Prompt caching:** a provider feature that saves the processed version of a stable chunk of your prompt and reuses it, so you do not pay to reprocess it every request.

## Why this unit matters

In Unit 1 you learned to *drive* a coding agent. The single biggest lever on what you get back is how you talk to the model and what you put in front of it. Most "the AI is not good enough" complaints are really "the prompt was vague" or "the model was buried in irrelevant text." This unit fixes both, and the skills carry to every model and every later unit, because every agent you build is, underneath, a prompt plus a carefully chosen context.

> 🔑 **Best, not most.** Context is a finite resource. The model has a fixed window and, just as importantly, a limited "attention budget": its focus spreads thinner as you add text. The goal is always the smallest set of high-signal tokens that still gets the job done, not the largest pile you can fit.

## Learning objectives

By the end of this unit you will be able to:

1. Write a clear, specific, well-structured prompt using the core techniques (clear instructions, structure, examples, roles, output formatting).
2. Use a **system prompt**, **few-shot examples**, and **structured output** the same way across Claude, Gemini, and GPT, and recognise the small differences.
3. Explain context engineering, the difference between it and prompting, and what **context rot** is.
4. Budget a context window, keep every token earning its place, and use **prompt caching** to cut cost and latency on repeated calls.
5. Treat prompts as versioned artifacts: write one, test it, and commit it to git.

## Prerequisites

- **From Unit 1:** a working workstation (editor, terminal, git), the `atlasos` repository cloned to your computer, and one coding agent installed and signed in.
- **What you do NOT need:** any machine-learning background, or to have written a prompt before. We start from the first principle.
- **One honest note:** you will write prompts in plain text. There is no special syntax to learn. The skill is in clarity and judgment, not in memorising a format.

---

## Part 1: What makes a prompt work (the core techniques)

A prompt is just text, but a model cannot read your mind: it fills any gap you leave with a guess. Reliable prompting comes down to a small set of moves you combine, not one trick you pick. These are vendor-neutral, meaning they hold no matter whose model you use, because they come from how all of these models read and continue text.

- **Be clear, direct, and specific.** Say exactly what you want, in what format, for whom, and what to avoid. *"Summarize this in three bullet points for a busy manager, no jargon"* beats *"summarize this."* The more precisely you describe the finished thing, the less the model has to guess.
- **Give it structure.** When a prompt holds several different things at once (instructions, reference text, examples), wrap each part in clearly labeled sections so the model does not confuse them. Many practitioners use lightweight tags like `<instructions>`, `<context>`, `<examples>`, or plain Markdown headings. The point is unambiguous boundaries.
- **Show, do not only tell (few-shot).** A handful of worked input-and-output examples often locks in tone and format better than a paragraph of rules. Examples are the single most effective move for tasks like classification, extraction, and translation.
- **Set a role and standing rules (system prompt).** *"You are a careful financial analyst. Never invent numbers."* A role frames everything that follows.
- **Ask for the exact output shape.** If your code will read the answer, ask for a strict, machine-readable format (such as JSON) and describe the exact fields.
- **For hard reasoning, give room to think.** Adding *"think step by step"* (called **chain-of-thought**) helps on math, logic, and multi-step decisions. Some newer "reasoning" models already do this internally, so you may not need to ask. The durable principle: match the amount of reasoning effort to the difficulty of the task.
- **Iterate against examples, not vibes.** Do not judge a prompt by one nice answer. Collect real example inputs with the outputs you expect, and tune until the prompt passes them.

> 🔑 **Examples carry the load.** A good example often replaces a paragraph of instructions. When you are tempted to add another rule, ask first whether one worked example would teach it more cleanly.

> ❌ **The "prompt and pray" trap.** Shipping a prompt with no test set, then being surprised when it fails on a new input. Even three or four example inputs paired with their expected outputs turn prompting from guesswork into a checkable craft.

---

## Part 2: Structure and output, with a worked before-and-after

The fastest way to feel how much structure matters is to clean up a messy prompt. Here is a real example: a support assistant whose prompt mixes everything into one paragraph, including text someone copied straight off a web page.

```text
You are a friendly human support rep for Meridian Mobile. Our hero image
shows... Always be polite. Never give wrong plan details, point them to the
URL. Plans: basic 10GB... We use cookies to... Always calculate prorated
amounts correctly.
```

The model cannot tell role from policy from data, and there is website junk ("hero image", "cookies") that has nothing to do with the task. Restructure it so each kind of information is clearly separated:

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
- Customers on legacy plans may have different allowances; these are in the
  customer's account context, which is the accurate source of truth.
</policy>

<output_format>
Respond with your message wrapped in <response>...</response> tags.
</output_format>

<plan_data>
...
</plan_data>
```

Just doing this, with no other change, improves the results. As one Anthropic engineer puts it: *"If you're reading a prompt and you can't tell guidelines from policy from data, most likely the model isn't able to either."*

**An output contract is a clear statement of the exact shape you want the answer in.** Above, the `<output_format>` block asks for a `<response>` wrapper. When your code depends on the format, do not trust the prompt text alone: back it up in the surrounding code (the "harness"). Two common ways:

- **A stop sequence:** you tell the API "stop generating the moment you produce this exact text." Set it to your closing tag (for example `</response>`) and the model stops cleanly right there.
- **Structured outputs / JSON mode:** all three major providers offer a mode that forces the answer into a fixed schema (a defined shape) automatically, instead of you hoping the model formats it right.

> ✅ **Define the output, then enforce it.** State the format in the prompt for the model's benefit, and enforce it in code (stop sequence or structured-output mode) for your program's benefit. Belt and suspenders.

---

## Part 3: The same moves across Claude, Gemini, and GPT

The techniques above are universal. The wiring differs a little per provider. Here is the parity you need so you are never locked in. (Model ids and exact field names change often; treat these as the shape, and verify against current docs.)

| Concept | Claude (Anthropic) | Gemini (Google) | GPT (OpenAI) |
|---|---|---|---|
| **System prompt** | a top-level `system` parameter, separate from messages | a `system_instruction` (system instruction) field | a message with `role: "system"` (or "developer") at the top |
| **Few-shot examples** | example turns in the `messages` list, or inside the prompt text | example turns in `contents`, or in the prompt text | example messages in the `messages` list |
| **Structured output** | tool/JSON schema, or strict output formatting | a `response_schema` with JSON response mode | JSON mode / "structured outputs" with a schema |
| **Reasoning effort** | a "thinking" / extended-thinking mode you can turn on | a "thinking" budget on reasoning-capable models | a reasoning-effort setting on reasoning models |
| **Stop sequence** | `stop_sequences` | `stop_sequences` | `stop` |

The big picture: **every provider gives you a separate place for standing instructions (the system prompt), a way to show examples, and a way to demand a strict output shape.** Learn the concept once and you can read any of their docs in minutes.

Here is the *same* tiny request expressed in each, so you can see the parity. (Pseudo-code; the field names are close to real but verify against the current SDK.)

```text
# Claude (Anthropic)
client.messages.create(
    model="claude-sonnet-...",          # hold the id loosely; verify current docs
    system="You are Scout, a precise research assistant. Cite sources.",
    messages=[{"role": "user", "content": "Summarize this article: ..."}],
)

# Gemini (Google)
client.models.generate_content(
    model="gemini-...",                  # verify current id
    config={"system_instruction": "You are Scout, a precise research assistant. Cite sources."},
    contents="Summarize this article: ...",
)

# GPT (OpenAI)
client.responses.create(
    model="gpt-...",                     # verify current id
    input=[
        {"role": "system", "content": "You are Scout, a precise research assistant. Cite sources."},
        {"role": "user",   "content": "Summarize this article: ..."},
    ],
)
```

> 💡 **One prompt, three homes.** Notice the *instruction* ("You are Scout, a precise research assistant. Cite sources.") is identical. Only the plumbing around it changes. That is why this unit is model-agnostic: you write the prompt once and route it to whichever model fits.

---

## Part 4: From prompting to context engineering (the bigger lens)

Prompt engineering controls *how the model communicates*: the phrasing and instructions. **Context engineering** widens the lens to *what the model knows*: the full set of information it can see while it works. In Unit terms, prompting is the words you choose; context engineering is everything you put in the room with the model.

Why does this matter more as you build agents? A single answer came from a single prompt. But an agent runs over many turns, calls tools, and accumulates results as it goes. The context is no longer a fixed string you write once; it is an evolving **state** you have to manage: old material trimmed, fresh material pulled in, the whole thing kept within budget.

> 🔑 **The shift that matters.** Prompt engineering is one part of the bigger task. The bigger task is curating everything the model can see while it works. Hold this sentence; it is the hinge the rest of the course turns on.

The guiding heuristic is simple to say and hard to live by: **aim for the smallest set of high-signal tokens that still gets the job done.** Every token should earn its place. A related idea is writing instructions at the "right altitude": specific enough to steer clearly, but not so packed with rigid detail that the model has no room to adapt. Too vague and it wanders; too rigid and it breaks on anything unexpected.

```text
        CONTEXT BUDGET (one request)

   ┌───────────────────────────────────────────────┐
   │  system prompt   (your standing rules, role)   │  keep tight + stable
   │  examples        (few-shot, if used)           │  high value per token
   │  reference docs  (only the relevant parts)     │  curate hard
   │  conversation    (past turns)                  │  trim / summarize
   │  tool results    (only what's needed)          │  shape before adding
   └───────────────────────────────────────────────┘
         everything here competes for attention
```

---

## Part 5: Context rot, and why bigger is not a free lunch

It is tempting to think a giant context window means you can just stuff everything in. The opposite is often true.

**Context rot** is the measurable tendency of a model to recall and reason *less* accurately as its context grows. The cause is that limited attention budget: the more tokens you add, the more relationships the model has to weigh, and its focus on any one detail gets diluted. The analogy practitioners use is human working memory: you can only hold so much in mind before details start slipping.

This shows up in "needle in a haystack" tests, where a single fact is buried in a long document and the model is asked to find it. As the document grows, recall drops. The exact numbers vary by model and keep changing, but the direction is consistent and real across providers: **a large context window lets you add more text, but adding more text often makes quality worse, not better.**

The practical consequences for how you work:

- ✅ **Make every token earn its place.** If removing something does not hurt the result, leave it out.
- ✅ **Pull information in just-in-time.** Add what the current step needs, rather than front-loading everything up front.
- ✅ **Measure recall on your own data.** Do not assume a big window means the model is using all of it well.
- ❌ **Do not "just stuff the whole document in."** More text frequently lowers quality.
- ❌ **Do not confuse a large window with good context engineering.** The window is capacity; engineering is what you choose to put in it.

> 💡 **Feel it once.** A great exercise: take a working prompt, deliberately surround your real input with 20,000+ tokens of loosely related junk, and watch quality drop. That drop is context rot, produced on purpose. Then cut back to only the high-signal tokens and watch quality recover. You learn this in your gut, not just in theory.

This is where prompting and context engineering meet experienced practitioners arriving at the same conclusion from different directions: most of the craft of getting good results from a model comes down to managing its context. When working engineers and the labs converge on that sentence independently, it is a sign the idea is load-bearing, not a passing trend.

---

## Part 6: Prompt caching (cheaper, faster, same answer)

One concrete, vendor-neutral lever pays for itself immediately: **prompt caching.**

When you send a request, the provider processes your input tokens before generating a reply. If the *beginning* of your context is long and does not change between requests (a big system prompt, a fixed reference document, a set of tool definitions), most providers let you cache that stable prefix so it does not have to be reprocessed every time. On the next request, only the *new* tokens are processed; the stable prefix is pulled from the cache.

Three benefits, and the order matters because cost is usually the headline:

| Benefit | What you get |
|---|---|
| **Cost** | A large discount on cached tokens (commonly around a 90% reduction with Claude), because they are not reprocessed. Savings vary by provider, so verify current docs. |
| **Rate limits** | Cached tokens often do not count the same against your usage cap, so you can effectively send more. |
| **Latency** | You stop reprocessing the whole prefix each turn, so your time to first token drops as the conversation grows. |

> 🔑 **Caching does not change the answer.** It is the exact same output, just pre-processed and cheaper. There is no intelligence trade-off. If you remember one cost lever from this unit, remember this one.

The one rule that makes or breaks it: **the cached prefix must be byte-for-byte identical between requests.** The most common mistake is putting a **timestamp** ("today is ...") at the top of the system prompt. It seems helpful, but it changes every request, which changes the prefix, which breaks the cache. Keep changing values out of the stable part.

All three major providers offer caching, and the shape is the same: mark or arrange a stable prefix, then reuse it. The exact mechanism differs (some automatic, some you mark explicitly), so check each provider's current docs.

```text
# Claude (Anthropic): mark the stable prefix to cache it, then verify.
response = client.messages.create(
    model="claude-...",                   # verify current id
    system=large_stable_system_prompt,    # keep this byte-for-byte identical
    cache_control={"type": "ephemeral"},  # cache the stable prefix
    messages=messages,
)
print(response.usage.cache_read_input_tokens)   # > 0 means the cache is being used
```

> 💡 **Measure first.** The first question every team that does this well asks is: what is my cache hit rate right now? Most providers expose it (Claude reports `cache_read_input_tokens`; check your provider's usage fields). If it is near 0%, that is not a failure, it is your starting line.

---

## Key takeaways

1. **Prompting is a small set of moves you combine:** clear and specific instructions, clean structure, few-shot examples, a role/system prompt, and a strict output shape. Examples often beat more rules.
2. **Enforce output in code, not just in words.** A stop sequence or a structured-output mode is more reliable than hoping the model formats it right.
3. **The same moves work across Claude, Gemini, and GPT.** Each has a system prompt, a way to show examples, and a structured-output mode. The instruction is identical; only the plumbing differs.
4. **Context engineering is the bigger lens:** curate what the model *knows*, not just how it talks. Aim for the smallest set of high-signal tokens.
5. **Bigger context is not free.** Context rot is real: more text often lowers quality. Make every token earn its place and pull information in just-in-time.
6. **Prompt caching is a free win** on repeated calls (cheaper, faster, same answer). Keep the cached prefix identical; no timestamps.
7. **Prompts are artifacts.** Version them in git, change one thing at a time, and test against examples.

## Common pitfalls

- ❌ Vague instructions that leave the model to guess the format, audience, or scope.
- ❌ One big undivided paragraph mixing rules, tone, and data, with website junk left in.
- ❌ "Prompt and pray": shipping with no test inputs, then being surprised by failures.
- ❌ Trusting the prompt alone for output format when a stop sequence or structured output would be reliable.
- ❌ "Just stuff the whole document in," confusing a large context window with good context engineering.
- ❌ Letting an agent's context grow unbounded across turns with no trimming or summarizing.
- ❌ A timestamp (or any per-request value) in the system prompt, silently breaking the cache.
- ❌ Editing prompts in place with no version history, so you cannot tell what changed or why.

---

## 🛠️ The Build: your `prompts/` library and Scout's first system prompt

> The hands-on payoff. You will create a real prompts library inside your `atlasos` repo and write the first versioned system prompt for **Scout**, AtlasOS's research-and-synthesis agent, complete with a few-shot example and an output contract, then test it and commit it. From now on, prompts are real, versioned artifacts in your project, not throwaway text.

### What you will build

A `prompts/` folder in the `atlasos` repository (from Unit 1) containing `scout-system-v1.md`: a structured system prompt for Scout that sets its role, gives it one worked few-shot example, and defines a strict output contract. You will test it against two sample inputs with your coding agent, then commit it to git.

### Milestones (in order, each fully explained)

**1. Open your project and start your agent.** In your VS Code terminal, move into the repo and start your agent (the one you installed in Unit 1):

```text
cd ~/atlasos
claude        # or: gemini  /  codex
```

**2. Create the `prompts/` folder.** You can do this by hand (in VS Code's left panel, click the New Folder icon, name it `prompts`) or just ask your agent: *"Create a folder named `prompts` in this repo."* This folder is Scout's home and will fill up over later units.

**3. Write Scout's system prompt as a versioned file.** Create `prompts/scout-system-v1.md`. The `-v1` in the name is deliberate: **prompts are versioned artifacts**, like code. When you improve it later, you save `scout-system-v2.md` and keep the old one, so you can always see what changed and why. Paste this real, structured starting prompt:

```text
# Scout: system prompt (v1)

<role>
You are Scout, the research-and-synthesis agent for AtlasOS. You gather
information from the sources you are given, weigh it, and produce a tight,
accurate synthesis for a busy reader. You do not invent facts.
</role>

<guidelines>
- Use only the sources provided in <sources>. If they do not answer the
  question, say so plainly instead of guessing.
- Prefer the smallest accurate answer. Cut anything that does not earn its place.
- Attribute every claim to a source by its number, like [1].
- If sources disagree, surface the disagreement rather than smoothing it over.
</guidelines>

<output_format>
Respond with valid JSON only, matching exactly:
{
  "summary": "<2-3 sentence synthesis>",
  "key_points": ["<point with citation [n]>", "..."],
  "confidence": "high | medium | low",
  "gaps": "<what the sources do not cover, or empty string>"
}
</output_format>
```

**4. Add a few-shot example so Scout copies the pattern.** Below the prompt, in the same file, add one worked example. This single example teaches tone, citation style, and the exact JSON shape better than another paragraph of rules:

```text
<example>
<sources>
[1] Tokyo's population is about 14 million in the city proper.
[2] The Greater Tokyo Area has about 37 million people.
</sources>
<question>How big is Tokyo?</question>
<response>
{
  "summary": "Tokyo's size depends on the boundary used: about 14 million in the city proper [1], and about 37 million across the Greater Tokyo Area [2].",
  "key_points": ["City proper: ~14 million [1]", "Greater Tokyo Area: ~37 million [2]"],
  "confidence": "high",
  "gaps": "No date given for these figures."
}
</response>
</example>
```

**5. Test Scout against a fresh input.** Still in your agent, ask it to act as Scout using this prompt. Type something like: *"Use `prompts/scout-system-v1.md` as the system prompt. Here are the sources: [1] Our Q2 sign-ups grew 12%. [2] Q2 churn rose from 3% to 5%. Question: How did Q2 go? Return only the JSON contract."* Read the reply. You should get back valid JSON with `summary`, `key_points` carrying `[1]`/`[2]` citations, a `confidence`, and `gaps`. If it adds prose around the JSON or drops a citation, that is your signal to tighten the prompt.

**6. Test a second, harder input to probe the edges.** Try one where the sources do not answer the question, for example sources about pricing with the question *"What is our refund policy?"* A good Scout returns `low` confidence and names the gap, rather than inventing a policy. This is your control-versus-edge intuition from real prompting: one case that should work cleanly, one that probes a known failure (inventing facts).

**7. Note caching in a comment (no code yet).** At the bottom of the file, add one line: `# Caching: this system prompt is stable, so it is a good candidate to cache as a fixed prefix once Scout runs on the API.` This plants the idea you will wire up in a later unit, and records *why* the prompt is kept stable (so it stays cacheable).

**8. Commit the prompt as an artifact.** Leave the agent (`exit`) and save your work to git, exactly like the heartbeat from Unit 1:

```text
git add -A
git commit -m "Add prompts/ library and Scout system prompt v1 with few-shot and output contract"
git push
```

Refresh your repo on GitHub: `prompts/scout-system-v1.md` is there, versioned and visible. That is the whole point: a prompt is now a tracked, reviewable artifact, not a message you typed once and lost.

**9. Stretch (optional).** Run the same two test inputs against a second model (if you have access to Gemini or GPT) using the identical instruction text, and note any differences in how strictly each follows the JSON contract. That is model-agnostic prompting in practice: same prompt, different homes.

### How you will know you are done

- ✅ A `prompts/` folder exists in `atlasos` with `scout-system-v1.md` inside it.
- ✅ The file has a clear `<role>`, `<guidelines>`, an `<output_format>` contract, and one `<example>`.
- ✅ Scout returns valid JSON matching the contract on a normal input.
- ✅ On an input the sources cannot answer, Scout reports low confidence and names the gap instead of inventing facts.
- ✅ The file is committed to git and visible on GitHub, with `-v1` in its name.

> 💡 **If Scout ignored part of the contract, that is useful, not a failure.** Tighten the relevant section, save it (still v1 while you are iterating today), and re-test. The habit of test, adjust, re-test is the whole craft.

---

## Cheat sheet

```text
PROMPTING (shape the words)
  clear + specific : say what, what format, for whom, what to avoid
  structure        : label sections (<role> <guidelines> <policy> <examples>)
  few-shot         : show 1-3 worked examples; they beat extra rules
  system prompt    : role + standing rules, separate + higher priority
  output contract  : ask for exact shape; enforce in code (stop seq / JSON mode)

SAME MOVES, THREE MODELS  (verify ids/fields against current docs)
  system prompt : Claude system | Gemini system_instruction | GPT system role
  structured    : all three offer a JSON/schema mode
  the instruction text is identical; only the plumbing differs

CONTEXT ENGINEERING (curate what it knows)
  goal     : smallest set of HIGH-SIGNAL tokens that does the job
  rot      : more text often LOWERS quality (attention budget)
  rule     : every token earns its place; pull info in just-in-time

PROMPT CACHING (cheaper, faster, same answer)
  cache the stable prefix (big system prompt / fixed docs)
  must be byte-for-byte identical -> NO timestamps in the system prompt
  measure your hit rate first (e.g. cache_read_input_tokens > 0)

PROMPTS ARE ARTIFACTS
  version them (scout-system-v1.md), commit to git, change one thing at a time
```

## How this connects to the rest of the course

- **Next, Unit 3 (Picking the right model and the thinking lever):** now that you can write a prompt, you learn to choose which model runs it and how hard it should think, judged with real tests, "cost per successful outcome" rather than cost per token. Scout's prompt is what you will route.
- **Throughout:** the `prompts/` library you started here grows with the fleet. Every agent in AtlasOS (Atlas, Cortex, Warden, and the rest) gets its own versioned system prompt, and the context-engineering habits from this unit (smallest high-signal context, caching the stable parts) underpin every one of them.

---

*Unit 2 of the combined path. Fuses the vendor-neutral principles of Agentic Engineering Modules 2 and 3 with current, model-agnostic practice across Claude (Anthropic), Gemini (Google), and GPT (OpenAI). Tool commands, model ids, and API field names change quickly; verify against current documentation.*
