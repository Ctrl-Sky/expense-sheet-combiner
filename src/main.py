import argparse
import setup_sheets 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('credit_td_sheet')
    parser.add_argument('credit_ae_sheet')
    parser.add_argument('debit_td_sheet')
    args = parser.parse_args()

    # ae_df = setup_credit_AE(args.credit_ae_sheet)
    # print()
    # td_credit_df = setup_credit_TD(args.credit_td_sheet)
    # print()
    # combine_df(ae_df, td_credit_df)

    # Consider doing e transfer only for td
    td_debit_df = setup_sheets.setup_credit_TD(args.debit_td_sheet, is_debit=True)