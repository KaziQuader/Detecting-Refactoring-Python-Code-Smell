from check_method import check_method
from extract_method import extract_method
from refactor import refactor
from check_file_format import check_file_format

def main(filename):
    # Your main function to orchestrate everything
    check_file_format(filename)
    data, long_condition = check_method(filename)
    print(long_condition)
    # if len(long_condition) != 0:
    #     functions = extract_method(data, long_condition)
    #     refactor(functions, long_condition, filename)
    # else:
    #     print("There is no if statement that is between 6 and 50")
    

if __name__ == "__main__":
    main('Refactor/example_code.py')