import pandas as pd
import numpy as np

def process_data(info_df, wiki_data):
    '''
    Process Wikipedia pageviews data and calculate data points for
    each individual film and data points aggregated across each subcategory
    :param info_df: (pandas dataframe) contains each film's release date and release platform
    :param wiki_data: (pandas dataframe) contains wikipedia daily pageviews for 30 films
    :return: movie_analysis: (pandas dataframe) contains data points for each film
    :return: summary_df: (pandas dataframe) contains data points aggregated across each subcategory
    '''

    '''
    Process movie data (streaming & theatrical releases)
    '''
    # Convert dates to datetime
    info_df['release_dt'] = pd.to_datetime(info_df['release_dt'])
    wiki_data.index = pd.to_datetime(wiki_data.index)

    # Sort index
    wiki_data = wiki_data.sort_index()

    # Initialize dataframe
    movie_analysis = pd.DataFrame(columns=['max_pageviews',
                                           'max_pageviews_dt', 'days_to_max_pageviews',
                                           '1st_mode_dt', 'days_to_1st_mode_dt'])

    # For each movie, get all relevant data points
    for movie in info_df.index.tolist():
        # Get the the film release date
        release_dt = info_df.loc[movie, 'release_dt']
        # Get daily pageviews data for movie after release_dt
        film_data = wiki_data.loc[wiki_data.index >= release_dt, movie]
        # Calculate 3 data points using film data
        data_pts = get_datapoints(release_dt, film_data)
        # Save data to movie_analysis dataframe
        movie_analysis.loc[movie] = data_pts

    # Convert columns in days to int
    movie_analysis['days_to_max_pageviews'] = (movie_analysis['days_to_max_pageviews']/np.timedelta64(1, 'D')).astype(int)
    movie_analysis['days_to_1st_mode_dt'] = (movie_analysis['days_to_1st_mode_dt']/np.timedelta64(1, 'D')).astype(int)

    # Convert column with total # of pageviews to float
    movie_analysis['max_pageviews'] = movie_analysis['max_pageviews'].astype(float)

    # Merge release date data with movie analysis dataframe
    movie_analysis = pd.concat([movie_analysis, info_df], axis=1)

    '''
    Get summarized data across each subset 
    '''
    # Create summary_df columns
    summary_cols = ['max_pageviews', 'days_to_max_pageviews', 'days_to_1st_mode_dt']

    # Initialize lists to create summary_df indices
    categories = ['streaming', 'theatrical', 'theatrical']
    release_yr = [np.NaN, 2019, 2022]
    data_aggregates = ['average', 'max', 'max_movie', 'min', 'min_movie']

    # Create summary_df multiindex
    summary_idx = []
    for i in range(0,3):
        for j in range(0,5):
            if categories[i] == 'theatrical':
                    summary_idx = summary_idx + [(str(release_yr[i]) + ' ' + categories[i], data_aggregates[j])]
            else:
                    summary_idx = summary_idx + [(categories[i], data_aggregates[j])]
    summary_idx = pd.MultiIndex.from_tuples(summary_idx, names=('category', 'data'))

    # Initialize dataframe
    summary_df = pd.DataFrame(columns= summary_cols, index=summary_idx)

    # Initialize variable for indexing multiindex dataframes
    idx = pd.IndexSlice

    # Iterate through each category and release year and record summary data
    for category, yr in zip(categories, release_yr):
        for datapoint in summary_cols:
            # If release_yr is NaN (aka for streaming releases), just use the category to create a subset of the data
            if pd.isnull(yr):
                # Get a subset of the dataframe
                subset = movie_analysis.loc[movie_analysis['category'] == category, datapoint]
                # Save average for each datapoint
                summary_df.loc[idx[category, 'average'], datapoint] = subset.mean()
                # Save min for each datapoint
                summary_df.loc[idx[category, 'min'], datapoint] = subset.min()
                # Save movie with min for each datapoint
                summary_df.loc[idx[category, 'min_movie'], datapoint] \
                                                                    = subset[subset.isin([subset.min()])].index.tolist()
                # Save max for each datapoint
                summary_df.loc[idx[category, 'max'], datapoint] = subset.max()
                # Save movie with max for each datapoint
                summary_df.loc[idx[category, 'max_movie'], datapoint] \
                                                                    = subset[subset.isin([subset.max()])].index.tolist()

            # If release_yr is not NaN, use the category and release_yr to create a subset of the data
            else:
                # Get a subset of the dataframe
                subset = movie_analysis.loc[(movie_analysis['category'] == category)
                                                & (movie_analysis['release_dt'].dt.year == yr), datapoint]
                # Save average for each datapoint
                summary_df.loc[idx[str(yr)+' '+category, 'average'], datapoint] = subset.mean()
                # Save min for each datapoint
                summary_df.loc[idx[str(yr) + ' ' + category, 'min'], datapoint] = subset.min()
                # Save movie with min for each datapoint
                summary_df.loc[idx[str(yr) + ' ' + category, 'min_movie'], datapoint] \
                                                                    = subset[subset.isin([subset.min()])].index.tolist()
                # Save max for each datapoint
                summary_df.loc[idx[str(yr) + ' ' + category, 'max'], datapoint] = subset.max()
                # Save movie with max for each datapoint
                summary_df.loc[idx[str(yr) + ' ' + category, 'max_movie'], datapoint] \
                                                                    = subset[subset.isin([subset.max()])].index.tolist()

    return movie_analysis, summary_df

