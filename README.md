# README.md

# Multi-Agent Chat System

This project implements a multi-agent group chat functionality, allowing multiple agents to communicate with each other in a chat environment. The system is designed to be extensible and modular, making it easy to add new features and agents.

## Project Structure

```
multi-agent-chat
├── src
│   ├── agents
│   │   ├── agent.py          # Defines the Agent class for individual agents
│   │   ├── base_agent.py     # Base class for all agents
│   │   └── agent_factory.py   # Factory for creating agent instances
│   ├── chat
│   │   ├── chat_room.py      # Manages chat rooms and agent communication
│   │   ├── message.py        # Represents messages in the chat system
│   │   └── chat_manager.py    # Coordinates chat functionality
│   ├── config
│   │   └── config.py         # Configuration settings for the project
│   ├── utils
│   │   ├── logger.py         # Logging utility for the application
│   │   └── validators.py      # Validation functions for messages and configurations
│   └── main.py               # Entry point for the application
├── tests
│   ├── test_agent.py         # Unit tests for the Agent class
│   └── test_chat.py          # Unit tests for ChatRoom and ChatManager classes
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd multi-agent-chat
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To start the chat system, run the following command:
```
python src/main.py
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.