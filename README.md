Collecting workspace information`@workspace` accuracy and speed can be improved by building a remote workspace index. [Learn More](https://aka.ms/vscode-copilot-workspace-remote-index)

Build remote workspace index

# SIMAS: Smart Intelligent Multi-Agent System

A sophisticated multi-agent conversation framework designed for collaborative problem-solving across diverse domains including mathematics, knowledge reasoning, open-ended discussions, and code generation.

## Overview

SIMAS is a Python-based multi-agent system that leverages large language models (LLMs) to enable intelligent agents to collaborate, debate, and reach consensus on complex problems. The system supports multiple problem types and evaluation methodologies, making it suitable for academic research and practical applications.

## Key Features

- **Multi-Agent Collaboration**: Agents with distinct personalities, expertise, and beliefs engage in dynamic discussions
- **Multiple Problem Domains**: Support for MMLU, AIME2025, E-KAR, open-ended problems, and code challenges
- **Flexible Agent Modes**: 
  - `DEFAULT_MODE (0)`: Full agent characteristics
  - `NONE_ALL (1)`: Stripped of all characteristics
  - `NONE_PERSONALITY (2)`: Without personality
  - `NONE_EXPERTISE (3)`: Without expertise descriptions
  - `NONE_BELIEF (4)`: Without belief systems

- **Chain-of-Thought Reasoning**: Single-agent reasoning mode for baseline comparisons
- **Conversation Recording**: Detailed logging of all discussions with timestamps and metadata
- **Evaluation Framework**: Automatic answer evaluation and accuracy computation
- **Token Tracking**: Monitor LLM API usage and cost

## Project Structure

```
src/
├── agents/                          # Agent implementations
│   ├── agent.py                     # Base Agent class with personality & beliefs
│   ├── llm_agent.py                 # LLM-powered agent
│   ├── open_ended_llm_agent.py      # Specialized for open-ended problems
│   ├── code_llm_agent.py            # Specialized for code problems
│   ├── agent_factory.py             # Factory for agent creation
│   └── agent_generator.py           # Dynamic agent generation
├── chat/
│   ├── chat_manager.py              # Chat room management
│   ├── chat_room.py                 # Individual chat room logic
│   └── message.py                   # Message data structure
├── utils/
│   ├── problem_base.py              # Base problem provider interface
│   ├── mmlu_provider.py             # MMLU dataset provider
│   ├── aime25_provider.py           # AIME2025 dataset provider
│   ├── ekar_provider.py             # E-KAR knowledge reasoning provider
│   ├── open_ended_provider.py       # Open-ended problems provider
│   ├── code_provider.py             # Code problems provider
│   ├── open_ended_evaluator.py      # LLM-based evaluator for open-ended answers
│   ├── conversation_recorder.py     # Conversation history logging
│   ├── llm_service.py               # LLM API wrapper
│   ├── saver.py                     # Result persistence
│   └── visualizer.py                # Result visualization
├── config/
│   └── config.py                    # Global configuration
├── main.py                          # Multi-agent chat experiments
├── SingleAgent.py                   # Single-agent baseline experiments
├── Reasoning.py                     # Reasoning-focused experiments
├── open_ended_comparison.py         # CoT vs SIMAS on open-ended problems
└── code_comparison.py               # CoT vs SIMAS on code problems
```

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd SIMAS
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure LLM settings in config.py:
```python
LLM_MODEL = 'qwen2.5:72b-instruct'  # Your LLM model
API_BASE_URL = "http://localhost:11434/api/generate"  # Your API endpoint
```

## Quick Start

### Multi-Agent Chat Experiment

Run a multi-agent discussion on MMLU problems:

```bash
cd src
python main.py
```

Or with custom parameters:

```python
from main import main

main(
    max_rounds=3,           # Number of discussion rounds
    agent_count=3,          # Number of agents
    subject='college_physics',  # Problem subject
    problem_count=10,       # Number of problems
    experiment_count=3      # Number of experiments
)
```

### Single-Agent Baseline

Compare against single-agent performance:

```bash
cd src
python SingleAgent.py
```

### Reasoning-Focused Mode

Test agents in reasoning-intensive tasks:

```bash
cd src
python Reasoning.py
```

### Open-Ended Problem Comparison

Compare Chain-of-Thought (CoT) vs SIMAS on open-ended questions:

```bash
cd src
python open_ended_comparison.py --problems 15 --agents 3 --rounds 3
```

### Code Problem Comparison

Compare approaches on programming challenges:

```bash
cd src
python code_comparison.py --problems 5 --agents 3 --rounds 3
```

## Usage Examples

### Creating Agents

```python
from agents.agent_factory import AgentFactory
from agents.agent import Personality

factory = AgentFactory()

# Create multiple agents dynamically
agents = factory.create_agents(
    count=3,
    subject='college_physics',
    mode=0  # DEFAULT_MODE
)

# Or create a single agent manually
from agents.llm_agent import LLMAgent

agent = factory.create_agent(
    name="Alice",
    personality=Personality.FRIENDLY,
    description="An expert in physics with strong analytical skills",
    belief_thoughts=["Physics is fundamental to understanding nature"]
)
```

### Loading Problems

```python
from utils.mmlu_provider import MMLUProblemProvider
from utils.aime25_provider import AIME2025ProblemProvider

# MMLU problems
mmlu_provider = MMLUProblemProvider(
    subject='abstract_algebra',
    total_problems=10
)

# AIME2025 problems
aime_provider = AIME2025ProblemProvider(
    data_path="aime25/test.jsonl",
    total_problems=10
)

# Get problems
problem = mmlu_provider.get_next_problem()
print(problem.question)
print(problem.answer)
```

### Running a Chat Session

```python
from chat.chat_manager import ChatManager

chat_manager = ChatManager()

# Create a chat room
chat_room = chat_manager.create_chat_room(
    room_name="Physics_Discussion_1",
    max_round=3
)

# Add agents
for agent in agents:
    chat_room.add_agent(agent)

# Send initial problem
chat_manager.send_message(
    room_name="Physics_Discussion_1",
    sender=agents[0],
    content="Let's solve this physics problem together..."
)
```

### Saving Results

```python
from utils.saver import save_evaluation_result

save_evaluation_result(
    subject='college_physics',
    agent_count=3,
    max_rounds=3,
    problem_provider=provider,
    model='qwen2.5:72b-instruct',
    mode='Multi-Agent-Chat',
    agent_mode=0,
    metadata={
        'experiment_count': 3,
        'average_accuracy': 0.85,
        'std_deviation': 0.05
    }
)
```

## Configuration

Edit config.py to customize:

```python
# LLM Configuration
LLM_MODEL = 'qwen2.5:72b-instruct'
API_BASE_URL = "http://localhost:11434/api/generate"

# Problem Settings
DEFAULT_MMLU_SUBJECT = 'college_physics'
TOTAL_PROBLEMS_TO_LOAD = 10
PROBLEMS_PER_CHAT = 1

# Chat Parameters
CHAT_ROOM_PARAMETERS = {
    'max_agents': 10,
    'max_message_length': 256,
    'timeout': 300,
}

# Agent Modes
DEFAULT_MODE = 0              # Full characteristics
NONE_ALL = 1                  # No characteristics
NONE_PERSONALITY = 2          # No personality
NONE_EXPERTISE = 3            # No expertise
NONE_BELIEF = 4               # No beliefs
```

## Supported Datasets

| Dataset | Provider | Type | Status |
|---------|----------|------|--------|
| MMLU | `MMLUProblemProvider` | Multiple Choice | ✅ |
| AIME2025 | `AIME2025ProblemProvider` | Short Answer | ✅ |
| E-KAR | `EKARProblemProvider` | Analogies | ✅ |
| Open-Ended | `OpenEndedProblemProvider` | Free Form | ✅ |
| Code | `CodeProblemProvider` | Programming | ✅ |

## Agent Personality Types

```python
from agents.agent import Personality

Personality.FRIENDLY    # Collaborative and supportive
Personality.NEUTRAL     # Objective and balanced
Personality.SKEPTICAL   # Critical and questioning
Personality.AGGRESSIVE  # Competitive and assertive
```

## Results and Output

Experiment results are saved to `evaluate_result/<subject>/` with:
- Accuracy metrics
- Token usage statistics
- Agent mode information
- Problem metadata
- Conversation logs

Visualizations are generated in figures:

```bash
python src/utils/visualizer.py
```

## Key Components

### Agent System

- **Personality**: Defines communication style and interaction patterns
- **Beliefs**: Internal knowledge with confidence scores
- **Relationships**: Dynamic trust/rapport between agents
- **Expertise**: Domain-specific knowledge description

### Problem Providers

All providers inherit from `ProblemProvider` and implement:
- `get_next_problem()`: Retrieve next problem
- `evaluate_answer()`: Check answer correctness
- `get_accuracy()`: Compute current accuracy
- `record_answer()`: Log agent response

### Chat Management

The `ChatManager` orchestrates:
- Room creation and lifecycle
- Message broadcasting
- Round management
- Metadata tracking

## Performance Metrics

Track the following metrics:
- **Accuracy**: Percentage of correct answers
- **Token Efficiency**: Tokens used per problem
- **Agreement Rate**: How often agents reach consensus
- **Discussion Quality**: Length and depth of conversations

## Advanced Features

### Custom Evaluation

Implement custom evaluators for domain-specific assessment:

```python
from utils.open_ended_evaluator import OpenEndedEvaluator

evaluator = OpenEndedEvaluator(model="gpt-4")
result = evaluator.compare_answers(
    problem="Discuss climate change",
    answer_a=cot_response,
    answer_b=simas_response,
    criteria=["depth", "accuracy", "clarity"]
)
```

### Conversation Recording

Automatic recording of all conversations:

```python
from utils.conversation_recorder import ConversationRecorder

recorder = ConversationRecorder(experiment_type="comparison")
recorder.record_mas_conversation(
    problem_id="p001",
    problem=problem.question,
    chat_room=chat_room
)
recorder.save_conversations()
```

## Testing

Run the test suite:

```bash
cd tests
python -m pytest
```

## Performance Tips

1. **Parallel Experiments**: Run multiple experiments concurrently
2. **Batch Processing**: Process multiple problems in sequence
3. **Cache Results**: Save intermediate results to avoid re-computation
4. **Model Selection**: Use smaller models for rapid prototyping
5. **Token Optimization**: Set appropriate context windows

## Troubleshooting

### LLM Connection Issues

```bash
# Verify API connectivity
curl http://localhost:11434/api/generate
```

### Dataset Loading Problems

```python
# Check data path configuration
import os
print(os.path.exists("aime25/test.jsonl"))
```

### Memory Issues

Reduce `problem_count` or `agent_count` in experiments

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Submit a pull request


## Acknowledgments

- Built with Python and cutting-edge LLM APIs
- Inspired by research in multi-agent systems and collaborative AI
- Dataset credits: MMLU, AIME, E-KAR communities

## Contact & Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: [jialingli22@m.fudan.edu.cn]

**Last Updated**: 2026.1.2  
**Version**: 1.0.0