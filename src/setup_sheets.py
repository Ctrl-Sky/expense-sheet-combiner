import pandas as pd
import numpy as np
import helpers as hp

def setup_credit_AE(credit_ae_sheet):
    """
    American bank xlsx file originally looks like:

    Date    Description     Space     Amount

    Convert American express bank xlsx file into data frame with this format:

    Date     Description     Space1     Space2      Space3      Amount      Card

    Date is a datetime value
    Description includes info on where the purchase was made
    Space is empty value for easier readibility for description
    Amount is $ spent or earned (can be pos or neg)
    """
    df = pd.read_excel(credit_ae_sheet, header=12)
    df = hp.remove_credit_card_thank_you(df)

    df['Description'] = df['Description'].str.lstrip('=')
    df['Amount'] = df['Amount'].str.replace('$', '')
    df['Amount'] = df['Amount'].str.replace(',', '')

    hp.column_to_date_time(df, "Date", "%d %b %Y")

    df.rename(columns={"Unnamed: 2": "Space1"}, inplace=True) # Rename empty column
    hp.insert_new_column(df, 3, "Space2", [np.nan]*len(df))
    hp.insert_new_column(df, 4, "Space3", [np.nan]*len(df))
    hp.insert_new_column(df, 6, "Card", ["Amex"]*len(df))
    df["Amount"] = pd.to_numeric(df['Amount'])

    print(df)
    return df

def setup_TD(td_sheet, is_debit=False):
    """
    Original TD Bank csv file looks like:

    Date    Description     Lost    Gained      Total

    Convert TD bank csv file into data frame with this format:

    Date     Description     Space1     Space2      Space3      Amount      Card

    Date is a datetime value
    Description includes info on where the purchase was made
    Space is empty value for easier readibility for description
    Amount is $ spent or earned (can be pos or neg)
    """
    card_name = "Debit TD" if is_debit else "Credit TD"

    df = pd.read_csv(td_sheet, usecols=[0,1,2,3], names=["Date", "Description", "Amount", "Gained"])

    # Remove pay back credit card statement
    df = hp.remove_credit_card_thank_you(df)

    # Add 3 empty comlumns, Space1, Space2, Space3 between Description and Amount
    for i in range(2,5):
        hp.insert_new_column(df, i, "Space" + str(i-1), [np.nan]*len(df))

    # Move gained value into amount as a negative and delete column
    df['Amount'] = df['Amount'].fillna(-df['Gained'])
    df = df.drop(df.columns[-1], axis=1)
    
    # Only included e-transfer information for debit card
    if is_debit:
        filter = df["Description"].str.contains("SEND E-TFR|E-TRANSFER")
        df = df[filter]
        hp.column_to_date_time(df, "Date", "%Y-%m-%d")
    else:
        hp.column_to_date_time(df, "Date", "%m/%d/%Y")

    hp.insert_new_column(df, 6, "Card", [card_name]*len(df))

    print(df)
    return df
