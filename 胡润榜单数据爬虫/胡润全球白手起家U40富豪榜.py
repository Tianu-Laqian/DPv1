import json
import pandas as pd
import time

def process_gu40_json_to_csv(json_file_path, output_csv_path):
    """
    处理胡润全球白手起家U40富豪榜 JSON，
    拆分多人物记录，输出与原CSV字段一致的表格。
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 支持顶层 dict 包含 rows，或直接列表
        if isinstance(data, dict) and 'rows' in data:
            items = data['rows']
        elif isinstance(data, list):
            items = data
        else:
            print("不支持的 JSON 格式")
            return False

        print(f"成功读取 JSON，共 {len(items)} 条记录")

        # 初始化所有列的列表
        Fullname_Cn, Age, BirthPlace_Cn, Gender = [], [], [], []
        ComName_Cn, ComHeadquarters_Cn, Industry_Cn = [], [], []
        Ranking, Ranking_Change = [], []
        Wealth, Wealth_Change = [], []
        Education_Cn, School = [], []
        Relations, CharacterCount = [], []

        for it in items:
            # 中文名与年龄可能含多个，用中文顿号或逗号分隔
            names = it.get("hs_Rank_GU40_ChaName_Cn", "").replace("、", ",").split(",")
            ages  = it.get("hs_Rank_GU40_Age", "").replace("、", ",").split(",")

            # 若年龄数量不足，则补空串
            while len(ages) < len(names):
                ages.append("")

            # 共享字段
            resid    = it.get("hs_Rank_GU40_Residence_Cn", "")
            comp     = it.get("hs_Rank_GU40_ComName_Cn", "")
            industry = it.get("hs_Rank_GU40_Industry_Cn", "")
            rank     = it.get("hs_Rank_GU40_Ranking", "")
            rank_chg = it.get("hs_Rank_GU40_Ranking_Change", "")
            wealth   = it.get("hs_Rank_GU40_Wealth", "")
            wealth_chg = it.get("hs_Rank_GU40_Wealth_Change", "")
            rel      = it.get("hs_Rank_GU40_Relations", "")

            # 拆分多人物
            for n, a in zip(names, ages):
                Fullname_Cn.append(n.strip())
                Age.append(a.strip())
                BirthPlace_Cn.append(resid)
                Gender.append("")  # JSON 中无性别字段
                ComName_Cn.append(comp)
                ComHeadquarters_Cn.append("")  # 无总部字段
                Industry_Cn.append(industry)
                Ranking.append(rank)
                Ranking_Change.append(rank_chg)
                Wealth.append(wealth)
                Wealth_Change.append(wealth_chg)
                Education_Cn.append("")  # 无学历字段
                School.append("")        # 无毕业院校字段
                Relations.append(rel)
                CharacterCount.append(len(names))

        # 构造 DataFrame 并输出
        df = pd.DataFrame({
            '姓名': Fullname_Cn,
            '关系': Relations,
            '条目人数': CharacterCount,
            '性别': Gender,
            '年龄': Age,
            '出生地': BirthPlace_Cn,
            '学历': Education_Cn,
            '毕业院校': School,
            '公司名称': ComName_Cn,
            '公司总部地': ComHeadquarters_Cn,
            '所在行业': Industry_Cn,
            '排名': Ranking,
            '排名变化': Ranking_Change,
            '财富值_人民币/亿元': Wealth,
            '财富值变化': Wealth_Change,
        })

        df.to_csv(output_csv_path, index=False, encoding='utf_8_sig')
        print(f"已保存 CSV: {output_csv_path}")
        print(f"总共导出 {len(df)} 条人物记录")
        return True

    except Exception as e:
        print(f"处理出错：{e}")
        return False


if __name__ == "__main__":
    input_path  = "胡润全球白手起家U40富豪榜.json"
    timestamp   = time.strftime('%Y%m%d%H%M%S')
    output_path = f"胡润全球白手起家U40富豪榜_{timestamp}.csv"
    if process_gu40_json_to_csv(input_path, output_path):
        print("全部完成！")
    else:
        print("处理失败，请检查错误。")
