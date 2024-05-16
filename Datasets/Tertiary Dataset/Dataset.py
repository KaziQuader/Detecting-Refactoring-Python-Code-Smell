import pandas as pd

df_LC = pd.read_csv('result100LargeClass.csv')
df_LM = pd.read_csv('result100LongMethod.csv')
LMC_LPL_LLF = pd.read_csv('LMC_LPL_LLF.csv')

df_LC = df_LC.drop(['experience-based', 'statistics-based'], axis = 1)
df_LM = df_LM.drop(['experience-based', 'statistics-based'], axis = 1)

df_smelly_LC = df_LC[(df_LC['tuning machine'] == 1)]
df_smelly_LM = df_LM[(df_LM['tuning machine'] == 1)]

random_df_not_smelly_LC = df_LC[(df_LC['tuning machine'] == 0)].sample(n=len(df_smelly_LC))
random_df_not_smelly_LM = df_LM[(df_LM['tuning machine'] == 0)].sample(n=len(df_smelly_LM))

resultant_df_LC = pd.concat([df_smelly_LC, random_df_not_smelly_LC], ignore_index=True)
resultant_df_LC = resultant_df_LC.sample(frac=1).reset_index(drop=True)

resultant_df_LM = pd.concat([df_smelly_LM, random_df_not_smelly_LM], ignore_index=True)
resultant_df_LM = resultant_df_LM.sample(frac=1).reset_index(drop=True)

resultant_df_LC.rename(columns={'subject':'Project', 'open':'File Name','lineno':'Line_LC', 'CLOC':'CLOC', 'tuning machine':'LC'}, inplace=True)
resultant_df_LM.rename(columns={'subject':'Project', 'open':'File Name','lineno':'Line_LM', 'MLOC':'MLOC', 'tuning machine':'LM'}, inplace=True)

LC_LM = pd.merge(resultant_df_LC, resultant_df_LM, on=['Project', 'File Name'], how='outer')
final_df = pd.merge(LC_LM, LMC_LPL_LLF, on=['Project', 'File Name'], how='outer')
final_df.fillna(0, inplace=True)

# print(resultant_df_LC)
# print(resultant_df_LM)
# print(final_df)

final_df.to_csv('code_smell_dataset.csv', index=False)