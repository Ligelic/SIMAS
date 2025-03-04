from typing import Dict, List, Optional
from .chat_room import ChatRoom
from utils.logger import log_message
from .message import Message

class ChatManager:
    def __init__(self):
        self.chat_rooms: Dict[str, ChatRoom] = {}
        
    def create_chat_room(self, room_name: str) -> ChatRoom:
        if room_name in self.chat_rooms:
            raise ValueError(f"Chat room '{room_name}' already exists")
        
        chat_room = ChatRoom(room_name)
        self.chat_rooms[room_name] = chat_room
        log_message(f"Created new chat room: {room_name}")
        return chat_room

    def get_chat_room(self, room_name: str) -> Optional[ChatRoom]:
        return self.chat_rooms.get(room_name)
    
    def remove_chat_room(self, room_name: str):
        if room_name in self.chat_rooms:
            del self.chat_rooms[room_name]
            log_message(f"Removed chat room: {room_name}")

    def send_message(self, room_name, sender, content):
        chat_room = self.get_chat_room(room_name)
        if chat_room:
            message = Message(
                sender=sender, 
                content=content,
                chat_room=chat_room
            )
            chat_room.broadcast_message(message)
        else:
            raise ValueError(f"Chat room '{room_name}' does not exist.")

    def list_chat_rooms(self):
        return list(self.chat_rooms.keys())