# Unit 2: Reading and Judging Code

> **Course:** Agentic Engineering, a model-agnostic self-paced path *(working title)*
> **Unit 2 of 12:** The floor under everything: read any code your agent writes, trace it, judge whether it is right, debug it when it breaks, and decide what should be built
> **The how, across agents:** use your coding agent (Claude Code, Gemini CLI, or Codex CLI) as an explainer, but you do the judging
> **AtlasOS build:** the Warden verification rubric, and your first read, explain, break, fix pass on real code
> **Estimated time:** 2 to 3 hours

---

## In one sentence

Typing code is now optional because the agent does it, but judging code is not: this unit builds the load-bearing floor of agentic engineering, the ability to read any file the agent produced, follow how it works, decide whether it is correct or subtly wrong, break it on purpose to learn where it is fragile, and fix it, which is exactly the skill that turns "code I generated" into "a system I can stand behind."

> 🎯 **Where this unit is heading.** The payoff is a **Build** that you will reuse in every later unit: a short **verification rubric** (the seed of Warden, the course's quality gatekeeper) plus a hands-on *read, explain, break, fix* pass on the real code from your Unit 1 project. From here on, every unit ends by running its new component through this same rubric. Jump to **"The Build"** to see the finish line, then come back.

## First-principles companion

> 💡 **The durable ideas behind this unit.** Reading and judging code is the oldest skill in software, and it long predates AI. For the timeless versions:
>
> - **[Google Engineering Practices: Code Review Developer Guide](https://google.github.io/eng-practices/review/)** (guide). How professional engineers read a change and decide if it is good. Written for human reviewers; it applies exactly the same to an agent's diff.
> - **[OWASP Top Ten](https://owasp.org/www-project-top-ten/)** (reference). The classes of security flaw to read for. You do not memorise it; you learn to recognise the shapes.
> - **[The lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)** (essay). Why an agent with private data, untrusted input, and a way to send data out is dangerous, and why spotting that pattern requires reading the code.

## A few plain-language basics first

- **Reading code:** following a file you did not write to understand what it does, before you run it.
- **Control flow:** the order in which lines run (which branch, which loop, which function calls which).
- **Data flow:** where each value comes from and where it goes (which input becomes which output).
- **Function:** a named, reusable block of code that takes inputs (arguments) and usually returns a result.
- **Stack trace:** the report a program prints when it crashes, showing the chain of calls that led to the error. It is a map, not noise.
- **Test:** a small piece of code that runs your code with a known input and checks the output is what you expected.
- **Diff:** the side-by-side of what changed in a file: removed lines (often red), added lines (often green). Reading a diff is how you review a change.
- **API:** an agreed way for one program to ask another for something (for example, your code asking a model provider for a completion).
- **Async (asynchronous):** code that can start a slow task (like a network call) and do other things while it waits, instead of freezing. Agent loops and tool calls are full of this.

## Why this unit matters

Unit 1 drew the line of the whole course: agentic engineering, not vibe coding, which rests on staying responsible for the result and reviewing the agent's work like an engineer. That promise is empty if you cannot read and judge the code. A learner who merges what the agent wrote because it "looks right" is, by the course's own definition, on the vibe-coding side of the line. This unit is what moves you to the right side, and it is the floor that makes every later unit's verification step real.

> 🔑 **The one rule of this course.** Do not merge anything the agent writes that you cannot read, explain out loud, and break on purpose. Everything in this unit exists to make that rule easy to follow. It is the difference between "AtlasOS, the thing I drove an agent to produce" and "AtlasOS, the thing I understand well enough to defend."

You are not learning to out-type the model. You are learning to out-judge it.

## Learning objectives

By the end of this unit you will be able to:

1. Read a file you did not write and trace its control flow and data flow.
2. Predict what a piece of code does before running it, from its core constructs.
3. Read a stack trace and debug by hypothesis, not by guesswork.
4. Read a test and say what it does and does not prove.
5. Reason about how an agent talks to the outside world (APIs, HTTP, async).
6. Read a diff and judge whether a change is good.
7. Spot the common shapes of subtly wrong or unsafe code, including the lethal trifecta.
8. Apply a verification rubric to any component before you keep it.

## Prerequisites

- **From Unit 1:** your `atlasos` repository, a coding agent installed, and the plan, act, verify loop.
- **No prior coding experience required.** You will read code, not write it from scratch. Your agent is your tutor; this unit teaches you to check the tutor.

---

## Part 1: Reading beats writing now (and the one rule)

A generation of engineers learned by writing code. You are learning in an era where the agent writes it, so your leverage moves to a different skill: judgment. The brutal truth is that an agent produces code that runs and looks plausible far more easily than it produces code that is correct, safe, and right for your problem. The gap between "runs" and "right" is exactly where your reading lives.

```text
   THE OLD FLOOR              THE NEW FLOOR
   you type the code    ->    the agent types the code
   you debug your typos ->    you judge the agent's logic
   skill = writing      ->    skill = reading + judging
```

The habit that builds this floor is small and you apply it to every component you build:

1. **Read it.** Open the files and follow them top to bottom.
2. **Explain it.** Say, out loud, what each part does and why. If you cannot, you do not understand it yet.
3. **Break it on purpose.** Change one thing so it should fail, predict the failure, run it, and check you were right.
4. **Fix it.** Undo your break, fix anything genuinely weak, re-run your checks.

> ✅ **Use the agent as a tutor, not an oracle.** When you do not understand a line, ask your agent (Claude Code, Gemini CLI, or Codex CLI) to explain *that specific part* in plain English, then re-explain it back in your own words. Understanding is when you can explain it without the agent, and predict what changing it would do.

---

## Part 2: Read any file (control flow and data flow)

Reading code is not reading prose top to bottom; it is tracing two things at once.

- **Control flow** is the order things run. Find the entry point (where execution starts), then follow each branch (`if`/`else`), loop (`for`/`while`), and function call. Ask: "what runs next, and under what condition?"
- **Data flow** is where values travel. Pick an input and follow it: which variable holds it, which function transforms it, what comes out. Ask: "where did this value come from, and where does it go?"

Here is a small, real example. Read it before reading the explanation under it.

```python
def summarize(sources, max_items=3):
    cleaned = [s.strip() for s in sources if s.strip()]
    top = cleaned[:max_items]
    if not top:
        return "No sources provided."
    return " | ".join(top)
```

Tracing it: the entry is `summarize`. **Data flow:** `sources` (a list of strings) flows into `cleaned`, which keeps only the non-empty ones with spaces trimmed; `cleaned` flows into `top`, the first `max_items` of them. **Control flow:** if `top` is empty, it returns a message; otherwise it joins the items with `" | "`. Now you can predict outputs without running it: `summarize(["a ", "", " b"])` gives `"a | b"`; `summarize([])` gives `"No sources provided."`.

> 💡 **Trace on paper, then confirm.** Write down what you think a function returns for one input, then run it and check. Every time you are wrong, you just found a gap in your mental model, which is the point.

> ❌ **The skim trap.** Scrolling a 200-line file and thinking "looks fine" is not reading. Reading is being able to answer "what happens when this input is empty / huge / malformed?" If you cannot, you have not read it.

---

## Part 3: The core constructs (predict before you run)

You do not need computer-science theory. You need enough of the everyday building blocks to predict what code does:

- **Variables and types:** a name holding a value, and what kind it is (a number, a string of text, a list, a `true`/`false`). Many bugs are a value being the wrong type (a string `"3"` where a number `3` was expected).
- **Data structures:** mostly **lists** (ordered collections) and **dictionaries / maps / objects** (key to value lookups). Knowing which one a function uses tells you how it will behave.
- **Conditionals:** `if` / `else if` / `else`. Read every branch, especially the one that handles "nothing" or "error", because that is where agents cut corners.
- **Loops:** doing something for each item. Ask: "what if the collection is empty? what if it is enormous?"
- **Functions:** inputs in, result out. A function with no clear single job is a smell worth questioning.

> 🔑 **Read the edges first.** The happy path (normal input, everything present) is usually fine. Correctness lives at the edges: empty input, missing keys, zero, negative numbers, very large input, two things happening at once. When you judge agent code, go straight to the edges.

A quick model-agnostic drill you can do with any agent: ask it to write a small function, then *before running it*, write down what it returns for the empty case and one weird case. Run it. Where you were wrong, read until you understand why.

---

## Part 4: When it breaks (stack traces, failure handling, debugging)

Code breaks. The skill is reading the break and forming a hypothesis, not pasting the error back to the model and hoping.

**Read the stack trace bottom to top.** The last line is usually the actual error (for example `KeyError: 'temperature'`). The lines above it are the trail of calls that led there, most-recent last. The trace tells you *what* failed and *where*. That is most of the diagnosis.

```text
Traceback (most recent call last):
  File "scout.py", line 42, in run
    cfg = settings["temperature"]
KeyError: 'temperature'
```

Read that: at `scout.py` line 42, the code asked a dictionary `settings` for the key `"temperature"`, which was not there. The fix is not random; it is "either add that key or handle its absence." That is a hypothesis you can confirm.

**Judge the failure handling.** Robust code expects things to go wrong. When you read agent code, look for:
- **Error handling:** does it catch failures (`try`/`except`, `try`/`catch`) or crash on the first hiccup?
- **Retries and backoff:** for network or model calls, does it retry on a transient failure, waiting a little longer each time, rather than giving up or hammering?
- **Timeouts:** does a call that could hang forever have a time limit?

Agents frequently write the happy path and skip all three. Spotting their absence is a core judgment.

> 💡 **The debugging method (works for any language).** (1) Reproduce the failure reliably. (2) Form one hypothesis about the cause. (3) Isolate: change or print one thing to test that hypothesis. (4) Confirm or reject, then repeat. This beats "ask the agent to fix it" because it is how you *know* the fix is real, and it is how you catch the agent's fix that only hides the symptom.

---

## Part 5: Tests, and what they do and do not prove

A **test** runs your code with a known input and checks the output. Reading and writing a few is how you make verification repeatable instead of a one-time eyeball.

```python
def test_summarize_skips_empties():
    assert summarize(["a ", "", " b"]) == "a | b"

def test_summarize_handles_empty():
    assert summarize([]) == "No sources provided."
```

`assert X == Y` means "if X is not Y, fail loudly." A passing test says "this specific case behaved as expected."

> 🔑 **A test proves presence, not absence.** Passing tests show the cases you thought of work. They do not show the code is correct in general, and they cannot catch a case you did not write. So the skill is choosing cases: the normal one, the empty one, the malformed one, the boundary. When an agent writes tests, read them and ask "what did it *not* test?" That gap is usually where the bug is.

You can have your agent write tests, but you decide what is worth testing, and you read the tests to confirm they actually check the thing that matters (a test that always passes proves nothing).

---

## Part 6: Talking to the outside world (APIs, HTTP, async, the loop)

Every agent you build talks to other systems: a model provider, a database, a tool. Reading that code means understanding three ideas.

- **API and HTTP.** Your code sends a **request** (a method like GET to read or POST to send, a URL, and usually a JSON body) and gets back a **response** (a status code like `200` for success or `500` for a server error, plus a body). When you read a call to a model, you are reading exactly this: a POST with your prompt, a response with the completion and a token count. Reading the status code is the first debugging step when a call fails.
- **Async.** A network call is slow, so code often runs it *asynchronously*: it starts the call and continues, picking up the result when it arrives (you will see `async` / `await`, promises, or callbacks). This matters because an agent loop fires many such calls; reading async code is how you understand why steps happen in the order they do, and why two calls running at once can interfere.
- **The agent loop.** Underneath, an agent is a loop: call the model, read its response, if it asked to use a tool then run the tool and feed the result back, repeat until done. Reading this loop, the same plan, act, verify cycle from Unit 1, is how you understand any agent framework, because they are all variations on it.

> 💡 **The same shape across providers.** A call to Claude, Gemini, or GPT is the same idea: an HTTP request with your messages and settings, a response with the text and usage. The field names differ; the shape does not. Read one and you can read all three. Verify exact field names against the provider's current docs.

> ❌ **Unread external calls are where money and data leak.** A loop with no step cap can call a paid model forever. A tool with broad permissions can touch things it should not. You only catch these by reading the call site, not by trusting that it is fine.

---

## Part 7: Reading a diff and judging a change

Most of your real work is not reading whole files; it is reading **diffs**, the specific lines a change added or removed. This is where you accept or reject the agent's work.

```text
 def run(settings):
-    cfg = settings["temperature"]
+    cfg = settings.get("temperature", 0.7)
     return call_model(cfg)
```

Read it: the old line crashed if `temperature` was missing (the `KeyError` from Part 4); the new line asks for it with a default of `0.7`, so it no longer crashes. That is a good change, and you can say *why*. Judging a diff well means asking, for every change: what does this line now do, why did it change, what could it break elsewhere, and is the default or assumption it introduces actually correct?

- **Version-control fluency is more than running git.** You learned the `add` / `commit` / `push` heartbeat in Unit 1. The judgment skill is reading the diff before you commit and being able to defend every changed line. `git diff` (before staging) and `git diff --staged` (what you are about to commit) are the two commands you will live in.
- **Small diffs are reviewable; giant ones are not.** If an agent hands you a 600-line change you cannot read, that is a signal to ask it to work in smaller steps, not to approve on faith.

> ✅ **Your coding agent can help you review.** Ask it: "explain this diff line by line, and tell me what it might break." Then judge its explanation. Claude Code's `/code-review`, Gemini CLI's review, and Codex's `@codex review` all exist for this, but the final call is yours.

---

## Part 8: Security reading (spotting subtle wrongness)

The most dangerous agent code is not the code that crashes; it is the code that runs fine and is quietly unsafe. You do not need to be a security expert. You need to recognise a few shapes, the ones Unit 10 (safety) defends against architecturally and that you can only spot by reading.

- **Injection.** Untrusted text (a user message, a fetched web page, a tool result) is treated as a trusted instruction or slipped into a command or query. In agents this is **prompt injection**: content the agent reads tells it to do something it should not.
- **Data-exfiltration paths.** Is there a route by which private data could leave (an outbound request, a log, an email tool) that an attacker could trigger?
- **Unsafe tool permissions.** A tool that can run any shell command, delete files, or call any URL is a loaded gun. Read what each tool is *allowed* to do.

> 🔑 **The lethal trifecta.** An agent is dangerous when it has all three of: access to private data, exposure to untrusted content, and a way to send data outward. Any one alone is usually fine; all three together is an exfiltration waiting to happen. You can only spot this combination by reading what data the agent sees and what it is allowed to do. This is the concrete reason the floor is load-bearing: the architecture in Unit 10 cannot protect a learner who cannot read for the trifecta in their own agent's code.

A model-agnostic habit: for any agent you build, write one sentence answering "what private data can it see, what untrusted input can reach it, and how could data get out?" If all three have an answer, you have a trifecta to design around.

---

## Key takeaways

1. **Typing is optional; judging is not.** Your leverage is reading and judging the agent's code, not writing it.
2. **The one rule:** do not merge what you cannot read, explain out loud, and break on purpose.
3. **Read for control flow and data flow, and go straight to the edges**, where correctness actually lives.
4. **Debug by hypothesis.** Read the stack trace, form a guess, isolate, confirm. Do not paste-and-pray.
5. **Tests prove presence, not absence**, and a diff is where you accept or reject a change, line by line.
6. **Read for the lethal trifecta:** private data, untrusted input, and an outward path together is the danger.

## Common pitfalls

- ❌ Skimming a file and calling it "read" when you cannot answer what happens on empty or malformed input.
- ❌ Pasting an error back to the agent and accepting whatever it returns, without forming your own hypothesis.
- ❌ Trusting green tests as proof of correctness, instead of asking what was not tested.
- ❌ Approving a giant diff on faith because reading it is tedious.
- ❌ Ignoring missing error handling, retries, or timeouts because the happy path works.
- ❌ Never asking the three trifecta questions of your own agent.

---

## 🛠️ The Build: the Warden rubric, and your first read, explain, break, fix

> The hands-on payoff. You create the verification rubric you will use for the rest of the course (the seed of Warden, the AtlasOS quality gatekeeper), and you run a real component through the full read, explain, break, fix cycle. From now on, every unit ends by passing its new component through this rubric.

### What you will build

A short, committed `atlas/warden/verification-rubric.md`, plus a completed first pass: you read a piece of real code from your Unit 1 project (or your Unit 0 first-call script), explain it, deliberately break it, predict and confirm the failure, then fix it.

### Milestones (in order, each fully explained)

1. **Open your project.** In your VS Code terminal: `cd ~/atlasos`, then `code .`. Pick a real file the agent helped you make earlier (the Unit 1 README task, or the Unit 0 first-call script). This is the code you will judge.

2. **Write the Warden rubric.** Create the folder and file (`atlas/warden/verification-rubric.md`). Put this checklist in it, in your own words. It travels with every component you build:

```text
# Warden verification rubric
Before a component is "done", I can answer YES to all five:
1. TRACE  - I can follow its control flow and data flow end to end.
2. EXPLAIN- I can explain, out loud and without the agent, what each part does and why.
3. EDGES  - I know what it does on empty, missing, huge, or malformed input.
4. BREAK  - I can name at least one way it fails, and I have broken it on purpose to confirm.
5. SECURE - I have asked the trifecta questions: private data? untrusted input? outward path?
```

3. **Read and explain (rubric 1, 2, 3).** Trace your chosen file. Where a line is unclear, ask your coding agent to explain *that line*, then re-explain it back in your own words. Write a two-sentence summary of what the file does at the top of a scratch note. If you cannot, keep reading until you can.

4. **Break it on purpose (rubric 4).** Change one thing that should make it fail (rename a variable, remove a check, pass an empty input). **Before running**, write down what you predict will break. Run it. Read the stack trace and confirm whether you were right. Being wrong is useful: it shows a gap to close.

5. **Fix it (and harden it).** Undo your deliberate break. Then fix one *real* weakness you noticed while reading (a missing empty-input check, no timeout on a call, a key that could be absent). Re-run and confirm.

6. **Run the security questions (rubric 5).** Write one sentence each: what private data could this touch, what untrusted input could reach it, how could data get out? If all three have an answer, note the trifecta to design around later.

7. **Commit it.** Save the rubric and your notes with the git heartbeat from Unit 1: `git add -A`, `git commit -m "Add Warden verification rubric and first read-break-fix pass"`, `git push`.

8. **Stretch (optional).** Ask your agent to write a small function, then trace it and write two tests *before* running anything: one normal case, one edge case. Run them. If a test passes when it should not, you have found a bad test, which is its own lesson.

### How you will know you are done

- ✅ `atlas/warden/verification-rubric.md` exists and is committed.
- ✅ You read a real file and can explain it without the agent.
- ✅ You broke it on purpose, predicted the failure, and confirmed it from the stack trace.
- ✅ You fixed one genuine weakness and re-verified.
- ✅ You answered the three trifecta questions for that code.

> 💡 If reading the file felt slow, that is normal and it is the work. Speed comes with reps. You will get one every single unit from here on.

---

## Cheat sheet

```text
THE ONE RULE
  Don't merge what you can't read, explain out loud, and break on purpose.

READ A FILE
  control flow = what runs next, under what condition
  data flow    = where each value comes from and goes
  go to the EDGES: empty, missing, huge, malformed, two-at-once

WHEN IT BREAKS
  read the stack trace bottom-up: last line = the error
  debug by hypothesis: reproduce -> guess -> isolate -> confirm
  look for missing: error handling, retries/backoff, timeouts

JUDGE A CHANGE
  read the diff line by line; defend every changed line
  tests prove presence, not absence: ask "what wasn't tested?"

SECURITY (the lethal trifecta)
  private data + untrusted input + outward path = danger
  read each tool's permissions; ask the three questions

WARDEN RUBRIC: trace - explain - edges - break - secure
```

## How this connects to the rest of the course

- **Next, Unit 3 (Prompting and context engineering):** with the floor in place, you sharpen how you instruct the model. You will read the outputs it produces with the eye you just trained.
- **Throughout:** every later unit ends by running its new AtlasOS component through the Warden rubric from this unit. The automated version of Warden, a graded eval harness, is built in Unit 9; this rubric is the human seed it grows from.
