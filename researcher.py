from base_agent import Agent

FALLBACK = [
    "Teams using AI agents report cutting routine research time by roughly half.",
    "Multi-agent systems split work into roles, such as researcher, writer and reviewer.",
    "Agents coordinate by passing structured messages instead of sharing one giant prompt.",
]


class Researcher(Agent):
    name = "researcher"

    async def handle(self, msg):
        topic = msg.content["topic"]
        self.think(f"researching: {topic}")
        text = await self.llm(f"Give exactly 3 short, concrete facts about: {topic}. One per line, no numbering.",
                              "\n".join(FALLBACK))
        facts = [l.strip("-•* 0123456789.").strip() for l in text.splitlines() if l.strip()][:3]
        if len(facts) < 3:
            facts = FALLBACK
        await self.send("orchestrator", "result", {"topic": topic, "facts": facts})
