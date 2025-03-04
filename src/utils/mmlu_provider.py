from typing import List, Optional
import pandas as pd
from .problem_base import Problem, ProblemProvider

class MMLUProblemProvider(ProblemProvider):
    def __init__(self, subject: str = 'mathematics', total_problems: int = 10):
        """
        Initialize MMLU problem provider
        Args:
            subject: The MMLU subject to load
            total_problems: Total number of problems to load
        """
        self.problems: List[Problem] = []
        self.used_problems: List[Problem] = []  # Track used problems
        self._load_mmlu_problems(subject, total_problems)
        
    def _load_mmlu_problems(self, subject: str, n_problems: int):
        # Load MMLU dataset
        try:
            # Assuming MMLU data is in CSV format with columns: question, A, B, C, D, answer
            df = pd.read_csv(f'data/mmlu/{subject}_test.csv', encoding='utf-8')
            
            # Take first n_problems
            df = df.head(n_problems)
            
            for _, row in df.iterrows():
                # Format question with options
                question = (
                    f"{row['question']}\n"
                    f"A) {row['A']}\n"
                    f"B) {row['B']}\n"
                    f"C) {row['C']}\n"
                    f"D) {row['D']}"
                )
                
                self.problems.append(Problem(
                    question=question,
                    answer=row['answer'],
                    metadata={
                        "type": "multiple_choice",
                        "subject": subject
                    }
                ))
                
        except Exception as e:
            print(f"Error loading MMLU dataset: {e}")
            # Generate sample problem as fallback
            self._generate_sample_problem()
    
    def _generate_sample_problem(self):
        """Generate a sample problem if dataset loading fails"""
        self.problems = [
            Problem(
                question="What is the capital of France?\nA) London\nB) Paris\nC) Berlin\nD) Madrid",
                answer="B",
                metadata={"type": "multiple_choice", "subject": "geography"}
            )
        ]
    
    def get_next_problem(self) -> Optional[Problem]:
        """Get next problem and move it to used problems list"""
        if not self.problems:
            return None
        problem = self.problems.pop(0)
        self.used_problems.append(problem)
        return problem
        
    def evaluate_answer(self, problem: Problem, answer: str) -> bool:
        try:
            # Extract answer from agent's response
            # Looking for pattern like "The answer is [A/B/C/D]" or just "[A/B/C/D]"
            import re
            match = re.search(r"(?:answer is |选择|答案是|选项)?\s*([A-D])", answer, re.IGNORECASE)
            if not match:
                return False
                
            student_answer = match.group(1).upper()
            return student_answer == problem.answer.upper()
            
        except Exception as e:
            print(f"Error evaluating answer: {e}")
            return False

    def get_remaining_count(self) -> int:
        """Get number of remaining unused problems"""
        return len(self.problems)
        
    def reset(self):
        """Reset problems - move all used problems back to available"""
        self.problems.extend(self.used_problems)
        self.used_problems.clear()