import pandas as pd
from datetime import datetime
import re
import numpy as np

def process_tv_data(streaming_df, reboots_df, revivals_df, manual_reboot_df):
    '''
    Processes streaming tv data in 'streaming_df', and marks tv shows as either reboots or non-reboots
    :param streaming_df: Pandas dataframe with raw data pulled from a Wikipedia page
    :param reboots_df: Pandas dataframe with raw data pulled from a Wikipedia page
    :param revivals_df: Pandas dataframe with raw data pulled from a Wikipedia page
    :param manual_reboot_df: Pandas dataframe manually created in 'get_data_v2.py'
    :return: streaming_df
    '''
    # Drop irrelevant columns from dataset, do nothing if the column doesn't exist
    try:
        streaming_df = streaming_df.drop(columns=['Finale'])
    except KeyError:
        pass
    try:
        streaming_df = streaming_df.drop(columns=['Runtime'])
    except KeyError:
        pass
    try:
        streaming_df = streaming_df.drop(columns=['Notes'])
    except KeyError:
        pass
    try:
        streaming_df = streaming_df.drop(columns=['Length'])
    except KeyError:
        pass
    try:
        streaming_df = streaming_df.drop(columns=['Unnamed: 5'])
    except KeyError:
        pass
    try:
        streaming_df = streaming_df.drop(columns=['Partner/Country'])
    except KeyError:
        pass
    try:
        streaming_df = streaming_df.drop(columns=['Netflix exclusive regions'])
    except KeyError:
        pass
    try:
        streaming_df = streaming_df.drop(columns=['Partner'])
    except KeyError:
        pass

    # Remove footnotes (i.e. [#]) from all dataframe entries (replace nan values with '' to avoid errors)
    streaming_df = streaming_df.replace({np.nan:''})
    streaming_df = streaming_df.applymap(lambda x: re.sub("\[.*\]","", x))

    # Remove "Awaiting release" rows
    streaming_df = streaming_df[streaming_df['Title'] != 'Awaiting release']

    # Convert premiere date to a datetime object
    streaming_df['Premiere'] = pd.to_datetime(streaming_df['Premiere'])

    # Remove shows that haven't premiered yet
    todays_date = datetime.today()
    streaming_df = streaming_df[streaming_df['Premiere'] < todays_date]

    # Remove non-English shows (Note: Shows where 'Language' column is blank are English shows)
    try:
        streaming_df = streaming_df[(streaming_df['Language'] == 'English') | (streaming_df['Language'] == '')]
    except KeyError:
        # If the dataset doesn't have a 'Language' column, pass because in that case all the shows are in English
        pass

    # Remove shows that aren't comedies or dramas
    general_genre_names = ['Animation', 'Animated', 'animation', 'animated', 'family', 'docu', 'competition', 'reality',
                           'Children', 'Reality', 'Docu']
    genres_to_remove = streaming_df['Genre'].apply(lambda genre_entry:
                                                        any([genre_name in genre_entry
                                                             for genre_name in general_genre_names]))
    streaming_df = streaming_df[~genres_to_remove]

    '''
    Create a separate column for the total number of seasons,
    including all the seasons the show has been renewed for
    '''
    # Load '# of seasons' data into 'Total Seasons' column
    streaming_df['Total Seasons'] = streaming_df.iloc[:,3].map(lambda x: x.split(' ')[0])
    # Replace 'TBA' values with np.nan to avoid errors
    streaming_df['Total Seasons'] = streaming_df['Total Seasons'].replace({'TBA': np.nan})
    # Convert the new column to float type
    streaming_df['Total Seasons'] = streaming_df['Total Seasons'].astype(float)
    # For all shows that have been renewed, increment the total seasons by 1
    streaming_df.loc[streaming_df['Status'] == 'Renewed', 'Total Seasons'] += 1
    # Drop the 'Seasons' column
    streaming_df = streaming_df.drop(columns=streaming_df.columns.to_list()[2])

    # Remove all miniseries
    streaming_df = streaming_df[streaming_df['Status'] != 'Miniseries']

    '''
    Mark shows as reboots or non-reboots
    '''
    # Create a new column for reboot status, mark all shows as non-reboots by default
    streaming_df['Reboot'] = False

    # Create a list of all reboot/revival titles
    reboot_titles_df = pd.concat([reboots_df['Title'], revivals_df['Original work'],
                                  revivals_df['Revival'], manual_reboot_df['Title']], axis=0)
    reboot_titles_df = reboot_titles_df.reset_index(drop=True)

    # Check if the list of reboot titles contains any of the streaming service tv show titles
    # and record the index of matching titles
    matched_reboot_titles = streaming_df['Title'].apply(lambda show_title:
                                                        any([show_title in reboot_title
                                                        for reboot_title in reboot_titles_df.to_list()]))
    # Flag tv show reboots in streaming_df
    streaming_df.loc[matched_reboot_titles, 'Reboot'] = True

    # Reset index
    streaming_df = streaming_df.reset_index(drop=True)
    return streaming_df

