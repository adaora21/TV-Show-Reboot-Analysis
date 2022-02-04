import pandas as pd
import re
import numpy as np


def process_wikipedia_data(streaming_df, startyear, endyear):
    '''
    Cleans movie data in 'streaming_df' and removes unnecessary columns
    :param streaming_df: Pandas dataframe with raw data pulled from a Wikipedia page
    :param startyear: Starting year for analysis
    :param endyear: End year for analysis
    :return: processed_streaming_df
    '''
    # Copy 'streaming_df' to avoid errors
    processed_streaming_df = streaming_df.copy()

    # Drop irrelevant columns from dataset, do nothing if the column doesn't exist
    try:
        processed_streaming_df = processed_streaming_df.drop(columns=['Studio'])
    except KeyError:
        pass
    try:
        processed_streaming_df = processed_streaming_df.drop(columns=['Genre'])
    except KeyError:
        pass
    try:
        processed_streaming_df = processed_streaming_df.drop(columns=['Genre(s)'])
    except KeyError:
        pass
    try:
        processed_streaming_df = processed_streaming_df.drop(columns=['Language'])
    except KeyError:
        pass

    # Remove footnotes (i.e. [#]) from all dataframe entries (replace nan values with '' to avoid errors)
    processed_streaming_df = processed_streaming_df.replace({np.nan: ''})
    processed_streaming_df = processed_streaming_df.applymap(lambda x: re.sub("\[.*\]", "", x))

    # Remove notes in brackets in date column (i.e. (...))
    processed_streaming_df = processed_streaming_df.applymap(lambda x: re.sub("\(.*\)", "", x))

    # Remove "Awaiting release" rows
    processed_streaming_df = processed_streaming_df[processed_streaming_df['Title'] != 'Awaiting release']

    # Convert release date (sometimes labelled 'premiere') to a datetime object
    try:
        processed_streaming_df['Release date'] = pd.to_datetime(processed_streaming_df['Release date'])
    except KeyError:
        try:
            processed_streaming_df['Release date'] = pd.to_datetime(processed_streaming_df['Premiere'])
            processed_streaming_df = processed_streaming_df.drop(columns=['Premiere'])
        except KeyError:
            processed_streaming_df['Release date'] = pd.to_datetime(processed_streaming_df['Release'])
            processed_streaming_df = processed_streaming_df.drop(columns=['Release'])

    # Create new column for release year and remove release date column
    processed_streaming_df['release year'] = processed_streaming_df['Release date'].dt.year
    processed_streaming_df = processed_streaming_df.drop(columns=['Release date'])

    # Restrict dataset to movies released between startyear and endyear
    processed_streaming_df = processed_streaming_df[(processed_streaming_df['release year'] >= startyear)
                                                    & (processed_streaming_df['release year'] <= endyear)]

    # Convert column names to lowercase
    processed_streaming_df.columns = processed_streaming_df.columns.str.lower()

    # Reset index
    processed_streaming_df = processed_streaming_df.reset_index(drop=True)

    return processed_streaming_df

def process_amazon_data(streaming_df, startyear, endyear):
    '''
    Cleans movie data in 'streaming_df'
    :param streaming_df: Pandas dataframe with raw data pulled from an IMDb page
    :param startyear: Starting year for analysis
    :param endyear: End year for analysis
    :return: processed_streaming_df
    '''
    # Copy 'streaming_df' to avoid errors
    processed_streaming_df = streaming_df.copy()

    processed_streaming_df['release year'] = processed_streaming_df['release year'].astype(int)

    # Restrict dataset to movies released between startyear and endyear
    processed_streaming_df = processed_streaming_df[(processed_streaming_df['release year'] >= startyear)
                                                    & (processed_streaming_df['release year'] <= endyear)]
    # Reset index
    processed_streaming_df = processed_streaming_df.reset_index(drop=True)

    return processed_streaming_df

def runtime_regex_function(runtime):
    '''
    Converts runtime in string type to runtime in int type (units: minutes)
    :param runtime: (string) movie runtime
    :return: int_runtime: (int) movie runtime in minutes
    '''
    # Match 'hour' and 'minute' digits in runtime string
    matches = re.findall("((\d*)\s*h\w*)?\D*((\d*)\s*m\w*)?", runtime)
    # Convert '' entries to 0 to facilitate conversion to int
    matches[0] = [0 if x == '' else x for x in list(matches[0])]
    # Use matched 'hour' and 'minute' digits to convert runtime to int
    int_runtime = int(matches[0][1])*60+int(matches[0][3])
    return int_runtime

def convert_runtime(df):
    '''
    Takes df['runtime'] and converts runtime to minutes
    :param df: Pandas dataframe with a 'runtime' column
    :return: Pandas dataframe
    '''
    df['runtime'] = df['runtime'].apply(runtime_regex_function)
    return df

def process_boxoffice_data(startyear, endyear):
    '''
    Pulls box office data from start year to end year, cleans the dataframes and
    aggregates the data into 1 dataframe
    :param startyear: (int)
    :param endyear: (int)
    :return: df: Pandas dataframe containing all box office data from startyear to endyear
    '''
    # Initialize aggregate df
    df = pd.DataFrame()
    for year in range(startyear, endyear+1):
        # Load streaming service data
        annual_df = pd.read_csv('data/raw_box_office_data_'+str(year)+'.csv', index_col=0)
        # Release year matches year on file
        annual_df['release year'] = year
        # Drop irrelevant columns
        annual_df = annual_df.drop(columns=['release date'])
        # Remove rows with blank entry for 'runtime'
        annual_df = annual_df.dropna(subset=['runtime'])
        # Add data to aggregate df
        df = pd.concat([df, annual_df], axis=0, ignore_index=True, sort=False)

    # Convert runtime to minutes
    df = convert_runtime(df)

    # Reset index
    df = df.reset_index(drop=True)

    return df

if __name__ == "__main__":
    # List of streaming services
    streaming_services = ['netflix', 'disney', 'amazon', 'apple', 'hulu', 'hbo', 'peacock', 'paramount']

    # Initialize parameters for analysis
    startyear = 1991
    endyear = 2021

    '''
    Process streaming data
    '''
    # Loop through streaming service raw data, process it and concatenate it into 'all_streaming_df'
    all_streaming_df = pd.DataFrame()
    for service in streaming_services:
        print("Processing " + service + " data...")
        # Load streaming service data
        service_df = pd.read_csv('data/raw_' + service + '_feature_films_2022-01-11.csv', index_col=0)
        if service != 'amazon':
            # Process streaming data sourced from Wikipedia
            service_df = process_wikipedia_data(service_df, startyear=startyear, endyear=endyear)
        elif service == 'amazon':
            # Process data differently since it was sourced from IMDb
            service_df = process_amazon_data(service_df, startyear=startyear, endyear=endyear)
        # Add data to 'all_streaming_df' dataframe
        all_streaming_df = pd.concat([all_streaming_df, service_df], axis=0, ignore_index=True, sort=False)

    # Convert runtime to minutes
    final_streaming_df = convert_runtime(all_streaming_df)
    # Save processed df to csv
    final_streaming_df.to_csv('data/processed_streaming_films_runtime.csv')

    '''
    Process box office data
    '''
    print("Processing box office data...")
    # Process box office data
    boxoffice_df = process_boxoffice_data(startyear, endyear)

    # Save processed df to csv
    boxoffice_df.to_csv('data/processed_boxoffice_films_runtime.csv')
