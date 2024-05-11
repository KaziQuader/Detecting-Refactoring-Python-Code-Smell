method_count = 1
function_name_ending = ['):', '\n', '']
functions = ['']

def write_function_name(parameters):
    global method_count, function_name_ending, functions
    function_name = ['def', ' ', f'method_{method_count}(']
        
    for i in range(len(parameters)):
        if i != len(parameters) - 1:
            function_name.append(parameters[i] + ',')
            function_name.append(' ')
        else:
            function_name.append(parameters[i])

    function_name.extend(function_name_ending)
    method_count += 1
    
    # print(function_name)
    name = '    '
    for i  in function_name[2:]:
        if i == '):':
            i = ')'
        name += i
    functions.append(name)
    # print(functions)
    return function_name


def extract_method(data, long_condition):
    new_method = open('Refactor/new_method.py', 'w')
    
    for key in long_condition:
        parameters = long_condition[key][1]

        function_name = write_function_name(parameters)
        new_method.writelines(function_name)
        
        
        start = long_condition[key][0][0]
        end = long_condition[key][0][1]

        while start != end + 1:
            code = data[start]

            if start == end:
                code.append('\n')

            new_method.writelines(code)
            start += 1

    new_method.close()

    return functions