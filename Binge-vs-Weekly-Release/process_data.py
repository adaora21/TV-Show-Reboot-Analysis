import pandas as pd
from datetime import timedelta
import numpy as np

def process_data(df):
    '''
    Process Google Trends data
    :param df: Pandas dataframe
    :return: df: Pandas dataframe
    '''

    # Copy df to avoid errors
    df = df.copy()

    # Set row containing tv show titles as the header
    df.columns = df.loc['Week']

    # Drop row with tv show titles and NaN rows
    df = df.drop(['Week'])
    if np.nan in df.index.tolist():
        df = df.drop([np.nan])

    # Replace all "<1" entries with 0
    df = df.replace({'<1':0})

    # Change dataframe type to float
    df = df.astype(float)

    return df

def convert_to_weeks(df):
    '''
    Convert release dates in df to the Sunday in the same calendar week as the release date,
    since Google Trends data is given on a weekly basis
    :param df: Pandas dataframe
    :return: df: Pandas dataframe
    '''

    # Copy df to avoid errors
    df = df.copy()

    # Convert all columns to datetime
    for i in range(df.shape[1]):
        df.iloc[:, i] = pd.to_datetime(df.iloc[:, i])

    # Convert all release dates to the Sunday in the same calendar week as the release date
    df = df.applymap(lambda x: x - timedelta(days=(x.weekday()+1)), na_action='ignore')

    return df



if __name__ == "__main__":
    '''
    Process Google Trends data
    '''
    google_file_names = ['agentsofshield', 'disneyplus_shows', 'netflix_shows']
    for file_name in google_file_names:
        # Load data
        df = pd.read_csv('data/raw_'+file_name+'.csv', index_col=0)
        # Process data
        processed_df = process_data(df)
        # Save data
        processed_df.to_csv('data/processed_'+file_name+'.csv')

    '''
    Process release date data
    '''
    # Load data
    dates_df = pd.read_csv('data/raw_release_dates.csv', index_col=0)
    # Convert release dates to weeks
    weekly_dates = convert_to_weeks(dates_df)
    # Save data
    weekly_dates.to_csv('data/processed_weekly_release_dates.csv')
