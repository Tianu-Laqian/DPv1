import csv
import requests
from lxml import etree
import re
from time import sleep
from urllib.parse import urljoin
import random

# 定义路径

# 配置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def extract_year(resume):
    # 提取当选年份
    match = re.search(r'(\d{4})年当选[^,.，。、]*?科学院',resume)
    return match.group(1) if match else ''

def process_row(row):
    #开始爬取
    try:
        if not row[1].startswith('http'):
            print(f"跳过无效链接：{row[1]}")
            return row

        response = requests.get(row[1], headers=headers, timeout=10)
        response.encoding = 'utf-8'
        tree = etree.HTML(response.text)

        # 提取简历
        resume = tree.xpath('//*[@id="zoom"]/div[2]//text()[not(ancestor::style)]')
        resume_text = ''.join(resume).strip() if resume else ''
        resume_text = re.sub(r'\s+','',resume_text)
        row[2] = resume_text

        # 提取当选年份
        row[3] = extract_year(resume_text) if resume_text else ''

        # 提取图片链接,处理相对路径
        img_src = tree.xpath('//*[@id="zoom"]/div[1]/img/@src')
        if img_src:
            img_split = img_src[0].replace('./','')
            row[4] = urljoin(row[1], img_split)
        else:
            row[4] = ''


    except Exception as e:
        print(f"处理{row[0]}时出错：{str(e)}")
    
    return row

def main():
    with open('zky_pass.csv', 'r', encoding='utf-8') as fr, \
         open('中科院已故院士名单.csv', 'w', encoding='utf-8', newline='') as fw:

        reader = csv.reader(fr)
        writer = csv.writer(fw)

        header = next(reader)
        writer.writerow(header)

        for i, row in enumerate(reader, start=1):
            new_row = process_row(row)
            writer.writerow(new_row)
            sleep(random.uniform(4, 7))
            if i % 20 == 0:
                print(f"已处理 {i} 条记录")

    print("处理完成，结果已保存到中科院已故院士名单.csv")

# 开始运行
main()