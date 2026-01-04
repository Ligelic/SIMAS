from agents.agent_factory import AgentFactory
from chat.chat_manager import ChatManager
from utils.code_provider import CodeProblemProvider
from utils.open_ended_evaluator import OpenEndedEvaluator
from utils.conversation_recorder import ConversationRecorder
from chat.message import Message
from agents.code_llm_agent import CodeLLMAgent
from agents.llm_agent import LLMAgent
from config.config import LLM_MODEL
from typing import Dict, List, Optional, Any, Tuple
import json
from datetime import datetime
import os

class CodeComparison:
    """SIMAS与CoT在代码问题上的比较"""
    
    def __init__(self, evaluator_model: str = None):
        self.chat_manager = ChatManager()
        self.agent_factory = AgentFactory()
        self.evaluator = OpenEndedEvaluator(evaluator_model or LLM_MODEL)
        self.recorder = ConversationRecorder(experiment_type="code_comparison")  # 新增
        
    def run_cot_single_agent(self, problem, agent_mode: int = 0, session_id: str = None) -> Tuple[str, Dict]:
        """运行CoT单智能体"""
        # 创建单智能体
        if agent_mode == 0:
            agent = self.agent_factory.create_agents(1, subject="code", from_file=False)[0]
        else:
            agent = self.agent_factory.create_agents(1, subject="code", from_file=True, mode=agent_mode)[0]
            agent.mode = agent_mode
            
        agent.question_type = problem.metadata.get('type', 'code')
        agent.programming_language = problem.metadata.get('language', 'Python')
        
        # 创建聊天室（仅用于消息传递）
        chat_room = self.chat_manager.create_chat_room(f"CoT_Code_Evaluation_{session_id}", max_round=1)
        
        # 使用增强的CoT提示词
        cot_prompt = self._create_enhanced_cot_prompt(problem)
        enhanced_message = Message(
            sender=agent,
            content=cot_prompt,
            chat_room=chat_room
        )
        
        answer = agent.receive_cot_request(enhanced_message)
        
        # 记录对话历史
        problem_id = f"code_{session_id}"
        conversation = self.recorder.record_cot_conversation(
            problem_id=problem_id,
            problem=problem.question,
            prompt=cot_prompt,
            response=answer,
            metadata={
                "category": problem.metadata.get('category', 'algorithm'),
                "difficulty": problem.metadata.get('difficulty', 'medium'),
                "language": problem.metadata.get('language', 'Python'),
                "agent_name": agent.name,
                "agent_description": agent.description,
                "agent_personality": str(agent.personality)
            }
        )
        
        return answer, conversation
    
    # 修改 run_simas_multi_agent 方法
    def run_simas_multi_agent(self, problem, agent_count: int = 3, rounds: int = 3, agent_mode: int = 0, session_id: str = None) -> Tuple[str, Dict]:
        """运行SIMAS多智能体系统"""
        # 创建聊天室
        chat_room = self.chat_manager.create_chat_room(f"SIMAS_Code_Session_{session_id}", max_round=rounds)
        
        # 创建智能体
        if agent_mode == 0:
            agents = self.agent_factory.create_agents(
                count=agent_count, 
                subject="code",
                from_file=False,
                agent_class=CodeLLMAgent
            )
        else:
            agents = self.agent_factory.create_agents(
                count=agent_count, 
                subject="code",
                from_file=True,
                mode=agent_mode,
                agent_class=CodeLLMAgent
            )
            for agent in agents:
                agent.mode = agent_mode
                agent.question_type = problem.metadata.get('type', 'code')
                agent.programming_language = problem.metadata.get('language', 'Python')
        
        # 添加智能体到聊天室
        for agent in agents:
            chat_room.add_agent(agent)
            agent.question_type = problem.metadata.get('type', 'code')
            agent.programming_language = problem.metadata.get('language', 'Python')
        
        # 开始讨论
        chat_room.metadata['current_problem'] = problem
        
        # 第一轮开始
        self.chat_manager.send_message(
            room_name=chat_room.name,
            sender=agents[0],
            content=f"让我们讨论这个代码问题：\n\n{problem.question}\n\n编程语言：{problem.metadata.get('language', 'Python')}\n\n限制条件：{problem.metadata.get('constraints', [])}请分享你的解决方案。"
        )
            
        # 获取最终答案
        final_answer = chat_room.final_answer
        
        # 记录对话历史
        problem_id = f"code_{session_id}"
        conversation = self.recorder.record_mas_conversation(
            problem_id=problem_id,
            problem=problem.question,
            chat_room=chat_room,
            metadata={
                "category": problem.metadata.get('category', 'algorithm'),
                "difficulty": problem.metadata.get('difficulty', 'medium'),
                "language": problem.metadata.get('language', 'Python'),
                "agent_count": agent_count,
                "rounds": rounds,
                "agent_names": [agent.name for agent in agents],
                "agent_descriptions": [agent.description for agent in agents]
            }
        )
        
        return final_answer, conversation
    
    def _create_enhanced_cot_prompt(self, problem) -> str:
        """创建增强的CoT提示词，针对代码问题优化"""
        language = problem.metadata.get('language', 'Python')
        constraints = problem.metadata.get('constraints', [])
        constraints_str = "\n".join([f"- {constraint}" for constraint in constraints]) if constraints else "无特殊约束"
        
