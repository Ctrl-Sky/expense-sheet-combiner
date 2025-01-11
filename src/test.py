import os
import pandas as pd
import numpy as np

def remove_credit_card_thank_you(df):
    filter = df["Description"].str.contains("THANK YOU")
    return df[~filter]

def get_latest_date(card):
    if os.path.isfile('sheets/master.xlsx'):
        excel_file = pd.ExcelFile('sheets/master.xlsx')
        for sheet_name in reversed(excel_file.sheet_names):
            df = excel_file.parse(sheet_name)
            for index, row in reversed(list(df.iterrows())):
                if row['Card'] == card:
                    return row['Date']
        return None
    return None

def initialize_TD(td_sheet, is_debit=False):
    """
    Original TD Bank csv file looks like:

    Date    Description     Lost    Gained      Total

    Standardize TD bank credit or debit file to look like data frame with this format:

    Date     Description     Space1     Space2      Space3      Amount      Card

    Date is a datetime value
    Description includes info on where the purchase was made
    Space is empty value to make description easier to read
    Amount is $ spent or earned (can be pos or neg)
    """
    card_name = "Debit" if is_debit else "Credit"
    format = "%Y-%m-%d" if is_debit else "%m/%d/%Y"

    df = pd.read_csv(td_sheet, usecols=[0,1,2,3], names=["Date", "Description", "Amount", "Gained"])

    # Add or remove row and columns for standardization
    for i in range(2,5):
        df.insert(i, "Space" + str(i-1), [np.nan]*len(df))
    df = remove_credit_card_thank_you(df) # Remove credit card payback row
    df.insert(6, "Card", [card_name]*len(df)) # Column for identifying which card the purchases was made with

    # Move values in Gained column into Amount column as negative values
    df['Amount'] = df['Amount'].fillna(-df['Gained'])
    df = df.drop(df.columns[-1], axis=1)

    df['Date'] = pd.to_datetime(df['Date'], format=format)
    
    # Only included e-transfer information for debit card
    if is_debit:
        filter = df["Description"].str.contains("SEND E-TFR|E-TRANSFER")
        df = df[filter]
        latest_date = get_latest_date('Debit')
        # print(latest_date)
        # print(df['Date'] > latest_date)
        df = df[df['Date'] > latest_date]
    
    print(df)
    return df

td_debit_df = initialize_TD("sheets/accountactivity.csv", is_debit=True)