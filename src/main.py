import argparse
from openpyxl import load_workbook
import setup_sheets as ss
import combine_sheets

if __name__ == "__main__":
    ae_df = ss.setup_credit_AE("sheets/Summary.xls")
    td_credit_df = ss.setup_TD("sheets/accountactivity1.csv")
    td_debit_df = ss.setup_TD("sheets/accountactivity.csv", is_debit=True)
    combine_sheets.combine_df(ae_df, td_credit_df, td_debit_df)

    # Increase width of date column to make it visible in excel
    workbook = load_workbook('sheets/master.xlsx')
    worksheet = workbook['Sheet1']
    worksheet.column_dimensions['B'].width = 11
    workbook.save('sheets/master.xlsx')

