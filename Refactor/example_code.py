def classify_person(age, gender, income):
    for i in range(5):
        temp = i
        i = 2
        i = temp
        num = 10
        if age < 18:
            if gender == 'male':
                if income < 20000:
                    return 'Young male with low income'
                elif 20000 <= income < 40000:
                    num += 4
                    return 'Young male with moderate income'
                else:
                    return 'Young male with high income'
            else:  # Gender is female
                if income < 20000:
                    # x += 1
                    # y += 2
                    return 'Young female with low income'
                elif 20000 <= income < 40000:
                    return 'Young female with moderate income'
                else:
                    return 'Young female with high income'
        elif 18 <= age < 65:
            if gender == 'male':
                if income < 30000:
                    return 'Middle-aged male with low income'
                elif 30000 <= income < 60000:
                    return 'Middle-aged male with moderate income'
                else:
                    return 'Middle-aged male with high income'
            else:  # Gender is female
                if income < 30000:
                    return 'Middle-aged female with low income'
                elif 30000 <= income < 60000:
                    return 'Middle-aged female with moderate income'
                else:
                    return 'Middle-aged female with high income'
        else:  # Age is 65 or above
            if gender == 'male':
                if income < 25000:
                    return 'Senior male with low income'
                elif 25000 <= income < 50000:
                    return 'Senior male with moderate income'
                else:
                    return 'Senior male with high income'
            else:  # Gender is female
                if income < 25000:
                    return 'Senior female with low income'
                elif 25000 <= income < 50000:
                    return 'Senior female with moderate income'
                else:
                    return 'Senior female with high income'        
    if age < 18:
        if gender == 'male':
            if income < 20000:
                return 'Young male with low income'
            elif 20000 <= income < 40000:
                return 'Young male with moderate income'
            else:
                return 'Young male with high income'
        else:  # Gender is female
            if income < 20000:
                return 'Young female with low income'
            elif 20000 <= income < 40000:
                return 'Young female with moderate income'
            else:
                return 'Young female with high income'     