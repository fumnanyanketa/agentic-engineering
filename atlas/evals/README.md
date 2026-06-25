# Evals — Warden's test suites

Graded cases for each agent and for the system end to end, including at least one deliberately
hard case (your "the exponential moved" detector). This is the discipline that makes
everything else trustworthy. Nothing ships past Warden without passing.

**First built in:** Module 3. **Extended:** whenever you add a capability.

## What is here (Warden's first suite, for Scout)

- `scout_cases.json` — 6 graded cases for the Scout research agent (control, two edge,
  one capability/handoff, one subjective, and one deliberately hard). Each case has a
  pass criterion. The `exp-moved` case is expected to FAIL today on purpose.
- `scout_outputs.sample.json` — recorded Scout v0 answers, so the suite runs offline with
  no API key. Replace with a live model call to grade a real agent.
- `run_evals.py` — the runner and graders (code graders + a simple LLM-as-judge). Prints a
  pass/fail grid and a single suite score.

## Run it

```text
cd atlas/evals
python run_evals.py
```

Today's score is **5/6 (83%)**, with `exp-moved` red. That is the intended state: a passing
hard case would mean the exponential moved (a better model arrived), and you would write a
new, harder one.

## Model-agnostic

The eval methods are provider-neutral. Point `run_scout()` at Claude, Gemini, or GPT and run
the **same** suite against each to compare. For the LLM-as-judge, prefer a **different** model
than the one under test, to avoid a model grading its own style favorably.

## TODO (fill in as you go)
- [x] M3 L7: Warden's first graded suite, with one case today's model fails
- [ ] M6 L22: wire evals into the self-improving prompt loop
- [ ] ongoing: add cases each time an agent gains a new capability
