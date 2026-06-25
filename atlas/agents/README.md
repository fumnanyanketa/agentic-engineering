# Agents — the fleet

Specialized workers, each a prompt + tools + (optionally) subagents:

- **Scout** — research and intelligence (build this one first).
- **Forge** — the builder (ships code via Claude Code).
- **Pulse** — analytics (the agentic analytics harness, M9 L37).
- **Herald** — comms and reporting.
- **Warden** — review, safety, and verification (eval gatekeeper; see [`../evals/`](../evals/)).

**First built in:** Module 5. **Vertical flagship chosen in:** Module 9.

## TODO (fill in as you go)
- [ ] M5 L13–L15: ship Scout to production (managed agent), then harden it
- [ ] M5 L16: document the tool-vs-skill-vs-subagent decomposition
- [ ] M5 L19: harvest winning patterns from the agent-battle drill
- [ ] M9 L32–L37: build one flagship vertical agent; finish Pulse
