import random
import time
import os
import json
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# 你的榜单编号列表（CTop500 一般只有一个）
all_list = ['Y7SPAAYO']
filename = f'2025年胡润中国500强_{time.strftime("%Y%m%d%H%M%S")}.csv'

# 创建具有重试机制的 requests 会话
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
            # 随机休眠，防止被封
            time.sleep(random.uniform(10, 20))
            
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
            print(f"状态码: {r.status_code}, 榜单: {num}, 页码: {page}")
            if r.status_code != 200:
                break

            data = r.json().get("rows", [])
            if not data:
                print("已无更多数据，退出。")
                break

            # 用于存储本页所有拆分后的人物记录
            rows = {
                '姓名': [], '关系': [], '条目人数': [], '性别': [], '年龄': [],
                '出生地': [], '学历': [], '毕业院校': [],
                '公司名称': [], '公司总部地': [], '所在行业': [],
                '排名': [], '排名变化': [], '财富值_人民币/亿元': [], '财富值变化': []
            }

            for item in data:
                # 拆分多人物姓名与年龄
                names = item.get("hs_Rank_CTop500_ChaName_Cn", "")\
                        .replace("、", ",").split(",")
                ages  = item.get("hs_Rank_CTop500_Age", "")\
                        .replace("、", ",").split(",")
                while len(ages) < len(names):
                    ages.append("")

                # 共享字段
                rel   = item.get("hs_Rank_CTop500_Relations", "")
                comp  = item.get("hs_Rank_CTop500_ComName_Cn", "")
                hq    = item.get("hs_Rank_CTop500_ComHeadquarters_Cn", "")
                ind   = item.get("hs_Rank_CTop500_Industry_Cn", "")
                rank  = item.get("hs_Rank_CTop500_Ranking", "")
                rchg  = item.get("hs_Rank_CTop500_Ranking_Change", "")
                w     = item.get("hs_Rank_CTop500_Wealth", "")
                wchg  = item.get("hs_Rank_CTop500_Wealth_Change", "")
                
                for name, age in zip(names, ages):
                    rows['姓名'].append(name.strip())
                    rows['关系'].append(rel)
                    rows['条目人数'].append(len(names))
                    rows['性别'].append("")   # JSON 中无性别字段
                    rows['年龄'].append(age.strip())
                    rows['出生地'].append("") # JSON 中无出生地字段
                    rows['学历'].append("")   # 无学历
                    rows['毕业院校'].append("") # 无毕业院校
                    rows['公司名称'].append(comp)
                    rows['公司总部地'].append(hq)
                    rows['所在行业'].append(ind)
                    rows['排名'].append(rank)
                    rows['排名变化'].append(rchg)
                    rows['财富值_人民币/亿元'].append(w)
                    rows['财富值变化'].append(wchg)

            # 将本页数据写入 CSV
            df = pd.DataFrame(rows)
            header = not os.path.exists(filename) or os.path.getsize(filename) == 0
            df.to_csv(filename, mode='a', index=False, header=header, encoding='utf_8_sig')
            print(f"已保存：第 {page} 页，共 {len(df)} 条拆分后记录")

            page += 1

        except Exception as e:
            print(f"错误：{e}，等待后重试…")
            time.sleep(30)
            continue

print("全部抓取并保存完成！")
