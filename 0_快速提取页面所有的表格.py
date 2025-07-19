import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def extract_tables_to_excel(url, output_file):
    """
    提取网页中所有表格并保存到Excel文件
    
    参数:
    url: 目标网页URL
    output_file: 输出的Excel文件名
    """
    try:
        # 1. 获取网页内容
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        
        # 2. 解析HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 3. 查找所有表格
        tables = soup.find_all('table')
        
        if not tables:
            print(f"在 {url} 中没有找到任何表格")
            return False
        
        print(f"找到 {len(tables)} 个表格")
        
        # 4. 准备Excel写入器
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # 5. 处理每个表格
            for i, table in enumerate(tables):
                # 提取表格数据到二维列表
                table_data = []
                for row in table.find_all('tr'):
                    row_data = []
                    for cell in row.find_all(['td', 'th']):
                        # 合并行列跨度的单元格处理
                        colspan = int(cell.get('colspan', 1))
                        rowspan = int(cell.get('rowspan', 1))
                        
                        # 添加单元格内容（处理空单元格）
                        cell_text = cell.get_text(strip=True) or ''
                        row_data.append(cell_text)
                        
                        # 处理跨列
                        for _ in range(1, colspan):
                            row_data.append('')
                    
                    if row_data:  # 跳过空行
                        table_data.append(row_data)
                
                # 创建DataFrame
                try:
                    # 找出最大列数以对齐所有行
                    max_cols = max(len(row) for row in table_data)
                    
                    # 确保所有行有相同列数
                    for row in table_data:
                        while len(row) < max_cols:
                            row.append('')
                    
                    df = pd.DataFrame(table_data)
                    
                    # 生成sheet名称（确保唯一且有效）
                    sheet_name = f"Table_{i+1}"
                    if len(sheet_name) > 31:  # Excel sheet名称长度限制
                        sheet_name = sheet_name[:28] + "..."
                    
                    # 保存到Excel
                    df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
                    print(f"表格 {i+1} 已保存到 sheet: {sheet_name}")
                
                except Exception as e:
                    print(f"处理表格 {i+1} 时出错: {str(e)}")
        
        print(f"\n所有表格已保存到: {output_file}")
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"网络请求失败: {str(e)}")
    except Exception as e:
        print(f"处理过程中出错: {str(e)}")
    
    return False


if __name__ == "__main__":
    # 用户输入
    webpage_url = input("请输入要提取表格的网页URL: ").strip()
    output_filename = input("请输入输出Excel文件名(例如: tables.xlsx): ").strip()
    
    # 添加默认扩展名
    if not output_filename.lower().endswith('.xlsx'):
        output_filename += '.xlsx'
    
    # 执行提取
    extract_tables_to_excel(webpage_url, output_filename)