#         return f"""请解决以下代码问题。请使用逐步推理的方法，并提供完整、高效的代码解决方案。

# 问题：
# {problem.question}

# 编程语言：{language}
# 约束条件：
# {constraints_str}

# 请按照以下步骤进行思考：
# 1. 理解问题：明确输入、输出和约束条件
# 2. 设计算法：分析可能的算法，选择最优方案
# 3. 考虑边界情况：识别并处理所有边界情况
# 4. 编写代码：提供完整、可运行的代码实现
# 5. 测试验证：设计测试用例验证代码正确性
# 6. 复杂度分析：分析时间和空间复杂度

# 你的解决方案应该：
# - 完全满足问题要求
# - 代码清晰、可读性强
# - 高效且正确
# - 包含必要的注释

# 请以以下格式组织你的回答：
# ### 问题分析
# [你的分析]

# ### 算法设计
# [选择的算法和理由]

# ### 代码实现
# [完整的代码实现]

# ### 复杂度分析
# [时间复杂度和空间复杂度]

# ### 测试用例
# [验证代码的测试用例]

# ### 最终代码
# [完整的代码解决方案]
# """
        return f"""请解决以下代码问题。请使用逐步推理的方法，并提供完整、高效的代码解决方案。

问题：
{problem.question}

编程语言：{language}
约束条件：
{constraints_str}


你的解决方案应该：
- 完全满足问题要求
- 代码清晰、可读性强
- 高效且正确
- 包含必要的注释

请以以下格式组织你的回答：
### 推理过程
[你的分析]

### 最终代码
[完整的代码解决方案]
"""
    
    def compare_methods(self, problem, cot_answer: str, simas_answer: str) -> Dict:
        """比较两种方法的答案"""
        # 使用代码特定的评估标准
        default_criteria = ["正确性", "代码质量", "效率", "可读性", "鲁棒性", "完整性"]
        criteria = problem.metadata.get('evaluation_criteria', default_criteria)
        
        comparison = self.evaluator.compare_answers(
            problem=problem.question,
            answer_a=cot_answer,
            answer_b=simas_answer,
            method_a="CoT单智能体",
            method_b="SIMAS多智能体",
            criteria=criteria
        )
        
        return comparison
    
    def run_experiment(self, problem_count: int = 5, agent_count: int = 3, 
                      rounds: int = 3, experiment_count: int = 1) -> Dict:
        """运行完整实验"""
        problem_provider = CodeProblemProvider(total_problems=problem_count)
        
        results = {
            "experiment_info": {
                "model": LLM_MODEL,
                "agent_count": agent_count,
                "rounds": rounds,
                "problem_count": problem_count,
                "experiment_count": experiment_count,
                "subject": "code"
            },
            "per_problem_results": [],
            "summary": {
                "cot_wins": 0,
                "simas_wins": 0,
                "ties": 0,
                "avg_cot_score": 0,
                "avg_simas_score": 0
            }
        }
        
        total_cot_score = 0
        total_simas_score = 0
        comparison_results = []  # 用于保存比较结果
        
        for exp_num in range(experiment_count):
            print(f"\n=== 代码问题实验 {exp_num+1}/{experiment_count} ===")
            
            problem_provider.reset()
            
            for i in range(min(problem_count, len(problem_provider.problems) + len(problem_provider.used_problems))):
                problem = problem_provider.get_next_problem()
                if not problem:
                    break
                    
                print(f"\n--- 代码问题 {i+1} ---")
                print(f"问题: {problem.question[:100]}...")
                print(f"类别: {problem.metadata.get('category', 'N/A')}")
                print(f"难度: {problem.metadata.get('difficulty', 'N/A')}")
                print(f"语言: {problem.metadata.get('language', 'N/A')}")
                
                # 运行CoT单智能体
                print("\n运行CoT单智能体...")
                cot_answer, cot_conversation = self.run_cot_single_agent(problem, session_id=f"{exp_num}_{i}")
                print(f"CoT答案长度: {len(cot_answer)} 字符")
                self.agent_factory.clear_agents()
                
                # 运行SIMAS多智能体
                print("\n运行SIMAS多智能体...")
                simas_answer, mas_conversation = self.run_simas_multi_agent(problem, agent_count=agent_count, rounds=rounds, session_id=f"{exp_num}_{i}")
                print(f"SIMAS答案长度: {len(simas_answer)} 字符")
                
                # 比较答案
                print("\n比较答案...")
                comparison = self.compare_methods(problem, cot_answer, simas_answer)
                self.agent_factory.clear_agents()
                
                # 记录比较结果
                problem_id = f"code_{exp_num}_{i}"
                comparison_result = self.recorder.record_comparison_result(
                    problem_id=problem_id,
                    problem=problem.question,
                    cot_conversation=cot_conversation,
                    mas_conversation=mas_conversation,
                    comparison_result=comparison,
                    metadata={
                        "category": problem.metadata.get('category', 'algorithm'),
                        "difficulty": problem.metadata.get('difficulty', 'medium'),
                        "language": problem.metadata.get('language', 'Python'),
                        "experiment": exp_num + 1,
                        "problem_index": i
                    }
                )
                comparison_results.append(comparison_result)

                # 记录结果
                problem_result = {
                    "problem_index": i,
                    "problem": problem.question[:200],
                    "category": problem.metadata.get('category', 'algorithm'),
                    "difficulty": problem.metadata.get('difficulty', 'medium'),
                    "language": problem.metadata.get('language', 'Python'),
                    "cot_answer_preview": self._extract_code_preview(cot_answer, 200),
                    "simas_answer_preview": self._extract_code_preview(simas_answer, 200),
                    "comparison": comparison
                }
                
                results["per_problem_results"].append(problem_result)
                
                # 更新统计
                cot_score = comparison.get("answer_a_scores", {}).get("total", 0)
                simas_score = comparison.get("answer_b_scores", {}).get("total", 0)
                
                total_cot_score += cot_score
                total_simas_score += simas_score
                
                winner = comparison.get("comparison", {}).get("winner", "unknown")
                if winner == "A":
                    results["summary"]["cot_wins"] += 1
                elif winner == "B":
                    results["summary"]["simas_wins"] += 1
                elif winner == "tie":
                    results["summary"]["ties"] += 1
                    
                print(f"CoT得分: {cot_score:.2f}, SIMAS得分: {simas_score:.2f}, 胜者: {winner}")
        
        # 计算平均值
        if problem_count > 0:
            results["summary"]["avg_cot_score"] = total_cot_score / problem_count
            results["summary"]["avg_simas_score"] = total_simas_score / problem_count
        
        return results
    
    def _extract_code_preview(self, text: str, max_length: int) -> str:
        """提取代码预览"""
        import re
        
        # 尝试提取代码块
        code_pattern = r"```(?:python|python3)?\n(.*?)\n```"
        matches = re.findall(code_pattern, text, re.DOTALL)
        
        if matches:
            code = matches[0]
            if len(code) > max_length:
                return code[:max_length] + "..."
            return code
        else:
            # 如果没有找到代码块，返回文本预览
            if len(text) > max_length:
                return text[:max_length] + "..."
            return text
    
    def save_results(self, results: Dict):
        """保存实验结果"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_dir = f"evaluate_result/code_comparison"
        os.makedirs(result_dir, exist_ok=True)
        
        filename = f"code_comparison_{timestamp}.json"
        filepath = os.path.join(result_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
            
        # 同时保存简化的文本报告
        txt_filepath = os.path.join(result_dir, f"code_comparison_{timestamp}_summary.txt")
        with open(txt_filepath, 'w', encoding='utf-8') as f:
            f.write("=== SIMAS vs CoT 代码问题比较实验 ===\n\n")
            f.write(f"模型: {results['experiment_info']['model']}\n")
            f.write(f"智能体数量: {results['experiment_info']['agent_count']}\n")
            f.write(f"讨论轮次: {results['experiment_info']['rounds']}\n")
            f.write(f"问题数量: {results['experiment_info']['problem_count']}\n")
            f.write(f"实验次数: {results['experiment_info']['experiment_count']}\n")
            f.write(f"主题: {results['experiment_info']['subject']}\n\n")
            
            f.write("=== 总结 ===\n")
            f.write(f"CoT单智能体平均得分: {results['summary']['avg_cot_score']:.2f}\n")
            f.write(f"SIMAS多智能体平均得分: {results['summary']['avg_simas_score']:.2f}\n")
            f.write(f"CoT获胜次数: {results['summary']['cot_wins']}\n")
            f.write(f"SIMAS获胜次数: {results['summary']['simas_wins']}\n")
            f.write(f"平局次数: {results['summary']['ties']}\n\n")
            
            f.write("=== 详细结果 ===\n")
            for i, problem_result in enumerate(results['per_problem_results']):
                f.write(f"\n问题 {i+1}:\n")
                f.write(f"类别: {problem_result['category']}\n")
                f.write(f"难度: {problem_result['difficulty']}\n")
                f.write(f"语言: {problem_result['language']}\n")
                f.write(f"CoT代码预览: {problem_result['cot_answer_preview']}\n")
                f.write(f"SIMAS代码预览: {problem_result['simas_answer_preview']}\n")
                comparison = problem_result.get('comparison', {})
                if isinstance(comparison, dict):
                    cot_score = comparison.get('answer_a_scores', {}).get('total', 0)
                    simas_score = comparison.get('answer_b_scores', {}).get('total', 0)
                    winner = comparison.get('comparison', {}).get('winner', 'unknown')
                    f.write(f"得分: CoT={cot_score:.2f}, SIMAS={simas_score:.2f}, 胜者={winner}\n")
        
        # 保存对话历史
        conv_files = self.recorder.save_conversations(
            experiment_info=results["experiment_info"],
            output_dir=f"evaluate_result/conversations/code_comparison"
        )

        print(f"结果已保存到: {filepath}")
        print(f"总结报告已保存到: {txt_filepath}")
        
        return filepath, txt_filepath

def main_code_comparison():
    """主函数：运行SIMAS与CoT的代码问题比较实验"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SIMAS vs CoT 代码问题比较实验')
    parser.add_argument('--problems', type=int, default=5, help='问题数量')
    parser.add_argument('--agents', type=int, default=3, help='智能体数量')
    parser.add_argument('--rounds', type=int, default=3, help='讨论轮次')
    parser.add_argument('--experiments', type=int, default=1, help='实验次数')
    parser.add_argument('--model', type=str, default=None, help='评估器模型')
    
    args = parser.parse_args()
    
    print("=== SIMAS vs CoT 代码问题比较实验 ===")
    print(f"问题数量: {args.problems}")
    print(f"智能体数量: {args.agents}")
    print(f"讨论轮次: {args.rounds}")
    print(f"实验次数: {args.experiments}")
    
    comparison = CodeComparison(evaluator_model=args.model)
    results = comparison.run_experiment(
        problem_count=args.problems,
        agent_count=args.agents,
        rounds=args.rounds,
        experiment_count=args.experiments
    )
    
    comparison.save_results(results)
    
    print("\n=== 实验完成 ===")
    print(f"CoT单智能体平均得分: {results['summary']['avg_cot_score']:.2f}")
    print(f"SIMAS多智能体平均得分: {results['summary']['avg_simas_score']:.2f}")
    print(f"CoT获胜次数: {results['summary']['cot_wins']}")
    print(f"SIMAS获胜次数: {results['summary']['simas_wins']}")
    print(f"平局次数: {results['summary']['ties']}")

if __name__ == "__main__":
    main_code_comparison()