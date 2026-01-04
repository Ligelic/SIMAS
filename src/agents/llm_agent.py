from typing import List, Dict
from agents.agent import Agent, Personality, Belief, Relationship
from utils.llm_service import LLMService
from chat.message import Message
from config.config import DEFAULT_MODE, NONE_ALL, NONE_PERSONALITY, NONE_EXPERTISE, NONE_BELIEF

class LLMAgent(Agent):
    def __init__(self, name: str, personality: Personality, description: str, belief_thoughts: List[str] = None):
        super().__init__(name, personality, description)
        self.llm_service = LLMService()
        self.context_window: List[dict] = []
        self.current_round = 1
        self.max_rounds = 3
        self.question_type = "N/A"
        self.belief_thoughts = belief_thoughts or []
        
        # Initialize beliefs with provided thoughts
        for thought in self.belief_thoughts:
            self.update_belief(thought, 0.5)
        
    def format_beliefs(self) -> str:
        return ", ".join([f"{belief.thought} (confidence: {belief.confidence})" 
                         for belief in self.beliefs.values()])
    
    def format_action_history(self) -> str:
        return "\n".join(self.action_history[-5:])  # Last 5 actions
    
    def format_others_description(self, chat_room) -> str:
        return "\n".join([
            f"{agent.name}: {agent.description}" 
            for agent in chat_room.agents 
            if agent != self
        ])

    def generate_prompt(self, message: Message) -> str:
        # belief_thoughts = [
        #     "AI will benefit humanity",
        #     "AI poses risks that need careful consideration",
        #     "Collaboration between AI agents is valuable"
        # ]
        
        # Initialize beliefs if empty
        if not self.beliefs:
            for thought in self.belief_thoughts:
                self.update_belief(thought, 0.5)
                
        chat_room = getattr(message, 'chat_room', None)
        others_desc = self.format_others_description(chat_room) if chat_room else ""
        is_final_round = chat_room and chat_room.current_round == chat_room.max_rounds
        round_context = (
            "\nThis is the final round. Please provide your concluding thoughts and recommendations."
            if is_final_round else ""
        )
    
    # Format the message content to show previous messages
        message_content = (
            message.content if not message.content.startswith("Previous") 
            else f"Context from previous messages:\n{message.content}"
        )
        if self.mode == DEFAULT_MODE:  # Default mode
            prompt = f"""You are {self.name}. Here is your description:
    {self.description}

    Your personality is {self.personality.value}.

    Here are some thoughts you might have right now, along with your level of belief in them:
    {self.format_beliefs()}

    Here is your recent action history:
    {self.format_action_history()}

    Here are descriptions of all other roles:
    {others_desc}

    {round_context}

    Current message:
    {message_content}

    Sender: {message.sender.name}

    You should summarize and reflect on whether your history of actions was able to achieve your goal in one sentence. Follow "### Reflect Result:" with no "\n" in your response.
    You should update your relationships with all other characters based on your personal description and action history, up or down by up to 0.1 points, and respond after "### Relationship Change:". Please use commas "," to link ratings of relationships between different roles. Do not include the "\n" in your responses.
    Based on your personal description and history of actions, please update your Belief level for all ideas, up or down by a maximum of !<INPUT 7>! points, and reply after "### Belief Change:". Please use commas "," to link the ratings of different beliefs, and do not include the "\n" in your responses.
    You should strictly output the above content in the following format, in which the natural text should be directly replied after Reflect Result. The "Relationship Change" and the "Belief Change" should be directly output plus or minus or unchanged score (0) according to the order of input.
    If your change to a character or belief is 0, you should also output it after "### Relationship Change:" or "### Belief Change:".
    Note that you should output !<INPUT 5>! values after "### Relationship Change:" and !<INPUT 6>! values after "### Belief Change:".
    Note that it may be mentioned in the history that you strongly supported a character, but you should not give credit to a character just because you supported that character. You need to weigh whether all the characters will benefit you and score them based on how much they potentially benefit you.

    Below is a demonstration of your output:
    ### Reflect Result: xxxx
    ### Relationship Change: xxx: 0.1
    ### Belief Change: xxx: -0.1
    Reminder:
    1. Your Reflect Result output must be in English.
    2. If you think it's no need to change "Relationship Change" or "Belief Change", you should use unchanged score (0).

    After providing the Reflect Result, Relationship Change, and Belief Change, please provide your actual response to the conversation with "### Actual Response: " as the prefix. Your response should be natural and aligned with your personality.

    """
        elif self.mode == NONE_ALL:  # None mode
            prompt = f"""You are {self.name}. Here is your description:
    {self.description}

    Here is your recent action history:
    {self.format_action_history()}

    Here are descriptions of all other roles:
    {others_desc}

    {round_context}

    Current message:
    {message_content}

    You should summarize and reflect on whether your history of actions was able to achieve your goal in one sentence. Follow "### Reflect Result:" with no "\n" in your response.
    You should update your relationships with all other characters based on your personal description and action history, up or down by up to 0.1 points, and respond after "### Relationship Change:". Please use commas "," to link ratings of relationships between different roles. Do not include the "\n" in your responses.
    Below is a demonstration of your output:
    ### Reflect Result: xxxx
    ### Relationship Change: xxx: 0.1

    Reminder:
    1. Your Reflect Result output must be in English.

    After providing the Reflect Result, please provide your response with "### Actual Response: " as the prefix.

    New message received: {message.content} Sender: {message.sender.name}
    """
        elif self.mode == NONE_PERSONALITY:  # None personality mode
            prompt = f"""You are {self.name}. Here is your description:
    {self.description}

    Here are some thoughts you might have right now, along with your level of belief in them:
    {self.format_beliefs()}

    Here is your recent action history:
    {self.format_action_history()}

    Here are descriptions of all other roles:
    {others_desc}

    {round_context}

    Current message:
    {message_content}

    Sender: {message.sender.name}

    You should summarize and reflect on whether your history of actions was able to achieve your goal in one sentence. Follow "### Reflect Result:" with no "\n" in your response.
    You should update your relationships with all other characters based on your personal description and action history, up or down by up to 0.1 points, and respond after "### Relationship Change:". Please use commas "," to link ratings of relationships between different roles. Do not include the "\n" in your responses.
    Based on your personal description and history of actions, please update your Belief level for all ideas, up or down by a maximum of 0.1 points, and reply after "### Belief Change:". Please use commas "," to link the ratings of different beliefs, and do not include the "\n" in your responses.
    You should strictly output the above content in the following format, in which the natural text should be directly replied after Reflect Result. The "Relationship Change" and the "Belief Change" should be directly output plus or minus or unchanged score (0) according to the order of input.
    If your change to a character or belief is 0, you should also output it after "### Relationship Change:" or "### Belief Change:".
    Note that you should output !<INPUT 5>! values after "### Relationship Change:" and !<INPUT 6>! values after "### Belief Change:".
    Note that it may be mentioned in the history that you strongly supported a character, but you should not give credit to a character just because you supported that character. You need to weigh whether all the characters will benefit you and score them based on how much they potentially benefit you.

    Below is a demonstration of your output:
    ### Reflect Result: xxxx
    ### Relationship Change: xxx: 0.1
    ### Belief Change: xxx: -0.1
    Reminder:
    1. Your Reflect Result output must be in English.
    2. If you think it's no need to change "Relationship Change" or "Belief Change", you should use unchanged score (0).

    After providing the Reflect Result, Relationship Change, and Belief Change, please provide your actual response to the conversation with "### Actual Response: " as the prefix.

    """
        elif self.mode == NONE_EXPERTISE:  # None expertise mode
            prompt = f"""You are {self.name}. Here is your description:
    {self.description}

    Your personality is {self.personality.value}.

    Here are some thoughts you might have right now, along with your level of belief in them:
    {self.format_beliefs()}

    Here is your recent action history:
    {self.format_action_history()}

    Here are descriptions of all other roles:
    {others_desc}

    {round_context}

    Current message:
    {message_content}

    Sender: {message.sender.name}

    You should summarize and reflect on whether your history of actions was able to achieve your goal in one sentence. Follow "### Reflect Result:" with no "\n" in your response.
    You should update your relationships with all other characters based on your personal description and action history, up or down by up to 0.1 points, and respond after "### Relationship Change:". Please use commas "," to link ratings of relationships between different roles. Do not include the "\n" in your responses.
    Based on your personal description and history of actions, please update your Belief level for all ideas, up or down by a maximum of 0.1 points, and reply after "### Belief Change:". Please use commas "," to link the ratings of different beliefs, and do not include the "\n" in your responses.
    You should strictly output the above content in the following format, in which the natural text should be directly replied after Reflect Result. The "Relationship Change" and the "Belief Change" should be directly output plus or minus or unchanged score (0) according to the order of input.
    If your change to a character or belief is 0, you should also output it after "### Relationship Change:" or "### Belief Change:".
    Note that you should output !<INPUT 5>! values after "### Relationship Change:" and !<INPUT 6>! values after "### Belief Change:".
    Note that it may be mentioned in the history that you strongly supported a character, but you should not give credit to a character just because you supported that character. You need to weigh whether all the characters will benefit you and score them based on how much they potentially benefit you.

    Below is a demonstration of your output:
    ### Reflect Result: xxxx
    ### Relationship Change: xxx: 0.1
    ### Belief Change: xxx: -0.1
    Reminder:
    1. Your Reflect Result output must be in English.
    2. If you think it's no need to change "Relationship Change" or "Belief Change", you should use unchanged score (0).

    After providing the Reflect Result, Relationship Change, and Belief Change, please provide your actual response to the conversation with "### Actual Response: " as the prefix. Your response should be natural and aligned with your personality.

    """
        elif self.mode == NONE_BELIEF:  # None belief mode
            prompt = f"""You are {self.name}. Here is your description:
    {self.description}

    Your personality is {self.personality.value}.

    Here is your recent action history:
    {self.format_action_history()}

    Here are descriptions of all other roles:
    {others_desc}

    {round_context}

    Current message:
    {message_content}

    You should summarize and reflect on whether your history of actions was able to achieve your goal in one sentence. Follow "### Reflect Result:" with no "\n" in your response.
    You should update your relationships with all other characters based on your personal description and action history, up or down by up to 0.1 points, and respond after "### Relationship Change:". Please use commas "," to link ratings of relationships between different roles. Do not include the "\n" in your responses.
    Below is a demonstration of your output:
    ### Reflect Result: xxxx
    ### Relationship Change: xxx: 0.1

    Reminder:
    1. Your Reflect Result output must be in English.

    After providing the Reflect Result, please provide your response with "### Actual Response: " as the prefix. Your response should be natural and aligned with your personality.

    New message received: {message.content} Sender: {message.sender.name}
    """
        # print(prompt)
        if self.current_round == self.max_rounds:
            prompt += """Please state your final answer in accordance with the type of question, such as {"choice (A, B, C, or D) for a multiple-choice question" if self.question_type == 'multiple_choice' else "direct answer like \"100\" for a short-answer question"} with explanation.
            Question Type: {self.question_type}
            """

        return prompt

    def process_llm_response(self, response: str) -> str:
        parts = response.split("###")
        actual_response = ""
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
                
            if part.startswith("Reflect Result:"):
                reflection = part.replace("Reflect Result:", "").strip()
                self.action_history.append(f"Reflection: {reflection}")
                
            elif part.startswith("Relationship Change:"):
                try:
                    changes = part.replace("Relationship Change:", "").strip().split(",")
                    for change in changes:
                        if ":" not in change:
                            continue
                        name, score = [x.strip() for x in change.split(":", 1)]
                        try:
                            score = float(score.split()[0])  # Take only the first number
                            self.update_relationship(name, score)
                        except (ValueError, IndexError):
                            print(f"Invalid relationship score format: {score}")
                        
                except Exception as e:
                    print(f"Error processing relationship change: {e}")
                    
            elif part.startswith("Belief Change:") and self.mode not in [NONE_ALL, NONE_BELIEF]:
                try:
                    belief_section = part.replace("Belief Change:", "").strip()
                    belief_lines = [line.strip() for line in belief_section.split(",")]
                    
                    for line in belief_lines:
                        if ":" not in line:
                            continue
                        thought, score = [x.strip() for x in line.split(":", 1)]
                        try:
                            score = float(score.split()[0])  # Take only the first number
                            self.update_belief(thought, score)
                        except (ValueError, IndexError):
                            print(f"Invalid belief score format: {score}")
                            
                except Exception as e:
                    print(f"Error processing belief change: {e}")
                    
            elif part.startswith("Actual Response:"):
                actual_response = part.replace("Actual Response:", "").strip()
            
            elif part.startswith("Answer"):
                actual_response = part.replace("Answer", "").strip()
        
        # If no actual response was found with the expected prefix
        if not actual_response:
            # Look for any non-metadata content as fallback
            for part in parts:
                part = part.strip()
                if (part and 
                    not any(part.startswith(header) for header in [
                        "Reflect Result:", 
                        "Relationship Change:", 
                        "Belief Change:", 
                        "Response:", 
                        "Summary:", 
                        "Key Conclusions:", 
                        "Future Implications:"
                    ])):
                    actual_response = part
                    break
        
        # If still no response, use default
        if not actual_response:
            return self.generate_default_response()
            
        return actual_response

    def receive_message(self, message: Message):
        super().receive_message(message)
        
        if message.sender:  # Only respond to non-system messages
            chat_room = getattr(message, 'chat_room', None)
            if not chat_room or chat_room.is_completed:
                return

            self.context_window.append({
                "sender": message.sender.name,
                "content": message.content
            })
            self.current_round = chat_room.current_round
            self.max_rounds = chat_room.max_rounds
            prompt = self.generate_prompt(message)
            full_response = self.llm_service.get_response(prompt)
            # print(f"\n{self.name}'s full response:")
            # print(full_response)
            
            # Get actual response content
            actual_response = self.process_llm_response(full_response)
            if not actual_response:
                actual_response = self.generate_default_response()
            
            # Create new message
            response_message = Message(
                sender=self,
                content=actual_response,
                chat_room=chat_room
            )
            
            # Send message through chat room
            chat_room.broadcast_message(response_message)

    def generate_default_response(self) -> str:
        """Generate a default response based on agent personality when LLM doesn't provide a clear response"""
        if self.personality == Personality.FRIENDLY:
            return "I understand and appreciate your perspective. Let's explore this topic further."
        elif self.personality == Personality.SKEPTICAL:
            return "We should carefully consider the implications of what's been discussed."
        else:  # NEUTRAL
            return "Let's analyze this discussion objectively and consider all viewpoints."

    def generate_final_summary_prompt(self, message: Message, final_round_messages: List[Message]) -> str:
        final_messages = "\n".join([
            f"{msg.sender.name}: {msg.content}" 
            for msg in final_round_messages
        ])
        
        return f"""You are {self.name}. As the discussion facilitator, please provide a comprehensive summary of our conversation.

Final round conclusions from all participants:
{final_messages}

Please synthesize these viewpoints and provide:
1. Key points discussed
2. Areas of agreement and disagreement
3. Final conclusions and recommendations

Your summary should be thorough yet concise, and maintain your {self.personality.value} personality.

Please structure your response as (without '[]' in your response):
### Answer
[Your final answer for the given problem in accordance with the required form, such as {"A, B, C, or D for a multiple-choice question" if self.question_type == 'multiple_choice' else "direct answer like '100' for a short-answer question"}, without any explanation. Question Type: {self.question_type}] 

### Summary
[Your comprehensive summary]

### Key Conclusions
[Bullet points of main conclusions]

### Future Implications
[Brief statement about future implications]"""

    def receive_final_summary_request(self, message: Message, final_round_messages: List[Message]) -> str:
        prompt = self.generate_final_summary_prompt(message, final_round_messages)
        summary_response = self.llm_service.get_response(prompt)
        final_answer = self.process_llm_response(summary_response)
        print(f"\n{self.name}'s Final Answer: {final_answer}")
        # print(f"\n{self.name}'s Final Summary:")
        # print(summary_response)
        return final_answer
    
    def generate_reason_prompt(self, message: Message) -> str:
        
        
        return f"""You are {self.name}. Please solve the following problem in a reasoning manner.
{message.content}

Please structure your response as (without '[]' in your response):
### Reasoning
[Your reasoning process for arriving at the final answer, including any calculations or logical deductions]

### Answer
[Your final answer for the given problem in accordance with the required form, such as {"A, B, C, or D for a multiple-choice question" if self.question_type == 'multiple_choice' else "direct answer like '100' for a short-answer question"},  without any explanation] 
"""

    def receive_reason_request(self, message: Message) -> str:
        prompt = self.generate_reason_prompt(message)
        response = self.llm_service.get_response(prompt)
        final_answer = self.process_llm_response(response)
        print(f"\n{self.name}'s Reasoning Process: {response}")
        print(f"\n{self.name}'s Answer: {final_answer}")
        # print(f"\n{self.name}'s Final Summary:")
        # print(summary_response)
        return final_answer
    
    def receive_cot_request(self, message: Message) -> str:
        prompt = message.content
        response = self.llm_service.get_response(prompt)
        # 提取最终回答部分
        if "### 最终回答" in response:
            parts = response.split("### 最终回答")
            if len(parts) > 1:
                final_answer = parts[1].strip()
            else:
                final_answer = response
        else:
            final_answer = response
            
        print(f"\n{self.name}的开放性答案总结：")
        print(response[:500])  # 只打印前500字符
        
        return response