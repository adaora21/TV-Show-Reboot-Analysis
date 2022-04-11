import pandas as pd
import numpy as np
from datetime import datetime as dt

def get_release_period(id_df, ep_df):
    '''
    Returns pandas dataframe with the length of the original release period of each podcast in id_df
    :param id_df: (Pandas dataframe) Contains the top 50 podcasts in the US in 2021
    :param ep_df: (Pandas dataframe) Contains Spotify data for every episode of each podcast in id_df
    :return: podcast_release_df: Pandas dataframe
    '''
    # Copy id_df and ep_df to avoid errors
    podcast_release_df = id_df.copy()
    ep_df = ep_df.copy()

    # Remove unnecessary columns
    podcast_release_df = podcast_release_df.drop(columns=['publisher (Edison)','publisher'])
    ep_df = ep_df.drop(columns=['duration_ms'])

    # Convert dates to datetime
    ep_df['release_date'] = pd.to_datetime(ep_df['release_date'])

    # Get the release dates of the first and last episodes of each podcast, according to Spotify
    ep_release_df = ep_df.groupby('podcast_id')['release_date'].agg(first_ep_release_date='min', last_ep_release_date='max')
    ep_release_df = ep_release_df.reset_index()

    # Merge ep_release_df with podcast_release_df to get podcast titles and other data
    podcast_release_df = podcast_release_df.merge(ep_release_df, left_on='podcast_id', right_on='podcast_id', how='left')

    # Manually add release periods for podcasts where all episodes are not available on Spotify
    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'Dr. Death', 'first_ep_release_date'] \
        = pd.to_datetime('2018-09-04')
    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'Dr. Death', 'last_ep_release_date'] \
        = pd.to_datetime('2021-09-21')

    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'This American Life', 'first_ep_release_date'] \
        = pd.to_datetime('1995-11-17')
    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'This American Life', 'last_ep_release_date'] \
        = pd.to_datetime('2021-08-03')

    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'Pod Save America', 'first_ep_release_date'] \
        = pd.to_datetime('2017-01-01')
    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'Pod Save America', 'last_ep_release_date'] \
        = pd.to_datetime('2022-03-31')

    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'The Ben Shapiro Show', 'first_ep_release_date'] \
        = pd.to_datetime('2015-09-01')
    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'The Ben Shapiro Show', 'last_ep_release_date'] \
        = pd.to_datetime('2022-04-01')

    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'Wait Wait… Don’t Tell Me!', 'first_ep_release_date'] \
        = pd.to_datetime('1998-01-03')
    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'Wait Wait… Don’t Tell Me!', 'last_ep_release_date'] \
        = pd.to_datetime('2022-04-01')

    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'Planet Money', 'first_ep_release_date'] \
        = pd.to_datetime('2008-09-06')
    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'Planet Money', 'last_ep_release_date'] \
        = pd.to_datetime('2022-03-30')

    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'Fresh Air', 'first_ep_release_date'] \
        = pd.to_datetime('1985-01-01')
    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'Fresh Air', 'last_ep_release_date'] \
        = pd.to_datetime('2022-04-01')

    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'Up First', 'first_ep_release_date'] \
        = pd.to_datetime('2017-04-05')
    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'Up First', 'last_ep_release_date'] \
        = pd.to_datetime('2022-04-01')

    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'The Dan Bongino Show', 'first_ep_release_date'] \
        = pd.to_datetime('2017-01-01')
    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'The Dan Bongino Show', 'last_ep_release_date'] \
        = pd.to_datetime('2022-04-01')

    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'Radiolab', 'first_ep_release_date'] \
        = pd.to_datetime('2002-01-01')
    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'Radiolab', 'last_ep_release_date'] \
        = pd.to_datetime('2022-04-01')

    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'TED Talks Daily', 'first_ep_release_date'] \
        = pd.to_datetime('2014-05-23')
    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'TED Talks Daily', 'last_ep_release_date'] \
        = pd.to_datetime('2022-04-01')

    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'The Dave Ramsey Show', 'first_ep_release_date'] \
        = pd.to_datetime('1992-06-15')
    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'The Dave Ramsey Show', 'last_ep_release_date'] \
        = pd.to_datetime('2022-03-31')

    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'WTF with Marc Maron Podcast', 'first_ep_release_date'] \
        = pd.to_datetime('2009-09-01')
    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'WTF with Marc Maron Podcast', 'last_ep_release_date'] \
        = pd.to_datetime('2022-03-31')

    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'The Rachel Maddow Show', 'first_ep_release_date'] \
        = pd.to_datetime('2008-09-08')
    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'The Rachel Maddow Show', 'last_ep_release_date'] \
        = pd.to_datetime('2022-04-01')

    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'The Breakfast Club', 'first_ep_release_date'] \
        = pd.to_datetime('2010-12-01')
    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'The Breakfast Club', 'last_ep_release_date'] \
        = pd.to_datetime('2021-06-07')

    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'Frenemies Podcast', 'first_ep_release_date'] \
        = pd.to_datetime('2020-09-15')
    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'Frenemies Podcast', 'last_ep_release_date'] \
        = pd.to_datetime('2021-06-07')

    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'The Joe Budden Podcast', 'first_ep_release_date'] \
        = pd.to_datetime('2015-02-18')
    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'The Joe Budden Podcast', 'last_ep_release_date'] \
        = pd.to_datetime('2022-03-30')

    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'The Best of Car Talk', 'first_ep_release_date'] \
        = pd.to_datetime('1977-01-01')
    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'The Best of Car Talk', 'last_ep_release_date'] \
        = pd.to_datetime('2012-10-01')

    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'The Moth', 'first_ep_release_date'] \
        = pd.to_datetime('2009-08-01')
    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'The Moth', 'last_ep_release_date'] \
        = pd.to_datetime('2022-03-28')

    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'Bill Burr’s Monday Morning Podcast', 'first_ep_release_date'] \
        = pd.to_datetime('2007-05-01')
    podcast_release_df.loc[podcast_release_df['podcast_title'] == 'Bill Burr’s Monday Morning Podcast', 'last_ep_release_date'] \
        = pd.to_datetime('2022-03-31')

    podcast_release_df.loc[
        podcast_release_df['podcast_title'] == 'Last Podcast On The Left', 'first_ep_release_date'] \
        = pd.to_datetime('2011-03-29')
    podcast_release_df.loc[
        podcast_release_df['podcast_title'] == 'Last Podcast On The Left', 'last_ep_release_date'] \
        = pd.to_datetime('2022-04-01')

    podcast_release_df.loc[
        podcast_release_df['podcast_title'] == 'Pardon My Take', 'first_ep_release_date'] \
        = pd.to_datetime('2016-02-29')
    podcast_release_df.loc[
        podcast_release_df['podcast_title'] == 'Pardon My Take', 'last_ep_release_date'] \
        = pd.to_datetime('2022-04-01')

    # Remove "NPR News Now" because data on the original release period is unavailable
    podcast_release_df = podcast_release_df[podcast_release_df['podcast_title'] != 'NPR News Now']
    podcast_release_df = podcast_release_df.reset_index(drop=True)

    # Calculate the length of each podcast's original release period in years
    podcast_release_df['release_period_length_(yrs)'] = \
        (podcast_release_df['last_ep_release_date'] - podcast_release_df['first_ep_release_date']).dt.days/365.25

    return podcast_release_df

