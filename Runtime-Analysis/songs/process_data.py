import pandas as pd


if __name__ == "__main__":
    # Initialize parameters for analysis
    startyear = 1991
    endyear = 2021

    '''
    Process song data and aggregate it into one dataframe
    '''

    # Initialize aggregate df
    df = pd.DataFrame()
    for year in range(startyear, endyear+1):
        # Load song data
        spotify_df = pd.read_csv('data/raw_spotify_data_'+str(year)+'.csv', index_col=0)

        # Convert duration from milliseconds to seconds
        spotify_df['duration'] = spotify_df['duration_ms']/1000
        spotify_df = spotify_df.drop(columns=['duration_ms'])

        # Convert release date to a datetime object
        spotify_df['release date'] = pd.to_datetime(spotify_df['release date'])
        # Create new column for release year and remove release date column
        spotify_df['release year'] = spotify_df['release date'].dt.year
        spotify_df = spotify_df.drop(columns=['release date'])

        # Remove songs that were released more than 1 year before or after the playlist year
        # (this indicates that the version of the song listed on Spotify is likely a re-release,
        # and re-releases are excluded for simplicity)
        spotify_df = spotify_df[(spotify_df['release year'] - spotify_df['playlist_year'] < 2) &
                                (spotify_df['release year'] - spotify_df['playlist_year'] > -2)]
        spotify_df = spotify_df.drop(columns=['playlist_year'])

        # Filter for songs released within the analysis period
        spotify_df = spotify_df[(spotify_df['release year'] >= startyear) &
                                (spotify_df['release year'] <= endyear)]

        # Add data to aggregate df
        df = pd.concat([df, spotify_df], axis=0, ignore_index=True, sort=False)

    # Reset index
    df = df.reset_index(drop=True)

    # Save processed df to csv
    df.to_csv('data/processed_spotify_songs_duration.csv')