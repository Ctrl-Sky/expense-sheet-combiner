from openpyxl import load_workbook
import pandas as pd

MASTER_PATH = 'sheets/master.xlsx'

def alter_column_width(sheetname, column, width):
    workbook = load_workbook(MASTER_PATH)
    worksheet = workbook[sheetname]
    worksheet.column_dimensions[column].width = width
    workbook.save(MASTER_PATH)

def write_to_master(split_df):
    for month, sub_df in split_df.items():
        sub_df['Date'] = sub_df['Date'].dt.date
        try:
            with pd.ExcelWriter(MASTER_PATH, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                if month in writer.sheets:
                    startrow = writer.sheets[month].max_row
                    sub_df.to_excel(writer, sheet_name=month, startrow=startrow, index=False, header=False)
                else:
                    sub_df.to_excel(writer, sheet_name=month, index=False)
        except FileNotFoundError:
            with pd.ExcelWriter(MASTER_PATH, engine='openpyxl') as writer:
                sub_df.to_excel(writer, sheet_name=month, index=False)

        alter_column_width(month, 'A', 11)