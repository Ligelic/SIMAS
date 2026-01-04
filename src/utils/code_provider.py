from typing import List, Optional
import json
import os
from .problem_base import Problem, ProblemProvider

class CodeProblemProvider(ProblemProvider):
    """代码问题提供器，包含编程问题和测试用例"""
    
    def __init__(self, problem_file: str = "data/code/code_problems.json", 
                 total_problems: int = 10):
        self.problems: List[Problem] = []
        self.used_problems: List[Problem] = []
        self.correct_answers = 0
        self.total_answered = 0
        self._load_code_problems(problem_file, total_problems)
        
    def _load_code_problems(self, problem_file: str, n_problems: int):
        """从JSON文件加载代码问题"""
        try:
            if not os.path.exists(problem_file):
                # 创建示例代码问题
                self._create_sample_problems()
                return
                
            with open(problem_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            for item in data[:n_problems]:
                self.problems.append(Problem(
                    question=item["question"],
                    answer=item.get("reference_code", ""),  # 参考答案代码
                    metadata={
                        "type": "code",
                        "category": item.get("category", "algorithm"),
                        "difficulty": item.get("difficulty", "medium"),
                        "language": item.get("language", "Python"),
                        "constraints": item.get("constraints", []),
                        "test_cases": item.get("test_cases", []),
                        "evaluation_criteria": item.get("evaluation_criteria", [
                            "正确性", "代码质量", "效率", "可读性", "鲁棒性"
                        ])
                    }
                ))
                
        except Exception as e:
            print(f"Error loading code problems: {e}")
            self._create_sample_problems()
    
    def _create_sample_problems(self):
        """创建示例代码问题"""
        sample_problems = [
            # {
            #     "question": "实现一个函数，接受一个整数数组nums和一个目标值target，返回数组中两数之和等于target的索引。\n\n要求：\n1. 假设每个输入只有一个解\n2. 不能使用同一个元素两次\n3. 时间复杂度尽可能低\n\n示例：\nnums = [2, 7, 11, 15], target = 9\n返回：[0, 1]",
            #     "category": "algorithm",
            #     "difficulty": "easy",
            #     "language": "Python",
            #     "constraints": ["时间复杂度O(n)", "空间复杂度O(n)"],
            #     "test_cases": [
            #         {"input": {"nums": [2,7,11,15], "target": 9}, "output": [0,1]},
            #         {"input": {"nums": [3,2,4], "target": 6}, "output": [1,2]},
            #         {"input": {"nums": [3,3], "target": 6}, "output": [0,1]}
            #     ],
            #     "evaluation_criteria": ["正确性", "时间复杂度", "代码简洁性", "边界处理"]
            # },
            # {
            #     "question": "实现二叉树的层序遍历。给定一个二叉树的根节点root，返回其节点值的层序遍历结果（即逐层从左到右访问所有节点）。\n\n例如：\n输入：root = [3,9,20,null,null,15,7]\n输出：[[3],[9,20],[15,7]]",
            #     "category": "data_structure",
            #     "difficulty": "medium",
            #     "language": "Python",
            #     "constraints": ["使用队列实现", "不使用递归"],
            #     "test_cases": [
            #         {"input": {"root": [3,9,20,None,None,15,7]}, "output": [[3],[9,20],[15,7]]},
            #         {"input": {"root": [1]}, "output": [[1]]},
            #         {"input": {"root": []}, "output": []}
            #     ],
            #     "evaluation_criteria": ["算法正确性", "代码清晰度", "边界情况处理", "空间复杂度"]
            # },
            # {
            #     "question": "设计一个LRU（最近最少使用）缓存。实现LRUCache类：\n- LRUCache(int capacity) 以正整数作为容量 capacity 初始化缓存\n- int get(int key) 如果关键字 key 存在于缓存中，则返回关键字的值，否则返回 -1\n- void put(int key, int value) 如果关键字已经存在，则变更其数据值；如果不存在，则插入该组「关键字-值」。当缓存容量达到上限时，它应该在写入新数据之前删除最久未使用的数据值，从而为新的数据值留出空间。\n\n要求：\nget 和 put 必须以 O(1) 的平均时间复杂度运行。",
            #     "category": "system_design",
            #     "difficulty": "hard",
            #     "language": "Python",
            #     "constraints": ["O(1)时间复杂度", "使用双向链表和哈希表"],
            #     "test_cases": [
            #         {"input": ["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"], 
            #          "args": [[2], [1,1], [2,2], [1], [3,3], [2], [4,4], [1], [3], [4]], 
            #          "output": [None, None, None, 1, None, -1, None, -1, 3, 4]}
            #     ],
            #     "evaluation_criteria": ["设计合理性", "时间复杂度", "代码结构", "可维护性"]
            # },
            # {
            #     "question": "实现一个简单的正则表达式匹配器。支持以下两种通配符：\n'.' 匹配任意单个字符\n'*' 匹配零个或多个前面的元素\n\n实现函数：def is_match(s: str, p: str) -> bool:\n其中s是要匹配的字符串，p是模式。",
            #     "category": "string_algorithm",
            #     "difficulty": "hard",
            #     "language": "Python",
            #     "constraints": ["使用动态规划", "处理边界情况"],
            #     "test_cases": [
            #         {"input": {"s": "aa", "p": "a"}, "output": False},
            #         {"input": {"s": "aa", "p": "a*"}, "output": True},
            #         {"input": {"s": "ab", "p": ".*"}, "output": True},
            #         {"input": {"s": "aab", "p": "c*a*b"}, "output": True},
            #         {"input": {"s": "mississippi", "p": "mis*is*p*."}, "output": False}
            #     ],
            #     "evaluation_criteria": ["算法正确性", "边界情况覆盖", "时间复杂度", "代码可读性"]
            # },
            # {
            #     "question": "实现一个多线程的生产者-消费者模型。要求：\n1. 生产者线程生成数据并放入缓冲区\n2. 消费者线程从缓冲区取出数据\n3. 缓冲区有最大容量限制\n4. 当缓冲区满时，生产者等待；当缓冲区空时，消费者等待\n5. 使用线程安全的队列或锁机制",
            #     "category": "concurrency",
            #     "difficulty": "medium",
            #     "language": "Python",
            #     "constraints": ["线程安全", "避免死锁", "使用queue模块"],
            #     "test_cases": [],
            #     "evaluation_criteria": ["线程安全", "代码清晰", "死锁避免", "资源管理"]
            # },
                {
      "question": "灾后应急通信与资源调度模拟系统：设计一个后端系统，模拟在重大自然灾害（如地震）后，通信部分中断、道路受损情况下的应急信息传递与关键资源（如水、医疗包）调度优化。需实现多智能体（救援队、受灾点）通信、最短路径动态规划（考虑路况变化）和调度优先级算法。",
      "category": "simulation_backend",
      "difficulty": "hard",
      "language": ["Python", "Java 或 Go"],
      "constraints": [
        "必须使用面向对象设计，至少包含地图模块、智能体模块、调度算法模块",
        "最短路径算法需能动态更新权重（如道路损坏程度），时间复杂度不高于O((V+E)logV)",
        "需提供至少两种不同的资源调度策略（如基于优先级队列、基于遗传算法）并进行对比",
        "系统需输出可视化的调度过程动画（可使用matplotlib/pyplot）或实时日志",
        "需编写单元测试，覆盖核心算法，测试覆盖率不低于80%",
        "需考虑并发场景下智能体间的通信模拟"
      ],
      "evaluation_criteria": ["系统架构清晰度", "算法效率与优化能力", "模拟场景的真实性与复杂性", "代码可扩展性与模块化", "测试完备性"]
    },
    {
      "question": "实时金融市场情绪分析与事件检测平台：构建一个数据处理管道，实时爬取或接收新闻、社交媒体文本，运用NLP模型进行情绪分析（正面/负面/中性）和关键金融事件（如财报发布、并购）识别。将结果进行时间序列可视化，并尝试与历史股价波动进行关联性提示（非预测）。",
      "category": "data_science_web",
      "difficulty": "hard",
      "language": ["Python"],
      "constraints": [
        "数据管道必须包含数据采集（至少1个来源，如Twitter API或模拟数据流）、清洗、情感分析、存储和可视化完整流程",
        "情感分析需使用预训练的Transformer模型（如BERT、FinBERT），不得使用简单词典方法",
        "系统需支持实时流式处理（如使用Kafka或RabbitMQ模拟）和批量处理两种模式",
        "前端可视化需使用Web框架（如Streamlit/Dash或Flask+ECharts），展示情感时间序列和事件标记",
        "需建立简单的关联分析模块，计算情感指数与指定股票历史价格的滚动相关系数",
        "所有模块必须容器化（Docker），并提供一键启动脚本"
      ],
      "evaluation_criteria": ["数据处理管道稳定性与实时性", "NLP模型选择与效果", "系统前后端整合度", "可视化清晰度与交互性", "工程化水平（容器化、模块化）"]
    },
    {
      "question": "分布式微服务架构的在线协作白板：实现一个类似Miro的多人实时协作白板核心服务。要求支持多种元素（图形、文字、便签）的实时创建、编辑、删除和同步；使用WebSocket保证低延迟通信；设计微服务（如用户管理、画布服务、实时同步服务、存储服务）并考虑服务发现、通信和最终一致性。",
      "category": "web_development_distributed_systems",
      "difficulty": "hard",
      "language": ["TypeScript/JavaScript (Node.js)", "可选Go或Java用于部分服务"],
      "constraints": [
        "前端必须使用React/Vue等现代框架，实现完整的白板绘制和交互界面",
        "后端至少拆分为3个独立的微服务（例如：认证服务、画布管理服务、实时同步服务），每个服务必须可独立部署",
        "实时同步必须使用WebSocket，并实现操作转换（OT）或CRDT算法解决冲突",
        "需使用消息队列（如Redis Pub/Sub或Kafka）进行服务间通信",
        "必须实现服务发现（如Consul或Eureka）和API网关",
        "数据持久化需支持至少两种存储（如PostgreSQL存储画布元数据，Redis存储会话数据）",
        "需提供压力测试报告，模拟至少100个并发用户同时编辑"
      ],
      "evaluation_criteria": ["实时同步的准确性与性能", "微服务划分合理性", "系统容错与扩展性设计", "前端交互流畅性与用户体验", "分布式事务与一致性处理"]
    },
    {
      "question": "基于强化学习的经典游戏AI对战平台：选择一款经典游戏（如俄罗斯方块、吃豆人、简易星际争霸微操场景），实现其游戏环境，并训练一个强化学习智能体（如使用DQN, PPO等）进行游戏。平台需提供可视化对战界面，允许用户与AI对战，或不同AI之间对战，并记录与展示比赛数据。",
      "category": "ai_gaming",
      "difficulty": "hard",
      "language": ["Python"],
      "constraints": [
        "必须从零实现游戏环境逻辑（可使用Pygame等库进行渲染，但不能直接使用Gym的预置环境）",
        "需实现至少两种不同的强化学习算法（如DQN和PPO）并进行对比",
        "训练过程需支持断点续训，并实时记录训练指标（如奖励曲线）到TensorBoard",
        "平台需提供图形界面，支持人机对战、AI对战、回放功能",
        "需设计一个评估体系，从得分、胜率、策略复杂度等维度评估不同AI",
        "代码必须模块化，清晰分离环境、智能体、训练、评估和前端模块",
        "最终提交的AI在测试集上应达到合理水平（如俄罗斯方块至少能消1000行）"
      ],
      "evaluation_criteria": ["游戏环境模拟的准确性", "强化学习算法实现与训练效果", "平台交互完整度", "代码结构与实验可复现性", "算法创新与优化程度"]
    },
    {
      "question": "物联网设备监控与智能规则引擎：设计一个后端系统，用于接收和处理来自模拟或真实物联网传感器（如温度、湿度、运动）的数据流。系统需实现数据持久化、实时阈值告警，并提供一个规则引擎，允许用户通过图形化界面或DSL自定义复杂的联动规则（如‘当客厅温度>30度且有人移动时，开启空调并发送通知’）。",
      "category": "iot_backend",
      "difficulty": "hard",
      "language": ["Java (Spring Boot) 或 Go"],
      "constraints": [
        "必须实现设备认证与鉴权（如MQTT over TLS或HTTPS），支持至少1000个设备的模拟接入",
        "数据存储需使用时序数据库（如InfluxDB或TimescaleDB）和关系型数据库（如PostgreSQL）",
        "规则引擎需支持至少5种操作符（>, <, =, AND, OR）和自定义函数，规则执行延迟低于1秒",
        "需提供完整的RESTful API用于设备管理和规则管理",
        "必须实现至少两种告警通知方式（如邮件、Webhook）",
        "需提供基于Web的管理界面，支持设备数据可视化（图表）和规则的可视化配置",
        "系统需支持水平扩展，关键组件（如规则引擎）需设计为无状态"
      ],
      "evaluation_criteria": ["数据流处理能力与稳定性", "规则引擎的设计灵活性与表达能力", "系统安全性考虑（设备认证、数据隐私）", "API设计与前端管理界面易用性", "系统扩展性与容错性"]
    }
        ]
        
        for item in sample_problems:
            self.problems.append(Problem(
                question=item["question"],
                answer=item.get("reference_code", ""),
                metadata={
                    "type": "code",
                    "category": item["category"],
                    "difficulty": item["difficulty"],
                    "language": item["language"],
                    "constraints": item["constraints"],
                    "test_cases": item.get("test_cases", []),
                    "evaluation_criteria": item["evaluation_criteria"]
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
        """记录答案，代码问题需要评估正确性"""
        self.total_answered += 1
        
        # 简单的代码正确性检查（在实际应用中应该运行测试用例）
        # 这里仅做示例，实际应该执行代码验证
        if problem.answer and "def" in problem.answer and "def" in answer:
            # 简单检查是否包含必要的函数定义
            self.correct_answers += 1
            return True
        return True  # 暂时总是返回True，实际评估在外部进行

    def evaluate_answer(self, problem: Problem, answer: str) -> bool:
        """评估答案，代码问题返回True（实际评估在外部进行）"""
        return True

    def get_remaining_count(self) -> int:
        """获取剩余问题数量"""
        return len(self.problems)
    
    def get_accuracy(self) -> float:
        """获取准确率"""
        if self.total_answered == 0:
            return 0.0
        return self.correct_answers / self.total_answered
        
    def reset(self):
        """重置问题列表"""
        self.problems.extend(self.used_problems)
        self.used_problems.clear()