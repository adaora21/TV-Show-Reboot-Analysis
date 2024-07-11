import pandas as pd
import numpy as np

def process_df(df, app, upper_bound):
    '''
    Process Instagram & TikTok data
    :param df: (pandas dataframe) Contains celebrity personal & brand names + follower data
    :param upper_bound: (float) Maximum follower count for celebrity personal accounts, expressed in millions
                                This can be infinity
    :param app: (string) Social media app (either TikTok or Instagram)
    :return: processed_df: (pandas dataframe) Processed pandas dataframe, ready for analysis
    '''
    # Filter to app-related rows only
    processed_df = df[['celebrity', 'brand', 'c_'+app, 'b_'+app]].copy()
    # Express each follower count in millions
    processed_df['c_'+app] = processed_df['c_'+app] / 1e6
    processed_df['b_'+app] = processed_df['b_'+app] / 1e6
    # Filter to celebrities with < upper_bound followers on their personal account
    processed_df = processed_df[processed_df['c_'+app] < upper_bound]
    # Remove rows where either the celebrity's personal or brand follower count is null
    processed_df = processed_df.dropna()
    # Reset index after filters
    processed_df = processed_df.reset_index(drop=True)

    return processed_df

if __name__ == "__main__":
    '''
    Process Instagram & TikTok data
    '''
    # Load data
    df = pd.read_csv('data/celebrity_brands.csv')
    processing_parameters = [['instagram', np.inf], ['instagram', 50], ['tiktok', np.inf], ['tiktok', 10]]

    # Create 4 separate datasets and save each one
    for i in processing_parameters:

        processed_data = process_df(df, app=i[0], upper_bound=i[1])

        # Set file name label
        if i[1] == np.inf:
            limit_label = 'all'
        else:
            limit_label = 'less_than_'+str(i[1])+'M'

        # Print the number of data points in the dataset
        print("There are " +str(processed_data.shape[0])+ " celebrity brands in the "+i[0]+" "+limit_label+" dataset")

        # Save data
        processed_data.to_csv('data/processed_celebrity_brands_'+i[0]+'_'+limit_label+'.csv')