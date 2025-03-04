from typing import List
from .agent import Personality, Agent
from .llm_agent import LLMAgent
from utils.llm_service import LLMService

class AgentGenerator:
    def __init__(self):
        self.llm_service = LLMService()

    def generate_agent_description(self, index: int, total: int) -> dict:
        prompt = f"""Generate a description for an AI agent that will participate in a group discussion to solve math problems.
This is agent {index} of {total} total agents.

Please provide the following in JSON format:
1. name: A simple name for the agent
2. personality: One of [FRIENDLY, SKEPTICAL, NEUTRAL]
3. description: A brief description in Chinese of the agent's characteristics and role in discussions
4. expertise: The agent's main strength in mathematical problem solving

Example output:
{{
    "name": "Alice",
    "personality": "FRIENDLY",
    "description": "A warm and friendly assistant who excels at explaining complex concepts through diagrams.",
    "expertise": "visualization and explanation"
}}

Make sure each agent has a unique role and expertise that complements the others."""

        response = self.llm_service.get_response(prompt)
        try:
            import json
            return json.loads(response)
        except:
            # Fallback default agent if LLM fails
            return {
                "name": f"Agent_{index}",
                "personality": "NEUTRAL",
                "description": f"第{index}号数学讨论者，擅长逻辑分析",
                "expertise": "logical analysis"
            }

    def create_agents(self, count: int) -> List[LLMAgent]:
        agents = []
        personalities = {
            "FRIENDLY": Personality.FRIENDLY,
            "SKEPTICAL": Personality.SKEPTICAL,
            "NEUTRAL": Personality.NEUTRAL
        }

        for i in range(count):
            agent_info = self.generate_agent_description(i + 1, count)
            
            agent = LLMAgent(
                name=agent_info["name"],
                personality=personalities[agent_info["personality"]],
                description=f"{agent_info['description']} (专长：{agent_info['expertise']})"
            )
            agents.append(agent)

        return agents