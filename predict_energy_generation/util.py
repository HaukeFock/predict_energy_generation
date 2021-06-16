import pandas as pd

def load_feature_df(path, date_as_index=True):
    df = pd.read_csv(path)
    if date_as_index:
        #print(('Date' in list(df.columns)))
        if 'Date' in list(df.columns):
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)
    return df
