from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Message:
    sender: Optional['Agent']  # Make sender optional to support system messages
    content: str
    chat_room: Optional['ChatRoom'] = None
    timestamp: datetime = field(default_factory=datetime.now)
    sentiment: float = 0.0  # Range -1 to 1
    reply_to: Optional['Message'] = None
    metadata: dict = field(default_factory=dict)

    def __str__(self):
        sender_name = self.sender.name if self.sender else "SYSTEM"
        return f"[{self.timestamp}] {sender_name}: {self.content}"