from openpyxl import load_workbook
import pandas as pd

MASTER_PATH = 'sheets/master.xlsx'

def alter_column_width(sheetname, column, width):
    workbook = load_workbook(MASTER_PATH)
    worksheet = workbook[sheetname]
    worksheet.column_dimensions[column].width = width
    workbook.save(MASTER_PATH)

def concat_with_existing_df(df, sheetname):
    existing_df = pd.read_excel(MASTER_PATH, sheet_name=sheetname)
    new_df = pd.concat([existing_df, df])
    new_df.drop_duplicates(['Description', 'Amount'], inplace=True, keep='last')
    return alter_datetime_and_sort(new_df)

def alter_datetime_and_sort(df):
    df['Date'] = df['Date'].dt.date
    df.sort_values(by='Date', inplace=True)
    return df

def write_to_master(split_df):
    for month, sub_df in split_df.items():
        try:
            with pd.ExcelWriter(MASTER_PATH, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                if month in writer.sheets:
                    new_df = concat_with_existing_df(sub_df, sheetname=month)
                    new_df.to_excel(writer, sheet_name=month, index=False)
                else:
                    sub_df.to_excel(writer, sheet_name=month, index=False)
        except FileNotFoundError:
            with pd.ExcelWriter(MASTER_PATH, engine='openpyxl') as writer:
                sub_df.to_excel(writer, sheet_name=month, index=False)

        alter_column_width(month, 'A', 11) # Increase width of date column tp see full value

# Catching Error
# add nov-dec statement to master
# try adding dec statement to master
# all the purchases added to dec in nov-dec will then be moved to top and mess up the datetime