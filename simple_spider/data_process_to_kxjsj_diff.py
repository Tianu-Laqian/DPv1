import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import os
from time import sleep

# 创建保存CSV的目录
os.makedirs('beijing_science_awards', exist_ok=True)

beijing_sites = {
     2023: "https://kw.beijing.gov.cn/zwgk/sjfb/hjsj/202406/t20240628_3796506.html",
     # 2021/2022无统计 相关公告见 https://kw.beijing.gov.cn/zwgk/sjfb/hjsj/202212/t20221228_3796503.html
     2020: "https://kw.beijing.gov.cn/zwgk/sjfb/hjsj/202203/t20220301_3796499.html",
     2019: "https://kw.beijing.gov.cn/zwgk/sjfb/hjsj/202203/t20220301_3796494.html",
     2018: "https://kw.beijing.gov.cn/zwgk/sjfb/hjsj/202203/t20220301_3796492.html",
     2017: "https://kw.beijing.gov.cn/zwgk/sjfb/hjsj/202203/t20220301_3796491.html",
     2016: "https://kw.beijing.gov.cn/zwgk/sjfb/hjsj/202203/t20220301_3796490.html",
     2015: "https://kw.beijing.gov.cn/zwgk/sjfb/hjsj/202203/t20220301_3796489.html",
     2014: "https://kw.beijing.gov.cn/zwgk/sjfb/hjsj/202203/t20220301_3796488.html",
     2013: "https://kw.beijing.gov.cn/zwgk/sjfb/hjsj/202203/t20220301_3796493.html",
     2012: "https://kw.beijing.gov.cn/zwgk/sjfb/hjsj/202203/t20220301_3796487.html"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for year, url in beijing_sites.items():
    try:
        print(f"正在处理 {year} 年数据...")
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'  # 确保正确解析中文
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找目标表格
        target_table = None
        for table in soup.find_all('table'):
                target_table = table
                break
                
        if target_table is None:
            print(f"未找到表格: {year}")
            continue
        
        # 提取表格数据
        data = []
        for row in target_table.find_all('tr'):
            row_data = []
            for cell in row.find_all(['th', 'td']):
                # 合并跨行跨列单元格内容
                colspan = int(cell.get('colspan', 1))
                rowspan = int(cell.get('rowspan', 1))

                # 修复：保留完整的文本结构
                cell_text = cell.get_text('\n', strip=True)
                
                # 修复：合并姓名和单位
                # 将换行符+括号替换为括号，避免姓名和单位被分隔
                cell_text = re.sub(r'\n(?=[(（])', '', cell_text)
                # 将多个换行符替换为逗号分隔
                cell_text = re.sub(r'\n+', ',', cell_text)
                # 将左括号后的逗号（包括中英文括号）替换为左括号
                cell_text = re.sub(r'[（(]\s*,\s*', lambda m: m.group(0)[0], cell_text)
                # 将逗号后的右括号（包括中英文括号）替换为右括号
                cell_text = re.sub(r',\s*[）)]', lambda m: m.group(0)[-1], cell_text)

                # 处理空白单元格
                if not cell_text:
                    cell_text = ""
                    
                row_data.extend([cell_text] * colspan)
                
                # 简单处理rowspan
                for _ in range(rowspan - 1):
                    data.append([cell_text] * colspan)
            
            if row_data:
                data.append(row_data)
        
        # 创建DataFrame并保存
        df = pd.DataFrame(data)
        filename = f'beijing_science_awards/{year}_北京科学技术奖.csv'
        df.to_csv(filename, index=False, header=False, encoding='utf_8_sig')  # utf_8_sig支持Excel中文
        print(f"成功保存: {filename}")
        
    except Exception as e:
        print(f"处理 {year} 年时出错: {str(e)}")
    sleep(2)

print("所有数据处理完成！")