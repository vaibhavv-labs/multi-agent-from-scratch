import asyncio
import events
from base_agent import Agent


class Orchestrator(Agent):
    name = "orchestrator"
    busy = False

    async def handle(self, msg):
        if msg.type == "start":
            self.busy = True
            self.think("planning the run")
            await asyncio.sleep(0.8)
            await self.send("researcher", "task", {"topic": msg.content["topic"]})
        elif msg.type == "result":
            self.think("passing facts to the writer")
            await asyncio.sleep(0.8)
            await self.send("writer", "task", {"facts": msg.content["facts"],
                                               "brief": "Short LinkedIn post"})
        elif msg.type == "approved":
            post = msg.content["post"]
            print("\n\033[1;32m=== FINAL POST ===\033[0m\n" + post + "\n", flush=True)
            events.emit("final", post=post)
            self.busy = False
