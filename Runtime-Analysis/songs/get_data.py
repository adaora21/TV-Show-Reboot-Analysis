import spotipy
from spotipy.oauth2 import SpotifyClientCredentials  # To access authorised Spotify data
import pandas as pd

def get_playlist_data(id, column_names, year):
    '''
    Uses playlist ID to record 'playlist_url' and 'playlist_year', plus 'track_uri', 'title',
    'release date' and 'duration_ms' for each song in the playlist.
    :param playlist_id: (string) Spotify playlist ID
    :param column_names: (list of strings) list of column names for df
    :param year: (int) playlist year - the year when the songs in the playlist were top hits
    :return: df: Pandas dataframe containing playlist data
    '''

    # Pull playlist details using the playlist ID
    playlist_results = spotify.playlist_tracks(id)
    playlist_items = playlist_results['items']
    while playlist_results['next']:
        playlist_results = spotify.next(playlist_results)
        playlist_items.extend(playlist_results['items'])

    # Initialize dataframe to store playlist track data
    df = pd.DataFrame(columns=column_names)

    for i, track in enumerate(playlist_items):
        track_details = track['track']
        # Initialize a dictionary to hold track info
        track_df_entry = {}
        try:
            # Save track uri
            track_df_entry[column_names[1]] = track_details['uri']
            # Save track title
            track_df_entry[column_names[2]] = track_details['name']
            # Save track release date
            track_df_entry[column_names[3]] = track_details['album']['release_date']
            # Save track duration
            track_features = spotify.audio_features(track_details['id'])
            track_df_entry[column_names[4]] = track_features[0]['duration_ms']
            # Save playlist year
            track_df_entry[column_names[5]] = year
            # Save data to df
            df.loc[i] = track_df_entry
        except:
            continue

    return df

if __name__ == "__main__":
    CLIENT_ID = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    CLIENT_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    # Spotify API manager
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    # Spotify object to access API
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Set column names
    column_names = ['playlist_url', 'track_uri', 'title', 'release date', 'duration_ms', 'playlist_year']

    '''
    Pull songs from official Spotify 'Top Hits' playlists 
    '''
    # Pull data from 1991 to 2021
    startyear = 1991
    endyear = 1991

    for year in range(startyear, endyear+1):
        # Search for 'Top Hits' playlist
        search_results = spotify.search(q='Top Hits of '+str(year), type='playlist')
        search_items = search_results['playlists']['items']
        for search_item in search_items:
            # Select the official Spotify playlist
            if search_item['owner']['external_urls']['spotify'] == 'https://open.spotify.com/user/spotify'\
                        and search_item['name'] == 'Top Hits of '+str(year):
                print('Pulling data for '+search_item['name'])
                # Get playlist ID
                playlist_id = search_item['id']
                # Get playlist data
                df = get_playlist_data(playlist_id, column_names, year)
                # Save playlist url
                df['playlist_url'] = search_item['external_urls']['spotify']
                # Save dataframe to csv
                df.to_csv('data/raw_spotify_data_'+str(year)+'.csv')

    '''
    Pull songs from official Spotify "Top Tracks" list for 2020 and 2021
    '''
    # List playlist IDs
    playlist_ids = [('2020', '37i9dQZF1DX7Jl5KP2eZaS'), ('2021', '37i9dQZF1DX18jTM2l2fJY')]
    # Get playlist data
    for year, id in playlist_ids:
        print('Pulling data for Top Track of '+str(year))
        df = get_playlist_data(id, column_names, year)
        # Save playlist url
        df['playlist_url'] = 'https://open.spotify.com/playlist/'+id
        # Save dataframe to csv
        df.to_csv('data/raw_spotify_data_' + str(year) + '.csv')