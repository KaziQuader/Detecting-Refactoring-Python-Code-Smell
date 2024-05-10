def method(age, gender, income):
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
