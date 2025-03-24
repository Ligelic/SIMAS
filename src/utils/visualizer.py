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
    accuracies = [64.71, 58.82, 64.71,47.06, 47.06, 47.06, 47.06]
    subject = 'abstract_algebra'
    model = LLM_MODEL
    
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
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(os.path.join(save_dir, f'accuracy_vs_agents_{subject}.png'), 
                dpi=300, 
                bbox_inches='tight')
    plt.close()

def plot_accuracy_vs_agents_global_facts():
    # Data from results for global_facts
    agent_counts = [1, 2, 3, 4, 5, 6, 8]
    accuracies = [29.41, 35.29, 35.29, 47.06, 35.29, 35.29, 35.29]
    subject = 'global_facts'
    model = LLM_MODEL
    
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

if __name__ == "__main__":
    plot_accuracy_vs_agents()
    # plot_accuracy_vs_agents_global_facts()