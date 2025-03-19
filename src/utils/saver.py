import os
from datetime import datetime
from utils.mmlu_provider import MMLUProblemProvider

def save_evaluation_result(subject: str, agent_count: int, max_rounds: int, 
                         problem_provider: MMLUProblemProvider, model: str):
    # Create evaluate_result directory if it doesn't exist
    result_dir = "C:/Users/Administrator/multi-agent-chat/evaluate_result"
    os.makedirs(result_dir, exist_ok=True)
    
    # Get current date and find next available index
    now = datetime.now()
    base_filename = f"result_{now.month}_{now.day}"
    index = 1
    while os.path.exists(os.path.join(result_dir, f"{base_filename}({index}).txt")):
        index += 1
    
    # Create result file
    filepath = os.path.join(result_dir, f"{base_filename}({index}).txt")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"Model: {model}\n")
        f.write(f"Subject: {subject}\n")
        f.write(f"Agent Count: {agent_count} | Rounds: {max_rounds}\n")
        f.write("\nFinal Results:\n")
        f.write(f"Total Problems: {problem_provider.total_answered}\n")
        f.write(f"Correct Answers: {problem_provider.correct_answers}\n")
        accuracy = problem_provider.get_accuracy()
        f.write(f"Accuracy: {accuracy:.2%}\n\n\n\n")
    
    print(f"\nEvaluation results saved to: {filepath}")