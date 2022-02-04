import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def get_boxofficemojo_data(url_prefix, url_suffix, startyear, endyear):
    '''
    Function gets movie title, release date and runtime for each movie in a table of
    the top 200 movies by gross box office revenue, each year.
    :param url_prefix: Box Office Mojo domestic box office data url prefix
    :param url_suffix: Box Office Mojo domestic box office data url suffix
    :param startyear (int): Record box office data starting on this year
    :param endyear (int): Record box office data up to and including this year
    :return: Pandas dataframe containing data from Box Office Mojo
    '''
    # Initialize Pandas dataframe
    col_names = ['title', 'release date', 'runtime']
    df = pd.DataFrame(columns=col_names)

    # Iterate through years from startyear to endyear
    for year in range(startyear, endyear+1):
        # Send a HTTP request to the webpage
        website_req = requests.get(url_prefix+str(year)+url_suffix)
        # Parse the HTML
        website_soup = BeautifulSoup(website_req.text, 'html.parser')
        # Parse list of top 200 films for <year>
        parsed_table = website_soup.findAll('table')[0]
        data = [
                [col.a['href'] if col.find('a') else '' for col in row.find_all('td')]
                for row in parsed_table.find_all('tr')]
        # Save list of top 200 films to dataframe
        # Note: Links to individual title pages are in Col 1
        link_df = pd.DataFrame(data[1:], columns=[i for i in range(len(data[1]))])

        temp_df = pd.DataFrame(columns=col_names)

        # Pull movie title, release date and runtime
        for i, title_url in enumerate(link_df.iloc[:,1].to_list()):
            movie_data = {}
            # Send a HTTP request to the webpage
            title_website_req = requests.get('https://www.boxofficemojo.com'+title_url)
            # Parse the HTML
            title_soup = BeautifulSoup(title_website_req.text, 'html.parser')

            # If the movie is not a re-release, record data
            if not title_soup.find('h2', attrs={'class':'a-size-medium'}):
                # Save movie title
                movie_data[col_names[0]] = ''.join(title_soup.find('h1', attrs={'class':'a-size-extra-large'}).stripped_strings)

                # Iterate through summary table to save film release date and runtime
                title_summary = title_soup.find('div',
                                                attrs={'class':'a-section a-spacing-none mojo-summary-values mojo-hidden-from-mobile' })
                for summary_entry in title_summary.findAll('div', attrs={'class':'a-section a-spacing-none'}):
                    if summary_entry.findAll('span')[0].text == 'Release Date':
                        # Save release date
                        movie_data[col_names[1]] = ''.join(summary_entry.findAll('span')[1].stripped_strings)
                    elif summary_entry.findAll('span')[0].text == 'Running Time':
                        # Save runtime
                        movie_data[col_names[2]] = ''.join(summary_entry.findAll('span')[1].stripped_strings)
                # Load movie data into temp dataframe
                temp_df.loc[i] = movie_data
        # Add temp dataframe to final dataframe for output
        df = pd.concat([df, temp_df], axis=0, ignore_index=True, sort=False)
    return df

