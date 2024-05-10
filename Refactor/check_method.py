import re
import keyword

def check_method(filename):
    data, long_condition = {}, {}
    variables = []
    count, total_line_num, num_of_long_conditions, start = 0, 1, 0, 0
    indentation = False

    with open(filename, 'rb') as f:
        for line in f:
            line_with_whitespace = line.decode("utf-8")
            line_code_arr = re.split(r'(\s+)', line_with_whitespace)
            
            if total_line_num == 1:
                data[total_line_num] = line_code_arr
                total_line_num = 2
                continue

            if line_code_arr[2] == 'if' or line_code_arr[2] == 'elif' or line_code_arr[2] == 'else:' or len(line_code_arr[1]) >= 8:
                indentation = True
            else:
                indentation = False
                end = total_line_num - 1

            if indentation == True:
                count +=1
                for i in range(len(line_code_arr)):
                    if line_code_arr[i] == 'return' or line_code_arr[i] == '#':
                        break

                    if re.match(r'^["\']', line_code_arr[i]) is not None:
                        continue
                    
                    if line_code_arr[i].isalpha() and not keyword.iskeyword(line_code_arr[i]):
                        if line_code_arr[i] not in variables:
                            variables.append(line_code_arr[i])

                if line_code_arr[-1] != '':
                    indentation = False
                    end = total_line_num
            
            if count == 1:
                start = total_line_num

            if indentation == False:
                if count > 6:
                    num_of_long_conditions += 1
                    long_condition[num_of_long_conditions] = [[start, end], variables]
                count = 0
            
            data[total_line_num] = line_code_arr
            total_line_num += 1
                        
    # parameters = ''
    # for i in range(len(variables)):
    #     if i != len(variables) - 1:
    #         parameters += variables[i] + ', '
    #     else:
    #         parameters += variables[i]
    print(long_condition)
    return data, long_condition

check_method('Refactor/example_code.py')