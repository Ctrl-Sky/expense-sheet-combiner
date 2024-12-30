import pandas as pd

def split_df_by_month(df):
    df['year_month'] = df['Date'].dt.to_period('M') # Create year_month column for split, will be dropped after
    dataframes_by_month = {str(month): group.drop(columns='year_month') for month, group in df.groupby('year_month')}
    return dataframes_by_month

def combine_df(ae, tdc, tdd):
    df_combined = pd.concat([ae, tdc, tdd])
    return df_combined

def combine_and_split_by_month(df_AE, df_TD_credit, df_TD_debit):
    """
    Combine the 3 dataframes into one large one sorted by date.
    Split the dataframe into subdataframes depending on year-month the purchases were made.
    Returns a dictionary where the key is the unique year-month and the value is the subdataframe
    Example:
    {
    '2024-09':      Date  Description  Space1  Space2  Space3  Amount  Card
                2024-09-12    Hi        NaN     NaN     NaN    15.05  Credit,
    '2024-10':      Date  Description  Space1  Space2  Space3  Amount  Card
                2024-10-16    Hello     NaN     NaN     NaN     3.05  Credit
                2024-10-19    Hey       NaN     NaN     NaN    13.76  Credit
    }
    """
    df = combine_df(df_AE, df_TD_credit, df_TD_debit)
    split_df = split_df_by_month(df)
    return split_df