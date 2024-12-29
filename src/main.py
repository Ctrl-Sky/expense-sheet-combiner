from standardize import initialize_AE, initialize_TD
from combine_and_split import combine_and_split_by_month
from write import write_to_master

if __name__ == "__main__":
    ae_df = initialize_AE("sheets/Summary.xls")
    td_credit_df = initialize_TD("sheets/accountactivity1.csv")
    td_debit_df = initialize_TD("sheets/accountactivity.csv", is_debit=True)
    split_df = combine_and_split_by_month(ae_df, td_credit_df, td_debit_df)
    write_to_master(split_df)