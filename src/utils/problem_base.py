from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class Problem:
    question: str
    answer: str
    metadata: Dict[str, Any] = None  # Additional info like subject, difficulty, etc.

class ProblemProvider(ABC):
    """Base class for problem providers"""
    @abstractmethod
    def get_next_problem(self) -> Optional[Problem]:
        """Get next problem from the provider"""
        raise NotImplementedError
        
    @abstractmethod
    def evaluate_answer(self, problem: Problem, answer: str) -> bool:
        """Evaluate if the given answer is correct"""
        raise NotImplementedError