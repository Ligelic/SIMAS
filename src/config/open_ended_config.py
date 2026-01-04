OPEN_ENDED_CONFIG = {
    # 数据集配置
    "dataset": {
        "path": "data/open_ended/open_ended_problems.json",
        "default_count": 10,
        "categories": [
            "urban_planning",
            "education_tech", 
            "social_innovation",
            "economics",
            "business",
            "ethics",
            "technology",
            "environment",
            "healthcare",
            "creativity"
        ]
    },
    
    # 评估标准配置
    "evaluation_criteria": {
        "default": ["相关性", "深度", "逻辑性", "创新性", "可行性", "全面性"],
        "urban_planning": ["创新性", "可行性", "成本效益", "可持续性", "用户体验"],
        "education_tech": ["分析深度", "建议可行性", "前瞻性", "系统性"],
        "social_innovation": ["同理心", "实用性", "可持续性", "可扩展性"],
        "business": ["创新性", "可行性", "商业模式", "竞争优势"],
        "ethics": ["道德考量", "公平性", "透明性", "责任性"]
    },
    
    # 实验参数
    "experiment": {
        "default_problem_count": 5,
        "default_agent_count": 3,
        "default_rounds": 3,
        "default_experiments": 1,
        "max_answer_length": 5000,  # 最大答案长度
        "temperature": 0.7,  # 生成温度
        "evaluator_model": "qwen2.5:72b-instruct"  # 评估器模型
    },
    
    # 输出配置
    "output": {
        "result_dir": "evaluate_result/open_ended_comparison",
        "save_detailed_results": True,
        "save_summaries": True,
        "log_level": "INFO"
    }
}

# 开放性问题示例模板
OPEN_ENDED_TEMPLATES = [
    {
        "category": "urban_planning",
        "template": "设计一个创新的{solution_for}方案，解决{problem}问题。请考虑{specific_aspects}。",
        "variables": {
            "solution_for": ["城市交通", "废物管理", "能源供应", "住房"],
            "problem": ["高峰期拥堵", "环境污染", "资源浪费", "高昂成本"],
            "specific_aspects": ["可持续性、成本效益和用户体验", "技术可行性、社会接受度和环境影响", "短期效果和长期可持续性"]
        }
    },
    {
        "category": "ethics",
        "template": "分析{technology}的{ethical_aspect}影响，并提出{number}个具体的{guidelines_or_frameworks}。",
        "variables": {
            "technology": ["人工智能", "基因编辑", "自动驾驶", "面部识别"],
            "ethical_aspect": ["伦理", "社会", "隐私", "公平性"],
            "number": ["三", "五"],
            "guidelines_or_frameworks": ["伦理指南", "监管框架", "最佳实践", "风险评估方法"]
        }
    }
]