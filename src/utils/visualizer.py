import matplotlib.pyplot as plt
import numpy as np
import os
import sys
# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import DEFAULT_MMLU_SUBJECT, TOTAL_PROBLEMS_TO_LOAD, LLM_MODEL


def plot_accuracy_vs_agents():
    # Data from results
    agent_counts = [1, 2, 3, 4, 5, 6, 8]
    accuracies = [76.47, 76.47, 64.71, 52.94, 58.82, 58.82, 52.94]
    subject = 'abstract_algebra'
    model = 'TA/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo'
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(agent_counts, accuracies, 'bo-', linewidth=2, markersize=8)
    
    # Customize the plot
    plt.title(f'Accuracy vs Number of Agents\nSubject: {subject}\nModel: {model}', fontsize=14, pad=20)
    plt.xlabel('Number of Agents', fontsize=12)
    plt.ylabel('Accuracy (%)', fontsize=12)
    
    # Set x-axis ticks to show only the actual agent counts
    plt.xticks(agent_counts)
    
    # Add grid
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Add value labels on points
    for i, accuracy in enumerate(accuracies):
        plt.annotate(f'{accuracy:.2f}%', 
                    (agent_counts[i], accuracies[i]),
                    textcoords="offset points",
                    xytext=(0,10),
                    ha='center')
    
    # Set y-axis range to start from 50% for better visualization
    plt.ylim(0, 100)
    
    # Save the plot
    save_dir = "evaluate_result/figures"
    save_model = model.split('/')[-1]
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(os.path.join(save_dir, f'accuracy_vs_agents_{subject}_{save_model}.png'), 
                dpi=300, 
                bbox_inches='tight')
    plt.close()

def plot_accuracy_vs_agents_global_facts():
    # Data from results for global_facts
    agent_counts = [1, 2, 3, 4, 5, 6, 8]
    accuracies = [29.41, 35.29, 35.29, 47.06, 35.29, 35.29, 35.29]
    subject = 'global_facts'
    model = 'TA/Qwen/Qwen2.5-7B-Instruct-Turbo'
    
    # Create the plot
    plt.figure(figsize=(12, 7))
    plt.plot(agent_counts, accuracies, 'ro-', linewidth=2, markersize=8)
    
    # Customize the plot
    plt.title(f'Accuracy vs Number of Agents\nSubject: {subject}\nModel: {model}', fontsize=14, pad=20)
    plt.xlabel('Number of Agents', fontsize=12)
    plt.ylabel('Accuracy (%)', fontsize=12)
    
    # Set x-axis ticks to show only the actual agent counts
    plt.xticks(agent_counts)
    
    # Add grid
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Add value labels on points
    for i, accuracy in enumerate(accuracies):
        plt.annotate(f'{accuracy:.2f}%', 
                    (agent_counts[i], accuracies[i]),
                    textcoords="offset points",
                    xytext=(0,10),
                    ha='center')
    
    # Set y-axis range for better visualization
    plt.ylim(0, 100)
    
    # Save the plot
    save_dir = "evaluate_result/figures"
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(os.path.join(save_dir, f'accuracy_vs_agents_{subject}.png'), 
                dpi=300, 
                bbox_inches='tight')
    plt.close()

