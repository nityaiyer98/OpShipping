import pandas as pd

file_name = 'LV Box Dimensions.xlsx'
df = pd.read_excel(file_name)
print(df)

box_list = []
for index,row in df.iterrows():
    name = row['Box Name']
    dim1 = row['Length']
    dim2 = row['Width']
    dim3 = row['Height']
    box_list.append((name,[dim1,dim2,dim3]))
