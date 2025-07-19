import csv
import requests
from lxml import etree
from urllib.parse import urljoin
from time import sleep
import random

# 各地区主页 URL 列表
region_pages = [
    'https://www.mfa.gov.cn/web/zwjg_674741/zwsg_674743/yz_674745/',    # 亚洲
    'https://www.mfa.gov.cn/web/zwjg_674741/zwsg_674743/fz_674747/',    # 非洲
    'https://www.mfa.gov.cn/web/zwjg_674741/zwsg_674743/xo_674749/',    # 欧洲
    'https://www.mfa.gov.cn/web/zwjg_674741/zwsg_674743/xybf_674751/',  # 北美洲
    'https://www.mfa.gov.cn/web/zwjg_674741/zwsg_674743/dozy_674753/',  # 南美洲
    'https://www.mfa.gov.cn/web/zwjg_674741/zwsg_674743/bmdyz_674755/'  # 大洋洲
]

# CSV 文件头
csv_file = 'embassies.csv'
with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['地区', '机构', '姓名', '职务', 'url'])

# 创建无代理的会话
session = requests.Session()
# ↓ 这一行已取消代理设置
# session.proxies.update(proxies)
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
})

for region_url in region_pages:
    try:
        resp = session.get(region_url, timeout=10)
        resp.encoding = resp.apparent_encoding
        tree = etree.HTML(resp.text)
        region_name = tree.xpath('/html/body/div[4]/div[2]/div[2]/div/div/text()')
        region_name = region_name[0].strip() if region_name else ''
        sleep(2)

        # 提取所有使馆链接
        hrefs = tree.xpath('/html/body/div[4]/div[2]/div[2]/div/ul/li/a/@href')
        for href in hrefs:
            full_url = urljoin(region_url, href.strip())
            sleep(random.uniform(4, 7))

            try:
                r2 = session.get(full_url, timeout=10)
                r2.encoding = r2.apparent_encoding
                t2 = etree.HTML(r2.text)

                # 获取机构名
                inst = t2.xpath('/html/body/div[4]/div[2]/div/div[1]/h1/text()')
                inst = inst[0].strip() if inst else ''

                # 获取职务与姓名，尝试多种结构
                info_text = ''
                xpaths = [
                    '//*[@id="News_Body_Txt_A"]/div/div/p[1]/text()',
                    '//*[@id="News_Body_Txt_A"]/div/p[1]/text()',
                    '//*[@id="News_Body_Txt_A"]/p[1]/text()',
                    '//*[@id="News_Body_Txt_A"]//p[1]//text()',
                ]

                for xp in xpaths:
                    try:
                        result = t2.xpath(xp)
                        if result:
                            info_text = ''.join(result).strip()
                            if '：' in info_text:
                                break
                    except:
                        continue

                # 拆分职务与姓名
                if '：' in info_text:
                    duty, name = [s.strip() for s in info_text.split('：', 1)]
                else:
                    duty, name = '', info_text

                # 写入 CSV
                with open(csv_file, 'a', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow([region_name, inst, name, duty, full_url])
                print(f'已写入：[{region_name}] {inst} — {duty} {name}')
            except Exception as e:
                print(f'详情页请求失败：{full_url}，错误：{e}')

    except Exception as e:
        print(f'区域页请求失败：{region_url}，错误：{e}')

print('全部爬取完成，结果保存在', csv_file)
