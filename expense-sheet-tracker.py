import argparse
import pandas as pd
import numpy as np
import csv

# Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# def combineSheets():
#     append them together
#     remove thank you 
#     remove = sign 
#     sort by date time 
#     convert date time back to string 
#     write to excel file

def column_to_date_time(df, columnName, format):
    df[columnName] = pd.to_datetime(df[columnName], format=format)

def insert_new_column(df, position, name, values):
    df.insert(position, name, values)

def remove_credit_card_thank_you(df):
    filter = df["Description"].str.contains("THANK YOU")
    return df[~filter]

def setup_credit_AE(credit_ae_sheet):
    df = pd.read_excel(credit_ae_sheet, header=11)
    df = remove_credit_card_thank_you(df)
    df['Description'] = df['Description'].str.lstrip('=')
    df['Amount'] = df['Amount'].str.replace('$', '')
    df['Amount'] = df['Amount'].str.replace(',', '')
    column_to_date_time(df, "Date", "%d %b %Y")

    df.rename(columns={"Unnamed: 2": "Space1"}, inplace=True) # Rename empty column
    insert_new_column(df, 3, "Space2", [np.nan]*len(df))
    insert_new_column(df, 4, "Space3", [np.nan]*len(df))
    df["Amount"] = pd.to_numeric(df['Amount'])

    # df.to_excel('hi.xlsx')
    print(df)
    return df

def setup_credit_TD(td_sheet, is_debit=False):
    df = pd.read_csv(td_sheet, usecols=[0,1,2,3], names=["Date", "Description", "Amount", "Gained"])
    df = remove_credit_card_thank_you(df)

    column_to_date_time(df, "Date", "%m/%d/%Y")

    # Add empty columns in front of description column
    for i in range(2,5):
        insert_new_column(df, i, "Space" + str(i-1), [np.nan]*len(df))

    # Move gained value into amount as a negative and delete column
    df['Amount'] = df['Amount'].fillna(-df['Gained'])
    df = df.drop(df.columns[-1], axis=1)
    
    # Only included e-transfer information for debit card
    if is_debit:
        filter = df["Description"].str.contains("SEND E-TFR|E-TRANSFER")
        df = df[filter]

    # df.to_excel('hi2.xlsx')
    print(df)
    return df

def combine_df(ae, tdc):
    df_combined = pd.concat([ae, tdc])
    df_sorted = df_combined.sort_values(by='Date')
    df_sorted.reset_index(drop=True, inplace=True)
    df_sorted.to_excel('hi2.xlsx')


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
    td_debit_df = setup_credit_TD(args.debit_td_sheet, is_debit=True)

# Consider creating a masters excel file that concats everything to it
# In that masters excel, when you concat everything make sure you dont concat duplicates
# Be able to divide that up the masters into months
# Implement the debit sheet by only including etransfers
# Get the actual date to show and not just datetime
