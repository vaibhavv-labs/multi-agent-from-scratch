from dataclasses import dataclass, field
import uuid


@dataclass
class Message:
    sender: str
    to: str
    type: str
    content: dict
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:6])