def plot_models_comparison():
    # Data for different models
    models_data = {
        # 'Meta-Llama-3.1-8B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [76.47, 76.47, 64.71, 52.94, 58.82, 58.82, 52.94],
        #     'color': 'bo-',  # blue
        #     'label': 'Llama-3.1-8B'
        # },
        # 'Qwen2.5-72B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [100.00, 100.00, 64.71, 82.35, 82.35, 88.24, 70.59],
        #     'color': 'ro-',  # red
        #     'label': 'Qwen2.5-72B'
        # },
        # 'Qwen2.5-7B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [47.06, 64.71, 64.71, 76.47, 52.94, 58.82, 58.82],
        #     'color': 'go-',  
        #     'label': 'Qwen2.5-7B'
        # }
        # 'Llama-3.1-8B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [47.06, 29.41, 37.99, 43.14, 41.18, 29.41, 33.33],
        #     'std_devs': [0.00, 4.80, 12.01, 10.00, 8.32, 8.32, 10.00],
        #     'color': 'bo-',  # blue for main line
        #     'std_color': 'b--',  # blue dashed for std dev
        #     'label': 'Llama-3.1-8B'
        # },
        # 'Qwen2.5-72B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [29.41, 35.29, 35.29, 47.06, 35.29, 35.29, 35.29],
        #     'std_devs': [0,0,0,0,0,0,0],  # Placeholder for std devs
        #     'color': 'ro-',  # red
        #     'std_color': 'r--',  # red dashed for std dev
        #     'label': 'Qwen2.5-72B'
        # },
        # 'Qwen2.5-7B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [64.71, 58.82, 70.59, 52.94, 58.82, 35.29, 64.71],
        #     'std_devs': [0,0,0,0,0,0,0],  # Placeholder for std devs
        #     'color': 'go-', 
        #     'std_color': 'g--', 
        #     'label': 'Qwen2.5-7B'
        # }
        # global_facts

        # 'Llama-3.1-70B': {
        #     'agent_counts': [1, 2, 3, 4, 5],
        #     'accuracies': [58.82, 39.22, 25.49, 21.57, 35.85],
        #     'std_devs': [0.00, 2.77, 2.77, 12.09, 5.50],
        #     'color': 'yo-',  # blue for main line
        #     'std_color': 'y--',  # blue dashed for std dev
        #     'label': 'Llama-3.1-70B'
        # },
        # 'Llama-3.1-8B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [50.00, 39.22, 41.18, 49.02, 43.14, 31.37, 39.22],
        #     'std_devs': [0.00, 5.55, 4.80, 16.87, 12.09, 12.09, 18.18],
        #     'color': 'bo-',  # blue for main line
        #     'std_color': 'b--',  # blue dashed for std dev
        #     'label': 'Llama-3.1-8B'
        # },
        # 'Qwen2.5-72B': {
        #     'agent_counts': [1, 2, 3, 4, 6, 8],
        #     'accuracies': [58.82, 52.94, 47.06, 47.06, 52.94, 47.06],
        #     'std_devs': [0,0,0,0,0,0,0],  # Placeholder for std devs
        #     'color': 'ro-',  # red
        #     'std_color': 'r--',  # red dashed for std dev
        #     'label': 'Qwen2.5-72B'
        # },
        # 'Qwen2.5-7B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [47.06, 35.29, 41.18, 52.94, 41.18, 52.94, 41.18],
        #     'std_devs': [0,0,0,0,0,0,0],  # Placeholder for std devs
        #     'color': 'go-', 
        #     'std_color': 'g--', 
        #     'label': 'Qwen2.5-7B'
        # }
        # formal_logic

        'Llama-3.1-70B': {
            'agent_counts': [1, 2, 3, 4, 5, 6, 8],
            'accuracies': [52.94, 35.29, 45.10, 41.18, 39.22, 33.33, 25.49],
            'std_devs': [0.00, 9.61, 2.77, 9.61, 7.34, 2.77, 7.34],
            'color': 'yo-',  # blue for main line
            'std_color': 'y--',  # blue dashed for std dev
            'label': 'Llama-3.1-70B'
        },
        # 'Llama-3.1-8B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [17.65, 29.41, 11.76, 12.50, 23.53, 35.29, 23.53],
        #     'std_devs': [0.00, 0, 0, 0, 0, 0, 0],
        #     'color': 'bo-',  # blue for main line
        #     'std_color': 'b--',  # blue dashed for std dev
        #     'label': 'Llama-3.1-8B'
        # },
        'Llama-3.1-8B': {
            'agent_counts': [1, 2, 3, 4, 5, 6, 8],
            'accuracies': [31.37, 33.33, 35.29, 31.37, 43.14, 29.41, 35.29],
            'std_devs': [7.34, 10.00, 9.61, 7.34, 2.77, 4.80, 8.32],
            'color': 'bo-',  # blue for main line
            'std_color': 'b--',  # blue dashed for std dev
            'label': 'Llama-3.1-8B'
        },
        'Qwen2.5-72B': {
            'agent_counts': [1, 2, 3, 4, 5, 6, 8],
            'accuracies': [64.71, 52.94, 64.71, 47.06, 47.06, 47.06, 47.06],
            'std_devs': [0,0,0,0,0,0,0],  # Placeholder for std devs
            'color': 'ro-',  # red
            'std_color': 'r--',  # red dashed for std dev
            'label': 'Qwen2.5-72B'
        },
        'Qwen2.5-7B': {
            'agent_counts': [1, 2, 3, 4, 5, 6, 8],
            'accuracies': [41.18, 52.94, 35.29, 47.06, 35.29, 58.82, 47.06],
            'std_devs': [0,0,0,0,0,0,0],  # Placeholder for std devs
            'color': 'go-', 
            'std_color': 'g--', 
            'label': 'Qwen2.5-7B'
        }
        #abstract_algebra
        
        # 'Llama-3.1-8B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [47.06, 50.98, 39.22, 41.18, 31.37, 41.18, 41.05],
        #     'std_devs': [0.00, 5.55, 5.55, 4.80, 7.34, 14.41, 8.62],
        #     'color': 'bo-',  # blue for main line
        #     'std_color': 'b--',  # blue dashed for std dev
        #     'label': 'Llama-3.1-8B'
        # },
        # 'Qwen2.5-72B': {
        #     'agent_counts': [1, 2, 3, 4, 6],
        #     'accuracies': [70.59, 70.59, 64.71, 70.59, 70.59],
        #     'std_devs': [0,0,0,0,0,0,0],  # Placeholder for std devs
        #     'color': 'ro-',  # red
        #     'std_color': 'r--',  # red dashed for std dev
        #     'label': 'Qwen2.5-72B'
        # },
        # 'Qwen2.5-7B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [52.94, 47.06, 41.18, 35.29, 58.82, 35.29, 41.18],
        #     'std_devs': [0,0,0,0,0,0,0],  # Placeholder for std devs
        #     'color': 'go-', 
        #     'std_color': 'g--', 
        #     'label': 'Qwen2.5-7B'
        # }
        # college_physics
        # 'Llama-3.1-70B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [94.12, 68.63, 66.67, 60.78, 64.71, 66.67, 74.51],
        #     'std_devs': [0.00, 5.55, 2.77, 10.00, 4.80, 5.55, 2.77],
        #     'color': 'yo-',  # blue for main line
        #     'std_color': 'y--',  # blue dashed for std dev
        #     'label': 'Llama-3.1-70B'
        # },
        # 'Llama-3.1-8B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [76.47, 76.47, 64.71, 52.94, 58.82, 58.82, 52.94],
        #     'std_devs': [0.00, 0, 0, 0, 0, 0, 0],
        #     'color': 'bo-',  # blue for main line
        #     'std_color': 'b--',  # blue dashed for std dev
        #     'label': 'Llama-3.1-8B'
        # },
        # 'Llama-3.1-8B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [82.35, 58.82, 58.82, 60.78, 31.37, 47.06, 29.41],
        #     'std_devs': [0.00, 9.61, 8.32, 10.00, 12.09, 9.61, 9.61],
        #     'color': 'bo-',  # blue for main line
        #     'std_color': 'b--',  # blue dashed for std dev
        #     'label': 'Llama-3.1-8B'
        # },
        # 'Qwen2.5-72B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [100.00, 100.00, 64.71, 82.35, 82.35, 88.24, 70.59],
        #     'std_devs': [0,0,0,0,0,0,0],  # Placeholder for std devs
        #     'color': 'ro-',  # red
        #     'std_color': 'r--',  # red dashed for std dev
        #     'label': 'Qwen2.5-72B'
        # },
        # 'Qwen2.5-7B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [47.06, 64.71, 64.71, 76.47, 52.94, 58.82, 58.82],
        #     'std_devs': [0,0,0,0,0,0,0],  # Placeholder for std devs
        #     'color': 'go-', 
        #     'std_color': 'g--', 
        #     'label': 'Qwen2.5-7B'
        # }
        # philosophy
        # 'Llama-3.1-8B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [23.53, 43.14, 41.18, 37.25, 42.16, 29.90, 45.10],
        #     'std_devs': [0.00, 5.55, 4.80, 7.34, 6.04, 4.22, 2.77],
        #     'color': 'bo-',  # blue for main line
        #     'std_color': 'b--',  # blue dashed for std dev
        #     'label': 'Llama-3.1-8B'
        # },
        # 'Qwen2.5-72B': {
        #     'agent_counts': [1, 2, 4, 6, 8],
        #     'accuracies': [70.59, 64.71, 70.59, 58.82, 64.71],
        #     'std_devs': [0,0,0,0,0,0,0],  # Placeholder for std devs
        #     'color': 'ro-',  # red
        #     'std_color': 'r--',  # red dashed for std dev
        #     'label': 'Qwen2.5-72B'
        # }
        # college_computer_science
        # Add more models as needed
    }
    subject = 'abstract_algebra'
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    
    # Plot each model's data
    for model, data in models_data.items():
        plt.plot(data['agent_counts'], 
                data['accuracies'], 
                data['color'], 
                linewidth=2, 
                markersize=8,
                label=data['label'])
        
        plt.plot(data['agent_counts'],
                [acc + std for acc, std in zip(data['accuracies'], data['std_devs'])],
                data['std_color'],
                linewidth=1,
                label=f"{data['label']} (Std Dev)")
        plt.plot(data['agent_counts'],
                [acc - std for acc, std in zip(data['accuracies'], data['std_devs'])],
                data['std_color'],
                linewidth=1,
                )
        # Add value labels
        for i, accuracy in enumerate(data['accuracies']):
            plt.annotate(f'{accuracy:.2f}%', 
                        (data['agent_counts'][i], accuracy),
                        textcoords="offset points",
                        xytext=(0,10),
                        ha='center')
    
    # Customize the plot
    plt.title(f'Model Comparison: Accuracy vs Number of Agents\nSubject: {subject}', 
              fontsize=14, 
              pad=20)
    plt.xlabel('Number of Agents', fontsize=12)
    plt.ylabel('Accuracy (%)', fontsize=12)
    
    # Set x-axis ticks
    all_agent_counts = sorted(list(set(sum([data['agent_counts'] for data in models_data.values()], []))))
    plt.xticks(all_agent_counts)
    
    # Add grid and legend
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc='best', fontsize=10)
    
    # Set y-axis range
    plt.ylim(0, 100)
    
    # Save the plot
    save_dir = "multi-agent-chat/evaluate_result/figures"
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(os.path.join(save_dir, f'models_comparison_{subject}.png'), 
                dpi=300, 
                bbox_inches='tight')
    plt.close()

