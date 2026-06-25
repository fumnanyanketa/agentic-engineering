# Coding agents, current operational practice (verified June 2026)

Reference notes for authoring the model-agnostic units. Three CLI coding agents.
Commands/model ids move fast: re-verify against official docs near publication.

## Claude Code (Anthropic)
- Install: `curl -fsSL https://claude.ai/install.sh | bash` (native), or `npm i -g @anthropic-ai/claude-code`; verify `claude --version`, `claude doctor`. Needs Pro/Max/Team/Enterprise/Console (no free tier); CI via `ANTHROPIC_API_KEY`. Also Bedrock/Vertex/Foundry.
- Surfaces: terminal, Desktop app, VS Code + JetBrains extensions, web (claude.ai/code), mobile, Slack, GitHub Actions/GitLab.
- Core loop: plain-English prompts; reads files on demand; diffs for approval; runs tests. Plan mode = read-only (`Shift+Tab` cycles default -> acceptEdits -> plan; or `/plan`). `/clear`, `/compact`, `/context`.
- Autonomy: 6 permission modes (default, acceptEdits, plan, auto, dontAsk, bypassPermissions). `auto` mode routes risky actions to a separate classifier model (research preview). Rules: permissions.allow/deny/ask; eval deny->ask->allow. Sandboxing on macOS/Linux/WSL2.
- Memory: CLAUDE.md hierarchy (org -> ~/.claude -> project -> CLAUDE.local.md); `/init` scaffolds; `/memory`; auto-memory per-repo at ~/.claude/projects/<p>/memory/. `@import` paths. Resume: `claude -c` / `-r` / `/resume`.
- Parallelism: git worktrees (`claude --worktree`), subagents (`.claude/agents/`, `isolation: worktree`), background (`claude --bg`, `claude agents`), `/batch`, agent teams (experimental), web (`--remote`/`--teleport`).
- Automation: hooks in settings.json (events SessionStart/UserPromptSubmit/PreToolUse/PostToolUse/Stop/... ; handlers command/http/mcp_tool/prompt/agent; exit 2 blocks). `/loop [interval]`, `/goal <condition>`. GitHub: `anthropics/claude-code-action@v1`, `/install-github-app`, `@claude`.
- Tools/MCP: `claude mcp add [--transport stdio|sse|http] [--scope ...]`; `.mcp.json`; `/mcp`. Skills (`SKILL.md`), custom `/commands`.
- Review: `/code-review [--comment] [--fix]` (effort low|default|high|max), `/security-review`, Managed Code Review (GitHub App), `/autofix-pr` (green-PR loop).
- Essence: terminal-native, permission-graded, plain-English; deep operational surface (memory + worktrees + hooks + MCP + verification stack) across terminal/IDE/CI/web/mobile.

## Gemini CLI (Google) — open source, Apache-2.0
- IMPORTANT (verified): Google Developers Blog announced transition of Gemini CLI to **Antigravity CLI** for free/AI Pro/AI Ultra/individual + new GitHub-org installs, effective **2026-06-18**. Paid **Gemini Code Assist Standard/Enterprise** and Cloud/Vertex/API-key users keep Gemini CLI ("access remains unchanged"). Antigravity CLI carries over Skills, Hooks, Subagents, Extensions. Treat Gemini CLI as the canonical reference design for Google's terminal agent; note the rebrand.
- Install: `npm i -g @google/gemini-cli` (Node 20+), or `npx @google/gemini-cli`, `brew install gemini-cli`; run `gemini`.
- Auth: Google OAuth (browser), `GEMINI_API_KEY` (AI Studio), Vertex (`GOOGLE_GENAI_USE_VERTEXAI=true`), Code Assist license (`GOOGLE_CLOUD_PROJECT`). Free tier (pre-cutoff): ~1,000 req/day on Google login; 250/day Flash on API key. Gemini 3 Pro paid-only.
- Core loop: NL prompt at REPL or `-p` headless; official "reason and act (ReAct) loop"; built-in file/shell/web-fetch/Google-Search-grounding; `plan` approval mode (read-only).
- Autonomy: `--approval-mode default|auto_edit|plan|yolo` (yolo = approve all, CLI-only, `--yolo` / `Ctrl+Y`). Sandbox: `-s`/`GEMINI_SANDBOX` (Docker/Podman/Seatbelt/gVisor). Headless `-p` + `--output-format text|json|stream-json`.
- Memory: `GEMINI.md` hierarchical (~/.gemini/GEMINI.md global -> ./GEMINI.md -> ./src/GEMINI.md); `/memory show|add|refresh`; `save_memory` tool.
- Parallelism: subagents (`.gemini/agents/*.md`, YAML frontmatter, `@agent_name`, one level of delegation); `/chat save|resume`, checkpointing; `/restore` (file rollback), `/rewind`; run multiple processes per dir/worktree (no native worktree command).
- Automation: headless filter (`git diff | gemini -p "..." --output-format json | jq`); GitHub Action `google-github-actions/run-gemini-cli` (Dispatch/Issue Triage/PR Review/Assistant; `@gemini-cli /review`, cron); hooks in settings.json (BeforeTool/AfterTool/Stop/UserPromptSubmit; can block).
- Tools/MCP: `mcpServers` in settings.json (command/url/httpUrl); `gemini mcp add|list|...`; `/mcp`; Extensions (`/extensions`); Skills (`/skills`).
- Review: diff+approval in default/auto_edit; ReAct runs tests/lint and self-corrects; `/restore`/`/rewind`; PR Review workflow / `@gemini-cli /review`.
- Essence: open source, huge context (1M tokens), Google Search grounding built in, free on-ramp, Vertex integration. Same primitives as peers.

