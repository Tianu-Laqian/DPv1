import requests
from lxml import etree
import csv
from time import sleep

url = "https://www.guozi.org/certification/directory_index.php?page=1"

# 模拟请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for page in range(1,127):
    url = f"https://www.guozi.org/certification/directory_index.php?page={page}"
    # 发送请求
    response = requests.get(url=url, headers=headers)
    response.encoding = 'utf-8'
    print(f"正在爬取第{page}页……")

    # 检查请求是否成功
    if response.status_code != 200:
        print(f'请求第{page}页失败，状态码：{response.status_code}')
        continue

    html = etree.HTML(response.text)
    # 获取所有条目的容器
    items = html.xpath("/html/body/div[1]/div/div/div[2]/div/div[3]/div[2]/div[1]/div[3]/div/a")

    # 准备存储数据的列表
    data = []

    # 开始解析
    for item in items:
        entry = {
            '标识码': item.xpath("./div[1]/span[3]/text()")[0],
            '企业名称': item.xpath("./div[2]/span/text()")[0],
            '行业归属': item.xpath("./div[3]/span[1]/text()")[0],
            '管理层级': item.xpath("./div[3]/span[2]/text()")[0]
        }
        data.append(entry)

    # 写入csv
    csv_file = "企业数据.csv"
    with open(csv_file,'a',newline='',encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['标识码', '企业名称', '行业归属', '管理层级'])
        writer.writerows(data)
        
    print(f"成功爬取{len(data)}条数据，已保存到: {csv_file}")
    sleep(7)
