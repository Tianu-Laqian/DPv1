import json
import pandas as pd
import time
import os

def process_generic_rank_json(json_file_path, output_csv_path):
    """
    读取本地 JSON（带 "rows"），按 hs_Rank_* 字段映射到既有 CSV 列，
    拆分多人名条目，缺失字段留空。
    """
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 提取 rows
    if isinstance(data, dict) and 'rows' in data:
        items = data['rows']
    elif isinstance(data, list):
        items = data
    else:
        raise ValueError(f"无法识别的 JSON 结构：{type(data)}")

    # 初始化列容器
    cols = {
        '姓名': [], '关系': [], '条目人数': [], '性别': [], '年龄': [],
        '出生地': [], '学历': [], '毕业院校': [],
        '公司名称': [], '公司总部地': [], '所在行业': [],
        '排名': [], '排名变化': [], '财富值_人民币/亿元': [], '财富值变化': []
    }

    for itm in items:
        # 拆分姓名
        raw_names = itm.get("hs_Rank_ChaName_Cn", "")
        # 将顿号替换逗号，再分割
        names = [n.strip() for n in raw_names.replace("、", ",").split(",") if n.strip()]
        count = len(names)

        # 拆分年龄（相同逻辑，如果有多年龄也能对应）
        raw_ages = itm.get("hs_Rank_Age", "")
        ages = [a.strip() for a in raw_ages.replace("、", ",").split(",")] if raw_ages else []
        # 补齐年龄列表
        while len(ages) < count:
            ages.append("")

        # 共享字段
        rel   = itm.get("hs_Rank_Relations", "")
        comp  = itm.get("hs_Rank_ComName_Cn", "")
        hq    = itm.get("hs_Rank_ComHeadquarters_Cn", "")
        ind   = itm.get("hs_Rank_Industry_Cn", "")
        rank  = itm.get("hs_Rank_Ranking", "")
        rchg  = itm.get("hs_Rank_Ranking_Change", "")  # 如果不存在，取空
        wealth = itm.get("hs_Rank_Wealth", "")
        wchg   = itm.get("hs_Rank_Wealth_Change", "")  # 如果不存在，取空

        for idx, name in enumerate(names):
            cols['姓名'].append(name)
            cols['关系'].append(rel)
            cols['条目人数'].append(count)
            cols['性别'].append("")             # JSON 中无此字段
            cols['年龄'].append(ages[idx])
            cols['出生地'].append("")           # JSON 中无此字段
            cols['学历'].append("")             # JSON 中无此字段
            cols['毕业院校'].append("")         # JSON 中无此字段
            cols['公司名称'].append(comp)
            cols['公司总部地'].append(hq)
            cols['所在行业'].append(ind)
            cols['排名'].append(rank)
            cols['排名变化'].append(rchg)
            cols['财富值_人民币/亿元'].append(wealth)
            cols['财富值变化'].append(wchg)

    # 构造 DataFrame
    df = pd.DataFrame(cols)

    # 写入 CSV，若文件已存在则追加且不写 header
    need_header = not os.path.exists(output_csv_path) or os.path.getsize(output_csv_path) == 0
    df.to_csv(output_csv_path, index=False, header=need_header, encoding='utf_8_sig')
    print(f"已生成 {output_csv_path} ，共 {len(df)} 条记录")


if __name__ == "__main__":
    input_json  = "2024年胡润Under35s中国创业先锋.json"  # 修改为你的 JSON 文件
    ts = time.strftime("%Y%m%d%H%M%S")
    output_csv = f"2024年胡润Under35s中国创业先锋_{ts}.csv"
    process_generic_rank_json(input_json, output_csv)
