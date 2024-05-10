import re
import keyword

def extract_method(filename):
    line_num = 1
    codes = {}
    variables = []
    indentation = False
    
    new_method = open('new_method1.py', 'w')
    new_method.writelines(['def', ' ', 'method():', '\n', ''])

    count = 0
    with open(filename, 'rb') as f:
        # count = 0
        flag = ''
        for line in f:
            line_with_whitespace = line.decode("utf-8")
            
            line_code_arr = re.split(r'(\s+)', line_with_whitespace)

            if line_num == 1:
                codes[line_num] = line_code_arr
                line_num += 1
                # print(line_code_arr)
                continue
            
            # Process the parts as needed
            if line_code_arr[2] == 'if' or line_code_arr[2] == 'elif' or line_code_arr[2] == 'else' or len(line_code_arr[1]) >= 8:
                indentation = True
            else:
                indentation = False
                
                
            if line_code_arr[2] == 'if' and len(line_code_arr[1]) == 4:
                flag = 'start'   
            if (line_code_arr[2] == 'elif' and len(line_code_arr[1]) == 4) or (line_code_arr[2] == 'else' and len(line_code_arr[1]) == 4):
                flag = 'stop'
            if flag == 'start':
                count +=1 
            elif flag == 'stop':
                continue
                

            # print(indentation)
            print(line_code_arr)
            if indentation == True:
                # print([line_code_arr])
                # count += 1
                for i in range(len(line_code_arr)):
                    if line_code_arr[i] == 'return' or line_code_arr[i] == '#':
                        break

                    if re.match(r'^["\']', line_code_arr[i]) is not None:
                        continue
                    
                    if line_code_arr[i].isalpha() and not keyword.iskeyword(line_code_arr[i]):
                        if line_code_arr[i] not in variables:
                            variables.append(line_code_arr[i])

                new_method.writelines(line_code_arr)

            print(count)
    # print(variables)
    # print(codes)
            

    parameters = ''
    for i in range(len(variables)):
        if i != len(variables) - 1:
            parameters += variables[i] + ', '
        else:
            parameters += variables[i]
    
    # print(new_method.readlines())
    
    new_method.close()

    with open('new_method1.py', 'r') as f:
        new_method_lines = f.readlines()
     
    # print(new_method_lines)
    first_line = new_method_lines[0]
    modified_first_line = first_line.replace("(", f"({parameters}")
    new_method_lines[0] = modified_first_line

    with open('new_method1.py', 'w') as file:
        file.writelines(new_method_lines)

    # with open('new_method.py', r)

# ['', '    ', 'num', ' ', '=', ' ', '10', '\n', '']
# ['', '    ', 'if', ' ', 'age', ' ', '<', ' ', '18:', '\n', '']
# ['', '    ', 'okay', ' ', '=', ' ', "'okay'"]

extract_method('/Users/sharraf/Documents/CSE400/Detecting-Refactoring-Python-Code-Smell/Refactor/example_code.py')