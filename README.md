# Agents Talking

A live, visual demo showing how AI agents communicate with each other, built from scratch in plain Python with zero dependencies and a real-time 3D dashboard.

## Demo

https://github.com/vaibhavv-labs/multi-agent-from-scratch/raw/main/agent%20demo.mp4

<video src="agent%20demo.mp4" controls="controls" width="100%"></video>

> 📹 **Watch the demo video:** [`agent demo.mp4`](agent%20demo.mp4)  
> *(GIF placeholder: `![demo](demo.gif)`)*

---

## How It Works

At its core, an agent is just an inbox and a loop: it waits for a message, processes it, and sends a response.

In this project, each agent is an independent Python object with its own `asyncio.Queue` inbox. A shared message bus delivers messages between inboxes and introduces a brief pause so message delivery is visible. Every time a message is sent, the event is recorded and streamed over Server-Sent Events (SSE) to a 3D browser dashboard. The agents coordinate entirely through structured message passing without any external framework like CrewAI, LangGraph, or AutoGen.

---

## Message Flow

The demo runs a 7-step sequence between the four agents:

1. **orchestrator -> researcher** (`task`): The orchestrator receives "start" and sends the research topic.
2. **researcher -> orchestrator** (`result`): The researcher gathers 3 facts and returns them.
3. **orchestrator -> writer** (`task`): The orchestrator forwards the facts and brief to the writer.
4. **writer -> reviewer** (`draft`): The writer creates Draft v1 of a LinkedIn post.
5. **reviewer -> writer** (`feedback`): The reviewer rejects Draft v1 for lacking concrete examples and requests revisions.
6. **writer -> reviewer** (`draft`): The writer incorporates the feedback and submits Draft v2.
7. **reviewer -> orchestrator** (`approved`): The reviewer approves Draft v2, and the orchestrator prints the final post.

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
└── agent demo.mp4     # Demo recording of the live 3D dashboard run
```

### The 4 Agents
- **`orchestrator.py`**: Receives "start", sends a task to the researcher, forwards the researcher's facts to the writer, and on "approved" prints and emits the final post.
- **`researcher.py`**: Receives a task and returns 3 facts.
- **`writer.py`**: Drafts a short LinkedIn post, and revises it when it receives feedback.
- **`reviewer.py`**: Rejects vague drafts with feedback ("add a concrete example") and approves the revised version.

### Supporting Files
- **`base_agent.py`**: Agent base class with `send()`, `think()`, a run loop, and an `llm()` helper (calls the Anthropic API via `urllib` if `ANTHROPIC_API_KEY` is set, otherwise uses an offline fallback so the demo never fails).
- **`bus.py`**: Bus with one `asyncio.Queue` inbox per agent; every message goes through `bus.send()`, which emits a live event, prints a colored line in terminal, and waits ~1.4s so the message visibly travels.
- **`message.py`**: `Message` dataclass (`sender`, `to`, `type`, `content`, `id`).
- **`events.py`**: Thread-safe event list for the live event stream.
- **`server.py`**: Standard library HTTP server that serves `dashboard.html`, streams events over Server-Sent Events at `/events`, and starts a run on `POST /run`.
- **`dashboard.html`**: 3D dashboard (Three.js, loaded from CDN) with dark and beige themes (toggle with the button or the `T` key).
- **`main.py`**: Wires everything together, starts the server on port 8000, and opens the browser.

---

## Quick Start

1. Ensure Python 3.10+ is installed (no `pip install` required, uses standard library only).
2. Clone or download the repository files into a single directory.
3. Run the application:
   ```bash
   python main.py
   ```
4. The browser automatically opens at `http://localhost:8000`. Click **Run agents** (or press the button on the dashboard) to start the run.

---

## Optional: Using a Real Claude API Key

The demo runs completely offline out of the box using built-in fallback texts.

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

When set, `base_agent.py` calls Anthropic's Claude model (`claude-sonnet-4-6`) directly over HTTPS using Python's standard `urllib`. If the key is unset or an API call fails, the agent immediately falls back to local text so the run never crashes.

---

## Notes

- **Internet Access**: The 3D dashboard requires internet access to load Three.js and fonts from CDN.
- **Predictable Reviewer**: The reviewer is rule-based (rejects drafts that lack the phrase "for example"), ensuring a consistent two-step revision cycle every time.
- **Custom Port**: To change the default port (8000), edit `PORT` in `main.py`.

---

## Ideas to Extend It

- **Add a new agent**: Introduce a translator, fact-checker, or graphics prompt generator to the pipeline.
- **Add tools**: Give the researcher web search or file reading capabilities before returning facts.
- **Run agents in parallel**: Spawn multiple researchers or writers simultaneously and aggregate their responses.

---

## License

This project is licensed under the [MIT License](LICENSE).