def get_wiki_table(URL, table_list):
    '''
    Function that grabs tables from Wikipedia links and compiles them into a dataframe
    :param: URL: URL for a Wikipedia page with tables
    :param: num_tables: List of tables that need to be recorded from the Wikipedia link
                (ex. [1, 2, 31] indicates that the 1st, 2nd and 31st tables should be recorded)
    :return: Pandas dataframe containing data from Wikipedia tables
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
    # Pull feature film data
    table = website_soup.findAll('table', attrs={'class':'wikitable'})
    # Initialize a counter to count the number of tables recorded
    table_counter = 0
    for k, subtable in enumerate(table):
        # Check if k+1 (because 1st table is indexed at k=0) is one of the tables that should be pulled
        if k+1 in table_list:
            # Pull all data from table
            temp_df = pd.read_html(str(subtable))
            temp_df = pd.DataFrame(temp_df[0])
            # Add temporary dataframe to final dataframe for output
            df = pd.concat([df, temp_df], axis=0, ignore_index=True, sort=False)
            # Increment table counter because a table has been recorded
            table_counter += 1
            # If all the requested tables has been recorded, end the loop
            if len(table_list) == table_counter:
                break
    return df

def get_amazon_data(URL):
    '''
    Function that pulls movie title, release year and runtime for list of Amazon original movies
    :param URL: URL for a list of Amazon original movies on IMDb
    :return: Pandas dataframe
    '''
    # Send a HTTP request to the webpage
    website_req = requests.get(URL)
    # Parse the HTML
    website_soup = BeautifulSoup(website_req.text, 'html.parser')
    # Initialize Pandas dataframe
    col_names = ['title', 'release year', 'runtime']
    df = pd.DataFrame(columns=col_names)
    # Pull feature film data
    parsed_table = website_soup.find('div', attrs={'class': 'list_items_container'})
    # Iterate through table and pull title, runtime and release year for each movie
    for i, row in enumerate(parsed_table.findAll('div', attrs={'class':'row'})):
        for j, movie_section in enumerate(row.findAll('div', attrs={'class':'media'})):
            movie_data = {}
            # Save movie title
            movie_data[col_names[0]] = ''.join(movie_section.findAll('span', attrs={'class':'h4'})[1].stripped_strings)
            # Save release year
            movie_data[col_names[1]] = ''.join(movie_section.find('span', attrs={'class': 'nowrap'}).stripped_strings)\
                                                                        .replace('I','').replace('(','').replace(')','')
            # Save runtime
            movie_data[col_names[2]] = ''.join(movie_section.find('span', attrs={'class': 'runtime'}).stripped_strings)
            # Load movie data into dataframe
            df.loc[i*2+j] = movie_data
    return df


if __name__ == "__main__":
    # Load today's date
    todays_date = datetime.today().strftime('%Y-%m-%d')

    '''
    Get box office data
    '''
    print("Pulling box office data...")
    # Record prefix and suffix for url used to access annual box office data
    box_office_url_prefix = 'https://www.boxofficemojo.com/year/'
    box_office_url_suffix = '/?grossesOption=totalGrosses'

    # Get box office data
    df = get_boxofficemojo_data(box_office_url_prefix, box_office_url_suffix, startyear=1991, endyear=2021)

    # Save dataframe to csv
    df.to_csv('data/raw_box_office_data.csv')

    '''
    Get streaming service data
    '''
    # list of service name, url for wikipedia page and which tables to pull from url
    # (Example: [1] = pull the 1st table from the list of Disney original films on Wikipedia)
    streaming_urls = [('disney', 'https://en.wikipedia.org/wiki/List_of_Disney%2B_original_films', [1]),
            ('hbo', 'https://en.wikipedia.org/wiki/List_of_HBO_Max_original_programming', [16]),
            ('peacock', 'https://en.wikipedia.org/wiki/List_of_Peacock_original_programming', [11]),
            ('apple', 'https://en.wikipedia.org/wiki/List_of_Apple_TV%2B_original_programming', [10]),
            ('hulu', 'https://en.wikipedia.org/wiki/List_of_Hulu_original_programming', [11]),
            ('paramount', 'https://en.wikipedia.org/wiki/List_of_Paramount%2B_original_programming', [16])]

    netflix_urls = [('netflix_2015_2017', 'https://en.wikipedia.org/wiki/List_of_Netflix_original_films_(2015%E2%80%932017)', [1]),
            ('netflix_2018', 'https://en.wikipedia.org/wiki/List_of_Netflix_original_films_(2018)', [1]),
            ('netflix_2019', 'https://en.wikipedia.org/wiki/List_of_Netflix_original_films_(2019)', [1]),
            ('netflix_2020', 'https://en.wikipedia.org/wiki/List_of_Netflix_original_films_(2020)', [1]),
            ('netflix_2021', 'https://en.wikipedia.org/wiki/List_of_Netflix_original_films_(2021)', [1])]

    # Iterate through urls to collect and save data
    for service_name, link, tables in streaming_urls:
        print("Pulling " + service_name + " data...")
        df = get_wiki_table(link, tables)
        # Save dataframe to csv
        df.to_csv('data/raw_' + service_name + '_feature_films_' + todays_date + '.csv')

    # Iterate through Netflix urls to collect, concatenate and save data
    netflix_df = pd.DataFrame()
    for service_name, link, tables in netflix_urls:
        print("Pulling " + service_name + " data...")
        df = get_wiki_table(link, tables)
        netflix_df = pd.concat([netflix_df, df], axis=0, ignore_index=True, sort=False)
    # Save dataframe to csv
    netflix_df.to_csv('data/raw_netflix_feature_films_' + todays_date + '.csv')

    # Pull Amazon Prime original film data
    print("Pulling amazon data...")
    df = get_amazon_data('https://m.imdb.com/list/ls098565773/?ref_=m_ur')
    # Save dataframe to csv
    df.to_csv('data/raw_amazon_feature_films_' + todays_date + '.csv')
