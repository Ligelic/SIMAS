from agents.llm_agent import LLMAgent
from chat.message import Message
from typing import List

class CodeLLMAgent(LLMAgent):
    """针对代码问题的LLM Agent扩展"""
    
    def generate_code_prompt(self, message: Message) -> str:
        """为代码问题生成提示词"""
        chat_room = getattr(message, 'chat_room', None)
        others_desc = self.format_others_description(chat_room) if chat_room else ""
        
        # 获取问题类型和语言
        question_type = getattr(self, 'question_type', 'code')
        language = getattr(self, 'programming_language', 'Python')
        
        prompt = f"""你正在参与一个代码问题的讨论。请基于你的编程经验和知识提供高质量的代码解决方案。

你的角色：{self.name}
个性：{self.personality.value}
专长：{self.description}
编程语言：{language}

当前讨论的问题类型：{question_type}

请特别注意：
1. 提供正确的、高效的代码解决方案
2. 考虑边界情况和错误处理
3. 确保代码具有良好的可读性和可维护性
4. 如果有多种解决方案，请分析它们的优缺点
5. 在讨论中引用他人的代码并提供改进建议

对话历史：
{others_desc if others_desc else "这是讨论的开始"}

当前消息：
{message.content}

请按照以下格式回应：
### 代码分析：简要分析问题的要求和约束条件
### 解决方案：提出你的代码解决方案
### 代码实现：提供完整的、可运行的代码
### 时间复杂度分析：分析算法的时间复杂度
### 测试用例：提供测试用例验证你的代码
### 改进建议：对其他人的代码提出建设性意见

注意：代码应该包含必要的注释，遵循良好的编程实践。
"""
        return prompt
    
    def generate_final_code_summary(self, message: Message, final_round_messages: List[Message]) -> str:
        """为代码问题生成最终总结提示词"""
        final_messages = "\n".join([
            f"{msg.sender.name}: {msg.content}" 
            for msg in final_round_messages
        ])
        
        return f"""作为讨论的总结者，请基于以下讨论内容提供最终的代码解决方案。

讨论摘要：
{final_messages}

问题类型：{getattr(self, 'question_type', 'code')}
编程语言：{getattr(self, 'programming_language', 'Python')}

请提供：
1. 最终的、最优的代码实现
2. 代码解释和关键逻辑说明
3. 时间复杂度和空间复杂度分析
4. 测试用例
5. 可能的改进方向

你的代码解决方案应该：
- 完全满足问题要求
- 高效且正确
- 具有良好的代码风格
- 包含必要的注释

请以以下格式组织你的回答：
### 问题理解
[简要描述问题和约束条件]

### 最终代码实现
[提供完整的代码]

### 代码解释
[详细解释关键逻辑]

### 复杂度分析
[时间复杂度和空间复杂度]

### 测试用例
[提供验证代码的测试用例]

### 最终答案
[完整的代码解决方案]
"""
    
    def receive_code_final_summary(self, message: Message, final_round_messages: List[Message]) -> str:
        """处理代码问题的最终总结请求"""
        prompt = self.generate_final_code_summary(message, final_round_messages)
        summary_response = self.llm_service.get_response(prompt)
        
        # 提取最终代码部分
        if "### 最终代码实现" in summary_response:
            # 尝试提取代码块
            import re
            code_pattern = r"```(?:python|python3)?\n(.*?)\n```"
            matches = re.findall(code_pattern, summary_response, re.DOTALL)
            if matches:
                final_code = matches[0]
            elif "```" in summary_response:
                # 提取第一个代码块
                parts = summary_response.split("```")
                if len(parts) > 1:
                    final_code = parts[1].strip()
                    if final_code.startswith("python") or final_code.startswith("python3"):
                        final_code = final_code[6:].strip()
            else:
                final_code = summary_response
        else:
            final_code = summary_response
            
        print(f"\n{self.name}的代码解决方案：")
        print(final_code[:500])  # 只打印前500字符
        
        return summary_response