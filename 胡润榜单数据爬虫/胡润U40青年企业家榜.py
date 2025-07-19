import json
import pandas as pd
import time

def process_u40_json_to_csv(json_file_path, output_csv_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, dict) and 'rows' in data:
            item_list = data['rows']
        elif isinstance(data, list):
            item_list = data
        else:
            print("不支持的JSON格式")
            return False

        print(f"成功读取JSON数据，共 {len(item_list)} 条记录")

        # 初始化字段列表
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

        for item in item_list:
            names = item.get("hs_Rank_U40_ChaName_Cn", "").replace("、", ",").split(",")
            ages = item.get("hs_Rank_U40_Age", "").replace("、", ",").split(",")

            # 统一补齐年龄数组长度（如姓名有2个而年龄只有1个，则补空）
            while len(ages) < len(names):
                ages.append("")

            # 公共信息
            residence = item.get("hs_Rank_U40_Residence_Cn", "")
            company_name = item.get("hs_Rank_U40_ComName_Cn", "")
            industry = item.get("hs_Rank_U40_Industry_Cn", "")
            ranking = item.get("hs_Rank_U40_Ranking", "")
            ranking_change = item.get("hs_Rank_U40_Ranking_Change", "")
            wealth = item.get("hs_Rank_U40_Wealth", "")
            wealth_change = item.get("hs_Rank_U40_Wealth_Change", "")
            relations = item.get("hs_Rank_U40_Relations", "")

            for name, age in zip(names, ages):
                Fullname_Cn_list.append(name.strip())
                Age_list.append(age.strip())
                BirthPlace_Cn_list.append(residence)
                Gender_list.append("")  # 暂无性别字段
                ComName_Cn_list.append(company_name)
                ComHeadquarters_Cn_list.append("")  # 暂无总部字段
                Industry_Cn_list.append(industry)
                Ranking_list.append(ranking)
                Ranking_Change_list.append(ranking_change)
                Wealth_list.append(wealth)
                Wealth_Change_list.append(wealth_change)
                Education_Cn_list.append("")  # 暂无学历字段
                School_list.append("")  # 暂无院校字段
                Relations_list.append(relations)
                CharacterCount_list.append(len(names))

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

        df.to_csv(output_csv_path, index=False, encoding='utf_8_sig')
        print(f"数据处理完成，已保存为: {output_csv_path}")
        print(f"共处理 {len(df)} 条人物记录")
        return True

    except Exception as e:
        print(f"处理出错: {e}")
        return False

if __name__ == "__main__":
    input_json_path = "胡润U40青年企业家榜.json"
    output_csv_path = f"胡润U40青年企业家榜_{time.strftime('%Y%m%d%H%M%S')}.csv"
    success = process_u40_json_to_csv(input_json_path, output_csv_path)

    if success:
        print("处理成功完成!")
    else:
        print("处理失败！")
