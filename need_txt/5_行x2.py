with open('input.txt', 'r', encoding='utf-8') as infile:
    with open('result.txt', 'w', encoding='utf-8') as outfile:
        for raw_line in infile:
            line = raw_line.strip().replace(' ', '')
            outfile.write(line + '\n')
            outfile.write(line + '\n')