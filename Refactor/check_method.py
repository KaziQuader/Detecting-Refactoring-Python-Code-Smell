import re
import keyword

def check_method(filename):
    line_num = 1
    codes = {}
    data = {}
    variables = []
    indentation = False
    long_condition = {}
    

    count = 0
    total_line_num = 0
    num_of_long_conditions = 0
    with open(filename, 'rb') as f:

        flag = ''
        for line in f:
            line_with_whitespace = line.decode("utf-8")
            
            line_code_arr = re.split(r'(\s+)', line_with_whitespace)
            
            total_line_num += 1
            if line_num == 1:
                codes[line_num] = line_code_arr
                line_num += 1
                # print(line_code_arr)
                continue
            
            # Process the parts as needed
            if line_code_arr[2] == 'if' or line_code_arr[2] == 'elif' or line_code_arr[2] == 'else:' or len(line_code_arr[1]) >= 8:
                indentation = True
            else:
                indentation = False


            # print(indentation)
            print(line_code_arr)
            if indentation == True:
                count +=1 
                # total_line_num = total_line_num
                for i in range(len(line_code_arr)):
                    if line_code_arr[i] == 'return' or line_code_arr[i] == '#':
                        break

                    if re.match(r'^["\']', line_code_arr[i]) is not None:
                        continue
                    
                    if line_code_arr[i].isalpha() and not keyword.iskeyword(line_code_arr[i]):
                        if line_code_arr[i] not in variables:
                            variables.append(line_code_arr[i])
            
            if indentation == False:
                if count > 6:
                    num_of_long_conditions += 1
                    print(total_line_num)
                    start = total_line_num-count
                    end = total_line_num-1
                    long_condition[num_of_long_conditions] = [[start, end], variables]
                count = 0
            
    
            data[total_line_num] = line_code_arr
            print(long_condition)
            # print(total_line_num)
            # print(count)
            # print(data)
    # print(variables)
    # print(codes)
            
    parameters = ''
    for i in range(len(variables)):
        if i != len(variables) - 1:
            parameters += variables[i] + ', '
        else:
            parameters += variables[i]
    # print(new_method.readlines())
    
    return data, long_condition

check_method('/Users/sharraf/Documents/CSE400/Detecting-Refactoring-Python-Code-Smell/Refactor/example_code.py')