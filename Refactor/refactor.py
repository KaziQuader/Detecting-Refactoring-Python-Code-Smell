def refactor(functions, long_condition, filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    for key in reversed(long_condition.keys()):
        start = long_condition[key][0][0]
        end = long_condition[key][0][1]

        lines[start - 1] = functions[key]
        lines = lines[:start] + lines[end:]


    print(lines)
    lines.insert(0, 'from new_method import *\n')
    with open(filename, 'w') as f:
        f.writelines(lines)
