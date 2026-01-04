import os
import re
import json
from collections import defaultdict

def parse_file_content(content, subject_from_dir):
    lines = content.split('\n')
    data = {}
    for line in lines:
        if line.startswith('Model:'):
            data['model'] = line.split('Model:')[1].strip()
        elif line.startswith('Subject:'):
            data['subject'] = line.split('Subject:')[1].strip()
        elif line.startswith('Agent Mode:'):
            data['agent_mode'] = int(line.split('Agent Mode:')[1].strip())
        elif line.startswith('Agent Count:'):
            parts = line.split('Agent Count:')[1].split('|')
            data['agent_count'] = int(parts[0].strip())
        elif line.startswith('Average Accuracy:'):
            acc_str = line.split('Average Accuracy:')[1].strip().replace('%', '')
            data['avg_accuracy'] = float(acc_str)
        elif line.startswith('Standard Deviation:'):
            std_str = line.split('Standard Deviation:')[1].strip().replace('%', '')
            data['std_dev'] = float(std_str)
        elif line.startswith('Average Tokens per Experiment:'):
            tokens_str = line.split('Average Tokens per Experiment:')[1].strip()
            # 移除逗号并转换为整数
            tokens_str = tokens_str.replace(',', '')
            data['avg_tokens'] = int(tokens_str)
    
    if 'subject' not in data:
        data['subject'] = subject_from_dir
    return data

def main():
    base_dir = 'multi-agent-chat/temp_result'
    output_dir = 'multi-agent-chat/evaluate_result/json_data'
    index = 1
    while os.path.exists(os.path.join(output_dir, f"arranged_data({index}).json")):
        index += 1
    output_file = os.path.join(output_dir, f"arranged_data({index}).json")
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    pattern = re.compile(r'result_(\d+)_(\d+)\((\d+)\)\.txt$')
    
    mode_mapping = {
        0: 'ALL',
        1: 'NONE_ALL',
        2: 'NONE_PERSONALITY',
        3: 'NONE_EXPERTISE',
        4: 'NONE_BELIEF'
    }
    
    mode_style = {
        'ALL': {'color': 'blue', 'label': 'ALL Mode'},
        'NONE_ALL': {'color': 'red', 'label': 'NONE_ALL Mode'},
        'NONE_PERSONALITY': {'color': 'green', 'label': 'NONE_PERSONALITY Mode'},
        'NONE_EXPERTISE': {'color': 'purple', 'label': 'NONE_EXPERTISE Mode'},
        'NONE_BELIEF': {'color': 'orange', 'label': 'NONE_BELIEF Mode'}
    }
    
    latest_data = {}
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            match = pattern.match(file)
            if not match:
                continue
            month, day, number = map(int, match.groups())
            date_key = (month, day, number)
            subject = os.path.basename(root)
            filepath = os.path.join(root, file)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                file_data = parse_file_content(content, subject)
            except Exception as e:
                print(f"Error parsing {filepath}: {e}")
                continue
            
            model = file_data.get('model')
            agent_mode_num = file_data.get('agent_mode')
            agent_count = file_data.get('agent_count')
            avg_accuracy = file_data.get('avg_accuracy')
            std_dev = file_data.get('std_dev')
            avg_tokens = file_data.get('avg_tokens')
            
            if None in [model, agent_mode_num, agent_count, avg_accuracy, std_dev, avg_tokens]:
                print(f"Missing data in {filepath}")
                continue
            
            mode_str = mode_mapping.get(agent_mode_num)
            if mode_str is None:
                print(f"Unknown agent mode {agent_mode_num} in {filepath}")
                continue
            
            key = (subject, model, mode_str, agent_count)
            if key not in latest_data or date_key > latest_data[key]['date']:
                latest_data[key] = {
                    'date': date_key,
                    'avg_accuracy': avg_accuracy,
                    'std_dev': std_dev,
                    'avg_tokens': avg_tokens
                }
    
    result_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {
        'agent_counts': [],
        'accuracies': [],
        'std_devs': [],
        'tokens': [],
    })))
    
    for (subject, model, mode_str, agent_count), data in latest_data.items():
        mode_entry = result_dict[subject][model][mode_str]
        mode_entry['agent_counts'].append(agent_count)
        mode_entry['accuracies'].append(data['avg_accuracy'])
        mode_entry['std_devs'].append(data['std_dev'])
        mode_entry['tokens'].append(data['avg_tokens'])
    
    # 对每个模式的数据按agent_count排序
    for subject in result_dict:
        for model in result_dict[subject]:
            for mode_str in result_dict[subject][model]:
                mode_entry = result_dict[subject][model][mode_str]
                # 对agent_counts、accuracies、std_devs和tokens进行排序
                combined = sorted(zip(
                    mode_entry['agent_counts'], 
                    mode_entry['accuracies'], 
                    mode_entry['std_devs'],
                    mode_entry['tokens']
                ), key=lambda x: x[0])
                
                agent_counts, accuracies, std_devs, tokens = zip(*combined) if combined else ([], [], [], [])
                mode_entry['agent_counts'] = list(agent_counts)
                mode_entry['accuracies'] = list(accuracies)
                mode_entry['std_devs'] = list(std_devs)
                mode_entry['tokens'] = list(tokens)
                # 添加样式信息
                mode_entry.update(mode_style.get(mode_str, {}))
    
    # 将结果写入JSON文件，使用更紧凑的格式
    with open(output_file, 'w', encoding='utf-8') as f:
        # 使用自定义的JSON格式化器，使数组更紧凑
        class CompactJSONEncoder(json.JSONEncoder):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.indent = 4  # 设置缩进为4个空格
            
            def encode(self, obj):
                # 先使用默认的JSON编码
                result = super().encode(obj)
                # 然后处理数组，使其更紧凑
                lines = result.split('\n')
                compact_lines = []
                in_array = False
                array_lines = []
                
                for line in lines:
                    stripped = line.strip()
                    if stripped.startswith('[') and not stripped.endswith(']'):
                        in_array = True
                        array_lines = [line]
                    elif in_array and stripped.endswith(']'):
                        in_array = False
                        array_lines.append(line)
                        # 合并数组行
                        compact_array = ' '.join([l.strip() for l in array_lines])
                        compact_lines.append(compact_array)
                    elif in_array:
                        array_lines.append(line)
                    else:
                        compact_lines.append(line)
                
                return '\n'.join(compact_lines)
        
        json.dump(result_dict, f, cls=CompactJSONEncoder, ensure_ascii=False)
    
    
    print(f"Data successfully written to {output_file}")

if __name__ == '__main__':
    main()