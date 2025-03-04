from typing import Dict, List, Optional
from .agent import Agent, Personality
from .llm_agent import LLMAgent
from utils.llm_service import LLMService
import json

class AgentFactory:
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.llm_service = LLMService()

    def _generate_agent_description(self, index: int, total: int) -> dict:
        prompt = f"""Generate a description for an AI agent that will participate in a group discussion to solve math problems.
This is agent {index} of {total} total agents.

Please provide the following in JSON format:
1. name: A simple name for the agent (unique from existing agents)
2. personality: One of [FRIENDLY, SKEPTICAL, NEUTRAL]
3. description: A brief description in Chinese of the agent's characteristics and role in discussions
4. expertise: The agent's main strength in mathematical problem solving

Example output:
{{
    "name": "Alice",
    "personality": "FRIENDLY",
    "description": "一个热情友好的助手，擅长通过图解方式解释复杂概念",
    "expertise": "visualization and explanation"
}}

Make sure each agent has a unique role and expertise that complements the others."""

        response = self.llm_service.get_response(prompt)
        try:
            return json.loads(response)
        except:
            return {
                "name": f"Agent_{index}",
                "personality": "NEUTRAL",
                "description": f"第{index}号数学讨论者，擅长逻辑分析",
                "expertise": "logical analysis"
            }

    def create_agent(self, name: str, personality: Personality, description: str) -> Agent:
        if name in self.agents:
            raise ValueError(f"Agent '{name}' already exists")
            
        agent = LLMAgent(name=name, personality=personality, description=description)
        self.agents[name] = agent
        return agent

    def create_agents(self, count: int) -> List[Agent]:
        """Dynamically create a specified number of agents using LLM"""
        agents = []
        personalities = {
            "FRIENDLY": Personality.FRIENDLY,
            "SKEPTICAL": Personality.SKEPTICAL,
            "NEUTRAL": Personality.NEUTRAL
        }

        for i in range(count):
            agent_info = self._generate_agent_description(i + 1, count)
            
            # Ensure unique name
            while agent_info["name"] in self.agents:
                agent_info = self._generate_agent_description(i + 1, count)
            
            agent = self.create_agent(
                name=agent_info["name"],
                personality=personalities[agent_info["personality"]],
                description=f"{agent_info['description']} (专长：{agent_info['expertise']})"
            )
            agents.append(agent)

        return agents

    def get_agent(self, name: str) -> Optional[Agent]:
        return self.agents.get(name)

    def list_agents(self) -> List[str]:
        return list(self.agents.keys())

    def clear_agents(self):
        """Clear all registered agents"""
        self.agents.clear()