## Codex CLI (OpenAI) — open source, Rust. "Codex" = the coding agent (CLI+cloud+IDE+GitHub), NOT the 2021 model.
- Install: `npm i -g @openai/codex` (Node 18+), `brew install --cask codex`, or install script; verify `codex --version`.
- Auth: `codex login` -> Sign in with ChatGPT (Plus/Pro/Business/Edu/Enterprise) OR API key (usage billing, for CI). Headless `codex login --device-auth`. Creds ~/.codex/auth.json. Cloud requires ChatGPT sign-in. Models: current Codex-tuned GPT-5 family; `/model`, `model_reasoning_effort = minimal|low|medium|high|xhigh`.
- Surfaces: CLI (TUI), IDE extension, Cloud/Web (chatgpt.com/codex), GitHub (`@codex`).
- Core loop: `codex` in repo, send a message; reads/edits/runs in sandbox; `/plan`, `/diff`, `/review`, `/mention`/`/ide`, image attach.
- Autonomy: two layers. Sandbox `--sandbox read-only|workspace-write|danger-full-access`. Approval `--ask-for-approval untrusted|on-request|never` (+ granular, auto_review). Network off by default in workspace-write (`network_access=true`, domain allowlist). Full-auto = workspace-write + never; `--yolo` (`--dangerously-bypass-approvals-and-sandbox`) for disposable/CI.
- Memory: `AGENTS.md` (closest-to-cwd wins; ~/.codex/AGENTS.md global, project + nested per-dir; `## Review guidelines` steers reviewer); `/init`. Config `~/.codex/config.toml`, `.codex/config.toml`, `--profile`.
- Parallelism: Codex **cloud** runs many tasks in parallel, each in its own sandbox with built-in worktrees; delegate from IDE/CLI/GitHub. Local threads `/new`, `/fork`, `/side`, `/resume`; subagents `/agent`; `/ps`, `/stop`.
- Automation: `codex exec` (`codex e`) non-interactive; `--json`, `--output-schema`, `-o`, `--sandbox`, `--skip-git-repo-check`; `codex exec resume`. GitHub: `@codex review` / automatic reviews / `@codex fix...` (cloud task, pushes fix). Lifecycle hooks via `/hooks`.
- Tools/MCP: `[mcp_servers.<id>]` in config.toml or `codex mcp`; `/mcp`. Built-in file/shell/web-search (`--search`)/image/review. Custom prompts `~/.codex/prompts/*.md` (deprecated in favor of `/skills`). `/import` migrates Claude Code setup.
- Review: `/review`, `/diff`; cloud Codex code-review posts GitHub review surfacing only P0/P1; honors AGENTS.md `## Review guidelines`; tests run in sandbox (often `codex exec` CI step).
- Essence: cloud-parallel agents fused with the ChatGPT subscription; one agent across CLI/IDE/web/GitHub; delegate fan-out to ephemeral cloud sandboxes; PR-native P0/P1 review bot.

## Cross-tool convergence (the durable, model-agnostic shape)
- Project context file: CLAUDE.md / GEMINI.md / AGENTS.md (same idea; AGENTS.md is becoming a shared convention).
- Tiered autonomy: read-only/plan -> auto-edit -> full-auto/yolo, with sandboxing.
- A read-edit-run (ReAct / plan-act-verify) loop that self-corrects on test/lint failure.
- MCP for external tools/data, subagents for delegation, hooks for lifecycle automation.
- Headless/exec mode for CI + a GitHub PR review bot.
- The workflow is largely portable; pick by ecosystem/price/preference, not by losing capability.
