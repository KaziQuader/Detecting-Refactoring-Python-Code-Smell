from check_method import check_method
from extract_method import extract_method
from refactor import refactor

def main(filename):
    # Your main function to orchestrate everything
    data, long_condition = check_method(filename)
    
    if len(long_condition) != 0:
        functions = extract_method(data, long_condition)
        refactor(functions, long_condition, filename)
    else:
        print("There is no if statement that is between 6 and 50")
    

if __name__ == "__main__":
    main('example_code2.py')