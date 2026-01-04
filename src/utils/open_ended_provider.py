from typing import List, Optional
import json
import os
from .problem_base import Problem, ProblemProvider

class OpenEndedProblemProvider(ProblemProvider):
    """开放性问题提供器，答案空间不固定"""
    
    def __init__(self, problem_file: str = "data/open_ended/open_ended_problems.json", 
                 total_problems: int = 10):
        self.problems: List[Problem] = []
        self.used_problems: List[Problem] = []
        self.correct_answers = 0
        self.total_answered = 0
        self._load_open_ended_problems(problem_file, total_problems)
        
    def _load_open_ended_problems(self, problem_file: str, n_problems: int):
        """从JSON文件加载开放性问题"""
        try:
            if not os.path.exists(problem_file):
                # 创建示例开放性问题
                self._create_sample_problems()
                return
                
            with open(problem_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            for item in data[:n_problems]:
                self.problems.append(Problem(
                    question=item["question"],
                    answer=item.get("reference_answer", ""),  # 参考答案，用于评估
                    metadata={
                        "type": "open_ended",
                        "category": item.get("category", "general"),
                        "criteria": item.get("evaluation_criteria", []),  # 评估标准
                        "difficulty": item.get("difficulty", "medium")
                    }
                ))
                
        except Exception as e:
            print(f"Error loading open-ended problems: {e}")
            self._create_sample_problems()
    
    def _create_sample_problems(self):
        """创建示例开放性问题"""
        sample_problems = [
            {
                "question": "设计一个创新的城市交通解决方案，解决高峰期拥堵问题。请考虑可持续性、成本效益和用户体验。",
                "category": "urban_planning",
                "difficulty": "hard",
                "evaluation_criteria": ["创新性", "可行性", "成本效益", "可持续性", "用户体验"]
            },
            {
                "question": "分析人工智能对未来教育的影响，并提出三个具体的教育改革建议。",
                "category": "education_tech",
                "difficulty": "medium",
                "evaluation_criteria": ["分析深度", "建议可行性", "前瞻性", "系统性"]
            },
            {
                "question": "设计一个帮助老年人融入数字社会的项目方案，包括目标、实施步骤和预期成果。",
                "category": "social_innovation",
                "difficulty": "medium",
                "evaluation_criteria": ["同理心", "实用性", "可持续性", "可扩展性"]
            },
            {
                "question": "讨论气候变化对全球经济的影响，并提出应对策略。请从不同国家类型的角度分析（发达国家、发展中国家）。",
                "category": "economics",
                "difficulty": "hard",
                "evaluation_criteria": ["全面性", "深度分析", "具体建议", "平衡性"]
            },
            {
                "question": "设计一个创业计划：基于AI的健康管理应用。包括目标用户、核心功能、商业模式和竞争优势。",
                "category": "business",
                "difficulty": "medium",
                "evaluation_criteria": ["创新性", "可行性", "商业模式", "竞争优势"]
            },
            {
            "question": "设计一个循环经济模式下的社区共享资源平台，旨在最大化资源利用率并减少浪费。请说明其运作机制、激励措施和社区治理结构。",
            "category": "sustainability",
            "difficulty": "hard",
            "evaluation_criteria": ["系统性思维", "模式创新性", "社区可参与性", "环境效益量化"]
            },
            {
            "question": "为应对极端天气事件频发，请为一个沿海城市设计一套韧性城市改造方案，需综合考虑基础设施、社会组织和预警系统。",
            "category": "urban_planning",
            "difficulty": "hard",
            "evaluation_criteria": ["风险评估全面性", "方案集成度", "成本效益分析", "社会公平性"]
            },
            {
            "question": "分析远程办公和混合工作模式的普及对城市中心区商业生态、房地产和公共服务需求的长期影响，并提出城市规划调整建议。",
            "category": "economics_urban",
            "difficulty": "medium",
            "evaluation_criteria": ["趋势分析深度", "多维度影响考量", "建议的前瞻性与可行性"]
            },
            {
            "question": "设计一个面向青少年（12-18岁）的数字素养与心理健康综合教育项目，旨在帮助他们健康地使用社交媒体和处理网络信息。",
            "category": "education_psychology",
            "difficulty": "medium",
            "evaluation_criteria": ["目标群体针对性", "课程设计有效性", "家校社协同机制", "效果评估方法"]
            },
            {
            "question": "探讨在保护文化多样性的前提下，人工智能（如机器翻译、内容生成）对全球小众语言及文化遗产传承的可能影响与应对策略。",
            "category": "technology_society",
            "difficulty": "hard",
            "evaluation_criteria": ["洞察的辩证性", "文化敏感性", "技术方案的伦理考量", "策略的多层次性"]
            },
            {
            "question": "设计一个利用区块链技术提升公益慈善捐赠透明度和信任度的解决方案，涵盖从捐赠、执行到审计的全流程。",
            "category": "social_innovation_tech",
            "difficulty": "medium",
            "evaluation_criteria": ["技术应用合理性", "流程透明性设计", "用户体验", "可扩展性与成本"]
            },
            {
            "question": "针对大城市中的“城市农场”或垂直农业，分析其经济效益、环境效益及社会效益，并设计一个可行的社区推广商业模式。",
            "category": "business_sustainability",
            "difficulty": "medium",
            "evaluation_criteria": ["效益分析全面性", "商业模式创新", "社区融合度", "可持续运营能力"]
            },
            {
            "question": "从心理学和设计学角度，分析如何为视障人群优化公共场所（如地铁站、博物馆）的导航与信息获取体验，提出具体设计原则。",
            "category": "design_inclusion",
            "difficulty": "medium",
            "evaluation_criteria": ["用户同理心深度", "方案的多感官整合", "普适设计原则应用", "实施可行性"]
            },
            {
            "question": "讨论全球人口结构老龄化对创新生态（如创业活力、技术采纳、消费市场）带来的挑战与机遇，并提出政策应对框架。",
            "category": "economics_policy",
            "difficulty": "hard",
            "evaluation_criteria": ["宏观趋势把握", "挑战与机遇的平衡分析", "政策框架的系统性与创新性"]
            },
            {
            "question": "设计一个促进生物多样性保护的公民科学项目，让普通公众能有效参与数据收集和物种监测，并阐述其科学价值与社会价值。",
            "category": "environmental_science",
            "difficulty": "medium",
            "evaluation_criteria": ["公众参与机制设计", "数据质量保障", "科学目标明确性", "社会动员与教育价值"]
            }
        ]
        
        for item in sample_problems:
            self.problems.append(Problem(
                question=item["question"],
                answer="",  # 开放性问题没有固定答案
                metadata={
                    "type": "open_ended",
                    "category": item["category"],
                    "criteria": item["evaluation_criteria"],
                    "difficulty": item["difficulty"]
                }
            ))
    
    def get_next_problem(self) -> Optional[Problem]:
        """获取下一个问题"""
        if not self.problems:
            return None
        problem = self.problems.pop(0)
        self.used_problems.append(problem)
        return problem

    def record_answer(self, problem: Problem, answer: str) -> bool:
        """记录答案，开放性问题总是返回True（评估在外部进行）"""
        self.total_answered += 1
        # 注意：开放性问题不在此处评估正确性
        return True
    
    def get_accuracy(self) -> float:
        """获取准确率（开放性问题不使用此方法）"""
        return 0.0

    def evaluate_answer(self, problem: Problem, answer: str) -> bool:
        """评估答案，开放性问题返回True（评估在外部进行）"""
        return True

    def get_remaining_count(self) -> int:
        """获取剩余问题数量"""
        return len(self.problems)
        
    def reset(self):
        """重置问题列表"""
        self.problems.extend(self.used_problems)
        self.used_problems.clear()