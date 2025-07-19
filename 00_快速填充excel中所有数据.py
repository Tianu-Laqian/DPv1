import pandas as pd
import os

def fill_empty_cells(input_file, output_file=None):
    """
    读取Excel文件并填充空单元格（使用上方非空单元格的值）
    
    参数:
    input_file (str): 输入Excel文件路径
    output_file (str): 输出文件路径（默认为None，覆盖原文件）
    """
    try:
        # 读取Excel文件
        df = pd.read_excel(input_file, header=None)
        
        # 遍历每一列进行填充
        for col in range(df.shape[1]):
            # 使用ffill方法向前填充（使用上方非空值填充当前空值）
            df[col] = df[col].ffill()
        
        # 保存结果
        if output_file is None:
            output_file = input_file
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        df.to_excel(output_file, index=False, header=False)
        print(f"✅ 处理完成！结果已保存至: {output_file}")
        return True
    except Exception as e:
        print(f"❌ 处理过程中出错: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Excel空单元格填充工具")
    print("=" * 50)
    
    while True:
        # 获取输入文件路径
        input_file = input("\n📥 请输入Excel文件路径（或输入 'q' 退出）: ").strip()
        
        if input_file.lower() == 'q':
            print("👋 已退出程序")
            break
        
        # 验证文件是否存在
        if not os.path.isfile(input_file):
            print(f"❌ 文件不存在: {input_file}")
            continue
        
        # 获取输出文件路径
        output_file = input("\n📤 请输入输出文件路径（直接回车将覆盖原文件）: ").strip()
        
        # 如果用户未输入输出文件路径，使用原文件路径
        if not output_file:
            output_file = input_file
            print(f"⚠️ 注意：将覆盖原文件: {input_file}")
            confirm = input("   是否继续？(y/n): ").strip().lower()
            if confirm != 'y':
                print("↩️ 已取消操作")
                continue
        
        # 处理文件
        success = fill_empty_cells(input_file, output_file)
        
        # 询问是否继续处理其他文件
        if success:
            continue_option = input("\n🔄 是否继续处理其他文件？(y/n): ").strip().lower()
            if continue_option != 'y':
                print("👋 感谢使用，再见！")
                break