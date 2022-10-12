import pandas as pd

def process_data(file_info):
    '''
    Process raw subreddit data
    :param file_info: list of subreddit names and tech support label names for each service
    :return: posts_df: Pandas dataframe with processed subreddit data for all the inputted services
             stats_df: Pandas dataframe with stats on the number of tech supports posts on each service's subreddit
    '''

    # Initialize dataframes
    stats_df = pd.DataFrame(columns=['service', 'num tech posts', 'total posts', 'pct of tech posts'])

    posts_col = ['service', 'tech_flag', 'score', 'num_comments', 'upvote_ratio', 'title', 'all text']
    posts_df = pd.DataFrame(columns=posts_col)

    # For each service, load the raw data, process it, record its stats and add it to the posts_df
    for i in range(len(file_info)):
        # Get the service's subreddit name and the name of its tech support label
        service = file_info[i][0]
        tech_label = file_info[i][1]

        print("processing " + service + " data...")

        # Load the raw data
        raw_df = pd.read_csv('data/' + service + '_2022-09-25.csv', index_col=0, keep_default_na=False)

        # Flag all tech support posts
        processed_df = raw_df.copy()
        processed_df['tech_flag'] = 0
        processed_df.loc[processed_df['tag'] == tech_label, 'tech_flag'] = 1

        # Combine post title and body into one column
        processed_df['all text'] = processed_df[['title','body']].apply(lambda row: '. '.join(row.values.astype(str)), axis=1)

        # Rearrange column order and filter for relevant columns
        processed_df = processed_df[posts_col]

        # Record stats
        stats_df.loc[i, 'service'] = service
        stats_df.loc[i, 'num tech posts'] = processed_df[processed_df['tech_flag'] == 1].shape[0]
        stats_df.loc[i, 'total posts'] = processed_df.shape[0]
        stats_df.loc[i, 'pct of tech posts'] = stats_df.loc[i, 'num tech posts'] / stats_df.loc[i, 'total posts']

        # Add subreddit data to posts_df
        posts_df = pd.concat([posts_df, processed_df], axis=0, ignore_index=True, sort=False)

    return posts_df, stats_df

if __name__ == "__main__":
    # List out subreddit info for each service
    file_info = [['Hulu', 'Technical Support'], ['HBOMAX', 'Tech Support'],
                 ['peacock', 'Technical Support']]

    # Process data
    posts_df, stats_df = process_data(file_info)

    # Save processed data
    posts_df.to_csv('data/processed_posts.csv')
    stats_df.to_csv('data/processed_stats.csv')