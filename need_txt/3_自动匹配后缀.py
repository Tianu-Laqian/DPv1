with open('result.txt', 'r', encoding='utf-8') as fin, \
         open('result2.txt', 'w', encoding='utf-8') as fout:
        
        for line_num, line in enumerate(fin, 1):
            # 移除行尾换行符和空格
            clean_line = line.rstrip('\n').rstrip()
            new_line = clean_line

            if line_num % 2 == 1:
                if clean_line.endswith('处'):
                      new_line = clean_line + '处长'
                if clean_line.endswith('司'):
                      new_line = clean_line + '司长'
                if clean_line.endswith('室'):
                      new_line = clean_line + '主任'
                if clean_line.endswith('厅'):
                      new_line = clean_line + '主任'
                if clean_line.endswith('心'):
                      new_line = clean_line + '主任'
                if clean_line.endswith('会'):
                      new_line = clean_line + '会长'
                if clean_line.endswith('委'):
                      new_line = clean_line + '书记'
                if clean_line.endswith('局'):
                      new_line = clean_line + '局长'
                if clean_line.endswith('所'):
                      new_line = clean_line + '所长'
                if clean_line.endswith('院'):
                      new_line = clean_line + '院长'
                if clean_line.endswith('社'):
                      new_line = clean_line + '社长'
                if clean_line.endswith('部'):
                      new_line = clean_line + '部长'
                if clean_line.endswith('办'):
                      new_line = clean_line + '主任'
                
            else:
                if clean_line.endswith('处'):
                      new_line = clean_line + '副处长'
                if clean_line.endswith('司'):
                      new_line = clean_line + '副司长'
                if clean_line.endswith('室'):
                      new_line = clean_line + '副主任'
                if clean_line.endswith('厅'):
                      new_line = clean_line + '副主任'
                if clean_line.endswith('心'):
                      new_line = clean_line + '副主任'
                if clean_line.endswith('会'):
                      new_line = clean_line + '副会长'
                if clean_line.endswith('委'):
                      new_line = clean_line + '副书记'
                if clean_line.endswith('局'):
                      new_line = clean_line + '副局长'
                if clean_line.endswith('所'):
                      new_line = clean_line + '副所长'
                if clean_line.endswith('院'):
                      new_line = clean_line + '副院长'
                if clean_line.endswith('社'):
                      new_line = clean_line + '副社长'
                if clean_line.endswith('部'):
                      new_line = clean_line + '副部长'
                if clean_line.endswith('办'):
                      new_line = clean_line + '副主任'

            # 写入处理后的行并恢复换行符
            fout.write(new_line + '\n')