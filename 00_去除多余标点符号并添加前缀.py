import re
import argparse

def clean_line(line):
    # 定义要保留的标点
    preserved_chars = "、，（）"
    # 移除非保留标点之外的所有中英文标点符号
    cleaned = re.sub(rf'[^\w{re.escape(preserved_chars)}]', '', line)
    # 移除所有空格
    cleaned = cleaned.replace(' ', '')
    return cleaned

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--string', type=str, help='添加在行首的字符串')
    args = parser.parse_args()
    
    prefix = args.string if args.string else ''
    
    try:
        with open('input.txt', 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
    except FileNotFoundError:
        print("错误：未找到input.txt文件")
        return
    
    processed_lines = []
    for line in lines:
        cleaned = clean_line(line.strip())
        if cleaned:  # 跳过空行
            processed_lines.append(f"{prefix}{cleaned}")
    
    with open('result.txt', 'w', encoding='utf-8') as outfile:
        outfile.write('\n'.join(processed_lines))
    print("处理完成，结果已保存到result.txt")

if __name__ == "__main__":
    main()