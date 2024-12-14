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

def columnToDateTime(df, columnName, format):
    df[columnName] = pd.to_datetime(df[columnName], format=format)

def insertNewColumn(df, position, name, values):
    df.insert(position, name, values)

def removeCreditCardThankYou(df):
    filter = df["Description"].str.contains("THANK YOU")
    print(type(filter))
    return df[~filter]

def setUpCreditAE(credit_ae_sheet):
    df = pd.read_excel(credit_ae_sheet, header=11)
    df = removeCreditCardThankYou(df)
    df['Description'] = df['Description'].str.lstrip('=')
    df['Amount'] = df['Amount'].str.replace('$', '')
    df['Amount'] = df['Amount'].str.replace(',', '')
    columnToDateTime(df, "Date", "%d %b %Y")

    df.rename(columns={"Unnamed: 2": "Space1"}, inplace=True) # Rename empty column
    insertNewColumn(df, 3, "Space2", [np.nan]*len(df))
    insertNewColumn(df, 4, "Space3", [np.nan]*len(df))
    df["Amount"] = pd.to_numeric(df['Amount'])

    # df.to_excel('hi.xlsx')
    print(df)
    return df

def setUpTD(td_sheet):
    df = pd.read_csv(td_sheet, usecols=[0,1,2,3], names=["Date", "Description", "Amount", "Gained"])
    df = removeCreditCardThankYou(df)
    columnToDateTime(df, "Date", "%m/%d/%Y")
    for i in range(2,5):
        insertNewColumn(df, i, "Space" + str(i-1), [np.nan]*len(df))

    # Move gained value into amount as a negative and delete column
    df['Amount'] = df['Amount'].fillna(-df['Gained'])
    df = df.drop(df.columns[-1], axis=1)
    
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

    ae_df = setUpCreditAE(args.credit_ae_sheet)
    print()
    td_credit_df = setUpTD(args.credit_td_sheet)
    print()
    combine_df(ae_df, td_credit_df)

    # Consider doing e transfer only for td
    # td_debit_df = setUpTD(args.debit_td_sheet)