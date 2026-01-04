from agents.agent_factory import AgentFactory
from chat.chat_manager import ChatManager
from chat.message import Message
from utils.ekar_provider import EKARProblemProvider
from utils.mmlu_provider import MMLUProblemProvider
from utils.aime25_provider import AIME2025ProblemProvider
from utils.saver import save_evaluation_result
from config.config import (
    DEFAULT_MMLU_SUBJECT, 
    TOTAL_PROBLEMS_TO_LOAD,
    LLM_MODEL,
    DEFAULT_MODE,
    NONE_ALL,
    NONE_PERSONALITY,
    NONE_EXPERTISE,
    NONE_BELIEF
)
from statistics import mean

def run_reasoning_session(
    chat_manager: ChatManager,
    agent,
    problem_provider: MMLUProblemProvider,
    session_num: int
) -> bool:
    """Run a single session with one agent. Returns True if successful."""
    
    # Get next problem
    problem = problem_provider.get_next_problem()
    if not problem:
        return False
        
    print(f"\n=== Starting Session {session_num} ===")
    print(f"Remaining problems: {problem_provider.get_remaining_count()}")
    
    
    print(f"{problem.question}")
    
    # Send problem to agent

    chat_room = chat_manager.create_chat_room(f"Session_{session_num}", max_round=1)
    agent.problem_type = problem.metadata.get('type', 'N/A')

    message = Message(
            sender=agent, 
            content=problem.question,
            chat_room=chat_room
        )
    agent_response = agent.receive_reason_request(
        message=message
    )
    problem_provider.record_answer(problem, agent_response)
    
    return True

def run_reasoning_experiment(subject: str, problem_count: int, agent_mode: int = DEFAULT_MODE) -> tuple:
    """Run a single experiment with one agent and return accuracy and token usage"""
    chat_manager = ChatManager()
    agent_factory = AgentFactory()
    
    # Initialize problem provider
    if subject == 'e-kar':
        problem_provider = EKARProblemProvider(
        total_problems=problem_count
    )
    elif subject == 'aime2025':
        problem_provider = AIME2025ProblemProvider(
        total_problems=problem_count
    )
    else:
        problem_provider = MMLUProblemProvider(
            subject=subject,
            total_problems=problem_count
        )


    
    # Create single agent with specified mode
    if agent_mode == DEFAULT_MODE:
        agent = agent_factory.create_agents(1, subject=subject, from_file=False)[0]
    else:
        agent = agent_factory.create_agents(1, subject=subject, from_file=True, mode=agent_mode)[0]
        agent.mode = agent_mode

    print(f"\n=== Testing Agent ===")
    print(f"{agent.name}: {agent.description}")
    
    # Reset token counter
    agent.llm_service.reset_token_count()
    
    # Run sessions
    session_num = 1
    while True:
        success = run_reasoning_session(
            chat_manager=chat_manager,
            agent=agent,
            problem_provider=problem_provider,
            session_num=session_num
        )
        
        if not success:
            return problem_provider.get_accuracy(), agent.llm_service.get_total_tokens()
            
        session_num += 1
        print(f"\nCurrent Accuracy: {problem_provider.get_accuracy():.2%}")

def main_reasoning(subject: str = DEFAULT_MMLU_SUBJECT, 
                     problem_count: int = TOTAL_PROBLEMS_TO_LOAD,
                     experiment_count: int = 3,
                     agent_mode: int = DEFAULT_MODE):
    print(f"Initializing Single-Agent Testing System...")
    print(f"Running {experiment_count} experiments...")
    print(f"Mode: {agent_mode}")
    
    accuracies = []
    token_usages = []
    for i in range(experiment_count):
        print(f"\n=== Experiment {i+1}/{experiment_count} ===")
        accuracy, tokens = run_reasoning_experiment(
            subject=subject,
            problem_count=problem_count,
            agent_mode=agent_mode
        )
        accuracies.append(accuracy)
        token_usages.append(tokens)
        print(f"Experiment {i+1} Accuracy: {accuracy:.2%}")
        print(f"Experiment {i+1} Token Usage: {tokens:,}")
    
    # Calculate statistics
    avg_accuracy = mean(accuracies)
    avg_tokens = mean(token_usages)
    std_dev = (sum((x - avg_accuracy) ** 2 for x in accuracies) / len(accuracies)) ** 0.5
    
    # Print final results
    print("\n=== Final Results ===")
    print(f"Model: {LLM_MODEL}")
    print(f"Subject: {subject}")
    print(f"Mode: Reasoning")
    print(f"Agent Mode: {agent_mode}")
    print(f"Total problems: {problem_count}")
    print(f"Individual Accuracies: {[f'{acc:.2%}' for acc in accuracies]}")
    print(f"Average Accuracy: {avg_accuracy:.2%}")
    print(f"Standard Deviation: {std_dev:.2%}")
    print(f"Total Token Usage: {sum(token_usages):,}")
    print(f"Average Token Usage per Experiment: {avg_tokens:,.0f}")
    
    # Save results
    save_evaluation_result(
        subject=subject,
        agent_count=1,
        max_rounds=1,
        problem_provider=None,
        model=LLM_MODEL,
        mode='Reasoning',
        agent_mode=agent_mode,
        metadata={
            "experiment_count": experiment_count,
            "individual_accuracies": accuracies,
            "average_accuracy": avg_accuracy,
            "std_deviation": std_dev,
            "problem_count": problem_count,
            "token_usages": token_usages,
            "total_tokens": sum(token_usages),
            "avg_tokens_per_experiment": avg_tokens
        }
    )

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Single-Agent Problem Solving System')
    parser.add_argument('--subject', type=str, default=DEFAULT_MMLU_SUBJECT, help='MMLU subject')
    parser.add_argument('--problem_count', type=int, default=17, help='Number of problems to load')
    parser.add_argument('--experiments', type=int, default=3, help='Number of experiments to run')
    parser.add_argument('--mode', type=int, default=DEFAULT_MODE, help='Agent mode')
    args = parser.parse_args()
    
    main_reasoning(
        subject=args.subject, 
        problem_count=args.problem_count,
        experiment_count=args.experiments,
        agent_mode=NONE_ALL
    )