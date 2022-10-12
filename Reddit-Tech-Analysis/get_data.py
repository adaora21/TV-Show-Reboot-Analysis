import praw
import pandas as pd
from datetime import datetime
import time


def get_reddit_data(service):
    '''
    Get the top 1000 posts on the given service's subreddit in the past year + key attributes for each post
    :param service (string): title of the streaming service's subreddit (capitalization matters)
    :return: data_df: Pandas dataframe with subreddit post + attributes
    '''

    # Get the top 1000 posts in the past year
    posts = reddit.subreddit(service).top(limit=1000, time_filter='year')

    # List key attributes to pull for each post
    attributes = ['id','title', 'body', 'score', 'num_comments', 'upvote_ratio','tag','publish_date',]

    # Initialize a dataframe
    data_df = pd.DataFrame(columns=attributes)

    # Save each post's attributes
    for i, post in enumerate(posts):
        row = {}

        # Add the post ID
        row[attributes[0]] = post.id

        # Add the post title
        row[attributes[1]] = post.title

        # Add the body of the post
        row[attributes[2]] = post.selftext

        # Add the post score
        row[attributes[3]] = post.score

        # Add the total number of comments on the post
        row[attributes[4]] = post.num_comments

        # Add the percentage of upvotes out of all votes on the post
        row[attributes[5]] = post.upvote_ratio

        # Add the post's flair (aka tag)
        row[attributes[6]] = post.link_flair_text

        # Add the publish date
        row[attributes[7]] = post.created_utc

        # Save the post to the dataframe
        data_df.loc[i] = row

    # Add the subreddit name to the dataframe
    data_df['service'] = service

    return data_df

if __name__ == "__main__":
    # Load today's date
    todays_date = datetime.today().strftime('%Y-%m-%d')

    # Create a read-only Reddit instance
    reddit = praw.Reddit(client_id="XXXXXXXXXXXXXXXXXX", client_secret="XXXXXXXXXXXXXX", user_agent="XXXXXXXXXXXXXXXX")

    for service in ['Hulu','HBOMAX','peacock']:

        print("pulling "+service+" data...")

        # Get reddit data
        df = get_reddit_data(service)

        # Save the data in a pandas dataframe
        df.to_csv('data/'+service+'_'+todays_date+'.csv')

        # Wait 1 min after querying each podcast
        time.sleep(60)