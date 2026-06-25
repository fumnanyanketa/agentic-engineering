#!/usr/bin/env python3
"""
Warden's eval runner for the Scout research agent.

Run:    python run_evals.py
Output: a pass/fail grid and a single suite score.

By default this grades RECORDED Scout outputs (scout_outputs.sample.json) so it
runs offline with no API key. To grade a LIVE agent, set USE_LIVE_MODEL = True
and fill in run_scout() / llm_judge() with a real model call. The eval methods
here are provider-neutral: point run_scout at Claude, Gemini, or GPT and run the
SAME suite against each to compare. For the LLM-as-judge, prefer a DIFFERENT
model than the one under test.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
USE_LIVE_MODEL = False  # flip to True once run_scout()/llm_judge() call a real model


# --------------------------------------------------------------------------
# The agent under test. Offline by default; swap in a real call for live runs.
# --------------------------------------------------------------------------
def run_scout(question, sources):
    """Return Scout's answer string for one case."""
    if USE_LIVE_MODEL:
        # Example shape (pseudocode), provider-neutral:
        #   prompt = open("../prompts/scout.md").read()
        #   return call_model(system=prompt, user=question + "\n\nSOURCES:\n" + "\n".join(sources))
        raise NotImplementedError("Wire up a real model call (Claude / Gemini / GPT).")
    # Offline: look the answer up by case id (set on the case dict before calling).
    return _RECORDED[run_scout._cid]


# --------------------------------------------------------------------------
# Graders. Code graders are deterministic; llm_judge is the subjective one.
# --------------------------------------------------------------------------
def grade_must_contain(ans, case):
    text = ans.lower()
    needles = case.get("expect_all_of") or case["expect"]
    require_all = "expect_all_of" in case
    hits = [n for n in needles if n.lower() in text]
    ok = (len(hits) == len(needles)) if require_all else bool(hits)
    detail = f"found {hits or 'none'} of {needles}"
    if case.get("must_cite") and ok and not _looks_cited(ans):
        return False, detail + "; but missing a citation"
    return ok, detail


def grade_refuses_to_invent(ans, case):
    text = ans.lower()
    refused = any(m.lower() in text for m in case["expect_refusal_markers"])
    invented = any(f.lower() in ans for f in case.get("forbid", []))
    ok = refused and not invented
    return ok, f"refused={refused} invented_forbidden={invented}"


def grade_llm_judge(ans, case):
    """Subjective 'taste' grader. Returns (pass, reasoning)."""
    verdict, reasoning = llm_judge(case["rubric"], case["question"], ans)
    return verdict == "PASS", reasoning


def llm_judge(rubric, question, answer):
    """
    LLM-as-judge. Reason FIRST, then emit PASS/FAIL on the last line, so the
    score does not poison the reasoning. Offline, we apply the rubric's checks
    directly; live, send rubric+answer to a DIFFERENT model than Scout.
    """
    if USE_LIVE_MODEL:
        raise NotImplementedError("Send rubric + answer to a judge model; parse last line.")
    t = answer.lower()
    faithful = ("measure" in t) and ("bottleneck" in t)
    concise = answer.count(".") <= 3
    reasoning = (
        f"Faithful to sources (measurement + verification-as-bottleneck): {faithful}. "
        f"Concise (<= 2 sentences): {concise}."
    )
    verdict = "PASS" if (faithful and concise) else "FAIL"
    return verdict, reasoning


def _looks_cited(ans):
    a = ans.lower()
    return ("source" in a) or ("[" in ans and "]" in ans)


GRADERS = {
    "must_contain": grade_must_contain,
    "refuses_to_invent": grade_refuses_to_invent,
    "llm_judge": grade_llm_judge,
}


# --------------------------------------------------------------------------
# Runner
# --------------------------------------------------------------------------
def main():
    with open(os.path.join(HERE, "scout_cases.json")) as f:
        suite = json.load(f)
    global _RECORDED
    with open(os.path.join(HERE, "scout_outputs.sample.json")) as f:
        _RECORDED = json.load(f)

    print(f"\nWarden suite: {suite['suite']}\n" + "=" * 64)
    rows, passed = [], 0
    hard_total = hard_passed = 0

    for case in suite["cases"]:
        run_scout._cid = case["id"]
        ans = run_scout(case["question"], case["sources"])
        grader = GRADERS[case["grader"]]
        ok, detail = grader(ans, case)
        if case.get("hard"):
            hard_total += 1
            hard_passed += int(ok)
        passed += int(ok)
        mark = "PASS" if ok else "FAIL"
        flag = "  <-- 'the exponential moved' detector" if case.get("hard") else ""
        rows.append((case["id"], case["kind"], mark, detail, flag))

    width = max(len(r[0]) for r in rows)
    for cid, kind, mark, detail, flag in rows:
        print(f"  [{mark}] {cid.ljust(width)}  ({kind})  {detail}{flag}")

    total = len(suite["cases"])
    print("=" * 64)
    print(f"SCORE: {passed}/{total} passed  ({100*passed//total}%)")
    if hard_total:
        print(f"Hard cases passed: {hard_passed}/{hard_total}  "
              f"(0 is EXPECTED today; keep it red until a better model passes it)")
    print()
    # Exit 0 even with the hard case red: a red detector is the desired state.
    sys.exit(0)


if __name__ == "__main__":
    main()
