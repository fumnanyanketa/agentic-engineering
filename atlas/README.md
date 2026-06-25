# AtlasOS

> The north-star project for the **Building with Claude** course. A self-improving operating
> system of cooperating AI agents that runs knowledge work end to end.

This folder is the home of your real build. The course's 38 lessons each contribute one
component here, so by the end you have shipped one platform instead of 38 disconnected
exercises.

## Start here

1. **[`00-company-brief.md`](00-company-brief.md)** — what Atlas Group / AtlasOS is, and why.
   The editable source of truth.
2. **[`01-architecture.md`](01-architecture.md)** — how the pieces fit and the build order.
3. **[`02-roadmap.md`](02-roadmap.md)** — which lesson builds which component.

## The components (this skeleton)

| Folder | Layer | First built in |
|---|---|---|
| [`orchestrator/`](orchestrator/) | Atlas — plans and dispatches work | M4 |
| [`agents/`](agents/) | Scout, Forge, Pulse, Herald, Warden | M5 |
| [`memory/`](memory/) | Cortex — memory and the dreaming loop | M5 |
| [`prompts/`](prompts/) | Versioned prompt library + routing policy | M2 |
| [`evals/`](evals/) | Warden's graded test suites | M3 |
| [`tools/`](tools/) | Tool / MCP layer to the outside world | M5 |
| [`deploy/`](deploy/) | Running AtlasOS on a real cloud | M7 |
| [`ops/`](ops/) | Operating model + observability | M8 |

## The loop

Watch the talk → read the lesson → build its capstone **as the AtlasOS component** for that
lesson → commit it here → tick the box in [`../PROGRESS.md`](../PROGRESS.md). Repeat.

*Scaffold v0.1, 2026-06-16. Most folders below are intentionally near-empty: you fill them in
as the course progresses.*
