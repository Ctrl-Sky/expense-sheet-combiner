import pandas as pd

def column_to_date_time(df, columnName, format):
    df[columnName] = pd.to_datetime(df[columnName], format=format)

def insert_new_column(df, position, name, values):
    df.insert(position, name, values)

def remove_credit_card_thank_you(df):
    filter = df["Description"].str.contains("THANK YOU")
    return df[~filter]