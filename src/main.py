import argparse
from openpyxl import load_workbook
import pandas as pd
import setup_sheets as ss
import combine_sheets

if __name__ == "__main__":
    ae_df = ss.setup_credit_AE("sheets/Summary.xls")
    td_credit_df = ss.setup_TD("sheets/accountactivity1.csv")
    td_debit_df = ss.setup_TD("sheets/accountactivity.csv", is_debit=True)
    split_df = combine_sheets.combine_df(ae_df, td_credit_df, td_debit_df)

    MASTER_PATH = 'sheets/master.xlsx'
    for month, sub_df in split_df.items():
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


    # book = load_workbook('sheets/master.xlsx')
    # writer = pd.ExcelWriter('sheets/master.xlsx', engine='openpyxl')
    # # writer.book = book

    # for month, sub_df in split_df.items():
    #     print(f"Data for {month}:\n{sub_df}\n")
    #     sub_df.to_excel(writer, sheet_name=month, startrow=writer.sheets[month].max_row, index=False, header=False)

    #     worksheet = writer[month]
    #     worksheet.column_dimensions['B'].width = 11

    # writer.save()

    # Things to do:
    # Need to resize columns again
    # Need to restructure code again

