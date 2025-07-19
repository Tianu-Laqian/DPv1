import re
import string

with open('input.txt', 'r', encoding='utf-8') as infile:
    with open('result.txt', 'w', encoding='utf-8') as outfile:
        for raw_line in infile:
            # 预处理：去空格+处理括号
            line = raw_line.strip().replace(' ', '')
            
            # 新增：删除行首的中文数字标号（如一、二、等）
            line = re.sub(r'^[一二三四五六七八九十百千万]+、', '', line)
            line = re.sub(r'^（[一二三四五六七八九十百千万]+）', '', line)  # 全角括号
            line = re.sub(r'^\([一二三四五六七八九十百千万]+\)', '', line)  # 半角括号
            
            # 获取需保留的标点（括号），并构建需过滤的标点集合
            exclude_punct = set(string.punctuation) - {'(', ')'}
            # 构建正则模式：匹配需过滤的标点和数字
            pattern = r'[{}0-9]'.format(re.escape(''.join(exclude_punct)))
            line = re.sub(pattern, '', line)
            
            if '(' in line and ')' in line:
                # 拆分主名称和括号内容
                main_part, bracket_part = line.split('(', 1)
                bracket_part = bracket_part.replace(')', '')
                
                # 分别写入两次
                outfile.write(main_part + '\n')
                outfile.write(main_part + '\n')  # 主名称写两次
                outfile.write(bracket_part + '\n')
                outfile.write(bracket_part + '\n') 
            elif  '（' in line and '）' in line:
                # 拆分主名称和括号内容
                main_part, bracket_part = line.split('（', 1)
                bracket_part = bracket_part.replace('）', '')
                
                # 分别写入两次
                outfile.write(main_part + '\n')
                outfile.write(main_part + '\n')  # 主名称写两次
                outfile.write(bracket_part + '\n')
                outfile.write(bracket_part + '\n') 
            else:
                # 无括号内容直接翻倍
                outfile.write(line + '\n')
                outfile.write(line + '\n')