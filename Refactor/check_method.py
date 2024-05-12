import re
import keyword

def check_variable_scope(arr):
    arr_to_str = ', '.join(arr)
    line = arr_to_str

    # Splitting the line by '=' and extracting the variables
    variables_part = line.split('=')[0].strip()

    # Splitting the variables_part by ',' and stripping extra spaces
    variable_names = [var.strip() for var in variables_part.split(',')]
    variable_names = [element for element in variable_names if element != '']
    return variable_names

# def extract_params(arr):
#     arr_to_str = ', '.join(arr)
#     signature = arr_to_str
#     # print(signature)
#     # Extract parameters using regular expressions
#     parameters = re.findall(r'\b\w+\b', signature)[1:]
#     # print(parameters)
#     return parameters

def check_method(filename):
    data, long_condition = {}, {}
    variables = []
    count, total_line_num, num_of_long_conditions, start = 0, 1, 0, 0
    indentation = False
    condition_flag = False

    with open(filename, 'rb') as f:
    
        for line in f:
            line_with_whitespace = line.decode("utf-8")
            line_code_arr = re.split(r'(\s+)', line_with_whitespace)
            
            
            
            if line_code_arr[1] == '\n':
                total_line_num += 1
                condition_flag = False
                continue

            if total_line_num == 1:
                data[total_line_num] = line_code_arr
                total_line_num = 2
                continue
            
            # print(line_code_arr)
            if line_code_arr[2] == 'if' or line_code_arr[2] == 'elif' or line_code_arr[2] == 'else:':
                condition_flag = True
                # print(line_code_arr[2])
            elif len(line_code_arr[1]) == 4: 
                scope_variables = check_variable_scope(line_code_arr) 
                condition_flag = False

            # print(condition_flag)
            if condition_flag == True and len(line_code_arr[1]) >= 4:
                indentation = True
            else:
                condition_flag = False
                indentation = False
                end = total_line_num - 1

            # print(indentation)
            if indentation == True:
                count +=1
                for i in range(len(line_code_arr)):
                    if line_code_arr[i] == 'return' or line_code_arr[i] == '#':
                        break

                    if re.match(r'^["\']', line_code_arr[i]) is not None:
                        break
                    
                    
                    if (line_code_arr[i].isalpha() and not keyword.iskeyword(line_code_arr[i])):
                        if line_code_arr[i] not in variables:
                            variables.append(line_code_arr[i])
                        
                        # if line_code_arr[i] in scope_variables:
                        #     print(scope_variables)
                        #     print(line_code_arr[i])
                        #     variables.append(line_code_arr[i])
                        #     print(variables)
                # print(long_condition)
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
            
            
            # print(data[1])
            # params = extract_params(data[1])
            # print(params)
    print(long_condition)
                        
    return data, long_condition