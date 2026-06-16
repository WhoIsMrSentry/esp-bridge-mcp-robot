# CLAUDE.md

"Pip" — a desk robot: ESP32 + 128×64 OLED with animated eyes, over Bluetooth via
`python-esp-bridge[all]`. Driven by **Claude Code over MCP** (default) or a local
**Ollama** chat (`ROBOT_MCP=false`).

## Rules

Lean one-liner comments. YAGNI / DRY / KISS. Verb-y self-explaining names. No AI
attribution in commits/PRs.

## Run — uv, Python ≥3.13

```bash
uv sync
uv run src/main.py                   # MCP server over stdio (default); Claude Code spawns this via .mcp.json
ROBOT_MCP=false uv run src/main.py   # Ollama chat
uv run src/main.py --no-display      # no hardware
```

## Layout

Source under `src/`; imports are absolute from there (`from modules.…`). The same
package installs as `modules`, so `uvx --from git+<repo> pip-robot` runs it with no
checkout. Settings come from `os.getenv` (every read has a code default). Our
`modules/espbridge` ≠ the installed `espbridge` library. Add a capability in
`build_tools`; add a face by dropping one self-contained file in `eyes/moods/`,
`eyes/gestures/`, or `eyes/actions/` (each exposes a single `MOOD`/`GESTURE`/`ACTION` —
see `eyes/spec.py`), then list its name in that folder's `__init__.py` order tuple
(that tuple is the curated order — menus, showcase, LLM enum). Shared bits: `painters.py`
(lid carvers), `primitives.py` (draw/math), `engine.py` (renderer). Eyeball a face
headless with `uv run docs/make_gif.py <face>` (writes a 5-frame `docs/<face>_preview.png`,
gitignored); no args rebuilds the showcase `docs/pip-eyes.gif`.

## MCP

The MCP server runs over **stdio** (FastMCP `transport="stdio"`, the default). `.mcp.json`
is `{type: stdio, command: uv, args: [run, src/main.py]}`, so Claude Code *spawns* the
process itself and owns its lifecycle — one instance per session, which keeps it the sole
owner of the BLE link (stop it before running the demo). Because stdio uses **stdout** for
JSON-RPC, nothing may print to stdout — all logs go to stderr. No port, no HTTP.

## Face — keep Pip alive (do this, don't just read it)

**Both layers are automatic now — don't hand-drive either.**

- **Activity** (what Pip's *doing*): `mcp_tool` hooks in `.claude/settings.json` cover the
  Claude Code hook lifecycle (24 events). Each is **typed to how long it should read** — a
  looping `set_activity` for a state that lingers, a *bare* held `set_face` emotion for a mood
  that should dwell, and a one-shot `set_face` gesture only for a genuinely fleeting beat (a
  quick nod/wink). A flashing gesture where Pip should *dwell* feels wrong, so those became
  actions/bare-moods. The everyday flow: `thinking` on `UserPromptSubmit`, per-tool activities
  on `PreToolUse` (editing / working / scanning / searching / connecting), `waiting` while you
  ask the user something (`PreToolUse` on `AskUserQuestion` — `Notification` does *not* fire for
  it), `processing` while a subagent runs (`SubagentStart`, **pip-face excluded** via
  `^(?!pip-face).*`), `debugging` on `PostToolUseFailure`, `glitch` on `StopFailure`, `idle` on
  `Stop`. Big lifecycle beats use the four **self-ending actions** (in `eyes/actions/`, each ends
  itself via `Action.expired`): `wakeup` on `SessionStart` startup, `celebrate` on
  `TaskCompleted`, `meditate` (wears **zen**) on `PreCompact`, `powerdown` on `SessionEnd`.
  **smoking** rides `Notification/idle_prompt` (Pip takes a break while you're away). The MCP
  elicitation double-fire is deduped to the dedicated `Elicitation` (→ `listening`) /
  `ElicitationResult`. Deliberately **unmapped** to avoid strobe / BLE-flood: `MessageDisplay`,
  `FileChanged`, `PostToolUse`, `PostToolBatch`, `UserPromptExpansion`, `InstructionsLoaded`.
  Each action wears its own fitting face (its `Action.mood`), so an activity never blends with
  the emotional mood.
- **Emotional mood** (how Pip *feels*): a `UserPromptSubmit` command hook
  (`.claude/hooks/dispatch_mood.py`) re-injects a standing order every message to hand
  mood-picking to the cheap **pip-face (Haiku)** subagent. When you see it, dispatch
  pip-face (Agent, `subagent_type='pip-face'`) in your first tool-call batch, in parallel
  with your real work — it reads the message, picks a fitting mood, and sets it via
  `set_face` over the shared link. **Don't choose or call `set_face` yourself.**

All these hooks/subagents reuse this session's MCP connection, so they never open a second
BLE link.

**The only face you still drive by hand** is a one-off situational *action* mid-task, when
it genuinely fits — an event, not the per-message mood (pip-face owns that):

- **A snag or error** → `set_activity("glitch")`.
- **A win / a breather** → `set_activity("smoking")` (a chilled break — it's an action).
