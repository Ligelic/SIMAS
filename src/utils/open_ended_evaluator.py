import json
from typing import Dict, List, Tuple
from utils.llm_service import LLMService

class OpenEndedEvaluator:
    """开放性问题答案评估器"""
    
    def __init__(self, model: str = None):
        self.llm_service = LLMService()
        self.model = model
        
    def evaluate_single_answer(self, problem: str, answer: str, criteria: List[str] = None) -> Dict:
        """评估单个答案"""
        if criteria is None:
            criteria = ["相关性", "深度", "逻辑性", "创新性", "可行性"]
            
        prompt = self._create_evaluation_prompt(problem, answer, criteria)
        response = self.llm_service.get_response(prompt)
        
        try:
            # 尝试解析JSON格式的评估结果
            evaluation = json.loads(response)
        except json.JSONDecodeError:
            # 如果不是JSON，尝试提取评分信息
            evaluation = self._parse_evaluation_text(response, criteria)
            
        return evaluation
    
    def compare_answers(self, problem: str, answer_a: str, answer_b: str, 
                       method_a: str = "CoT", method_b: str = "SIMAS",
                       criteria: List[str] = None) -> Dict:
        """比较两个答案并评分"""
        if criteria is None:
            criteria = ["相关性", "深度", "逻辑性", "创新性", "可行性", "全面性"]
            
        prompt = self._create_comparison_prompt(
            problem, answer_a, answer_b, method_a, method_b, criteria
        )
        response = self.llm_service.get_response(prompt)
        print(response)
        try:
            comparison = json.loads(response)
        except json.JSONDecodeError:
            comparison = self._parse_comparison_text(response)
            
        return comparison
    
    def _create_evaluation_prompt(self, problem: str, answer: str, criteria: List[str]) -> str:
        """创建评估单个答案的提示词"""
        criteria_str = "\n".join([f"{i+1}. {criterion}" for i, criterion in enumerate(criteria)])
        
        return f"""作为专业评估专家，请对以下答案进行评估。

问题：
{problem}

答案：
{answer}

评估标准（每个标准1-10分）：
{criteria_str}

请提供详细的评估，包括：
1. 每个标准的评分及理由
2. 总体评价
3. 优点和改进建议

请以以下JSON格式返回结果：
{{
    "scores": {{
        "criterion1": {{"score": X, "reason": "..."}},
        ...
    }},
    "total_score": X,
    "overall_evaluation": "...",
    "strengths": ["...", "..."],
    "improvements": ["...", "..."]
}}

请确保总分是各个标准得分的平均值。
"""
    
    def _create_comparison_prompt(self, problem: str, answer_a: str, answer_b: str, 
                                 method_a: str, method_b: str, criteria: List[str]) -> str:
        """创建比较两个答案的提示词"""
        criteria_str = "\n".join([f"{i+1}. {criterion}" for i, criterion in enumerate(criteria)])
        
        return f"""作为专业评估专家，请比较两个AI系统生成的答案。

问题：
{problem}

答案A（由{method_a}生成）：
{answer_a}

答案B（由{method_b}生成）：
{answer_b}

评估标准（每个标准1-10分）：
{criteria_str}

请：
1. 分别评估两个答案在每个标准上的表现
2. 比较两个答案的优劣
3. 指出哪个答案更好，并说明理由

请以以下JSON格式返回结果：
{{
    "answer_a_scores": {{
        "total": X,
        "criteria": {{
            "criterion1": {{"score": X, "reason": "..."}},
            ...
        }}
    }},
    "answer_b_scores": {{
        "total": X,
        "criteria": {{
            "criterion1": {{"score": X, "reason": "..."}},
            ...
        }}
    }},
    "comparison": {{
        "winner": "A" 或 "B" 或 "tie",
        "reason": "...",
        "key_differences": ["...", "..."],
        "potential_synergy": "..."
    }}
}}

请确保评估公正、客观，基于答案内容而非生成方法。
请确保返回结果只有有效的json格式内容，没有其他任何其他话语或符号。
"""
    
    def _parse_evaluation_text(self, text: str, criteria: List[str]) -> Dict:
        """从文本中解析评估结果"""
        # 简化的文本解析逻辑
        result = {
            "scores": {},
            "total_score": 0,
            "overall_evaluation": text[:500],  # 截取前500字符
            "strengths": [],
            "improvements": []
        }
        
        # 尝试提取评分
        import re
        score_pattern = r'(\d+)\s*分|score.*?(\d+)'
        scores = re.findall(score_pattern, text, re.IGNORECASE)
        if scores:
            total_score = 0
            count = 0
            for match in scores:
                for group in match:
                    if group:
                        score = int(group)
                        if 1 <= score <= 10:
                            criterion = criteria[min(count, len(criteria)-1)]
                            result["scores"][criterion] = {"score": score, "reason": "从文本提取"}
                            total_score += score
                            count += 1
                            break
            if count > 0:
                result["total_score"] = total_score / count
                
        return result
    
    def _parse_comparison_text(self, text: str) -> Dict:
        """从文本中解析比较结果"""
        result = {
            "answer_a_scores": {"total": 0, "criteria": {}},
            "answer_b_scores": {"total": 0, "criteria": {}},
            "comparison": {
                "winner": "unknown",
                "reason": text[:300],
                "key_differences": [],
                "potential_synergy": ""
            }
        }
        
        # 简化的解析逻辑
        if "答案A" in text or "Answer A" in text:
            result["comparison"]["winner"] = "A"
        elif "答案B" in text or "Answer B" in text:
            result["comparison"]["winner"] = "B"
        elif "相当" in text or "平局" in text or "tie" in text.lower():
            result["comparison"]["winner"] = "tie"
            
        return result