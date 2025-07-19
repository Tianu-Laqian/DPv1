import re

with open('input.txt', 'r', encoding='utf-8') as infile:
    with open('result.txt', 'w', encoding='utf-8') as outfile:
        for line in infile:
            # 同时处理中文括号和英文括号
            # if line.strip() == '':
            #     continue
            processed_line = re.sub(r'\([^()]*\)|（[^（）]*）', '', line)
            processed_line2 = processed_line.strip().replace(' ', '')
            outfile.write(processed_line)


