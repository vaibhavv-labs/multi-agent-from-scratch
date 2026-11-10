import asyncio
from base_agent import Agent


class Reviewer(Agent):
    name = "reviewer"

    async def handle(self, msg):
        draft = msg.content["draft"]
        self.think(f"reviewing v{msg.content['version']}")
        await asyncio.sleep(1.2)
        if "for example" not in draft.lower():
            await self.send("writer", "feedback",
                            {"feedback": "Too vague. Add a concrete example.", "draft": draft})
        else:
            await self.send("orchestrator", "approved", {"post": draft})
