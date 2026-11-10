from base_agent import Agent


class Writer(Agent):
    name = "writer"

    def __init__(self, bus):
        super().__init__(bus)
        self.facts, self.version = [], 0

    async def handle(self, msg):
        if msg.type == "task":
            self.facts, self.version = msg.content["facts"], 1
            self.think("drafting v1")
            fb = ("AI agents are changing how teams work. They can research, write and review "
                  "on their own. Exciting times ahead for everyone! #AI #Agents")
            draft = await self.llm("Write a short, general LinkedIn post (under 60 words, no examples) using these facts:\n"
                                   + "\n".join(self.facts), fb)
        else:  # feedback
            self.version += 1
            self.think(f"revising → v{self.version}")
            fb = ("AI agents work best as a team, not a lone genius. For example, one agent gathers facts, "
                  "another drafts the post, and a third reviews it before anything ships. "
                  "Each hands off structured messages, which is why the work gets done in minutes. "
                  "#AI #Agents")
            draft = await self.llm(f"Revise this LinkedIn post (under 80 words). Feedback: {msg.content['feedback']}\n"
                                   f"Include the words 'For example'.\n\nPost:\n{msg.content['draft']}", fb)
        await self.send("reviewer", "draft", {"version": self.version, "draft": draft})
