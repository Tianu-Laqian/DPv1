import random
import time
import os
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# 枚举你要抓取的榜单编号（替换为实际的 GDr 列表号）
all_list = ['LR37jXR2']  
# 输出文件名
filename = f'2018年胡润平安中国好医生榜_{time.strftime("%Y%m%d%H%M%S")}.csv'

# 创建带重试的 Requests 会话
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
            time.sleep(random.uniform(10, 20))
            offset = (page - 1) * 200
            url = (
                "https://www.hurun.net/zh-CN/Rank/HsRankDetailsList"
                f"?num={num}&search=&offset={offset}&limit=200"
            )
            headers = {
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Referer': 'https://www.hurun.net/zh-CN/Rank/HsRankDetails?pagetype=rich'
            }
            resp = session.get(url, headers=headers, timeout=30)
            print(f"[{resp.status_code}] 榜单 {num} 第 {page} 页")
            if resp.status_code != 200:
                break

            rows = resp.json().get("rows", [])
            if not rows:
                print("无更多数据，退出分页。")
                break

            # 收集本页数据
            data = {
                '城市': [],
                '科室': [],
                '姓名': [],
                '所在医院': [],
                '职称': []
            }

            for itm in rows:
                # 直接映射字段
                data['城市'].append(itm.get("hs_Rank_GDr_City_Cn", "").strip())
                data['科室'].append(itm.get("hs_Rank_GDr_Depart_Cn", "").strip())
                data['姓名'].append(itm.get("hs_Rank_GDr_Name_Cn", "").strip())
                data['所在医院'].append(itm.get("hs_Rank_GDr_Hospital_Cn", "").strip())
                data['职称'].append(itm.get("hs_Rank_GDr_Title_Cn", "").strip())

            # 生成 DataFrame 并写入 CSV
            df = pd.DataFrame(data)
            header = not os.path.exists(filename) or os.path.getsize(filename) == 0
            df.to_csv(filename, mode='a', index=False, header=header, encoding='utf_8_sig')
            print(f"已保存 第 {page} 页，共 {len(df)} 条记录")

            page += 1

        except Exception as e:
            print(f"错误：{e}，等待重试…")
            time.sleep(30)
            continue

print("抓取完成，文件：", filename)
