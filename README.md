# Pip — an ESP32 desk robot with animated eyes 🤖

Pip is an **ESP32 + 128×64 OLED** that shows **procedurally animated eyes**, driven by
**Claude Code** (over MCP, default) or a **local Ollama** chat. Flash the board once over
USB; after that everything runs in Python on your computer and talks to the ESP32 over
**Bluetooth** via [python-esp-bridge](https://github.com/HamzaYslmn/python-esp-bridge).

<p align="center"><img src="docs/pip-eyes.gif" width="384" alt="Every Pip mood, gesture and activity"></p>
<p align="center"><img src="docs/smoking.gif" width="384" alt="Pip reacting live while Claude Code works"></p>

- **Expressive face** — 32 emotions · 24 gestures · 14 looping activities, drawn with PIL,
  with auto-blink, breathing and idle glances on a background thread.
- **Drives any pin** — tell Pip what's wired where; it controls servos, LEDs, motors and
  sensors through tool calls. No per-device code.
- **Two brains** — Claude Code over MCP (face + pins as tools), or a local Ollama model
  returning `{response, emotion, gesture}`.

## Hardware

| Need | Notes |
|---|---|
| **Classic ESP32** (ESP‑32S/D) | Bluetooth needs a *classic* ESP32 — S3/C3/C6/H2 are USB‑only and won't work wirelessly. |
| **128×64 I²C OLED** | SSD1306 or SH1106 (the common 0.96″/1.3″ modules). |
| **USB cable** | One‑time firmware flash; Bluetooth after that. |
| **[uv](https://docs.astral.sh/uv/)** | Installs Python + deps. |
| Ollama *(optional)* | Local chat mode only. |

Wire the OLED: **VCC→3V3, GND→GND, SDA→GPIO21, SCL→GPIO22** (other pins are fine — set
`ROBOT_OLED_SDA` / `ROBOT_OLED_SCL`).

## Setup

```bash
uv sync                  # 1. install deps (the bridge, OLED driver, flasher) — needs Python ≥3.13
uv run espbridge flash   # 2. flash firmware over USB (once) — lists ports, pick one
uv run espbridge info    # 3. unplug USB, confirm Bluetooth reaches the board (prints chip + MAC)
```

The firmware's default Bluetooth password is **`espbridge`**, which matches Pip's defaults —
so there's nothing to configure to get started.

<details><summary>Prefer the Arduino IDE for step 2?</summary>

Install the **python esp bridge** library (Library Manager), open *Examples → python esp
bridge → Bridge*, set the partition scheme to **Huge APP**, and Upload. The sketch is one line:

```cpp
EspBridge.begin();        // default Bluetooth password "espbridge"
```
</details>

## Use Pip in Claude Code

**One command — adds Pip to every project, no checkout needed:**

```bash
claude mcp add pip-robot --scope user -- \
  uvx --from git+https://github.com/HamzaYslmn/esp-bridge-mcp-robot pip-robot
```

That's it. `uvx` runs Pip's `pip-robot` server straight from GitHub, and Claude Code calls
the `set_face` / `set_activity` tools as it works — so the eyes react live while you code.
(MCP mode is the default; `uvx --refresh …` pulls the latest.)

> **Working inside this repo?** You don't even need that command — open the folder in Claude
> Code and approve the checked‑in `.mcp.json` when prompted.

The two face tools are pre‑allowed in `.claude/settings.json` so they never stall on a
permission prompt. The pin and `notify` tools ask first — add `"mcp__pip-robot__*"` to
pre‑approve moving hardware.

## Run it yourself

```bash
cp src/.env.example src/.env      # optional — the defaults already work
uv run src/main.py                # MCP server (default)
uv run src/main.py demo           # menu: play any mood / gesture / activity
uv run src/main.py --no-display   # no board attached (engine only)
```

Prefer local chat over Claude Code? Set `ROBOT_MCP=false` in `.env`, run
`ollama pull qwen3.5:4b`, then `uv run src/main.py` and talk to Pip in the terminal.

## Configuration

`src/.env` (copy from `src/.env.example`). Every value has a built‑in default — you only
set what you change.

| Var | Default | Meaning |
|---|---|---|
| `ROBOT_MCP` | `true` | `true` = MCP server, `false` = Ollama chat |
| `ROBOT_BLE_TARGET` | _(auto)_ | Board name or MAC (empty = first board found) |
| `ROBOT_PASSWORD` | `espbridge` | Firmware Bluetooth password (`EspBridge.begin(...)`) |
| `ROBOT_OLED_SDA` / `_SCL` | `21` / `22` | OLED I²C pins |
| `ROBOT_BRIGHTNESS` | `255` | Panel brightness cap, 0–255 (moods like `standby` dim below it) |
| `ROBOT_FPS` | `24` | Eye frame rate |
| `ROBOT_MODEL` | `qwen3.5:4b` | Ollama model (chat mode) |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server (chat mode) |

## Extending

Add a tool in `build_tools` for new hardware, or a face in **one line** — an emotion in
`eyes/moods.py`, a gesture in `eyes/gestures.py`, an activity in `eyes/activities.py`. Both
brains pick it up automatically. Rebuild the showcase GIF with `uv run docs/make_gif.py`.

## Troubleshooting

- **No board / won't connect** — flashed the firmware? board powered? `ROBOT_PASSWORD` matches?
  `uv run espbridge info` should print the chip and MAC.
- **Wireless doesn't work at all** — it must be a *classic* ESP32; S3/C3/C6/H2 are USB‑only.
- **Blank OLED** — check SDA/SCL match `ROBOT_OLED_SDA` / `_SCL`.
- **Bluetooth drops mid‑session** — Pip self‑heals; the face resumes once the board is back.
  Still dark? It lost power or is out of range.
- **`uv sync` fails on a wheel** — `uv python pin 3.13 && uv sync`.
