import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.ticker import MultipleLocator

def pie_chart(pie_chart_df):
    '''
    Plots pie chart of publishers of the top 50 podcasts in the US in 2021
    :param pie_chart_df: Pandas dataframe with pie chart data
    :return: None
    '''

    '''
    Plot data
    '''
    fig_pie, ax_pie = plt.subplots()

    ax_pie.pie(pie_chart_df.loc[:, 'percentage'], autopct='%1.0f%%',
                                                normalize=True,
                                                startangle=90,
                                                wedgeprops={'edgecolor': '#FFFFFF'}, pctdistance=0.6,
                                                textprops={'color': '#000000', 'fontsize': 16,
                                                           'fontweight': 'normal'},
                                                labels=pie_chart_df['publisher'], labeldistance=1.05,
                                                colors=['#FF9B62', '#88AAFF', '#76E991','#A687FF', '#FE86BE', '#D6D6D6'])

    '''
    Format chart
    '''
    # Set pie chart as a circle
    ax_pie.axis('equal')

    # Add pie chart footnotes
    ax_pie.text(-0.9, -1.3,
                'Data Source: U.S. Top 50 Podcasts Q1 2021 - Q4 2021 by Edison Research'
                ' \nCreated by: Adaora (uploading.substack.com)',
                fontsize=9)

    # Set pie chart title
    ax_pie.text(0, 1.15, "Podcast Publishers: \n Share of the Top 50 Podcasts in the US in 2021",
                      fontdict={'fontsize': 18, 'fontweight': 'semibold'}, horizontalalignment="center")

    plt.show()

def histogram(release_period_df):
    '''
    Plots a histogram for the distribution of the original release periods of the top 50 podcasts in the US in 2021
    :param release_period_df: Pandas dataframe containing the release periods of the top 50 podcasts
    :return: None
    '''

    '''
    Plot data
    '''
    plt.figure()
    # Plot release period data
    ax = sns.histplot(release_period_df['release_period_length_(yrs)'], color="#6F84FF", kde=False, alpha=0.6,
                        line_kws={'linewidth': 4}, kde_kws={'bw_adjust':0.5, 'bw_method':'silverman'},
                        edgecolor="white", bins=np.arange(0, 40, 2), linewidth=1)
    # Plot median
    plt.axvline(x=release_period_df['release_period_length_(yrs)'].median(axis=0), color="black", alpha=1,
                linewidth=3, linestyle='--')
    ax.text(release_period_df['release_period_length_(yrs)'].median(axis=0), 5, 'Median:\n6.5 yrs',
            fontdict={'fontsize': 11, 'fontweight': 'semibold', },
            horizontalalignment='center', color='black',
            bbox=dict(facecolor='w', edgecolor='#f0f0f0', boxstyle='round,pad=0.5'))

    '''
    Format graph
    '''
    # Format axis
    plt.xlim([0, 40])
    plt.xticks(np.arange(0, 40, 4))
    ax.xaxis.set_minor_locator(MultipleLocator(2))
    ax.yaxis.set_minor_locator(MultipleLocator(1))

    # Add title and label axes
    plt.title('Distribution of the Original Release Periods\nfor the Top 50 Podcasts in the US in 2021', fontsize=16, fontweight='semibold')
    plt.xlabel("Length of Original Release Period (yrs)", fontdict={'fontsize': 12}, horizontalalignment="center")
    plt.ylabel("Frequency", fontdict={'fontsize': 12}, horizontalalignment="center")

    # Add footnotes
    plt.text(0, -0.9,
            '\nData Sources: U.S. Top 50 Podcasts Q1 2021 - Q4 2021 by Edison Research, Spotify Podcasts API; '
            'Note: Length of original release period calculated as of April 1 2022'
            '\nCreated by: Adaora (uploading.substack.com)',
             verticalalignment='top', fontsize=9)


    plt.show()


if __name__ == "__main__":
    # Load data
    pie_chart_df = pd.read_csv('data/processed_publisher_data.csv', index_col=0)
    release_period_df = pd.read_csv('data/podcast_release_periods.csv', index_col=0)

    '''
    Generate pie chart 
    '''
    pie_chart(pie_chart_df)

    '''
    Generate histogram 
    '''
    histogram(release_period_df)
