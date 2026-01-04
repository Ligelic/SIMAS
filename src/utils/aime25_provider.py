from typing import List, Optional
import os
import json
import re
from .problem_base import Problem, ProblemProvider

class AIME2025ProblemProvider(ProblemProvider):
    def __init__(self, data_path: str = "multi-agent-chat/aime25/test.jsonl", total_problems: int = 10):
        """
        Initialize AIME2025 problem provider
        Args:
            data_path: Path to AIME2025 dataset file (JSONL format)
            total_problems: Total number of problems to load
        """
        self.problems: List[Problem] = []
        self.used_problems: List[Problem] = []
        self.correct_answers = 0
        self.total_answered = 0
        
        if data_path and os.path.exists(data_path):
            self._load_aime_problems(data_path, total_problems)
        else:
            self._generate_sample_problems(total_problems)
    
    def _load_aime_problems(self, data_path: str, n_problems: int):
        """Load AIME problems from JSONL file"""
        try:
            with open(data_path, 'r') as f:
                lines = f.readlines()
                
            for i, line in enumerate(lines[:n_problems]):
                data = json.loads(line.strip())
                
                self.problems.append(Problem(
                    question=data["problem"],
                    answer=str(data["answer"]),
                    metadata={
                        "type": "short-answer",
                        "id": data["id"],
                        "source": "AIME2025"
                    }
                ))
                
        except Exception as e:
            print(f"Error loading AIME dataset: {e}")
            self._generate_sample_problems(n_problems)
    
    def _generate_sample_problems(self, n_problems: int):
        """Generate sample AIME problems if dataset loading fails"""
        sample_problems = [
            {
                "problem": "Find the sum of all integer bases $b>9$ for which $17_b$ is a divisor of $97_b.$",
                "answer": "70",
                "id": "0"
            },
            {
                "problem": "In $\\triangle ABC$ points $D$ and $E$ lie on $\\overline{AB}$ so that $AD < AE < AB$, while points $F$ and $G$ lie on $\\overline{AC}$ so that $AF < AG < AC$. Suppose $AD = 4$, $DE = 16$, $EB = 8$, $AF = 13$, $FG = 52$, and $GC = 26$. Let $M$ be the reflection of $D$ through $F$, and let $N$ be the reflection of $G$ through $E$. The area of quadrilateral $DEGF$ is $288$. Find the area of heptagon $AFNBCEM$.",
                "answer": "588",
                "id": "1"
            },
            {
                "problem": "The $9$ members of a baseball team went to an ice-cream parlor after their game. Each player had a single scoop cone of chocolate, vanilla, or strawberry ice cream. At least one player chose each flavor, and the number of players who chose chocolate was greater than the number of players who chose vanilla, which was greater than the number of players who chose strawberry. Let $N$ be the number of different assignments of flavors to players that meet these conditions. Find the remainder when $N$ is divided by $1000.$",
                "answer": "16",
                "id": "2"
            }
        ]
        
        for i, data in enumerate(sample_problems[:n_problems]):
            self.problems.append(Problem(
                question=data["problem"],
                answer=str(data["answer"]),
                metadata={
                    "type": "aime",
                    "id": data["id"],
                    "source": "AIME2025_sample"
                }
            ))
    
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
        """Evaluate answer for AIME problems (numeric answers only)"""
        try:
            # Extract all numbers from the answer
            numbers = re.findall(r'\d+', answer)
            
            if not numbers:
                return False
                
            # Use the first number found as the answer
            student_answer = numbers[0]
            
            # Compare with the correct answer
            return student_answer == problem.answer
            
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