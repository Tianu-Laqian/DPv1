import random
import time
import os
import json
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# 你的 G1000 榜单编号列表
all_list = ['SSE9A6NO']  # 替换为真正的世界1000强编号
filename = f'2024年胡润世界1000强_{time.strftime("%Y%m%d%H%M%S")}.csv'

# 带重试的 Session
session = requests.Session()
session.trust_env = False
retry_strategy = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

for num in all_list:
    page = 1
    while True:
        try:
            time.sleep(random.uniform(10, 20))  # 随机休眠

            offset = (page - 1) * 200
            url = (
                "https://www.hurun.net/zh-CN/Rank/HsRankDetailsList"
                f"?num={num}&search=&offset={offset}&limit=200"
            )
            headers = {
                'User-Agent': (
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/125.0.0.0 Safari/537.36'
                ),
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Referer': (
                    'https://www.hurun.net/zh-CN/Rank/HsRankDetails?pagetype=rich'
                ),
            }
            r = session.get(url, headers=headers, timeout=30)
            print(f"[{r.status_code}] 榜单 {num} 第 {page} 页")
            if r.status_code != 200:
                break

            data = r.json().get("rows", [])
            if not data:
                print("无更多数据，结束。")
                break

            # 本页所有记录
            rows = {
                '姓名': [], '关系': [], '条目人数': [], '性别': [], '年龄': [],
                '出生地': [], '学历': [], '毕业院校': [],
                '公司名称': [], '公司总部地': [], '所在行业': [],
                '排名': [], '排名变化': [], '财富值_人民币/亿元': [], '财富值变化': []
            }

            for item in data:
                # G1000 样例中一般一人，无需多名拆分
                name = item.get("hs_Rank_G1000_ChaName_Cn", "").strip()
                age  = ""  # JSON 中无年龄字段
                rel  = item.get("hs_Rank_G1000_Relations", "")
                comp = item.get("hs_Rank_G1000_ComName_Cn", "")
                hq   = item.get("hs_Rank_G1000_ComHeadquarters_Cn", "")
                ind  = item.get("hs_Rank_G1000_Industry_Cn", "")
                rank = item.get("hs_Rank_G1000_Ranking", "")
                rchg = item.get("hs_Rank_G1000_Ranking_Change", "")
                w    = item.get("hs_Rank_G1000_Wealth", "")
                wchg = item.get("hs_Rank_G1000_Wealth_Change", "")

                # 填充一行
                rows['姓名'].append(name)
                rows['关系'].append(rel)
                rows['条目人数'].append(1)
                rows['性别'].append("")      # G1000 JSON 无性别
                rows['年龄'].append(age)
                rows['出生地'].append("")    # 无出生地字段
                rows['学历'].append("")      # 无学历字段
                rows['毕业院校'].append("")    # 无毕业院校字段
                rows['公司名称'].append(comp)
                rows['公司总部地'].append(hq)
                rows['所在行业'].append(ind)
                rows['排名'].append(rank)
                rows['排名变化'].append(rchg)
                rows['财富值_人民币/亿元'].append(w)
                rows['财富值变化'].append(wchg)

            # 写入 CSV
            df = pd.DataFrame(rows)
            header = not os.path.exists(filename) or os.path.getsize(filename) == 0
            df.to_csv(filename, mode='a', index=False, header=header, encoding='utf_8_sig')
            print(f"已保存：第 {page} 页，共 {len(df)} 条记录")

            page += 1

        except Exception as e:
            print(f"错误：{e}，等待重试…")
            time.sleep(30)
            continue

print("抓取并保存完成！")
