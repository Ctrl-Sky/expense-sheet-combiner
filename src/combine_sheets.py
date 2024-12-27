import pandas as pd

def split_df_by_month(df):
    df['year_month'] = df['Date'].dt.to_period('M')
    dataframes_by_month = {str(month): group.drop(columns='year_month') for month, group in df.groupby('year_month')}
    return dataframes_by_month

def combine_df(ae, tdc, tdd):
    df_combined = pd.concat([ae, tdc, tdd])
    df_combined.sort_values(by='Date', inplace=True)
    df_combined.reset_index(drop=True, inplace=True)
    # df_combined.to_excel('sheets/master.xlsx')
    split_df = split_df_by_month(df_combined)
    return split_df