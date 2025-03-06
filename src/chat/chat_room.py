from typing import List, Dict
from datetime import datetime
from .message import Message

class ChatRoom:
    def __init__(self, name: str):
        self.name = name
        self.agents = []
        self.messages: List[Message] = []
        self.created_at = datetime.now()
        self.metadata: Dict = {}
        self.current_round = 1  # Start from round 1
        self.max_rounds = 3  # Default value
        self.is_completed = False  # Add flag to track completion status

    def add_agent(self, agent):
        if agent not in self.agents:
            self.agents.append(agent)
            self.broadcast_system_message(f"{agent.name} joined the chat room")
    
    def remove_agent(self, agent):
        if agent in self.agents:
            self.agents.remove(agent)
            self.broadcast_system_message(f"{agent.name} left the chat room")
    
    def broadcast_message(self, message):
        if self.is_completed:
            return
            
        self.messages.append(message)
        
        if message.sender in self.agents:
            current_index = self.agents.index(message.sender)
            next_index = current_index + 1
            
            if next_index < len(self.agents):
                # Combine previous messages in this round with current message
                round_start_index = len(self.messages) - current_index - 1
                round_messages = self.messages[max(0, round_start_index):]
                combined_content = "\n".join([
                    f"{msg.sender.name}: {msg.content}" 
                    for msg in round_messages
                ])
                
                # Add round information to message
                round_info = (
                    f"[Round {self.current_round}/{self.max_rounds}]"
                    f"{' - Final Round! Please provide your concluding thoughts.' if self.current_round == self.max_rounds else ''}"
                )
                combined_content = combined_content.removeprefix(f"\n{round_info}\nPrevious messages in this round:\n")
                # Send combined messages to next agent
                next_agent = self.agents[next_index]
                self.send_direct_message(
                    sender=message.sender,
                    recipient=next_agent,
                    content=f"\n{round_info}\nPrevious messages in this round:\n{combined_content}"
                )
            
            # If this was the last agent in the round
            elif current_index == len(self.agents) - 1:
                if self.current_round < self.max_rounds:
                    self.current_round += 1
                    # Start new round
                    if self.current_round == self.max_rounds:
                        print(f"\n=== Starting Final Round {self.max_rounds}/{self.max_rounds} ===")
                    else:
                        print(f"\n=== Starting Round {self.current_round}/{self.max_rounds} ===")
                    
                    # Send last round's messages to first agent
                    round_messages = self.messages[-len(self.agents):]
                    combined_content = "\n".join([
                        f"{msg.sender.name}: {msg.content}" 
                        for msg in round_messages
                    ])
                    
                    round_info = (
                        f"[Round {self.current_round}/{self.max_rounds}]"
                        f"{' - Final Round! Please provide your concluding thoughts.' if self.current_round == self.max_rounds else ''}"
                    )
                    
                    self.send_direct_message(
                        sender=message.sender,
                        recipient=self.agents[0],
                        content=f"{round_info}\nPrevious round's messages:\n{combined_content}"
                    )
                else:
                    # Final round completed
                    self.is_completed = True
                    print(f"\n=== Discussion completed after {self.max_rounds} rounds ===")
                    print("Requesting final summary from first agent...")
                    
                    final_round_messages = self.messages[-len(self.agents):]
                    summary_request = Message(
                        sender=None,
                        content="Please provide a comprehensive summary of our discussion, "
                               "including the key points and conclusions from all participants.",
                        chat_room=self
                    )
                    self.agents[0].receive_final_summary_request(summary_request, final_round_messages)
    
    def broadcast_system_message(self, content: str):
        message = Message(sender=None, content=content)
        for agent in self.agents:
            agent.receive_message(message)

    def send_direct_message(self, sender, recipient, content: str):
        message = Message(
            sender=sender,
            content=content,
            chat_room=self
        )
        self.messages.append(message)
        recipient.receive_message(message)