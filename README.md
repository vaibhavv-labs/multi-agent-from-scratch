# Agents Talking

A live, visual demo showing how AI agents communicate with each other, built from scratch in plain Python with zero dependencies and a real-time 3D dashboard.

## Demo

https://github.com/vaibhavv-labs/multi-agent-from-scratch/raw/main/agent%20demo.mp4

<video src="agent%20demo.mp4" controls="controls" width="100%"></video>

> 📹 **Demo video:** [`agent demo.mp4`](agent%20demo.mp4)

![demo](demo.gif)

---

## How It Works

At its core, an agent is just an inbox and a loop: it waits for a message, processes it, and sends a response.

In this project, each agent is an independent Python object with its own `asyncio.Queue` inbox. A shared message bus delivers messages between inboxes and introduces a brief pause so message delivery is visible. Every time a message is sent, the event is recorded and streamed over Server-Sent Events (SSE) to a 3D browser dashboard. The agents coordinate entirely through structured message passing without any external framework like CrewAI, LangGraph, or AutoGen.

---

## Message Flow

The demo runs a 7-step sequence between the four agents:

1. **orchestrator -> researcher** (`task`): Orchestrator sends the research topic.
2. **researcher -> orchestrator** (`result`): Researcher extracts 3 facts and returns them.
3. **orchestrator -> writer** (`task`): Orchestrator forwards facts and brief to the writer.
4. **writer -> reviewer** (`draft v1`): Writer drafts a short LinkedIn post.
5. **reviewer -> writer** (`feedback`): Reviewer rejects draft v1 ("add a concrete example").
6. **writer -> reviewer** (`draft v2`): Writer incorporates feedback and revises the post.
7. **reviewer -> orchestrator** (`approved`): Reviewer approves the revised draft, and orchestrator prints and emits the final post.

---

## Project Structure

```text
agents-talking/
├── orchestrator.py    # Coordinates workflow, assigns tasks, outputs final post
├── researcher.py      # Researches topic and returns 3 concise facts
├── writer.py          # Drafts and revises a short LinkedIn post
├── reviewer.py        # Rule-based reviewer providing feedback and approval
├── base_agent.py      # Base agent class with send, think, loop, and llm helper
├── bus.py             # Message bus with per-agent queues and visual delay
├── message.py         # Message dataclass (sender, to, type, content, id)
├── events.py          # Thread-safe event buffer for SSE streaming
├── server.py          # Standard library HTTP server for dashboard and SSE
├── dashboard.html     # Live 3D Three.js dashboard with dark/beige themes
├── main.py            # Entry point wiring agents, bus, and server
└── agent demo.mp4     # Demo video showing the live 3D dashboard in action
```

### The 4 Agents
- **`orchestrator.py`**: Receives "start", sends a task to the researcher, forwards the researcher's facts to the writer, and on "approved" prints and emits the final post.
- **`researcher.py`**: Receives a task, returns 3 facts.
- **`writer.py`**: Drafts a short LinkedIn post, and revises it when it gets feedback.
- **`reviewer.py`**: Rejects vague drafts with feedback ("add a concrete example"), approves the revised one.

### Supporting Files
- **`base_agent.py`**: Agent base class with `send()`, `think()`, a run loop, and an `llm()` helper (calls the Anthropic API via `urllib` if `ANTHROPIC_API_KEY` is set, otherwise uses an offline fallback so the demo never fails).
- **`bus.py`**: Bus with one `asyncio.Queue` inbox per agent; every message goes through `bus.send()`, which emits a live event, prints a colored line, and waits ~1.4s so the message visibly travels.
- **`message.py`**: `Message` dataclass (`sender`, `to`, `type`, `content`, `id`).
- **`events.py`**: Thread-safe event list for the live stream.
- **`server.py`**: Standard library HTTP server that serves `dashboard.html`, streams events over Server-Sent Events at `/events`, and starts a run on `POST /run`.
- **`dashboard.html`**: 3D dashboard with dark and beige themes (toggle with the button or the `T` key).
- **`main.py`**: Wires everything together, starts the server on port 8000, and opens the browser.

---

## Quick Start

1. Put all files in one folder.
2. Run:
   ```bash
   python main.py
   ```
3. The browser opens at `http://localhost:8000`. Click "Run agents".
4. Optional: set `ANTHROPIC_API_KEY` to use real Claude responses. Without it, the demo runs offline with fixed texts.

---

## Optional: Using a Real Claude API Key

The demo runs completely offline out of the box using fixed fallback texts.

To generate live responses with Claude:

**macOS / Linux:**
```bash
export ANTHROPIC_API_KEY="your-api-key"
python main.py
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="your-api-key"
python main.py
```

**Windows (CMD):**
```cmd
set ANTHROPIC_API_KEY=your-api-key
python main.py
```

When set, `base_agent.py` calls Anthropic's Claude API (`claude-sonnet-4-6`) via `urllib` in Python's standard library. If the key is not set or the request encounters an error, the demo uses an offline fallback so it never fails.

---

## Notes

- **Internet connection**: The dashboard needs internet for the 3D libraries and fonts (CDN).
- **Rule-based reviewer**: The reviewer is rule-based (rejects drafts without a concrete example), so the run is predictable.
- **Custom port**: To change the port, edit `PORT` in `main.py`.

---

## Ideas to Extend It

- **Add a new agent**: Add an editor, translator, or fact-checker to the pipeline.
- **Add tools**: Give agents capabilities to call APIs, search the web, or read local files.
- **Run agents in parallel**: Run multiple researcher agents simultaneously and merge their outputs.

---

## License

MIT
