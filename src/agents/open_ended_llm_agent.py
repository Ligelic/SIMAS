from agents.llm_agent import LLMAgent
from chat.message import Message
from typing import List

class OpenEndedLLMAgent(LLMAgent):
    """针对开放性问题的LLM Agent扩展"""
    
    def generate_open_ended_prompt(self, message: Message) -> str:
        """为开放性问题生成提示词"""
        chat_room = getattr(message, 'chat_room', None)
        others_desc = self.format_others_description(chat_room) if chat_room else ""
        
        # 获取问题类型（从chat_room的metadata或消息中）
        question_type = getattr(self, 'question_type', 'open_ended')
        
        prompt = f"""你正在参与一个开放性问题的讨论。请基于你的专业知识和经验提供深入的见解。

你的角色：{self.name}
个性：{self.personality.value}
专长：{self.description}

当前讨论的问题类型：{question_type}

请特别注意：
1. 提供有深度的分析和见解
2. 考虑问题的多个方面和视角
3. 提出具体的、可行的建议
4. 如果适用，使用创新性思维
5. 在讨论中引用他人的观点并进行建设性互动

对话历史：
{others_desc if others_desc else "这是讨论的开始"}

当前消息：
{message.content}

请按照以下格式回应：
### 反思：简要总结你的思考过程
### 核心观点：陈述你的主要观点
### 详细分析：提供详细的分析和论证
### 具体建议：如果适用，提出具体建议
### 回应：对其他参与者的观点进行回应

注意：保持专业、深入，并体现你作为{self.name}的特点。
"""
        return prompt
    
    def generate_final_open_ended_summary(self, message: Message, final_round_messages: List[Message]) -> str:
        """为开放性问题生成最终总结提示词"""
        final_messages = "\n".join([
            f"{msg.sender.name}: {msg.content}" 
            for msg in final_round_messages
        ])
        
        return f"""作为讨论的总结者，请基于以下讨论内容提供一个全面的总结。

讨论摘要：
{final_messages}

问题类型：{getattr(self, 'question_type', 'open_ended')}

请提供：
1. 主要观点汇总
2. 达成的共识（如果有）
3. 存在的分歧和不同视角
4. 关键建议和见解
5. 未来方向或下一步建议

你的总结应该：
- 全面且平衡
- 突出最重要的见解
- 保持客观和专业
- 结构清晰，易于理解

请以以下格式组织你的回答：
### 综合总结
[全面的总结内容]

### 关键见解
[列出最重要的见解，用项目符号表示]

### 建议和方向
[具体的建议和未来方向]

### 最终回答
[对原始问题的直接回答，整合了讨论中的最佳见解]
"""
    
    def receive_open_ended_final_summary(self, message: Message, final_round_messages: List[Message]) -> str:
        """处理开放性问题的最终总结请求"""
        prompt = self.generate_final_open_ended_summary(message, final_round_messages)
        summary_response = self.llm_service.get_response(prompt)
        
        # 提取最终回答部分
        if "### 最终回答" in summary_response:
            parts = summary_response.split("### 最终回答")
            if len(parts) > 1:
                final_answer = parts[1].strip()
            else:
                final_answer = summary_response
        else:
            final_answer = summary_response
            
        print(f"\n{self.name}的开放性答案总结：")
        print(final_answer)  # 只打印前500字符
        
        return summary_response