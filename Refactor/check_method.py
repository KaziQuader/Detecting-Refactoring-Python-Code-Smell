import re
import keyword

def create_parameters(line_code_arr, all_variables, variables=None):
    for i in range(len(line_code_arr)):
        flag = False
        if line_code_arr[i] == 'return' or line_code_arr[i] == '#':
            break

        if re.match(r'^["\']', line_code_arr[i]) is not None:
            break

        if line_code_arr[i] == '':
            continue

        if line_code_arr[i][-1] == ':' or line_code_arr[i][-1] == ',':
            line_code_arr[i] = line_code_arr[i][:-1]
        
        if ("_" in line_code_arr[i] and line_code_arr[i].split('_')[-1].isalpha() and '.' not in line_code_arr[i]):
            flag = True

        if (line_code_arr[i].isalpha() or flag) and not keyword.iskeyword(line_code_arr[i]):
            print(line_code_arr[i])
            if variables is not None:
                if line_code_arr[i] not in variables:
                    variables.append(line_code_arr[i])

            if variables is None:
                all_variables[line_code_arr[i]] = "Seen"

            

def check_method(filename):
    data, long_condition = {}, {}
    variables = []
    count, total_line_num, num_of_long_conditions, start = 0, 1, 0, 0
    indentation = False
    condition_flag = False
    loop_flag = False
    all_variables = {}
    for_loop = 0
    spaces = 4
    refactor_arr = ['for', 'if', 'else', 'elif']

    with open(filename, 'rb') as f:

        for line in f:
            line_with_whitespace = line.decode("utf-8")
            line_code_arr = re.split(r'(\s+)', line_with_whitespace)

            if total_line_num == 1:
                data[total_line_num] = line_code_arr
                total_line_num = 2
                continue

            

            data[total_line_num] = line_code_arr
            if line_code_arr[1] == "#":
                total_line_num += 1
                continue

            if line_code_arr[1] == "    ":
                loop_flag = False

            if line_code_arr[2] == 'for':
                for_loop += 1
                loop_flag = True
                spaces += 4
                # total_line_num += 1
                # continue

            if loop_flag == False:
                spaces = 4
            
            print(spaces)
            print(line_code_arr)
            if line_code_arr[2] == 'if' or line_code_arr[2] == 'elif' or line_code_arr[2] == 'else:':
                condition_flag = True
            elif len(line_code_arr[1]) == spaces: 
                condition_flag = False

            
            # print(condition_flag)
            if condition_flag == True and len(line_code_arr[1]) >= spaces:
                indentation = True
            else:
                condition_flag = False
                indentation = False
                end = total_line_num - 1
            
            create_parameters(line_code_arr, all_variables)
            # print(indentation)
            if indentation == True:
                count +=1
                create_parameters(line_code_arr, all_variables, variables)
                        
                # print(long_condition)
                if line_code_arr[-1] != '':
                    indentation = False
                    end = total_line_num
            
            if count == 1:
                start = total_line_num 

            if indentation == False:
                if 6 < count < 50:
                    num_of_long_conditions += 1
                    long_condition[num_of_long_conditions] = [[start, end], variables, spaces]
                    variables = []
                else:
                    variables = []
                count = 0

            total_line_num += 1
    for key in all_variables.items() :
        print (key)    
        
    return data, long_condition