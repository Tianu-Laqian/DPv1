import json
import pandas as pd
import os
import time

def process_json_to_csv(json_file_path, output_csv_path):
    """
    从本地JSON文件读取数据并处理成CSV格式
    
    参数:
        json_file_path: 本地JSON文件路径
        output_csv_path: 输出CSV文件路径
    """
    try:
        # 读取JSON文件
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 检查数据格式，提取rows列表
        if isinstance(data, dict) and 'rows' in data:
            item_list = data['rows']
        elif isinstance(data, list):
            item_list = data
        else:
            print(f"不支持的JSON格式: {type(data)}")
            return
        
        print(f"成功读取JSON数据，共 {len(item_list)} 条记录")
        
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
        
        for item in item_list:
            # 获取所有相关人物
            characters = item.get("hs_Character", [])
            
            # 如果没有人物信息，跳过当前条目
            if not characters:
                continue
            
            # 获取共享信息 - 使用女企业家榜字段前缀
            relations = item.get("hs_Rank_CWomen_Relations", "")  
            company_name = item.get("hs_Rank_CWomen_ComName_Cn", "")  
            company_hq_cn = item.get("hs_Rank_CWomen_ComHeadquarters_Cn", "")  
            industry = item.get("hs_Rank_CWomen_Industry_Cn", "")  
            ranking = item.get("hs_Rank_CWomen_Ranking", "")  
            ranking_change = item.get("hs_Rank_CWomen_Ranking_Change", "")  
            wealth = item.get("hs_Rank_CWomen_Wealth", "")  
            wealth_change = item.get("hs_Rank_CWomen_Wealth_Change", "")  
            
            # 遍历所有人物
            for char in characters:
                # 添加个人信息
                Fullname_Cn_list.append(char.get("hs_Character_Fullname_Cn", ""))
                Gender_list.append(char.get("hs_Character_Gender_Lang", ""))
                Age_list.append(char.get("hs_Character_Age", ""))
                
                # 出生地处理：优先使用中文出生地
                birth_place = char.get("hs_Character_BirthPlace_Cn", "")
                if not birth_place:
                    birth_place = char.get("hs_Character_NativePlace_Cn", "")  # 备用使用籍贯
                BirthPlace_Cn_list.append(birth_place)
                
                Education_Cn_list.append(char.get("hs_Character_Education_Cn", ""))
                
                # 毕业院校处理：优先使用中文
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
        
        # 保存为CSV
        df.to_csv(output_csv_path, index=False, encoding='utf_8_sig')
        print(f"数据处理完成，已保存到: {output_csv_path}")
        print(f"共处理 {len(df)} 条记录")
        
        return True
        
    except Exception as e:
        print(f"处理JSON文件时发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    # 输入JSON文件路径
    input_json_path = "胡润女企业家榜.json"
    
    # 输出CSV文件路径
    output_csv_path = f"胡润女企业家榜_{time.strftime('%Y%m%d%H%M%S')}.csv"
    
    # 处理JSON并生成CSV
    success = process_json_to_csv(input_json_path, output_csv_path)
    
    if success:
        print("处理成功完成!")
    else:
        print("处理过程中出现问题，请检查错误信息")