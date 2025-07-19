import json
import pandas as pd
import time
import os

def process_u30_json_to_csv(json_file_path, output_csv_path):
    """
    读取本地 U30 创业先锋 JSON，拆分多姓名条目，
    并输出与既有 CSV 字段完全一致的表格。
    """
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 支持 dict 包含 rows 或者直接 list
    if isinstance(data, dict) and 'rows' in data:
        items = data['rows']
    elif isinstance(data, list):
        items = data
    else:
        raise ValueError(f"不支持的 JSON 结构: {type(data)}")

    # 初始化所有列
    cols = {
        '姓名': [], '关系': [], '条目人数': [], '性别': [], '年龄': [],
        '出生地': [], '学历': [], '毕业院校': [],
        '公司名称': [], '公司总部地': [], '所在行业': [],
        '排名': [], '排名变化': [], '财富值_人民币/亿元': [], '财富值变化': []
    }

    for itm in items:
        # 拆分多姓名
        raw_names = itm.get("hs_Rank_U30_ChaName_Cn", "")
        # 将“、”替换成英文逗号，再 split
        parts = [n.strip() for n in raw_names.replace("、", ",").split(",") if n.strip()]
        count = len(parts)

        # 共享字段
        rel  = itm.get("hs_Rank_U30_Relations", "")
        comp = itm.get("hs_Rank_U30_ComName_Cn", "")
        hq   = itm.get("hs_Rank_U30_ComHeadquarters_Cn", "")
        ind  = itm.get("hs_Rank_U30_Industry_Cn", "")
        rank = itm.get("hs_Rank_U30_Ranking", "")
        # U30 榜没有“排名变化”“财富”等，统一取空或 0
        rchg = ""  
        wealth = itm.get("hs_Rank_U30_Wealth", "")
        wchg = ""

        # 其他先锋字段 U30 JSON 中无性别/年龄/出生地/学历/学校
        for name in parts:
            cols['姓名'].append(name)
            cols['关系'].append(rel)
            cols['条目人数'].append(count)
            cols['性别'].append("")
            cols['年龄'].append("")
            cols['出生地'].append("")
            cols['学历'].append("")
            cols['毕业院校'].append("")
            cols['公司名称'].append(comp)
            cols['公司总部地'].append(hq)
            cols['所在行业'].append(ind)
            cols['排名'].append(rank)
            cols['排名变化'].append(rchg)
            cols['财富值_人民币/亿元'].append(wealth)
            cols['财富值变化'].append(wchg)

    # 输出为 DataFrame 并存 CSV
    df = pd.DataFrame(cols)
    # 如果文件已存在且非空，不写 header
    write_header = not os.path.exists(output_csv_path) or os.path.getsize(output_csv_path) == 0
    df.to_csv(output_csv_path, index=False, header=write_header, encoding='utf_8_sig')
    print(f"已生成 CSV：{output_csv_path}，共 {len(df)} 条记录")

if __name__ == "__main__":
    input_json = "2024年胡润Under30s创业先锋.json"  # 替换为你的 JSON 文件名
    timestamp = time.strftime("%Y%m%d%H%M%S")
    output_csv = f"2024年胡润Under30s创业先锋_{timestamp}.csv"
    process_u30_json_to_csv(input_json, output_csv)
