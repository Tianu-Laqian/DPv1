import csv
import re

def clean_string(s):
    """移除字符串中所有空白字符（空格、换行、制表符等）"""
    return re.sub(r'\s+', '', s)

def remove_digits(s):
    """删除字符串中的所有数字"""
    return re.sub(r'\d+', '', s)

def parse_contributor(contributor_str):
    """解析完成人字符串，返回(姓名, 单位)元组"""
    # 匹配格式：姓名(单位)，支持中英文括号混用
    match = re.match(r'^(.+?)[（(〔](.+?)[)）〕]$', contributor_str)
    if match:
        return match.group(1), match.group(2)
    return contributor_str, None

input_file = '23浙江科学技术奖.csv'
output_file = '科技奖汇总/re_23浙江科学技术奖.csv'

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', encoding='utf-8', newline='') as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    # 读取并清理标题行
    headers = next(reader)
    cleaned_headers = [clean_string(header) for header in headers]
    
    # 确定列索引
    try:
        main_contributor_idx = cleaned_headers.index('主要完成人')
        main_unit_idx = cleaned_headers.index('主要完成单位')
    except ValueError as e:
        print(f"文件缺少必要列: {e}")
        exit(1)
    
    writer.writerow(cleaned_headers)
    
    for row in reader:
        # 在清理前先处理主要完成人列的换行符
        if len(row) > main_contributor_idx:
            # 将换行符替换为逗号
            row[main_contributor_idx] = row[main_contributor_idx].replace('\n', ',').replace('\r', '')
        
        # 清理所有字段中的空白字符
        cleaned_row = [clean_string(field) for field in row]
        
        # 删除主要完成人中的数字
        cleaned_row[main_contributor_idx] = remove_digits(cleaned_row[main_contributor_idx])
        
        # 删除主要完成单位中的数字
        cleaned_row[main_unit_idx] = remove_digits(cleaned_row[main_unit_idx])
        original_unit = cleaned_row[main_unit_idx]  # 保存原始单位值
        
        # 分割主要完成人
        contributors = re.split(r',|，|、', cleaned_row[main_contributor_idx])
        
        # 为每个完成人创建新行
        for contributor in contributors:
            if not contributor:  # 跳过空名字
                continue
                
            new_row = cleaned_row.copy()
            # 解析完成人信息
            name, unit = parse_contributor(contributor)
            # 删除姓名中的数字
            name = remove_digits(name)
            new_row[main_contributor_idx] = name
            
            # 如果解析到单位信息则覆盖，否则保留原始单位
            if unit:
                # 删除单位中的数字
                unit = remove_digits(unit)
                new_row[main_unit_idx] = unit
            else:
                new_row[main_unit_idx] = original_unit
            
            writer.writerow(new_row)

print(f"处理完成！结果已保存到: {output_file}")