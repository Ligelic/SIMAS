def test_chat_room_initialization():
    from src.chat.chat_room import ChatRoom
    chat_room = ChatRoom()
    assert chat_room.agents == []
    assert chat_room.messages == []

def test_chat_room_add_agent():
    from src.chat.chat_room import ChatRoom
    from src.agents.agent import Agent

    chat_room = ChatRoom()
    agent = Agent(name="Agent1")
    chat_room.add_agent(agent)

    assert len(chat_room.agents) == 1
    assert chat_room.agents[0].name == "Agent1"

def test_chat_room_broadcast_message():
    from src.chat.chat_room import ChatRoom
    from src.agents.agent import Agent
    from src.chat.message import Message

    chat_room = ChatRoom()
    agent1 = Agent(name="Agent1")
    agent2 = Agent(name="Agent2")
    chat_room.add_agent(agent1)
    chat_room.add_agent(agent2)

    message = Message(sender=agent1.name, content="Hello, everyone!")
    chat_room.broadcast_message(message)

    assert len(chat_room.messages) == 1
    assert chat_room.messages[0].content == "Hello, everyone!"
    assert chat_room.messages[0].sender == "Agent1"

def test_chat_manager_initialization():
    from src.chat.chat_manager import ChatManager
    chat_manager = ChatManager()
    assert chat_manager.chat_rooms == []

def test_chat_manager_create_chat_room():
    from src.chat.chat_manager import ChatManager
    from src.chat.chat_room import ChatRoom

    chat_manager = ChatManager()
    chat_manager.create_chat_room("Room1")

    assert len(chat_manager.chat_rooms) == 1
    assert chat_manager.chat_rooms[0].name == "Room1"