import pytest
from src.agents.agent import Agent, Personality
from src.chat.message import Message

def test_agent_send_receive():
    # Create an agent
    agent = Agent(name="Agent1")

    # Create a message
    message_content = "Hello, this is a test message."
    message = Message(sender=agent.name, content=message_content)

    # Send the message
    agent.send_message(message)

    # Check if the message was received
    received_messages = agent.received_messages
    assert len(received_messages) == 1
    assert received_messages[0].content == message_content
    assert received_messages[0].sender == agent.name

def test_agent_initialization():
    agent = Agent(
        name="TestAgent",
        personality=Personality.FRIENDLY,
        description="A test agent"
    )
    assert agent.name == "TestAgent"
    assert agent.personality == Personality.FRIENDLY
    assert agent.description == "A test agent"
    assert len(agent.beliefs) == 0
    assert len(agent.relationships) == 0

def test_agent_belief_update():
    agent = Agent(
        name="TestAgent",
        personality=Personality.FRIENDLY,
        description="A test agent"
    )
    agent.update_belief("test thought", 0.5)
    assert "test thought" in agent.beliefs
    assert agent.beliefs["test thought"].confidence == 0.5

def test_agent_relationship_update():
    agent = Agent(
        name="TestAgent",
        personality=Personality.FRIENDLY,
        description="A test agent"
    )
    agent.update_relationship("other_agent", 0.3)
    assert "other_agent" in agent.relationships
    assert agent.relationships["other_agent"].score == 0.3

def test_agent_factory_creation():
    from src.agents.agent_factory import AgentFactory

    # Create an agent using the factory
    factory = AgentFactory()
    agent = factory.create_agent(name="Agent3")

    # Check agent properties
    assert agent.name == "Agent3"
    assert agent.received_messages == []  # Should start with an empty message list