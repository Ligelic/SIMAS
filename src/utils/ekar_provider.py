from typing import List, Optional, Dict, Any
from datasets import load_dataset, DownloadConfig
from .problem_base import Problem, ProblemProvider

class EKARProblemProvider(ProblemProvider):
    def __init__(self, total_problems: int = 10):
        """Initialize E-KAR problem provider"""
        self.problems: List[Problem] = []
        self.used_problems: List[Problem] = []
        self.correct_answers: int = 0
        self.total_answered: int = 0
        self._load_ekar_problems(total_problems)
        
    def _load_ekar_problems(self, n_problems: int) -> None:
        """Load problems from E-KAR dataset"""
        try:
            # Configure dataset loading
            config = DownloadConfig(resume_download=True, max_retries=100)
            dataset = load_dataset("jiangjiechen/ekar_english", download_config=config)
            
            # Take specified number of problems from test split
            test_data = dataset['test']
            for i in range(min(n_problems, len(test_data))):
                item = test_data[i]
                
                # Format question with choices
                question = f"{item['question']}\n"
                choices = item['choices']
                for label, text in zip(choices['label'], choices['text']):
                    question += f"{label}) {text}\n"
                
                # Create problem instance
                self.problems.append(Problem(
                    question=question.strip(),
                    answer=item['answerKey'],
                    metadata={
                        "id": item['id'],
                        "type": "analogy",
                        "explanation": item['explanation'],
                        "relation": item['relation']
                    }
                ))
                
        except Exception as e:
            print(f"Error loading E-KAR dataset: {e}")
            self._generate_sample_problem()

    def _generate_sample_problem(self) -> None:
        """Generate a sample problem if dataset loading fails"""
        self.problems = [
            Problem(
                question=(
                    "plant:coal\n"
                    "A) white wine:aged vinegar\n"
                    "B) starch:corn\n"
                    "C) milk:yogurt\n"
                    "D) pickled cabbage:cabbage"
                ),
                answer="C",
                metadata={
                    "id": "sample_001",
                    "type": "analogy",
                    "explanation": ["Raw material relationship - milk is used to make yogurt"],
                    "relation": [["milk", "yogurt", "R3.7"]]
                }
            )
        ]
    
    def get_next_problem(self) -> Optional[Problem]:
        """Get next problem and move it to used problems list"""
        if not self.problems:
            return None
        problem = self.problems.pop(0)
        self.used_problems.append(problem)
        return problem

    def record_answer(self, problem: Problem, answer: str) -> bool:
        """Record an answer and return whether it was correct"""
        is_correct = self.evaluate_answer(problem, answer)
        self.total_answered += 1
        if is_correct:
            self.correct_answers += 1
        return is_correct
    
    def get_accuracy(self) -> float:
        """Get current accuracy rate"""
        if self.total_answered == 0:
            return 0.0
        return self.correct_answers / self.total_answered

    def evaluate_answer(self, problem: Problem, answer: str) -> bool:
        try:
            import re
            patterns = [
                r'(?:final answer:|answer:|选择|答案是|选项)[^\w]*([A-D])[）).\s]',
                r'(?:^|\s)([A-D])[）).\s][^A-D]+$',
                r'(?:^|\s)([A-D])(?:\s|$)',
                r'(?:^|\s)\(?([A-D])\)',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, answer, re.IGNORECASE)
                if match:
                    student_answer = match.group(1).upper()
                    print(f"Answer text: {answer}")
                    print(f"Student answer: {student_answer}")
                    print(f"Correct answer: {problem.answer.upper()}")
                    return student_answer == problem.answer.upper()
                    
            print(f"No valid answer format found in: {answer}")
            return False
                
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