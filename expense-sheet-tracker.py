import argparse
import pandas as pd
import numpy as np
import csv

# Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

def columnToDateTime(df, columnName, format):
    df[columnName] = pd.to_datetime(df[columnName], format=format)

def insertNewColumn(df, position, name, values):
    df.insert(position, name, values)

def setNewHeader(new_header, df_body):
    df_body.columns = new_header
    return df_body

def removeCreditCardThankYou(df):
    filter = df["Description"].str.contains("THANK YOU")
    return df[~filter]

def setUpCreditAE(credit_ae_sheet):
    df = pd.read_excel(credit_ae_sheet, header=11)
    df = removeCreditCardThankYou(df)
    df['Description'] = df['Description'].str.lstrip('=')
    columnToDateTime(df, "Date", "%d %b %Y")

    df.rename(columns={"Unnamed: 2": "Space1"}, inplace=True) # Rename empty column
    insertNewColumn(df, 3, "Space2", [np.nan]*len(df))
    insertNewColumn(df, 4, "Space3", [np.nan]*len(df))

    # df.to_excel('hi.xlsx')
    print(df)
    return df

def setUpTD(td_sheet):
    df = pd.read_csv(td_sheet, usecols=[0,1,2,3], names=["Date", "Description", "Amount", "Gained"])
    df = removeCreditCardThankYou(df)
    for i in range(2,5):
        insertNewColumn(df, i, "Space" + str(i-1), [np.nan]*len(df))
        
    print(df)
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('credit_td_sheet')
    parser.add_argument('credit_ae_sheet')
    parser.add_argument('debit_td_sheet')
    args = parser.parse_args()

    setUpCreditAE(args.credit_ae_sheet)
    print()
    # setUpTD(args.credit_td_sheet)
    # print()
    # setUpTD(args.debit_td_sheet)