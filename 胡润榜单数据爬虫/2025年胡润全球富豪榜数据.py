import random
import time
import os
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

all_list = ['ND77BFWM']
filename = f'2025年胡润全球富豪榜_{time.strftime("%Y%m%d%H%M%S")}.csv'

# 创建具有重试机制的会话
session = requests.Session()
session.trust_env = False  # 忽略系统代理设置

# 设置重试策略
retry_strategy = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

for j in range(len(all_list)):
    num = all_list[j]
    for page in range(1, 20):
        try:
            sleep_seconds = random.uniform(10, 20)
            time.sleep(sleep_seconds)
            
            offset = (page - 1) * 200
            url = f"https://www.hurun.net/zh-CN/Rank/HsRankDetailsList?num={num}&search=&offset={offset}&limit=200"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Referer': 'https://www.hurun.net/zh-CN/Rank/HsRankDetails?pagetype=rich',
            }
            
            r = session.get(url, headers=headers, timeout=30)
            print(f"状态码: {r.status_code}, 榜单: {num}, 页码: {page}")
            
            if r.status_code != 200:
                print(f"请求失败，状态码: {r.status_code}")
                continue
                
            json_data = r.json()
            
            # 初始化数据容器
            Fullname_Cn_list = []  
            Age_list = []  
            BirthPlace_Cn_list = []  
            Gender_list = []  
            ComName_Cn_list = []  
            ComHeadquarters_Cn_list = []  
            Industry_Cn_list = []  
            Ranking_list = []  
            Ranking_Change_list = []  
            Wealth_list = []  
            Wealth_Change_list = []  
            Education_Cn_list = []
            School_list = []  
            Relations_list = []  
            CharacterCount_list = []  
            
            item_list = json_data.get("rows", [])
            if not item_list:
                print(f"无数据: 榜单 {num} 页码 {page}")
                break
                
            print(f"开始解析json数据，本页有 {len(item_list)} 条记录")
            
            for item in item_list:
                # 获取所有相关人物
                characters = item.get("hs_Character", [])
                
                # 如果没有人物信息，跳过当前条目
                if not characters:
                    continue
                
                # 获取共享信息 - 使用新的字段名前缀
                relations = item.get("hs_Rank_Global_Relations", "")  # 更新字段名
                company_name = item.get("hs_Rank_Global_ComName_Cn", "")  # 更新字段名
                company_hq_cn = item.get("hs_Rank_Global_ComHeadquarters_Cn", "")  # 更新字段名
                industry = item.get("hs_Rank_Global_Industry_Cn", "")  # 更新字段名
                ranking = item.get("hs_Rank_Global_Ranking", "")  # 更新字段名
                ranking_change = item.get("hs_Rank_Global_Ranking_Change", "")  # 更新字段名
                wealth = item.get("hs_Rank_Global_Wealth", "")  # 更新字段名
                wealth_change = item.get("hs_Rank_Global_Wealth_Change", "")  # 更新字段名
                
                # 遍历所有人物
                for char in characters:
                    # 添加个人信息
                    Fullname_Cn_list.append(char.get("hs_Character_Fullname_Cn", ""))
                    Gender_list.append(char.get("hs_Character_Gender_Lang", ""))
                    Age_list.append(char.get("hs_Character_Age", ""))
                    BirthPlace_Cn_list.append(char.get("hs_Character_BirthPlace_Cn", ""))
                    Education_Cn_list.append(char.get("hs_Character_Education_Cn", ""))
                    
                    # 处理毕业院校字段
                    school_cn = char.get("hs_Character_School_Cn", "")
                    school_en = char.get("hs_Character_School_En", "")
                    School_list.append(school_cn if school_cn else school_en)
                    
                    # 添加共享的公司信息和关系
                    Relations_list.append(relations)
                    ComName_Cn_list.append(company_name)
                    ComHeadquarters_Cn_list.append(company_hq_cn)
                    Industry_Cn_list.append(industry)
                    Ranking_list.append(ranking)
                    Ranking_Change_list.append(ranking_change)
                    Wealth_list.append(wealth)
                    Wealth_Change_list.append(wealth_change)
                    
                    # 记录当前条目中的人数
                    CharacterCount_list.append(len(characters))
            
            # 创建数据框
            df = pd.DataFrame({
                '姓名': Fullname_Cn_list,                
                '关系': Relations_list,
                '条目人数': CharacterCount_list,
                '性别': Gender_list,
                '年龄': Age_list,
                '出生地': BirthPlace_Cn_list,
                '学历': Education_Cn_list,
                '毕业院校': School_list,
                '公司名称': ComName_Cn_list,
                '公司总部地': ComHeadquarters_Cn_list,
                '所在行业': Industry_Cn_list,
                '排名': Ranking_list,
                '排名变化': Ranking_Change_list,
                '财富值_人民币/亿元': Wealth_list,
                '财富值变化': Wealth_Change_list,
            })
            
            # 智能写入表头
            header = not os.path.exists(filename) or os.path.getsize(filename) == 0
            df.to_csv(
                filename, 
                mode='a', 
                index=False, 
                header=header, 
                encoding='utf_8_sig'
            )
            print(f"榜单 {num} 第 {page} 页已保存, 共 {len(df)} 条记录")
            
        except Exception as e:
            print(f"发生错误: {str(e)}")
            # 等待更长时间后重试
            time.sleep(30)
            continue