from agents.agent_factory import AgentFactory
from chat.chat_manager import ChatManager
from utils.open_ended_provider import OpenEndedProblemProvider
from utils.open_ended_evaluator import OpenEndedEvaluator
from utils.saver import save_evaluation_result
from utils.conversation_recorder import ConversationRecorder
from chat.message import Message
from agents.open_ended_llm_agent import OpenEndedLLMAgent
from config.config import LLM_MODEL
from typing import Dict, List, Optional, Any, Tuple, Tuple
import json
from datetime import datetime
import os

class OpenEndedComparison:
    """SIMAS与CoT在开放性问题上的比较"""
    
    def __init__(self, evaluator_model: str = None):
        self.chat_manager = ChatManager()
        self.agent_factory = AgentFactory()
        self.evaluator = OpenEndedEvaluator(evaluator_model or LLM_MODEL)
        self.recorder = ConversationRecorder(experiment_type="open_ended_comparison")  # 新增
        
    def run_cot_single_agent(self, problem, agent_mode: int = 0, session_id: str = None) -> Tuple[str, Dict]:
        """运行CoT单智能体"""
        from agents.llm_agent import LLMAgent
        
        # 创建单智能体
        if agent_mode == 0:
            agent = self.agent_factory.create_agents(1, subject="open_ended", from_file=False)[0]
        else:
            agent = self.agent_factory.create_agents(1, subject="open_ended", from_file=True, mode=agent_mode)[0]
            agent.mode = agent_mode
            
        agent.question_type = problem.metadata.get('type', 'open_ended')
        
        # 创建聊天室（仅用于消息传递）
        chat_room = self.chat_manager.create_chat_room(f"CoT_Evaluation_{session_id}", max_round=1)
        
        # 使用增强的CoT提示词
        cot_prompt = self._create_enhanced_cot_prompt(problem)
        enhanced_message = Message(
            sender=agent,
            content=cot_prompt,
            chat_room=chat_room
        )
        
        answer = agent.receive_cot_request(enhanced_message)
        
        # 记录对话历史
        problem_id = f"open_ended_{session_id}"
        conversation = self.recorder.record_cot_conversation(
            problem_id=problem_id,
            problem=problem.question,
            prompt=cot_prompt,
            response=answer,
            metadata={
                "category": problem.metadata.get('category', 'general'),
                "difficulty": problem.metadata.get('difficulty', 'medium'),
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
        chat_room = self.chat_manager.create_chat_room(f"SIMAS_Session_{session_id}", max_round=rounds)
        
        # 创建智能体
        if agent_mode == 0:
            agents = self.agent_factory.create_agents(
                count=agent_count, 
                subject="open_ended",
                from_file=False,
                agent_class=OpenEndedLLMAgent
            )
        else:
            agents = self.agent_factory.create_agents(
                count=agent_count, 
                subject="open_ended",
                from_file=True,
                mode=agent_mode,
                agent_class=OpenEndedLLMAgent
            )
            for agent in agents:
                agent.mode = agent_mode
                agent.question_type = problem.metadata.get('type', 'open_ended')
        
        # 添加智能体到聊天室
        for agent in agents:
            chat_room.add_agent(agent)
            agent.question_type = problem.metadata.get('type', 'open_ended')
        
        # 开始讨论
        chat_room.metadata['current_problem'] = problem
        
        # 第一轮开始
        self.chat_manager.send_message(
            room_name=chat_room.name,
            sender=agents[0],
            content=f"让我们讨论这个问题：\n\n{problem.question}\n\n请分享你的想法。"
        )
            
        # 获取最终答案
        final_answer = chat_room.final_answer
        
        # 记录对话历史
        problem_id = f"open_ended_{session_id}"
        conversation = self.recorder.record_mas_conversation(
            problem_id=problem_id,
            problem=problem.question,
            chat_room=chat_room,
            metadata={
                "category": problem.metadata.get('category', 'general'),
                "difficulty": problem.metadata.get('difficulty', 'medium'),
                "agent_count": agent_count,
                "rounds": rounds,
                "agent_names": [agent.name for agent in agents],
                "agent_descriptions": [agent.description for agent in agents]
            }
        )
        
        return final_answer, conversation
    
    def _create_enhanced_cot_prompt(self, problem) -> str:
        """创建增强的CoT提示词，针对开放性问题优化"""
        criteria = problem.metadata.get('criteria', [])
        criteria_str = "\n".join([f"- {criterion}" for criterion in criteria]) if criteria else "无特定标准"
        
#         return f"""请深入分析以下开放性问题。请使用逐步推理的方法，并提供全面、深入的回答。

# 问题：
# {problem.question}

# 评估标准：
# {criteria_str}

# 请按照以下步骤进行思考：
# 1. 理解问题：解释问题的核心是什么，涉及哪些关键概念
# 2. 多角度分析：从至少三个不同角度分析问题
# 3. 深度探索：深入探讨每个角度的细节和影响
# 4. 提出解决方案：基于分析提出具体、可行的建议
# 5. 评估与反思：评估你的建议，考虑潜在挑战和改进空间

# 你的回答应该：
# - 全面且深入
# - 结构清晰
# - 有创新性和实用性
# - 符合评估标准

# 请以以下格式组织你的回答：
# ### 问题理解
# [你的分析]

# ### 多角度分析
# 1. [角度1]
# 2. [角度2]
# 3. [角度3]

# ### 深度探索
# [对每个角度的深入分析]

# ### 解决方案
# [具体建议和方案]

# ### 最终回答
# [对问题的直接、综合回答]
# """
        return f"""请深入分析以下开放性问题。请使用逐步推理的方法，并提供全面、深入的回答。

问题：
{problem.question}

评估标准：
{criteria_str}

你的回答应该：
- 全面且深入
- 结构清晰
- 有创新性和实用性
- 符合评估标准

请以以下格式组织你的回答：
### 推理过程
[你的分析]

### 最终回答
[对问题的直接、综合回答]
"""
    
    def compare_methods(self, problem, cot_answer: str, simas_answer: str) -> Dict:
        """比较两种方法的答案"""
        criteria = problem.metadata.get('criteria', ["相关性", "深度", "逻辑性", "创新性", "可行性", "全面性"])
        
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
        problem_provider = OpenEndedProblemProvider(total_problems=problem_count)
        
        results = {
            "experiment_info": {
                "model": LLM_MODEL,
                "agent_count": agent_count,
                "rounds": rounds,
                "problem_count": problem_count,
                "experiment_count": experiment_count
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
        
        for exp_num in range(experiment_count):
            print(f"\n=== 实验 {exp_num+1}/{experiment_count} ===")
            
            problem_provider.reset()
            
            for i in range(min(problem_count, len(problem_provider.problems) + len(problem_provider.used_problems))):
                problem = problem_provider.get_next_problem()
                if not problem:
                    break
                    
                print(f"\n--- 问题 {i+1} ---")
                print(f"问题: {problem.question[:100]}...")
                print(f"类别: {problem.metadata.get('category', 'N/A')}")
                
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
                problem_id = f"open_ended_{exp_num}_{i}"
                comparison_result = self.recorder.record_comparison_result(
                    problem_id=problem_id,
                    problem=problem.question,
                    cot_conversation=cot_conversation,
                    mas_conversation=mas_conversation,
                    comparison_result=comparison,
                    metadata={
                        "category": problem.metadata.get('category', 'general'),
                        "difficulty": problem.metadata.get('difficulty', 'medium'),
                        "experiment": exp_num + 1,
                        "problem_index": i
                    }
                )
                
                # 记录结果
                problem_result = {
                    "problem_index": i,
                    "problem": problem.question[:200],
                    "category": problem.metadata.get('category', 'general'),
                    "cot_answer_preview": cot_answer[:200] + "..." if len(cot_answer) > 200 else cot_answer,
                    "simas_answer_preview": simas_answer[:200] + "..." if len(simas_answer) > 200 else simas_answer,
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
    
    # 修改 save_results 方法
    def save_results(self, results: Dict, subject: str = "open_ended"):
        """保存实验结果和对话历史"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_dir = f"evaluate_result/open_ended_comparison"
        os.makedirs(result_dir, exist_ok=True)
        
        filename = f"comparison_{timestamp}.json"
        filepath = os.path.join(result_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
            
        # 同时保存简化的文本报告
        txt_filepath = os.path.join(result_dir, f"comparison_{timestamp}_summary.txt")
        with open(txt_filepath, 'w', encoding='utf-8') as f:
            f.write("=== SIMAS vs CoT 开放性问题比较实验 ===\n\n")
            f.write(f"模型: {results['experiment_info']['model']}\n")
            f.write(f"智能体数量: {results['experiment_info']['agent_count']}\n")
            f.write(f"讨论轮次: {results['experiment_info']['rounds']}\n")
            f.write(f"问题数量: {results['experiment_info']['problem_count']}\n")
            f.write(f"实验次数: {results['experiment_info']['experiment_count']}\n\n")
            
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
                f.write(f"CoT预览: {problem_result['cot_answer_preview']}\n")
                f.write(f"SIMAS预览: {problem_result['simas_answer_preview']}\n")
                comparison = problem_result.get('comparison', {})
                if isinstance(comparison, dict):
                    cot_score = comparison.get('answer_a_scores', {}).get('total', 0)
                    simas_score = comparison.get('answer_b_scores', {}).get('total', 0)
                    winner = comparison.get('comparison', {}).get('winner', 'unknown')
                    f.write(f"得分: CoT={cot_score:.2f}, SIMAS={simas_score:.2f}, 胜者={winner}\n")
        
        # 保存对话历史
        conv_files = self.recorder.save_conversations(
            experiment_info=results["experiment_info"],
            output_dir=f"evaluate_result/conversations/open_ended_comparison"
        )
        
        print(f"实验结果已保存到: {filepath}")
        print(f"总结报告已保存到: {txt_filepath}")
        
        return {
            "results_file": filepath,
            "summary_file": txt_filepath,
            "conversation_files": conv_files
        }

def main_comparison():
    """主函数：运行SIMAS与CoT的比较实验"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SIMAS vs CoT 开放性问题比较实验')
    parser.add_argument('--problems', type=int, default=15, help='问题数量')
    parser.add_argument('--agents', type=int, default=3, help='智能体数量')
    parser.add_argument('--rounds', type=int, default=3, help='讨论轮次')
    parser.add_argument('--experiments', type=int, default=1, help='实验次数')
    parser.add_argument('--model', type=str, default=None, help='评估器模型')
    
    args = parser.parse_args()
    
    print("=== SIMAS vs CoT 开放性问题比较实验 ===")
    print(f"问题数量: {args.problems}")
    print(f"智能体数量: {args.agents}")
    print(f"讨论轮次: {args.rounds}")
    print(f"实验次数: {args.experiments}")
    
    comparison = OpenEndedComparison(evaluator_model=args.model)
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
    main_comparison()