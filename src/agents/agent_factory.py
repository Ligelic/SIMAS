from typing import Dict, List, Optional
from .agent import Agent, Personality
from .llm_agent import LLMAgent
from utils.llm_service import LLMService
import json

class AgentFactory:
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.llm_service = LLMService()

    def _generate_agent_description(self, index: int, total: int, name: List[str]) -> dict:
        prompt = f"""Generate a description in English for an AI agent that will participate in a group discussion to solve math problems.
This is agent {index} of {total} total agents.

Existing agent names: {name}

Please provide the following in JSON format:
1. name: A simple name for the agent (unique from existing agents)
2. personality: One of [FRIENDLY, SKEPTICAL, NEUTRAL, AGGRESSIVE]
3. description: A brief description in English of the agent's characteristics and role in discussions
4. expertise: The agent's main strength in mathematical problem solving
5. beliefs: List of 3-5 beliefs relevant to mathematical problem solving that this agent holds

Example output:
{{
    "name": "Alice",
    "personality": "FRIENDLY",
    "description": "A warm and friendly assistant who excels at explaining complex concepts through diagrams",
    "expertise": "visualization and explanation",
    "beliefs": [
        "Clear visualization aids understanding",
        "Multiple approaches should be considered",
        "Collaboration improves problem solving"
    ]
}}

Remember to generate descriptions in English.
Make sure each agent has unique beliefs that align with their role and expertise."""

        response = self.llm_service.get_response(prompt)
        try:
            return json.loads(response)
        except:
            return {
                "name": f"Agent_{index}",
                "personality": "NEUTRAL",
                "description": f"第{index}号数学讨论者，擅长逻辑分析",
                "expertise": "logical analysis",
                "beliefs": [
                    "Systematic approach leads to solutions",
                    "Every problem has a logical structure",
                    "Mathematical rigor is essential"
                ]
            }

    def create_agent(self, name: str, personality: Personality, description: str, belief_thoughts: List[str] = None) -> Agent:
        if name in self.agents:
            raise ValueError(f"Agent '{name}' already exists")
            
        agent = LLMAgent(
            name=name, 
            personality=personality, 
            description=description,
            belief_thoughts=belief_thoughts
        )
        self.agents[name] = agent
        return agent

    def create_agents(self, count: int) -> List[Agent]:
        """Dynamically create a specified number of agents using LLM"""
        agents = []
        names = []
        personalities = {
            "FRIENDLY": Personality.FRIENDLY,
            "SKEPTICAL": Personality.SKEPTICAL,
            "NEUTRAL": Personality.NEUTRAL,
            "AGGRESSIVE": Personality.AGGRESSIVE
        }

        for i in range(count):
            # print(f"\nGenerating agent {i + 1} of {count}...")
            agent_info = self._generate_agent_description(i + 1, count, names)
            if agent_info["name"] not in names:
                names.append(agent_info["name"])
            # Ensure unique name
            while agent_info["name"] in self.agents:
                print(f"Agent name '{agent_info['name']}' already exists. Please provide a unique name.")
                agent_info = self._generate_agent_description(i + 1, count, names)
            
            agent = self.create_agent(
                name=agent_info["name"],
                personality=personalities[agent_info["personality"]],
                description=f"{agent_info['description']} (专长：{agent_info['expertise']})",
                belief_thoughts=agent_info.get("beliefs", [])
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