import asyncio
import events

COLORS = {"orchestrator": 33, "researcher": 36, "writer": 35, "reviewer": 32}


class Bus:
    def __init__(self, names, delay=1.4):
        self.inbox = {n: asyncio.Queue() for n in names}
        self.delay = delay

    async def send(self, msg):
        events.emit("message", id=msg.id, sender=msg.sender, to=msg.to,
                    type=msg.type, content=msg.content)
        c = COLORS.get(msg.sender, 37)
        preview = str(msg.content)[:70].replace("\n", " ")
        print(f"\033[{c}m● {msg.sender:<12} → {msg.to:<12} [{msg.type}]\033[0m {preview}",
              flush=True)
        await asyncio.sleep(self.delay)          # the message "travels"
        await self.inbox[msg.to].put(msg)
