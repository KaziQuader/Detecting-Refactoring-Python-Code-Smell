import re

def check_file_format(filename):
    new_lines = []
    need_format = False
    count = 0

    with open(filename, 'rb') as f:

        for line in f:
            modified_line = ''
            line_with_whitespace = line.decode("utf-8")
            line_code_arr = re.split(r'(\s+)', line_with_whitespace)
            
            if line_code_arr[1] == '\n' or line_code_arr[1] == '            \n':
                continue

            if count == 1 and len(line_code_arr[1]) > 4:
                need_format = True
            
            for i in range(len(line_code_arr)):
                if need_format:
                    if i == 1 and len(line_code_arr[i]) > 4:
                        spaces = len(line_code_arr[i]) - 4
                        indentation = ' ' * spaces
                        modified_line += indentation
                        continue

                modified_line += line_code_arr[i]

            new_lines.append(modified_line)
            count += 1

    with open(filename, 'w') as f:
        f.writelines(new_lines)