def plot_stats_histogram():
    """
    绘制两个并排的直方图：一个显示不同智能体数量下的方差，另一个显示平均值
    """
    # 使用相同的数据结构
    models_data = {
        # 'Meta-Llama-3.1-8B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [76.47, 76.47, 64.71, 52.94, 58.82, 58.82, 52.94],
        #     'color': 'bo-',  # blue
        #     'label': 'Llama-3.1-8B'
        # },
        # 'Qwen2.5-72B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [100.00, 100.00, 64.71, 82.35, 82.35, 88.24, 70.59],
        #     'color': 'ro-',  # red
        #     'label': 'Qwen2.5-72B'
        # },
        # 'Qwen2.5-7B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [47.06, 64.71, 64.71, 76.47, 52.94, 58.82, 58.82],
        #     'color': 'go-',  
        #     'label': 'Qwen2.5-7B'
        # }
        # 'Llama-3.1-8B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [47.06, 29.41, 37.99, 43.14, 41.18, 29.41, 33.33],
        #     'std_devs': [0.00, 4.80, 12.01, 10.00, 8.32, 8.32, 10.00],
        #     'color': 'bo-',  # blue for main line
        #     'std_color': 'b--',  # blue dashed for std dev
        #     'label': 'Llama-3.1-8B'
        # },
        # 'Qwen2.5-72B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [29.41, 35.29, 35.29, 47.06, 35.29, 35.29, 35.29],
        #     'std_devs': [0,0,0,0,0,0,0],  # Placeholder for std devs
        #     'color': 'ro-',  # red
        #     'std_color': 'r--',  # red dashed for std dev
        #     'label': 'Qwen2.5-72B'
        # },
        # 'Qwen2.5-7B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [64.71, 58.82, 70.59, 52.94, 58.82, 35.29, 64.71],
        #     'std_devs': [0,0,0,0,0,0,0],  # Placeholder for std devs
        #     'color': 'go-', 
        #     'std_color': 'g--', 
        #     'label': 'Qwen2.5-7B'
        # }
        # global_facts

        # 'Llama-3.1-70B': {
        #     'agent_counts': [1, 2, 3, 4, 5],
        #     'accuracies': [58.82, 39.22, 25.49, 21.57, 35.85],
        #     'std_devs': [0.00, 2.77, 2.77, 12.09, 5.50],
        #     'color': 'yo-',  # blue for main line
        #     'std_color': 'y--',  # blue dashed for std dev
        #     'label': 'Llama-3.1-70B'
        # },
        # 'Llama-3.1-8B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [50.00, 39.22, 41.18, 49.02, 43.14, 31.37, 39.22],
        #     'std_devs': [0.00, 5.55, 4.80, 16.87, 12.09, 12.09, 18.18],
        #     'color': 'bo-',  # blue for main line
        #     'std_color': 'b--',  # blue dashed for std dev
        #     'label': 'Llama-3.1-8B'
        # },
        # 'Qwen2.5-72B': {
        #     'agent_counts': [1, 2, 3, 4, 6, 8],
        #     'accuracies': [58.82, 52.94, 47.06, 47.06, 52.94, 47.06],
        #     'std_devs': [0,0,0,0,0,0,0],  # Placeholder for std devs
        #     'color': 'ro-',  # red
        #     'std_color': 'r--',  # red dashed for std dev
        #     'label': 'Qwen2.5-72B'
        # },
        # 'Qwen2.5-7B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [47.06, 35.29, 41.18, 52.94, 41.18, 52.94, 41.18],
        #     'std_devs': [0,0,0,0,0,0,0],  # Placeholder for std devs
        #     'color': 'go-', 
        #     'std_color': 'g--', 
        #     'label': 'Qwen2.5-7B'
        # }
        # formal_logic

        'Llama-3.1-70B': {
            'agent_counts': [1, 2, 3, 4, 5, 6, 8],
            'accuracies': [52.94, 35.29, 45.10, 41.18, 39.22, 33.33, 25.49],
            'std_devs': [0.00, 9.61, 2.77, 9.61, 7.34, 2.77, 7.34],
            'color': 'yellow',  # blue for main line
            'std_color': 'y--',  # blue dashed for std dev
            'label': 'Llama-3.1-70B'
        },
        # 'Llama-3.1-8B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [17.65, 29.41, 11.76, 12.50, 23.53, 35.29, 23.53],
        #     'std_devs': [0.00, 0, 0, 0, 0, 0, 0],
        #     'color': 'bo-',  # blue for main line
        #     'std_color': 'b--',  # blue dashed for std dev
        #     'label': 'Llama-3.1-8B'
        # },
        'Llama-3.1-8B': {
            'agent_counts': [1, 2, 3, 4, 5, 6, 8],
            'accuracies': [31.37, 33.33, 35.29, 31.37, 43.14, 29.41, 35.29],
            'std_devs': [7.34, 10.00, 9.61, 7.34, 2.77, 4.80, 8.32],
            'color': 'blue',  # blue for main line
            'std_color': 'b--',  # blue dashed for std dev
            'label': 'Llama-3.1-8B'
        },
        'Qwen2.5-72B': {
            'agent_counts': [1, 2, 3, 4, 5, 6, 8],
            'accuracies': [64.71, 52.94, 64.71, 47.06, 47.06, 47.06, 47.06],
            'std_devs': [0,0,0,0,0,0,0],  # Placeholder for std devs
            'color': 'red',  # red
            'std_color': 'r--',  # red dashed for std dev
            'label': 'Qwen2.5-72B'
        },
        'Qwen2.5-7B': {
            'agent_counts': [1, 2, 3, 4, 5, 6, 8],
            'accuracies': [41.18, 52.94, 35.29, 47.06, 35.29, 58.82, 47.06],
            'std_devs': [0,0,0,0,0,0,0],  # Placeholder for std devs
            'color': 'green', 
            'std_color': 'g--', 
            'label': 'Qwen2.5-7B'
        }
        #abstract_algebra
        
        # 'Llama-3.1-8B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [47.06, 50.98, 39.22, 41.18, 31.37, 41.18, 41.05],
        #     'std_devs': [0.00, 5.55, 5.55, 4.80, 7.34, 14.41, 8.62],
        #     'color': 'bo-',  # blue for main line
        #     'std_color': 'b--',  # blue dashed for std dev
        #     'label': 'Llama-3.1-8B'
        # },
        # 'Qwen2.5-72B': {
        #     'agent_counts': [1, 2, 3, 4, 6],
        #     'accuracies': [70.59, 70.59, 64.71, 70.59, 70.59],
        #     'std_devs': [0,0,0,0,0,0,0],  # Placeholder for std devs
        #     'color': 'ro-',  # red
        #     'std_color': 'r--',  # red dashed for std dev
        #     'label': 'Qwen2.5-72B'
        # },
        # 'Qwen2.5-7B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [52.94, 47.06, 41.18, 35.29, 58.82, 35.29, 41.18],
        #     'std_devs': [0,0,0,0,0,0,0],  # Placeholder for std devs
        #     'color': 'go-', 
        #     'std_color': 'g--', 
        #     'label': 'Qwen2.5-7B'
        # }
        # college_physics
        # 'Llama-3.1-70B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [94.12, 68.63, 66.67, 60.78, 64.71, 66.67, 74.51],
        #     'std_devs': [0.00, 5.55, 2.77, 10.00, 4.80, 5.55, 2.77],
        #     'color': 'yo-',  # blue for main line
        #     'std_color': 'y--',  # blue dashed for std dev
        #     'label': 'Llama-3.1-70B'
        # },
        # 'Llama-3.1-8B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [76.47, 76.47, 64.71, 52.94, 58.82, 58.82, 52.94],
        #     'std_devs': [0.00, 0, 0, 0, 0, 0, 0],
        #     'color': 'bo-',  # blue for main line
        #     'std_color': 'b--',  # blue dashed for std dev
        #     'label': 'Llama-3.1-8B'
        # },
        # 'Llama-3.1-8B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [82.35, 58.82, 58.82, 60.78, 31.37, 47.06, 29.41],
        #     'std_devs': [0.00, 9.61, 8.32, 10.00, 12.09, 9.61, 9.61],
        #     'color': 'bo-',  # blue for main line
        #     'std_color': 'b--',  # blue dashed for std dev
        #     'label': 'Llama-3.1-8B'
        # },
        # 'Qwen2.5-72B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [100.00, 100.00, 64.71, 82.35, 82.35, 88.24, 70.59],
        #     'std_devs': [0,0,0,0,0,0,0],  # Placeholder for std devs
        #     'color': 'ro-',  # red
        #     'std_color': 'r--',  # red dashed for std dev
        #     'label': 'Qwen2.5-72B'
        # },
        # 'Qwen2.5-7B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [47.06, 64.71, 64.71, 76.47, 52.94, 58.82, 58.82],
        #     'std_devs': [0,0,0,0,0,0,0],  # Placeholder for std devs
        #     'color': 'go-', 
        #     'std_color': 'g--', 
        #     'label': 'Qwen2.5-7B'
        # }
        # philosophy
        # 'Llama-3.1-8B': {
        #     'agent_counts': [1, 2, 3, 4, 5, 6, 8],
        #     'accuracies': [23.53, 43.14, 41.18, 37.25, 42.16, 29.90, 45.10],
        #     'std_devs': [0.00, 5.55, 4.80, 7.34, 6.04, 4.22, 2.77],
        #     'color': 'bo-',  # blue for main line
        #     'std_color': 'b--',  # blue dashed for std dev
        #     'label': 'Llama-3.1-8B'
        # },
        # 'Qwen2.5-72B': {
        #     'agent_counts': [1, 2, 4, 6, 8],
        #     'accuracies': [70.59, 64.71, 70.59, 58.82, 64.71],
        #     'std_devs': [0,0,0,0,0,0,0],  # Placeholder for std devs
        #     'color': 'ro-',  # red
        #     'std_color': 'r--',  # red dashed for std dev
        #     'label': 'Qwen2.5-72B'
        # }
        # college_computer_science
        # Add more models as needed
    }
    subject = 'abstract_algebra'

    # 创建一个包含两个子图的图表
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # 设置柱状图的宽度
    bar_width = 0.2
    
    # 获取所有智能体数量
    agent_counts = sorted(list(set(sum([data['agent_counts'] for data in models_data.values()], []))))
    x = np.arange(len(agent_counts))

    # 绘制方差直方图
    for i, (model, data) in enumerate(models_data.items()):
        # 确保数据对齐
        std_values = []
        for count in agent_counts:
            if count in data['agent_counts']:
                idx = data['agent_counts'].index(count)
                std_values.append(data['std_devs'][idx])
            else:
                std_values.append(0)
                
        ax1.bar(x + i*bar_width, std_values, bar_width, 
                label=data['label'], color=data['color'], alpha=0.7)

    ax1.set_xlabel('Number of Agents')
    ax1.set_ylabel('Standard Deviation')
    ax1.set_title('Standard Deviation by Number of Agents')
    ax1.set_xticks(x + bar_width/2)
    ax1.set_xticklabels(agent_counts)
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.3)

    # 绘制平均值直方图
    for i, (model, data) in enumerate(models_data.items()):
        # 确保数据对齐
        acc_values = []
        for count in agent_counts:
            if count in data['agent_counts']:
                idx = data['agent_counts'].index(count)
                acc_values.append(data['accuracies'][idx])
            else:
                acc_values.append(0)
                
        ax2.bar(x + i*bar_width, acc_values, bar_width,
                label=data['label'], color=data['color'], alpha=0.7)

    ax2.set_xlabel('Number of Agents')
    ax2.set_ylabel('Average Accuracy (%)')
    ax2.set_title('Average Accuracy by Number of Agents')
    ax2.set_xticks(x + bar_width/2)
    ax2.set_xticklabels(agent_counts)
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.3)

    # 调整布局并添加总标题
    plt.suptitle(f'Model Comparison Statistics: {subject}', fontsize=14, y=1.05)
    plt.tight_layout()

    # 保存图表
    save_dir = "multi-agent-chat/evaluate_result/figures"
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(os.path.join(save_dir, f'models_stats_histogram_{subject}.png'),
                dpi=300,
                bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    # plot_accuracy_vs_agents()
    # plot_models_comparison()
    plot_stats_histogram()