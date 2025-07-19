import random
import time
import os
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# 替换为你的“全球猎豹企业榜”编号
all_list = ['673NBWSE']  
filename = f'2024年胡润全球猎豹企业榜_{time.strftime("%Y%m%d%H%M%S")}.csv'

# 创建带重试机制的会话
session = requests.Session()
session.trust_env = False
retry = Retry(total=5, backoff_factor=1, status_forcelist=[429,500,502,503,504], allowed_methods=["GET"])
adapter = HTTPAdapter(max_retries=retry)
session.mount("http://", adapter)
session.mount("https://", adapter)

for num in all_list:
    page = 1
    while True:
        try:
            # 随机暂停，防封
            time.sleep(random.uniform(10, 20))
            offset = (page - 1) * 200
            url = (
                "https://www.hurun.net/zh-CN/Rank/HsRankDetailsList"
                f"?num={num}&search=&offset={offset}&limit=200"
            )
            headers = {
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Referer': 'https://www.hurun.net/zh-CN/Rank/HsRankDetails'
            }
            resp = session.get(url, headers=headers, timeout=30)
            if resp.status_code != 200:
                break

            data = resp.json().get("rows", [])
            if not data:
                break

            # 准备和之前完全一致的列容器
            rows = {
                '姓名': [], '关系': [], '条目人数': [], '性别': [], '年龄': [],
                '出生地': [], '学历': [], '毕业院校': [],
                '公司名称': [], '公司总部地': [], '所在行业': [],
                '排名': [], '排名变化': [], '财富值_人民币/亿元': [], '财富值变化': []
            }

            for item in data:
                # 拆分多位创始人
                names = item.get("hs_Rank_GCheetahs_Name_Cn", "")\
                            .replace("、", ",").split(",")
                names = [n.strip() for n in names if n.strip()]
                count = len(names)

                # 取公共字段
                comp = item.get("hs_Rank_GCheetahs_ComName_Cn", "")
                hq   = item.get("hs_Rank_GCheetahs_ComHeadquarters_Cn", "")
                ind  = item.get("hs_Rank_GCheetahs_Industry_Cn", "")
                # 由于没有“排名”，这里暂用“创立年份”填入“排名”（已删除）
                rank = item.get("hs_Rank_GCheetahs_Founding", "")
                
                for name in names:
                    rows['姓名'].append(name)
                    rows['关系'].append("")         # 无关系字段
                    rows['条目人数'].append(count)
                    rows['性别'].append("")         # 无性别字段
                    rows['年龄'].append("")         # 无年龄字段
                    rows['出生地'].append("")       # 无出生地字段
                    rows['学历'].append("")         # 无学历字段
                    rows['毕业院校'].append("")     # 无毕业院校字段
                    rows['公司名称'].append(comp)
                    rows['公司总部地'].append(hq)
                    rows['所在行业'].append(ind)
                    rows['排名'].append(rank)
                    rows['排名变化'].append("")     # 无排名变化字段
                    rows['财富值_人民币/亿元'].append("")   # 无财富值字段
                    rows['财富值变化'].append("")         # 无财富变化字段

            # 写入 CSV
            df = pd.DataFrame(rows)
            header = not os.path.exists(filename) or os.path.getsize(filename) == 0
            df.to_csv(filename, mode='a', index=False, header=header, encoding='utf_8_sig')
            print(f"已保存第 {page} 页，共 {len(df)} 条记录")
            page += 1

        except Exception as e:
            print(f"错误：{e}，等待 30 秒后重试")
            time.sleep(30)
            continue

print("抓取并保存完成 →", filename)
