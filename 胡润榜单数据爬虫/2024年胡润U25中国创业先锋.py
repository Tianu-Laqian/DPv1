import json
import pandas as pd
import time
import os

def process_u25_cn_json_to_csv(json_file_path, output_csv_path):
    """
    读取本地 U25 中国创业先锋 JSON（带 "rows"），按 hs_Rank_* 字段映射到既有 CSV 列，
    拆分多人名条目，缺失字段留空。
    """
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 提取 rows 列表
    if isinstance(data, dict) and 'rows' in data:
        items = data['rows']
    elif isinstance(data, list):
        items = data
    else:
        raise ValueError(f"不支持的 JSON 结构: {type(data)}")

    # 初始化所有列容器
    cols = {
        '姓名': [], '关系': [], '条目人数': [],
        '性别': [], '年龄': [],
        '出生地': [], '学历': [], '毕业院校': [],
        '公司名称': [], '公司总部地': [], '所在行业': [],
        '排名': [], '排名变化': [], '财富值_人民币/亿元': [], '财富值变化': []
    }

    for itm in items:
        # 拆分多姓名（顿号/逗号）
        raw_names = itm.get("hs_Rank_ChaName_Cn", "")
        names = [
            n.strip() for n in raw_names.replace("、", ",").split(",")
            if n.strip()
        ]
        count = len(names)

        # 拆分年龄，对应人数
        raw_age = itm.get("hs_Rank_Age", "")
        ages = []
        if isinstance(raw_age, (int, float)):
            ages = [str(raw_age)]
        elif isinstance(raw_age, str) and raw_age:
            ages = [a.strip() for a in raw_age.replace("、", ",").split(",")]
        while len(ages) < count:
            ages.append("")

        # 共享字段映射
        relations   = itm.get("hs_Rank_Relations", "")
        company     = itm.get("hs_Rank_ComName_Cn", "")
        headquarters= itm.get("hs_Rank_ComHeadquarters_Cn", "")
        industry    = itm.get("hs_Rank_Industry_Cn", "")
        ranking     = itm.get("hs_Rank_Ranking", "")
        ranking_chg = itm.get("hs_Rank_Ranking_Change", "")
        wealth      = itm.get("hs_Rank_Wealth", "")
        wealth_chg  = itm.get("hs_Rank_Wealth_Change", "")

        for idx, name in enumerate(names):
            cols['姓名'].append(name)
            cols['关系'].append(relations)
            cols['条目人数'].append(count)
            cols['性别'].append("")            # JSON 中无此字段
            cols['年龄'].append(ages[idx])
            cols['出生地'].append("")          # JSON 中无此字段
            cols['学历'].append("")            # JSON 中无此字段
            cols['毕业院校'].append("")        # JSON 中无此字段
            cols['公司名称'].append(company)
            cols['公司总部地'].append(headquarters)
            cols['所在行业'].append(industry)
            cols['排名'].append(ranking)
            cols['排名变化'].append(ranking_chg)
            cols['财富值_人民币/亿元'].append(wealth)
            cols['财富值变化'].append(wealth_chg)

    # 构造 DataFrame 并保存为 CSV
    df = pd.DataFrame(cols)
    need_header = not os.path.exists(output_csv_path) or os.path.getsize(output_csv_path) == 0
    df.to_csv(output_csv_path, index=False, header=need_header, encoding='utf_8_sig')
    print(f"已生成 CSV：{output_csv_path}，共 {len(df)} 条记录")


if __name__ == "__main__":
    input_json  = "2024年胡润U25中国创业先锋.json"  # 替换为你的 JSON 文件名
    ts = time.strftime("%Y%m%d%H%M%S")
    output_csv = f"2024年胡润U25中国创业先锋_{ts}.csv"
    process_u25_cn_json_to_csv(input_json, output_csv)
