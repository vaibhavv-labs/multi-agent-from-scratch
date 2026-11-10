import asyncio, os, webbrowser
import events
from bus import Bus
from message import Message
from orchestrator import Orchestrator
from researcher import Researcher
from writer import Writer
from reviewer import Reviewer
from server import serve

PORT, TOPIC = 8000, "How AI agents work together"


async def main():
    names = ["orchestrator", "researcher", "writer", "reviewer"]
    bus = Bus(names)
    orch = Orchestrator(bus)
    agents = [orch, Researcher(bus), Writer(bus), Reviewer(bus)]
    loop = asyncio.get_running_loop()

    def start_run():
        if orch.busy:
            return False
        orch.busy = True
        events.emit("reset")
        loop.call_soon_threadsafe(bus.inbox["orchestrator"].put_nowait,
                                  Message("user", "orchestrator", "start", {"topic": TOPIC}))
        return True

    serve(start_run, PORT)
    print(f"Dashboard: http://localhost:{PORT}  (press 'Run agents')")
    if not os.environ.get("NO_BROWSER"):
        webbrowser.open(f"http://localhost:{PORT}")
    await asyncio.gather(*(a.run() for a in agents))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
