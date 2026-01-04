import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from chat.message import Message
from chat.chat_room import ChatRoom

class DateTimeEncoder(json.JSONEncoder):
    """自定义JSON编码器，支持datetime对象序列化"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

class ConversationRecorder:
    """对话历史记录器"""
    
    def __init__(self, experiment_type: str = "comparison"):
        self.experiment_type = experiment_type
        self.conversations: List[Dict] = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def _convert_datetime_to_str(self, obj: Any) -> Any:
        """递归地将datetime对象转换为字符串"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {k: self._convert_datetime_to_str(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_datetime_to_str(item) for item in obj]
        elif hasattr(obj, '__dict__'):
            # 如果是对象，尝试转换为字典
            return self._convert_datetime_to_str(obj.__dict__)
        else:
            return obj
    
    def record_cot_conversation(self, 
                                problem_id: str,
                                problem: str,
                                prompt: str,
                                response: str,
                                metadata: Dict = None) -> Dict:
        """记录CoT对话历史"""
        
        conversation = {
            "method": "CoT",
            "problem_id": problem_id,
            "problem": problem[:500] + "..." if len(problem) > 500 else problem,
            "prompt": prompt,
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "metadata": self._convert_datetime_to_str(metadata or {})
        }
        
        self.conversations.append(conversation)
        return conversation
    
    def record_mas_conversation(self,
                               problem_id: str,
                               problem: str,
                               chat_room: ChatRoom,
                               metadata: Dict = None) -> Dict:
        """记录多智能体对话历史"""
        
        # 从聊天室提取消息，确保所有datetime对象都被转换
        messages = []
        for msg in chat_room.messages:
            # 处理sender，确保它是字符串或可序列化的对象
            sender_name = "System"
            sender_type = "System"
            
            if msg.sender:
                if hasattr(msg.sender, 'name'):
                    sender_name = str(msg.sender.name)
                else:
                    sender_name = str(msg.sender)
                
                if hasattr(msg.sender, '__class__'):
                    sender_type = msg.sender.__class__.__name__
            
            # 处理timestamp
            timestamp = getattr(msg, 'timestamp', datetime.now())
            if isinstance(timestamp, datetime):
                timestamp_str = timestamp.isoformat()
            else:
                timestamp_str = str(timestamp)
            
            message_data = {
                "round": getattr(msg, 'round', 0),
                "sender": sender_name,
                "sender_type": sender_type,
                "content": str(msg.content) if msg.content else "",
                "timestamp": timestamp_str
            }
            messages.append(message_data)
        
        # 提取轮次历史
        round_history = []
        for i, history in enumerate(chat_room.current_round_history):
            if history:
                round_history.append({
                    "round": i + 1,
                    "content": str(history)
                })
        
        # 确保所有智能体信息都是字符串
        agent_names = []
        for agent in chat_room.agents:
            if hasattr(agent, 'name'):
                agent_names.append(str(agent.name))
            else:
                agent_names.append(str(agent))
        
        conversation = {
            "method": "MAS",
            "problem_id": problem_id,
            "problem": problem[:500] + "..." if len(problem) > 500 else problem,
            "agent_count": len(chat_room.agents),
            "agent_names": agent_names,
            "rounds": chat_room.max_rounds,
            "messages": messages,
            "round_history": round_history,
            "final_answer": str(chat_room.final_answer) if chat_room.final_answer else "",
            "timestamp": datetime.now().isoformat(),
            "metadata": self._convert_datetime_to_str(metadata or {})
        }
        
        self.conversations.append(conversation)
        return conversation
    
    def record_comparison_result(self,
                                problem_id: str,
                                problem: str,
                                cot_conversation: Dict,
                                mas_conversation: Dict,
                                comparison_result: Dict,
                                metadata: Dict = None) -> Dict:
        """记录比较结果"""
        
        # 确保所有数据都是可序列化的
        safe_comparison_result = self._convert_datetime_to_str(comparison_result)
        
        # 提取cot_response，确保是字符串
        cot_response = cot_conversation.get("response", "")
        if not isinstance(cot_response, str):
            cot_response = str(cot_response)
        
        # 提取mas_final_answer，确保是字符串
        mas_final_answer = mas_conversation.get("final_answer", "")
        if not isinstance(mas_final_answer, str):
            mas_final_answer = str(mas_final_answer)
        
        comparison = {
            "method": "comparison",
            "problem_id": problem_id,
            "problem": problem[:500] + "..." if len(problem) > 500 else problem,
            "cot_summary": {
                "answer_preview": cot_response[:200] + "..." 
                    if len(cot_response) > 200 
                    else cot_response,
                "full_conversation_id": str(cot_conversation.get("conversation_id", "")),
                "score": safe_comparison_result.get("answer_a_scores", {}).get("total", 0)
            },
            "mas_summary": {
                "answer_preview": mas_final_answer[:200] + "..." 
                    if len(mas_final_answer) > 200 
                    else mas_final_answer,
                "full_conversation_id": str(mas_conversation.get("conversation_id", "")),
                "score": safe_comparison_result.get("answer_b_scores", {}).get("total", 0)
            },
            "comparison": {
                "winner": safe_comparison_result.get("comparison", {}).get("winner", "unknown"),
                "reason": safe_comparison_result.get("comparison", {}).get("reason", ""),
                "cot_advantages": safe_comparison_result.get("comparison", {}).get("advantages_a", []),
                "mas_advantages": safe_comparison_result.get("comparison", {}).get("advantages_b", [])
            },
            "timestamp": datetime.now().isoformat(),
            "metadata": self._convert_datetime_to_str(metadata or {})
        }
        
        self.conversations.append(comparison)
        return comparison
    
    def save_conversations(self, experiment_info: Dict = None, output_dir: str = None):
        """保存所有对话历史到文件"""
        
        if output_dir is None:
            output_dir = f"evaluate_result/conversations/{self.experiment_type}"
        
        os.makedirs(output_dir, exist_ok=True)
        
        # 为每个对话生成唯一ID
        for i, conv in enumerate(self.conversations):
            conv["conversation_id"] = f"{self.timestamp}_{self.experiment_type}_{i}"
        
        # 确保所有对话数据都是可序列化的
        serializable_conversations = self._convert_datetime_to_str(self.conversations)
        
        # 保存详细对话
        detailed_file = os.path.join(output_dir, f"conversations_{self.timestamp}.json")
        with open(detailed_file, 'w', encoding='utf-8') as f:
            json.dump({
                "experiment_info": self._convert_datetime_to_str(experiment_info or {}),
                "timestamp": self.timestamp,
                "conversation_count": len(self.conversations),
                "conversations": serializable_conversations
            }, f, ensure_ascii=False, indent=2, cls=DateTimeEncoder)
        
        # 保存简化的对话摘要
        summary_file = os.path.join(output_dir, f"summary_{self.timestamp}.json")
        summary = self._create_summary()
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(self._convert_datetime_to_str(summary), f, ensure_ascii=False, indent=2, cls=DateTimeEncoder)
        
        # 保存纯文本版本
        text_file = os.path.join(output_dir, f"conversations_{self.timestamp}.txt")
        self._save_as_text(text_file, experiment_info)
        
        print(f"对话历史已保存:")
        print(f"  详细对话: {detailed_file}")
        print(f"  对话摘要: {summary_file}")
        print(f"  文本版本: {text_file}")
        
        return detailed_file, summary_file, text_file
    
    def _create_summary(self) -> Dict:
        """创建对话摘要"""
        
        summary = {
            "timestamp": self.timestamp,
            "total_conversations": len(self.conversations),
            "cot_count": sum(1 for conv in self.conversations if conv.get("method") == "CoT"),
            "mas_count": sum(1 for conv in self.conversations if conv.get("method") == "MAS"),
            "comparison_count": sum(1 for conv in self.conversations if conv.get("method") == "comparison"),
            "unique_problems": len(set(str(conv.get("problem_id", "")) for conv in self.conversations)),
            "conversations_by_type": {},
            "problems": []
        }
        
        # 按问题组织对话
        problem_dict = {}
        for conv in self.conversations:
            problem_id = str(conv.get("problem_id", "unknown"))
            if problem_id not in problem_dict:
                problem_dict[problem_id] = {
                    "problem_id": problem_id,
                    "problem": conv.get("problem", ""),
                    "cot_conversation": None,
                    "mas_conversation": None,
                    "comparison": None
                }
            
            method = conv.get("method", "unknown")
            if method == "CoT":
                problem_dict[problem_id]["cot_conversation"] = conv
            elif method == "MAS":
                problem_dict[problem_id]["mas_conversation"] = conv
            elif method == "comparison":
                problem_dict[problem_id]["comparison"] = conv
        
        summary["problems"] = list(problem_dict.values())
        
        return summary
    
    def _save_as_text(self, filepath: str, experiment_info: Dict = None):
        """将对话保存为纯文本格式"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("CoT与MAS对话历史记录\n")
            f.write("=" * 80 + "\n\n")
            
            if experiment_info:
                f.write("实验信息:\n")
                for key, value in experiment_info.items():
                    f.write(f"  {key}: {value}\n")
                f.write("\n")
            
            f.write(f"总对话数: {len(self.conversations)}\n")
            f.write(f"生成时间: {self.timestamp}\n\n")
            
            # 按问题分组显示
            problems = {}
            for conv in self.conversations:
                problem_id = str(conv.get("problem_id", "unknown"))
                if problem_id not in problems:
                    problems[problem_id] = {"CoT": [], "MAS": [], "comparison": []}
                
                method = conv.get("method", "unknown")
                if method in ["CoT", "MAS", "comparison"]:
                    problems[problem_id][method].append(conv)
            
            for problem_id, convs in problems.items():
                f.write("\n" + "=" * 60 + "\n")
                f.write(f"问题ID: {problem_id}\n")
                
                # 显示问题
                if convs["CoT"]:
                    problem = convs["CoT"][0].get("problem", "N/A")
                    f.write(f"问题: {problem}\n")
                
                f.write("-" * 60 + "\n")
                
                # CoT对话
                if convs["CoT"]:
                    cot = convs["CoT"][0]
                    f.write("CoT单智能体对话:\n")
                    f.write(f"  提示词: {cot.get('prompt', 'N/A')[:100]}...\n")
                    f.write(f"  回答: {cot.get('response', 'N/A')[:200]}...\n")
                    f.write(f"  时间: {cot.get('timestamp', 'N/A')}\n")
                
                # MAS对话
                if convs["MAS"]:
                    mas = convs["MAS"][0]
                    f.write("\nMAS多智能体对话:\n")
                    f.write(f"  智能体数: {mas.get('agent_count', 'N/A')}\n")
                    f.write(f"  智能体: {', '.join(mas.get('agent_names', []))}\n")
                    f.write(f"  轮次: {mas.get('rounds', 'N/A')}\n")
                    f.write(f"  最终答案: {mas.get('final_answer', 'N/A')[:200]}...\n")
                    
                    # 显示消息统计
                    messages = mas.get('messages', [])
                    f.write(f"  总消息数: {len(messages)}\n")
                    
                    # 按发送者统计
                    sender_stats = {}
                    for msg in messages:
                        sender = msg.get('sender', 'Unknown')
                        sender_stats[sender] = sender_stats.get(sender, 0) + 1
                    
                    f.write("  消息分布:\n")
                    for sender, count in sender_stats.items():
                        f.write(f"    {sender}: {count}条\n")
                
                # 比较结果
                if convs["comparison"]:
                    comp = convs["comparison"][0]
                    f.write("\n比较结果:\n")
                    cot_score = comp.get('cot_summary', {}).get('score', 0)
                    mas_score = comp.get('mas_summary', {}).get('score', 0)
                    winner = comp.get('comparison', {}).get('winner', 'unknown')
                    winner_map = {"A": "CoT", "B": "MAS", "tie": "平局"}
                    f.write(f"  CoT得分: {cot_score:.2f}\n")
                    f.write(f"  MAS得分: {mas_score:.2f}\n")
                    f.write(f"  胜者: {winner_map.get(winner, winner)}\n")
                
                f.write("=" * 60 + "\n")