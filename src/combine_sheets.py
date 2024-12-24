import pandas as pd

def combine_df(ae, tdc, tdd):
    df_combined = pd.concat([ae, tdc, tdd])
    df_sorted = df_combined.sort_values(by='Date')
    df_sorted.reset_index(drop=True, inplace=True)
    df_sorted.to_excel('sheets/master.xlsx')

    

# Consider creating a masters excel file that concats everything to it
# In that masters excel, when you concat everything make sure you dont concat duplicates
# Be able to divide that up the masters into months
# Get the actual date to show and not just datetime