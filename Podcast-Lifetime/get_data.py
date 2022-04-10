import pandas as pd
import requests
import time
import math

def get_all_episode_data(token, column_names, id_df):
    '''
    Get all episodes (on Spotify) for each podcast in df
    :param id_df: Pandas dataframe with podcast Spotify IDs
    :return: episodes_df: Pandas dataframe with all episode data
    '''
    # Initialize dataframe to store playlist track data
    episode_df = pd.DataFrame(columns=column_names)

    # Initialize query parameters
    type = 'episodes'
    market = 'US'
    limit = 50

    # Iterate through list of podcast IDs and get all episode data for each podcast
    for i, podcast_id in enumerate(id_df['podcast_id'].tolist()):
        if podcast_id == '':
            # If the podcast has no podcast ID, skip
            continue

        print('Pulling data for: '+id_df.loc[i, 'podcast_title']+', with ID: '+str(podcast_id))

        # Initialize query counter
        counter = 0
        # Temporarily set total number of queries = 1 by default, so that the first query can be performed and used to
        # calculate the actual total number of queries needed
        total_num_queries = 1
        # Set query to start by returning the first item
        offset = 0

        # Create url for podcast with podcast_id
        endpoint_url = f"https://api.spotify.com/v1/shows/{podcast_id}/episodes?"

        # Run a while loop and perform queries until all episodes on Spotify have been saved
        while counter <= total_num_queries:
            # Set up query
            query = f'{endpoint_url}'
            query += f'&type={type}'
            query += f'&offset={offset}'
            query += f'&market={market}'
            query += f'&limit={limit}'

            # Send a get request using Spotify API
            query_response = requests.get(query,
                                          headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
            response_json = query_response.json()

            # Check that the first entry in the json response is not an error
            if next(iter(response_json)) != 'error':
                # Iterate through items in the json response, and save data
                for j in range(len(response_json['items'])):
                    # Initialize dictionary for episode data
                    ep_data = {}
                    # Save podcast ID
                    ep_data[column_names[0]] = podcast_id
                    # Save podcast title
                    ep_data[column_names[1]] = id_df.loc[i, 'podcast_title']
                    # Save episode ID
                    ep_data[column_names[2]] = response_json['items'][j]['id']
                    # Save episode title
                    ep_data[column_names[3]] = response_json['items'][j]['name']
                    # Save episode duration
                    ep_data[column_names[4]] = response_json['items'][j]['duration_ms']
                    # Save episode release date
                    ep_data[column_names[5]] = response_json['items'][j]['release_date']

                    # Save episode data to dataframe
                    episode_df.loc[episode_df.shape[0]] = ep_data

                if counter == 0:
                    # During the first query, calculate the total number of queries that need to be performed
                    # and update the variable
                    total_num_queries = math.floor(response_json['total'] // limit)

                # Increment counter and offset after each query is performed
                counter += 1
                # Increase the offset by limit (num of items returned each time)
                offset = offset + limit

            else:
                # If there's an error, print the error and break the loop
                print(response_json, ' for: ', id_df.loc[i, 'podcast_title'])
                break

        # Wait 1 min after querying each podcast
        time.sleep(60)

    return episode_df

if __name__ == "__main__":
    OAuthToken = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    # Load podcast IDs
    id_df = pd.read_csv('data/US_top50_podcasts_q1_to_q4_2021_processed.csv', keep_default_na=False)

    # Set column names
    column_names = ['podcast_id', 'podcast_title', 'episode_id', 'episode_title', 'duration_ms', 'release_date']

    # Get episode data
    episode_df = get_all_episode_data(OAuthToken, column_names, id_df)

    # Save data
    episode_df.to_csv('data/spotify_podcast_ep_data.csv')