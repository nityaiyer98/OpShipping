import pandas as pd
import openpyxl

nrows = 20
#
file_name = 'Dimensioning value pasted.xlsx'
book = openpyxl.load_workbook(filename = file_name, read_only = True, data_only=True)
first_sheet = book.worksheets[2]
rows_generator = first_sheet.values
header_row = next(rows_generator)
data_rows = [row for (_, row) in zip(range(nrows - 1), rows_generator)]
df = pd.DataFrame(data_rows, columns = header_row)
df.set_index('CODPRO', inplace = True)
print(df)
item = df.loc['N40050']
print()
print(item)
print()
print(item.HAUUVC)
# filter = df['CODPRO']=='N40050'
# print(df.loc(filter))

# df = pd.read_excel(file_name, sheet_name='Order Dimensions', nrows = 20, )
# print(df)
