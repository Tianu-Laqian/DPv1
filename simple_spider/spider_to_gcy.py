import csv
import requests
from lxml import etree
import re
from time import sleep
import random

# 定义路径
resume = '/html/body/div[4]/div/div[3]/div[2]'
img_src = '/html/body/div[4]/div/div[3]/div[1]/a/img/@src'
baike_href = '/html/body/div[4]/div/div[3]/div[1]/div/a/@href'

# 配置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def extract_year(resume_text):
    # 提取当选年份
    match = re.search(r'(\d{4})年当选[^,.，。、]*?工程院',resume_text)
    return match.group(1) if match else ''

def process_row(row):
    #开始爬取
    try:
        response = requests.get(row[1], headers=headers, timeout=10)
        response.encoding = 'utf-8'
        tree = etree.HTML(response.text)

        # 提取简历
        resume_x = tree.xpath(resume)
        resume_text = ''.join(resume_x[0].itertext()).strip() if resume_x else ''
        resume_text = re.sub(r'\s+', '', resume_text)
        row[2] = resume_text

        # 提取当选年份
        row[3] = extract_year(resume_text) if resume_text else ''

        # 提取图片链接
        img_src_x = tree.xpath(img_src)
        row[4] = f"https://www.cae.cn{img_src_x[0]}" if img_src_x else ''

        #提取百科链接
        baike_href_x = tree.xpath(baike_href)
        row[5] = baike_href_x[0] if baike_href_x else ''

    except Exception as e:
        print(f"处理{row[0]}时出错：{str(e)}")
    
    return row

def main():
    # 读csv
    with open('gcy_passwai.csv', 'r', encoding='utf-8') as f:
        data = list(csv.reader(f))
    
    # 分离表头和数据行
    header = data[0]
    rows = data[1:]
    
    # 处理并更新数据
    updated_rows = []
    total_rows = len(rows)
    
    for i, row in enumerate(rows):
        updated_rows.append(process_row(row))
        time = random.uniform(4,7)
        sleep(time)       
        # 打印进度提示
        if (i + 1) % 20 == 0:
            print(f"已处理 {i+1}/{total_rows} 条记录")
    
    # 写入新文件
    with open('工程院已故外籍院士名单.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(updated_rows)

    print(f"处理完成！共处理 {total_rows} 条记录，结果已保存到工程院已故外籍院士名单.csv")

# 开始运行
main()