def process_publisher_data(id_df):
    '''
    Returns pandas dataframe with the share of the top 50 podcasts attributed to each publisher
    :param id_df: (Pandas dataframe) Contains the top 50 podcasts in the US in 2021
    :return: processed_pub_df: Pandas dataframe
    '''

    # Calculate the share of the top 50 podcasts attributed to each podcast publisher
    processed_pub_df = id_df.groupby('publisher')['podcast_title'].agg(podcast_count='count')
    processed_pub_df['percentage'] = processed_pub_df['podcast_count']/processed_pub_df['podcast_count'].sum() * 100

    # Reset index to clean up dataframe
    processed_pub_df = processed_pub_df.reset_index()

    # Identify key publishers that will be individually identified in analysis
    key_publishers = ['Amazon Music', 'NPR', 'Sirius XM', 'Spotify', 'iHeartRadio']

    # Create a dataframe that only contains key publishers' share of the top 50 podcasts
    key_pub_df = processed_pub_df[processed_pub_df['publisher'].isin(key_publishers)].copy()

    # Reorder dataframe in descending order
    key_pub_df = key_pub_df.sort_values(['percentage'], ascending=[False])

    # Aggregate "non-key publishers" data into one entry called "Other"
    key_pub_df.loc[key_pub_df.shape[0]] = {'publisher':'Other',
                                                         'podcast_count':
                                                             processed_pub_df[~processed_pub_df['publisher']
                                                                 .isin(key_publishers)]['podcast_count'].sum(),
                                                         'percentage': processed_pub_df[~processed_pub_df['publisher']
                                                             .isin(key_publishers)]['percentage'].sum()}


    return key_pub_df

if __name__ == "__main__":
    # Load data
    ep_df = pd.read_csv('data/spotify_podcast_ep_data.csv', index_col=0)
    id_df = pd.read_csv('data/US_top50_podcasts_q1_to_q4_2021_processed.csv')

    '''
    Prepare publisher data for pie chart
    '''
    # Process data
    processed_publisher_df = process_publisher_data(id_df)
    # Save data
    processed_publisher_df.to_csv('data/processed_publisher_data.csv')

    '''
    Prepare release period data for distribution graph
    '''
    # Process data
    podcast_release_df = get_release_period(id_df, ep_df)
    # Save data
    podcast_release_df.to_csv('data/podcast_release_periods.csv')