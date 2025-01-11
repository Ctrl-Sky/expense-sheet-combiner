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
        return "2004-03-23"
    return "2004-03-23" # Arbritary date that no purchases should be older than

def initialize_AE(credit_ae_sheet, update):
    """
    American bank xlsx file originally looks like and starts at line 12:

    Date    Description     Space     Amount

    Standardize American express bank xlsx file to look like data frame with this format:

    id      Date     Description     Space1     Space2      Space3      Amount      Card

    id is the index. Together with Description and Amount, it is used to identify unique purchases
    Date is a datetime value
    Description includes info on where the purchase was made
    Space is empty value to make description easier to read
    Amount is $ spent or earned (can be pos or neg)
    """
    df = pd.read_excel(credit_ae_sheet, header=12)
    
    # Remove unwanted charcters for standardization
    df['Description'] = df['Description'].str.lstrip('=')
    df['Amount'] = df['Amount'].str.replace('$', '')
    df['Amount'] = df['Amount'].str.replace(',', '')

    # Add or remove row and columns for standardization
    df.rename(columns={"Unnamed: 2": "Space1"}, inplace=True)
    df.insert(3, "Space2", [np.nan]*len(df))
    df.insert(4, "Space3", [np.nan]*len(df))
    df = remove_credit_card_thank_you(df) # Remove credit card payback row
    df.insert(6, "Card", ["Amex"]*len(df)) # Column for identifying which card the purchases was made with

    # Misc. Standardization
    df["Amount"] = pd.to_numeric(df['Amount'])
    df['Date'] = pd.to_datetime(df['Date'], format="%d %b %Y")
    df.insert(0, "id", df.index)

    if update:
        latest_date = get_latest_date('Amex')
        df = df[df['Date'] > latest_date]

    return df

def initialize_TD(td_sheet, update, is_debit=False):
    """
    Original TD Bank csv file looks like:

    Date    Description     Lost    Gained      Total

    Standardize TD bank credit or debit file to look like data frame with this format:

    id      Date     Description     Space1     Space2      Space3      Amount      Card

    id is the index. Together with Description and Amount, it is used to identify unique purchases
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
    df.insert(0, "id", df.index)

    # Only included e-transfer information for debit card
    if is_debit:
        filter = df["Description"].str.contains("SEND E-TFR|E-TRANSFER")
        df = df[filter]

        # Cut off Debit card no matter what because csv file always includes every purchase
        latest_date = get_latest_date(card_name)
        df = df[df['Date'] > latest_date]

    if not is_debit and update:
        latest_date = get_latest_date(card_name)
        df = df[df['Date'] > latest_date]

    return df
