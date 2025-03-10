from agents.agent_factory import AgentFactory
from chat.chat_manager import ChatManager
from utils.mmlu_provider import MMLUProblemProvider
from config.config import (
    DEFAULT_MMLU_SUBJECT, 
    TOTAL_PROBLEMS_TO_LOAD,
    PROBLEMS_PER_CHAT
)

def run_chat_session(
    chat_manager: ChatManager,
    agents: list,
    problem_provider: MMLUProblemProvider,
    max_rounds: int,
    session_num: int
) -> bool:
    """Run a single chat session for one problem. Returns True if successful."""
    
    # Get next problem
    problem = problem_provider.get_next_problem()
    if not problem:
        return False
        
    print(f"\n=== Starting Chat Session {session_num} ===")
    print(f"Remaining problems: {problem_provider.get_remaining_count()}")
    
    # Create new chat room for this session
    chat_room = chat_manager.create_chat_room(f"Session_{session_num}")
    chat_room.max_rounds = max_rounds
    
    # Add agents to room
    for agent in agents:
        chat_room.add_agent(agent)

    # Store problem for evaluation
    chat_room.metadata['current_problem'] = problem
    chat_room.metadata['problem_provider'] = problem_provider
    print(f"{problem.question}")
    # Start discussion with problem
    # print(f"\n=== Starting Round 1/{max_rounds} ===")
    chat_manager.send_message(
        room_name=chat_room.name,
        sender=agents[0],
        content=f"Hello everyone! Let's discuss the following problem:\n\n{problem.question}"
    )
    
    
    
    return True

def main(max_rounds: int = 3, agent_count: int = 3, subject: str = DEFAULT_MMLU_SUBJECT):
    print("Initializing Multi-Agent Chat System...")
    
    # Create managers
    chat_manager = ChatManager()
    agent_factory = AgentFactory()
    
    # Initialize MMLU problem provider with total problems to load
    problem_provider = MMLUProblemProvider(
        subject=subject,
        total_problems=TOTAL_PROBLEMS_TO_LOAD
    )
    
    # Generate agents (only once for all sessions)
    agents = agent_factory.create_agents(agent_count)
    print("\n=== Generated Agents ===")
    for agent in agents:
        print(f"{agent.name}: {agent.description}")
    
    # Run chat sessions until we run out of problems
    session_num = 1
    while True:
        success = run_chat_session(
            chat_manager=chat_manager,
            agents=agents,
            problem_provider=problem_provider,
            max_rounds=max_rounds,
            session_num=session_num
        )
        
        if not success:
            print("\nNo more problems available. Discussion sessions completed.")
            accuracy = problem_provider.get_accuracy()
            print(f"\nFinal Results:")
            print(f"Total Problems: {problem_provider.total_answered}")
            print(f"Correct Answers: {problem_provider.correct_answers}")
            print(f"Accuracy: {accuracy:.2%}")
            break
            
        session_num += 1
        # Optional: wait for user input before starting next session
        print(f"\nCurrent Accuracy: {problem_provider.get_accuracy():.2%}")
        # input("\nPress Enter to start next problem discussion...")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Multi-Agent Math Discussion System')
    parser.add_argument('--agents', type=int, default=3, help='Number of agents to participate')
    parser.add_argument('--rounds', type=int, default=3, help='Number of rounds per problem')
    parser.add_argument('--subject', type=str, default=DEFAULT_MMLU_SUBJECT, help='MMLU subject')
    args = parser.parse_args()
    # main(max_rounds=args.rounds, agent_count=args.agents, subject=args.subject)
    main(max_rounds=3, agent_count=4, subject=args.subject)