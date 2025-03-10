import re
from typing import List, Dict
from datetime import datetime
from .message import Message

class ChatRoom:
    def __init__(self, name: str, round: int = 3):
        self.name = name
        self.agents = []
        self.messages: List[Message] = []
        self.created_at = datetime.now()
        self.metadata: Dict = {}
        self.current_round = 1  # Start from round 1
        self.max_rounds = round  # Default value
        self.is_completed = False  # Add flag to track completion status
        self.current_round_history = [f"" for i in range(self.max_rounds)]
        self.last_round_history = ''

    def add_agent(self, agent):
        if agent not in self.agents:
            self.agents.append(agent)
            self.broadcast_system_message(f"{agent.name} joined the chat room")
            # print(f"{agent.name} joined the chat room")
    
    def remove_agent(self, agent):
        if agent in self.agents:
            self.agents.remove(agent)
            self.broadcast_system_message(f"{agent.name} left the chat room")
    
    def _get_current_round_messages(self) -> List[Message]:
        """Get messages from current round only."""
        msgs = []
        message = Message(
            sender=self.agents[-1],
            content= self.messages[0].content + "\n" + self.current_round_history[self.current_round - 1],
            chat_room=self
        )
        msgs.append(message)
        return msgs
        # messages_per_round = len(self.agents)
        # start_index = (self.current_round - 1) * messages_per_round
        # end_index = start_index + messages_per_round  # Maximum possible index for this round
        # end_index = min(end_index, len(self.messages))  # Don't exceed actual messages
        
        # round_messages = []
        # for msg in self.messages[start_index:end_index]:
        #     if msg.sender in self.agents:
        #         round_messages.append(msg)
        # return round_messages

    def _get_last_round_messages(self) -> List[Message]:
        """Get all messages from the previous round."""
        if self.current_round <= 1:
            return []
        return self.current_round_history[self.current_round - 2]    
        # messages_per_round = len(self.agents)
        # start_index = (self.current_round - 2) * messages_per_round
        # end_index = (self.current_round - 1) * messages_per_round
        
        # round_messages = []
        # for msg in self.messages[start_index:end_index]:
        #     if msg.sender in self.agents:
        #         round_messages.append(msg)
        # return round_messages

    def broadcast_message(self, message):
        """Handle message broadcasting and round transitions."""
        if self.is_completed:
            return
            
        self.messages.append(message)
        self.current_round_history[self.current_round - 1] += message.sender.name + ": " + message.content + '\n'
        if message.sender in self.agents:
            current_index = self.agents.index(message.sender)
            next_index = current_index + 1
            
            if next_index < len(self.agents):
                # Within current round
                # round_messages = self._get_current_round_messages()
                # round_header = f"[Round {self.current_round}/{self.max_rounds}]"
                # content = self.format_round_messages(round_messages)
                round_header = f"[Round {self.current_round}/{self.max_rounds}]"
                if next_index == 0:
                    content = self.last_round_history
                else:
                    content = self.current_round_history[self.current_round - 1]
                self.send_direct_message(
                    sender=message.sender,
                    recipient=self.agents[next_index],
                    content=f"{round_header}\nPrevious messages in this round:\n{content}"
                )
                
            elif current_index == len(self.agents) - 1:
                # End of round
                if self.current_round < self.max_rounds:
                    self.last_round_history = self.current_round_history[self.current_round - 1]
                    self.current_round += 1
                    # print(f"\n=== Starting Round {self.current_round}/{self.max_rounds} ===")
                    round_header = (
                        f"[Round {self.current_round}/{self.max_rounds}]"
                        + (" - Final Round! Please provide your concluding thoughts."
                           if self.current_round == self.max_rounds else "")
                    )
                    
                    # last_round_messages = self._get_last_round_messages()
                    # content = self.format_round_messages(last_round_messages)
                    content = self.last_round_history
                    
                    self.send_direct_message(
                        sender=message.sender,
                        recipient=self.agents[0],
                        content=f"{round_header}\nPrevious round's messages:\n{content}"
                    )
                else:
                    # Handle final round completion
                    self.is_completed = True
                    # print(f"\n=== Discussion completed after {self.max_rounds} rounds ===")
                    # print("Requesting final summary from first agent...")
                    
                    final_messages = self._get_current_round_messages()
                    summary_request = Message(
                        sender=None,
                        content="Please provide a comprehensive summary of our discussion, "
                               "including the key points and conclusions from all participants.",
                        chat_room=self
                    )
                    final_answer = self.agents[0].receive_final_summary_request(summary_request, final_messages)
                    problem = self.metadata.get('current_problem')
                    if problem:
                        is_correct = self.metadata.get('problem_provider').record_answer(problem, final_answer)
                        # print(f"Answer {'correct' if is_correct else 'incorrect'} "
                        #     f"(Expected: {problem.answer})")
    
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

    def format_round_messages(self, messages: List[Message]) -> str:
        """Format messages with proper context."""
        formatted_messages = []
        seen_messages = set()  # Track unique messages
        
        for msg in messages:
            content = self._extract_core_content(msg.content)
            # Create unique identifier for message
            msg_key = f"{msg.sender.name}:{content}"
            
            if msg_key not in seen_messages:
                seen_messages.add(msg_key)
                formatted_messages.append(f"{msg.sender.name}: {content}")
        
        return "\n".join(formatted_messages)

    def _extract_core_content(self, content: str) -> str:
        """Extract core message content by removing headers and redundant info."""
        # Remove round headers
        content = re.sub(r'\[Round \d+/\d+\].*?\n', '', content)
        
        # Remove message history headers
        content = re.sub(r'Previous (?:round\'s )?messages in this round:\n', '', content)
        content = re.sub(r'Previous round\'s messages:\n', '', content)
        
        # Remove duplicate sender prefixes
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            # Remove repeated agent names at start of line
            line = re.sub(r'^(?:[A-Za-z]+: )+', '', line.strip())
            if line:
                cleaned_lines.append(line)
                
        return '\n'.join(cleaned_lines).strip()

    def _format_round_header(self) -> str:
        """Create consistent round header format."""
        final_round_suffix = (
            " - Final Round! Please provide your concluding thoughts."
            if self.current_round == self.max_rounds 
            else ""
        )
        return f"[Round {self.current_round}/{self.max_rounds}]{final_round_suffix}"