def remove_pending_shows(streaming_df):
    '''
    Removes all shows from dataframe where it's unknown if the show has been renewed for season 2
    :param streaming_df: Pandas dataframe of processed streaming tv show data,
                         must include 'Status' and 'Total Seasons' columns
    :return: streaming_df_excl_pending: Pandas dataframe
    '''

    # Copy dataframe
    streaming_df_excl_pending = streaming_df.copy()

    # Remove all shows with a pending status, if they have < 2 seasons
    streaming_df_excl_pending = streaming_df_excl_pending[((streaming_df_excl_pending['Status'] != 'Pending') &
                                                        (streaming_df_excl_pending['Status'] != 'Season 1 ongoing')) |
                                                        (streaming_df_excl_pending['Total Seasons'] >= 2)]

    # Reset index
    streaming_df_excl_pending = streaming_df_excl_pending.reset_index(drop=True)

    return streaming_df_excl_pending

if __name__ == "__main__":
    # Load reboots and revivals data
    reboots_df = pd.read_csv('data/raw_reboots_data_2021-12-18.csv', index_col=0)
    revivals_df = pd.read_csv('data/raw_revivals_data_2021-12-31.csv', index_col=0)
    manual_reboot_df = pd.read_csv('data/manual_reboots_data_2021-12-31.csv', index_col=0)

    # List of streaming services
    streaming_services = ['netflix_ended','netflix_ongoing', 'disney', 'amazon',
                          'apple', 'hulu','hbo', 'peacock', 'paramount']

    # Loop through streaming service raw data and process it
    for service in streaming_services:
        print("Processing " + service + " data...")
        # Load streaming service data
        service_df = pd.read_csv('data/raw_'+service+'_original_programming_2021-12-31.csv', index_col=0)

        # Add a 'Status' column to the 'netflix_ended' dataset
        # and mark each show as ended to standardize the dataset
        if service == 'netflix_ended':
            service_df['Status'] = 'Ended'

        '''
        Process streaming service data
        '''
        processed_df = process_tv_data(service_df, reboots_df, revivals_df, manual_reboot_df)

        # Manually make specific changes to rows in each dataset based on errors in the dataset & missing data
        if service == 'netflix_ongoing':
            # Address notes in 'Status' column

            # 'Stranger Things' renewed for season 4
            processed_df.loc[processed_df['Title'] == 'Stranger Things', 'Total Seasons'] = 4
            # 'The Crown' renewed for seasons 5 and 6, update total seasons to 6
            processed_df.loc[processed_df['Title'] == 'The Crown', 'Total Seasons'] = 6
            # 'Bridgerton' renewed for seasons 2-4
            processed_df.loc[processed_df['Title'] == 'Bridgerton', 'Total Seasons'] = 4
            # 'Ozark' renewed for season 4
            processed_df.loc[processed_df['Title'] == 'Ozark', 'Total Seasons'] = 4
            # 'The Umbrella Academy' renewed for season 3
            processed_df.loc[processed_df['Title'] == 'The Umbrella Academy', 'Total Seasons'] = 3
            # 'Raising Dion' renewed for season 2
            processed_df.loc[processed_df['Title'] == 'Raising Dion', 'Total Seasons'] = 2
            # 'Virgin River' renewed for season 4 and 5
            processed_df.loc[processed_df['Title'] == 'Virgin River', 'Total Seasons'] = 5
            # 'Locke & Key' renewed for season 3
            processed_df.loc[processed_df['Title'] == 'Locke & Key', 'Total Seasons'] = 3
            # 'Sweet Magnolias' renewed for season 2
            processed_df.loc[processed_df['Title'] == 'Sweet Magnolias', 'Total Seasons'] = 2
            # 'Firefly Lane' renewed for season 2
            processed_df.loc[processed_df['Title'] == 'Firefly Lane', 'Total Seasons'] = 2
            # 'After Life' renewed for season 3
            processed_df.loc[processed_df['Title'] == 'After Life', 'Total Seasons'] = 3
            # 'Dead to Me' renewed for season 3
            processed_df.loc[processed_df['Title'] == 'Dead to Me', 'Total Seasons'] = 3

            # Mark these shows as having _ seasons, as they're listed as having multiple parts but the parts make up
            # a different number of seasons
            processed_df.loc[processed_df['Title'] == 'Family Reunion', 'Total Seasons'] = 3

            # Remove shows that are continuations of shows from previous networks/services
            netflix_ongoing_continuations = ['Kota Factory (season 2)']
            processed_df = processed_df.loc[~(processed_df['Title'].isin(netflix_ongoing_continuations))]

        elif service == 'netflix_ended':
            # Mark these shows as non-reboots
            processed_df.loc[processed_df['Title'].isin(['A Series of Unfortunate Events', 'Shadow']), 'Reboot'] = False

            # Remove these shows as they are miniseries
            netflix_ended_miniseries = ['The Stranger', 'The English Game', 'Hollywood', 'Homemade', 'Social Distance',
                                        'Seven Seconds', 'What/If', 'Game On: A Comedy Crossover Event',
                                        'Wet Hot American Summer: First Day of Camp',
                                        'Trailer Park Boys Out of the Park: Europe',
                                        'Trailer Park Boys Out of the Park: USA', 'Best.Worst.Weekend.Ever.',
                                        'Dracula', 'I Am a Killer: Released', 'Collateral', 'Watership Down',
                                        'Alias Grace', 'Requiem', 'Pine Gap', 'Traitors', 'The Spy', 'Paranoid',
                                        'Troy: Fall of a City', 'Safe', 'Black Earth Rising', 'The Serpent',
                                        'The Last Dance']
            processed_df = processed_df.loc[~(processed_df['Title'].isin(netflix_ended_miniseries))]

            # Remove shows that are continuations of shows from previous networks/services
            netflix_ended_continuations = ['The Last Kingdom (season 2)', 'Interior Design Masters (season 1)',
                                           "Zumbo's Just Desserts (season 2)", 'Glitch (seasons 2–3)']
            processed_df = processed_df.loc[~(processed_df['Title'].isin(netflix_ended_continuations))]

            # Mark these shows as having _ seasons, as they're listed as having multiple parts but the parts make up
            # a different number of seasons
            processed_df.loc[processed_df['Title'].isin(['The Get Down', 'The Big Show Show',
                                                         'The Expanding Universe of Ashley Garcia',
                                                         'Prince of Peoria', 'Disjointed', 'No Good Nick', 'Team Kaylie'
                                                         ]), 'Total Seasons'] = 1
            processed_df.loc[processed_df['Title'] == 'Mr. Iglesias', 'Total Seasons'] = 2

            # First 2 seasons of 'Travelers' was a co-production with Netflix,
            # 'Travelers' season 3 was wholly-produced by Netflix
            processed_df.loc[processed_df['Title'] == 'Travelers (seasons 1-2)', 'Total Seasons'] = 3
            processed_df['Title'] = processed_df['Title'].replace({'Travelers (seasons 1-2)':'Travelers'})
        elif service == 'amazon':
            # Address notes in 'Status' column

            # 'Jack Ryan' renewed for season 3 and 4
            processed_df.loc[processed_df['Title'] == 'Jack Ryan', 'Total Seasons'] = 4
            # 'The Marvelous Mrs. Maisel' renewed for season 4
            processed_df.loc[processed_df['Title'] == 'The Marvelous Mrs. Maisel', 'Total Seasons'] = 4

            # Mark this show as a non-reboots
            processed_df.loc[processed_df['Title'].isin(['Hunters']), 'Reboot'] = False

            # Remove shows that are miniseries or continuations of shows from previous networks/services
            amazon_shows_to_remove = ['Ripper Street (seasons 3–5)', 'Small Axe', 'Flack (season 2)', 'Solos']
            processed_df = processed_df.loc[~(processed_df['Title'].isin(amazon_shows_to_remove))]
        elif service == 'apple':
            # Address notes in 'Status' column

            # 'Servant' renewed for season 3 and 4
            processed_df.loc[processed_df['Title'] == 'Servant', 'Total Seasons'] = 4
            # 'Mythic Quest' renewed for season 3 and 4
            processed_df.loc[processed_df['Title'] == 'Mythic Quest', 'Total Seasons'] = 4
        elif service == 'hulu':
            # Address notes in 'Status' column

            # 'Wu-Tang: An American Saga' renewed for season 3
            processed_df.loc[processed_df['Title'] == 'Wu-Tang: An American Saga', 'Total Seasons'] = 3
            # 'Dollface' renewed for season 2
            processed_df.loc[processed_df['Title'] == 'Dollface', 'Total Seasons'] = 2

            # Remove shows that are miniseries or continuations of shows from previous networks/services
            hulu_shows_to_remove = ['The Thick of It (series 4)']
            processed_df = processed_df.loc[~(processed_df['Title'].isin(hulu_shows_to_remove))]
        elif service == 'hbo':
            # Address notes in 'Status' column

            # 'Raised by Wolves' renewed for season 2
            processed_df.loc[processed_df['Title'] == 'Raised by Wolves', 'Total Seasons'] = 2
            # 'The Flight Attendant' renewed for season 2
            processed_df.loc[processed_df['Title'] == 'The Flight Attendant', 'Total Seasons'] = 2

            # Remove shows that are miniseries or continuations of shows from previous networks/services
            processed_df = processed_df.loc[~(processed_df['Title'].isin(['Station Eleven', 'And Just Like That...']))]
        elif service == 'paramount':
            # Address notes in 'Status' column

            # 'Star Trek: Picard' renewed for season 2 and 3
            processed_df.loc[processed_df['Title'] == 'Star Trek: Picard', 'Total Seasons'] = 3

        # Reset index
        processed_df = processed_df.reset_index(drop=True)

        # Create a 2nd dataframe and exclude pending shows from the dataset
        processed_df_excl_pending = remove_pending_shows(processed_df)

        # Save processed data to csv
        processed_df.to_csv('data/processed_'+service+'_data_incl_pending.csv')
        processed_df_excl_pending.to_csv('data/processed_'+service+'_data_excl_pending.csv')