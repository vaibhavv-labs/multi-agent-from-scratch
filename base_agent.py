import asyncio, json, os, urllib.request
import events
from message import Message


class Agent:
    name = "agent"

    def __init__(self, bus):
        self.bus = bus
        self.inbox = bus.inbox[self.name]

    async def send(self, to, type, content):
        events.emit("idle", agent=self.name)
        await self.bus.send(Message(self.name, to, type, content))

    def think(self, text="thinking..."):
        events.emit("thinking", agent=self.name, text=text)

    async def llm(self, prompt, fallback):
        """Real Claude call if ANTHROPIC_API_KEY is set; otherwise (or on any error) the fallback."""
        key = os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            await asyncio.sleep(1.2)
            return fallback
        try:
            return await asyncio.to_thread(self._call_api, key, prompt)
        except Exception as e:
            print(f"(llm failed, using fallback: {e})")
            return fallback

    @staticmethod
    def _call_api(key, prompt):
        body = json.dumps({"model": "claude-sonnet-4-6", "max_tokens": 400,
                           "messages": [{"role": "user", "content": prompt}]}).encode()
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages", data=body,
            headers={"content-type": "application/json", "x-api-key": key,
                     "anthropic-version": "2023-06-01"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)["content"][0]["text"].strip()

    async def handle(self, msg):
        raise NotImplementedError

    async def run(self):
        while True:
            msg = await self.inbox.get()
            await self.handle(msg)
            events.emit("idle", agent=self.name)
