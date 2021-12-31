import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import lxml

def get_wiki_table(URL, table_list):
    '''
    Function that grabs wikipedia tables from Wikipedia links and compiles them into a dataframe
    :param
    URL: URL for a Wikipedia page with tables
    num_tables: List of tables that need to be recorded from the Wikipedia link, in order (i.e. [1,2,31]
                indicates the 1st, 2nd and 31st tables)
    :return: Pandas dataframe
    '''
    # Send a HTTP request to the webpage
    website_req = requests.get(URL)
    # Parse the HTML
    website_soup = BeautifulSoup(website_req.text,'html.parser')

    '''
    Extract data from Wikipedia tables
    '''
    # Initialize Pandas dataframe
    df = pd.DataFrame()
    # Pull data on Drama and Comedy shows
    table = website_soup.findAll('table', attrs={'class':'wikitable'})
    # Initialize a counter to count the tables recorded
    table_counter = 0
    for k, subtable in enumerate(table):
        # Check if k+1 (because 1st table would be when k=0) is one of the tables that should be pulled
        if k+1 in table_list:
            # Pull all data from table
            temp_df = pd.read_html(str(subtable))
            temp_df = pd.DataFrame(temp_df[0])
            # Add temporary dataframe to final dataframe for output
            df = pd.concat([df, temp_df], axis=0, ignore_index=True, sort=False)
            # Increment table counter to record that a table has been pulled
            table_counter += 1
            # If all the requested tables has been pulled, end the loop
            if len(table_list) == table_counter:
                break
    return df


if __name__ == "__main__":
    # Load today's date
    todays_date = datetime.today().strftime('%Y-%m-%d')

    '''
    Get streaming service data
    '''
    # list of service name, url for programming and which tables to pull from url (i.e. [1,2,31] = pull the 1st, 2nd
    # and 31st tables from the list of ended Netflix original programming on Wikipedia)
    urls = [('netflix_ended', 'https://en.wikipedia.org/wiki/List_of_ended_Netflix_original_programming', [1, 2, 28]),
            ('disney', 'https://en.wikipedia.org/wiki/List_of_Disney%2B_original_programming', [1, 2]),
            ('netflix_ongoing', 'https://en.wikipedia.org/wiki/List_of_Netflix_original_programming', [1, 2, 24]),
            ('hbo', 'https://en.wikipedia.org/wiki/List_of_HBO_Max_original_programming', [1, 2, 13]),
            ('peacock', 'https://en.wikipedia.org/wiki/List_of_Peacock_original_programming', [1, 2, 7]),
            ('apple', 'https://en.wikipedia.org/wiki/List_of_Apple_TV%2B_original_programming', [1, 2, 9]),
            ('amazon', 'https://en.wikipedia.org/wiki/List_of_Amazon_Prime_Video_original_programming', [1, 2, 16]),
            ('hulu', 'https://en.wikipedia.org/wiki/List_of_Hulu_original_programming', [1, 2, 8]),
            ('paramount', 'https://en.wikipedia.org/wiki/List_of_Paramount%2B_original_programming', [1, 2, 8]),
            ('revivals', 'https://en.wikipedia.org/wiki/List_of_television_series_revivals', [1])]

    # Iterate through urls to collect and save data
    # for service_name, link, tables in urls:
    #     print("Pulling "+service_name+" data...")
    #     df = get_wiki_table(link, tables)
    #     # Save dataframe to csv
    #     if service_name == 'revivals':
    #         df.to_csv('data/raw_revivals_data_' + todays_date + '.csv')
    #     else:
    #         df.to_csv('data/raw_'+service_name+'_original_programming_'+todays_date+'.csv')

    '''
    Get reboot data 
    '''
    # print('Pulling reboot data...')
    # # Send a HTTP request to the Wikipedia tv reboot webpage
    # reboot_page_req = requests.get('https://en.wikipedia.org/wiki/Category:Television_series_reboots')
    # # Parse the webpage HTML
    # reboot_soup = BeautifulSoup(reboot_page_req.content,'html5lib')
    # # Pull data on Drama and Comedy shows
    # reboot_content = reboot_soup.findAll('div', attrs={'class': 'mw-category-group'})
    # # Initialize list of tv show titles, and then add each title to the list
    # titles = []
    # for entry in reboot_content:
    #     for bullet in entry.ul.findAll('li'):
    #         titles = titles + [bullet.text]
    # # Load tv show titles into dataframe
    # df = pd.DataFrame({'Title':titles})
    # # Save dataframe to csv
    # df.to_csv('data/raw_reboots_data_'+todays_date+'.csv')

    '''
    Export manual data into a csv
    '''
    # Manual list of reboots
    manual_reboots_list = ['Fuller House', 'House of Cards', 'Cowboy Bebop', 'Chilling Adventures of Sabrina',
                           'Fate: The Winx Saga', 'No Activity', 'Tell Me a Story', 'The Game', 'Greenhouse Academy',
                           'W/ Bob & David', 'Medical Police', 'Julie and the Phantoms', 'Trailer Park Boys',
                           'Medical Police', 'Doogie Kameāloha, M.D.', 'High School Musical: The Musical: The Series',
                           'Mad Dogs', 'Utopia', 'Back to the Rafters', 'Amazing Stories', 'Gossip Girl', 'MacGruber',
                           "Dirk Gently's Holistic Detective Agency", 'The New Legends of Monkey', 'Calls']
    # Convert list to dataframes
    manual_reboot_df = pd.DataFrame({'Title': manual_reboots_list})
    # Save dataframe to csv
    manual_reboot_df.to_csv('data/manual_reboots_data_' + todays_date + '.csv')

