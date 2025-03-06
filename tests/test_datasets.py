import sys
import os

# 获取当前脚本的父目录（假设tests和src同级）
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # 假设tests在项目根目录下
sys.path.append(project_root)

from datasets import load_dataset
import datasets
import pandas as pd
from src.utils.problem_base import Problem
# load_dataset("C:/Users/Administrator/multi-agent-chat/mmlu/hendrycks_test.py", "abstract_algebra", name='mmlu', trust_remote_code=True)
config = datasets.DownloadConfig(resume_download=True, max_retries=100) 
dataset = load_dataset("cais/mmlu", "abstract_algebra", download_config=config)
df = pd.DataFrame(dataset['test'][:10])
for _, row in df.iterrows():
    # Format question with options
    question = (
        f"{row['question']}\n"
        f"A) {row['choices'][0]}\n"
        f"B) {row['choices'][1]}\n"
        f"C) {row['choices'][2]}\n"
        f"D) {row['choices'][3]}"
    )
                
                # Convert numeric answer to letter (0->A, 1->B, etc)
    answer = chr(65 + row['answer'])  # Convert 0->A, 1->B, etc
                
    problem = Problem(
        question=question,
        answer=answer,
        metadata={
            "type": "multiple_choice",
            "subject": "abstract_algebra"
        }
    )            