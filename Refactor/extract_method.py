import re

def extract_method(filename):
    line_num = 1
    codes = {}
    variables = []

    with open(filename, 'rb') as f:
        for line in f:
            # Decode the binary line to a string, preserving white spaces
            line_with_whitespace = line.decode("utf-8")
            
            # Process the line as needed
            line_code_arr = re.split(r'(\s+)', line_with_whitespace)

            if line_num == 1:
                codes[line_num] = line_code_arr
                line_num += 1
                continue
        
            # Process the parts as needed
            print(line_code_arr)    

            


            
            


extract_method('/Users/kaziknobo/Desktop/CSE 400 Thesis/Refactor/example_code.py')