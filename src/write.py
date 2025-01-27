from openpyxl import load_workbook
import pandas as pd

MASTER_PATH = 'sheets/master.xlsx'

def alter_column_width(sheetname, column, width):
    workbook = load_workbook(MASTER_PATH)
    worksheet = workbook[sheetname]
    worksheet.column_dimensions[column].width = width
    workbook.save(MASTER_PATH)

def alter_and_sort_date(df, sheet_exist):
    df['Date'] = pd.to_datetime(df['Date'])
    if sheet_exist:
        df['Day'] = df['Date'].dt.day
    else:
        df.insert(2, 'Day', df['Date'].dt.day)
    df['Date'] = df['Date'].dt.date
    df.sort_values(by='Date', inplace=True)

def concat_with_existing_df(df, sheetname):
    existing_df = pd.read_excel(MASTER_PATH, sheet_name=sheetname)
    new_df = pd.concat([existing_df, df])
    new_df.drop_duplicates(['Description', 'Amount', 'id'], inplace=True, keep='last')
    return new_df

def write_to_master(split_df):
    """
    Iterates through a dictionary created in combine_and_split.py. See that file for how the dictionary may look
    
    It writes each sub dataframe to an excel file at MASTER_PATH and creates or appends to a sheet based on the dictionary's key.

    For each sheet:
    - If the sheet exists, the data is merged with the existing data in the sheet, and then sorted based on date
    - If the sheet does not exist, the data is sorted and written to a new sheet.
    """
    for month, sub_df in split_df.items():
        try:
            with pd.ExcelWriter(MASTER_PATH, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                if month in writer.sheets:
                    new_df = concat_with_existing_df(sub_df, sheetname=month)
                    alter_and_sort_date(new_df, sheet_exist=True)
                    new_df.to_excel(writer, sheet_name=month, index=False)
                else:
                    alter_and_sort_date(sub_df, sheet_exist=False)
                    sub_df.to_excel(writer, sheet_name=month, index=False)
        except FileNotFoundError:
            with pd.ExcelWriter(MASTER_PATH, engine='openpyxl') as writer:
                alter_and_sort_date(sub_df, sheet_exist=False)
                sub_df.to_excel(writer, sheet_name=month, index=False)

        alter_column_width(month, 'B', 11) # Increase width of date column tp see full value