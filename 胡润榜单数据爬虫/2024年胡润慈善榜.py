import json
import pandas as pd
import os

def process_charity_json_to_csv(json_file_path, output_csv_path):
    """
    读取本地 2024年胡润慈善榜 JSON（列表或带 "rows"），
    对 'hs_Rank_Charity_ChaName_Cn' 中以顿号/逗号分隔的多姓名进行拆分，
    并将对应的年龄和出生地也按顺序拆分，其他字段保持一致，输出 CSV。
    """
    # 1. 读取 JSON
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 支持 dict 包含 rows 或者直接 list
    items = data.get('rows', data) if isinstance(data, dict) else data

    # 2. 初始化记录列表
    records = []

    for itm in items:
        # 拆分多个姓名（中文顿号、英文连字符、逗号都当分隔符）
        raw_names = itm.get("hs_Rank_Charity_ChaName_Cn", "")
        names = [n.strip() for n in raw_names.replace("、", ",").split(",") if n.strip()]

        # 拆分年龄
        raw_ages = itm.get("hs_Rank_Charity_Age", "")
        ages = []
        if isinstance(raw_ages, str) and raw_ages:
            ages = [a.strip() for a in raw_ages.replace("、", ",").split(",")]
        # 如果只有一个值，复制到所有人
        if len(ages) == 1 and len(names) > 1:
            ages = ages * len(names)
        # 补齐
        while len(ages) < len(names):
            ages.append("")

        # 拆分出生地
        raw_places = itm.get("hs_Rank_Charity_Birthplace_Cn", "")
        places = []
        if isinstance(raw_places, str) and raw_places:
            places = [p.strip() for p in raw_places.replace("、", ",").split(",")]
        if len(places) == 1 and len(names) > 1:
            places = places * len(names)
        while len(places) < len(names):
            places.append("")

        # 共享字段
        common = {
            '年份':                  itm.get("hs_Rank_Charity_Year", ""),
            '关系':                  itm.get("hs_Rank_Charity_Relations", ""),
            '排名':                  itm.get("hs_Rank_Charity_Ranking", ""),
            '排名变化':              itm.get("hs_Rank_Charity_Ranking_Change", ""),
            '捐赠额（亿元）':         itm.get("hs_Rank_Charity_Donation", ""),
            '捐赠额_USD（亿美元）':   itm.get("hs_Rank_Charity_Donation_USD", ""),
            '捐赠变化':              itm.get("hs_Rank_Charity_Donation_Change", ""),
            '公司名称':              itm.get("hs_Rank_Charity_ComName_Cn", ""),
            '公司总部':              itm.get("hs_Rank_Charity_ComHead_Cn", ""),
            '捐赠领域':              itm.get("hs_Rank_Charity_Cause_Cn", ""),
            '详情':                  itm.get("hs_Rank_Charity_Detial_Cn", "")
        }

        # 3. 生成拆分后的记录
        for i, name in enumerate(names):
            rec = {
                **common,
                '姓名': name,
                '年龄': ages[i],
                '出生地': places[i]
            }
            records.append(rec)

    # 4. 转 DataFrame 并保存 CSV
    df = pd.DataFrame(records)
    df.to_csv(output_csv_path, index=False, encoding='utf_8_sig')
    print(f"已生成 CSV：{output_csv_path}，共 {len(df)} 条记录")


if __name__ == "__main__":
    input_json  = "2024年胡润慈善榜.json"  # 替换为你的文件名
    output_csv = "2024年胡润慈善榜_拆分后.csv"
    process_charity_json_to_csv(input_json, output_csv)
