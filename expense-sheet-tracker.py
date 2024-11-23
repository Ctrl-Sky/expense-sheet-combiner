import argparse
import pandas as pd
import numpy as np
import csv

# Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

def setNewHeader(new_header, df_body):
    df_body.columns = new_header
    return df_body

# def setUpCreditAE(credit_ae_sheet):
#     df = pd.read_excel(credit_ae_sheet)
    
#     # Header is still unset
#     df.drop(df.index[0:10], inplace=True) # Drop the useless info and keep the soon to be header 
#     df = df.reset_index(drop=True)
#     new_header = df.iloc[0] # Grab the header
#     df = df.iloc[1:] # Grab the section with ONLY the transactions

#     # Set the new header
#     df = setNewHeader(new_header, df)

#     # df.to_excel('hi.xlsx')

def removeCreditCardThankYou(df):
    filter = df["Description"].str.contains("THANK YOU")
    return df[~filter]

def setUpCreditAE(credit_ae_sheet):
    df = pd.read_excel(credit_ae_sheet, header=11)
    df = removeCreditCardThankYou(df)
    return df

def setUpTD(td_sheet):
    df = pd.read_csv(td_sheet, usecols=[0,1,2,3], names=["Date", "Description", "Amount", "Gained"])
    df = removeCreditCardThankYou(df)
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('credit_td_sheet')
    parser.add_argument('credit_ae_sheet')
    parser.add_argument('debit_td_sheet')
    args = parser.parse_args()

    # setUpCreditAE(args.credit_ae_sheet)
    setUpTD(args.credit_td_sheet)