def get_datapoints(release_dt, film_data):
    '''
    For the given film, calculate the max # of pageviews after the release date,
    the days between the max # of pageviews after the release date and the release date,
    and the days between the day when daily pageviews reverted to normal levels and the release date
    :param release_dt: (pandas datetime object) the film's release date
    :param film_data: (pandas dataframe) contains the film's daily Wikipedia pageviews on & after its release date
    :return: data_pts: (dictionary) contains the 3 data points listed in the description
    '''

    # Initialize dictionary to save data
    data_pts = {}

    '''
    Get data on max # of daily pageviews after release date
    '''
    # Get max # of pageviews
    data_pts['max_pageviews'] = film_data.max()
    # Get date of max # of pageviews
    data_pts['max_pageviews_dt'] = film_data.idxmax()
    # Get days between max # of pageviews & release date
    data_pts['days_to_max_pageviews'] = data_pts['max_pageviews_dt'] - release_dt

    '''
    Get date when daily pageviews reverted to normal levels
    '''
    # Get reversion date
    data_pts['1st_mode_dt'] = get_mode(film_data, release_dt)
    # Get days between reversion date & release date
    data_pts['days_to_1st_mode_dt'] = data_pts['1st_mode_dt'] - release_dt

    return data_pts

def get_mode(film_data, release_dt):
    '''
    For the given film, get the date when daily pageviews reverted to normal levels (after the max # of daily pageviews)
    :param film_data: (pandas dataframe) contains the film's daily Wikipedia pageviews on & after its release date
    :param release_dt: (pandas datetime object) the film's release date
    :return: earliest_dt: (pandas datetime object) reversion date
    '''

    # Filter the data to be within 1 year of the film's release date and round it to the nearest thousand
    rounded_data = film_data[film_data.index <= (release_dt + np.timedelta64(1, 'Y'))].round(-3)

    # Get all instances of the mode after the date with the max # of daily pageviews
    modes = rounded_data[(rounded_data.isin(rounded_data.mode().values.tolist())) &
                         (rounded_data.index >= film_data.idxmax())]

    try:
        # Get the 1st day when daily pageviews = the mode
        earliest_dt = min(modes.index)
    except:
        # If there's no mode given the criteria, return NaT
        earliest_dt = pd.NaT

    return earliest_dt


if __name__ == "__main__":
    # Load data
    info_df = pd.read_csv('data/release_dates_v2.csv', index_col=0)
    wiki_df1 = pd.read_csv('data/2019 box office top 10_wiki pageviews.csv', index_col=0)
    wiki_df2 = pd.read_csv('data/2022 box office top 10_wiki pageviews.csv', index_col=0)
    wiki_df3 = pd.read_csv('data/netflix top 10 films - daily wikipedia pageviews.csv', index_col=0)

    # Merge Wikipedia data into 1 dataframe
    wiki_data = pd.concat([wiki_df1, wiki_df2], axis=1)
    wiki_data = pd.concat([wiki_data, wiki_df3], axis=1)

    # Process data
    movie_analysis, summary_df = process_data(info_df, wiki_data)

    # Save processed data
    movie_analysis.to_csv('data/processed_movie_data.csv')
    summary_df.to_csv('data/processed_summarized_data.csv')
