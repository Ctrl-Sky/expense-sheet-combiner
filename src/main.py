import argparse
from standardize import initialize_AE, initialize_TD
from combine_and_split import combine_and_split_by_month
from write import write_to_master

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('update', help="True if its updating master.xlsx with new date or False for adding much older puchases to master.xlsx")
    args = parser.parse_args()

    ae_df = initialize_AE("sheets/Summary.xls", update=args.update)
    td_credit_df = initialize_TD("sheets/accountactivity1.csv", update=args.update)
    td_debit_df = initialize_TD("sheets/accountactivity.csv", is_debit=True, update=args.update)
    split_df = combine_and_split_by_month(ae_df, td_credit_df, td_debit_df)
    write_to_master(split_df)