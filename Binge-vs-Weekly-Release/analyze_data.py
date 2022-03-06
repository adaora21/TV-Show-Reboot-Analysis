import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

def disney_graph(dis_df, release_df):
    '''
    Plot a graph of Google Trends interest in Disney+ shows
    :param dis_df: Pandas dataframe containing tv show interest data
    :param release_df: Pandas dataframe containing tv show release dates
    :return: None
    '''
    # Convert the index to datetime
    dis_df.index = pd.to_datetime(dis_df.index)

    # Plot data
    fig, ax = plt.subplots()
    ax.plot(dis_df.index, dis_df.loc[:, 'The Mandalorian: (Worldwide)'], label='The Mandalorian', color='#4b7feb',
            linewidth=1.5)
    ax.axvspan(release_df.loc['s1_premiere', 'The Mandalorian'], release_df.loc['s1_finale', 'The Mandalorian'],
               alpha=0.25,color='#4b7feb', linestyle='-', linewidth=None)
    ax.text(pd.to_datetime('12/01/19'), 90, 'Season 1', fontdict={'fontsize': 11, 'fontweight': 'semibold', },
            horizontalalignment='center', color='#09255e', bbox=dict(facecolor='w', edgecolor='#f0f0f0', boxstyle='round,pad=0.5'))
    ax.axvspan(release_df.loc['s2_premiere', 'The Mandalorian'], release_df.loc['s2_finale', 'The Mandalorian'],
               alpha=0.25,color='#4b7feb', linestyle='-', linewidth=None)
    ax.text(pd.to_datetime('11/18/20'), 90, 'Season 2', fontdict={'fontsize': 11, 'fontweight': 'semibold', },
            horizontalalignment='center', color='#09255e', bbox=dict(facecolor='w', edgecolor='#f0f0f0', boxstyle='round,pad=0.5'))

    ax.plot(dis_df.index, dis_df.loc[:, 'WandaVision: (Worldwide)'], label='WandaVision', color='#ed2832',
            linewidth=1.5)
    ax.axvspan(release_df.loc['s1_premiere', 'WandaVision'], release_df.loc['s1_finale', 'WandaVision'],
               alpha=0.2, color='#ed2832', linestyle='-', linewidth=None)
    ax.text(pd.to_datetime('02/04/21'), 90, 'Season 1', fontdict={'fontsize': 11, 'fontweight':'semibold',},
            horizontalalignment='center', color='#ed2832', bbox=dict(facecolor='w', edgecolor='#f0f0f0', boxstyle='round,pad=0.5'))

    ax.plot(dis_df.index, dis_df.loc[:, 'The Falcon and the Winter Soldier: (Worldwide)'],
            label='The Falcon and the Winter Soldier', color='#949494', linewidth=1.5)
    ax.axvspan(release_df.loc['s1_premiere', 'The Falcon and the Winter Soldier'],
               release_df.loc['s1_finale', 'The Falcon and the Winter Soldier'], alpha=0.25,color='#949494')
    ax.text(pd.to_datetime('04/01/21'), 49, 'Season 1', fontdict={'fontsize': 11, 'fontweight': 'semibold', },
            horizontalalignment='center', color='#363636', bbox=dict(facecolor='w', edgecolor='#f0f0f0', boxstyle='round,pad=0.5'))

    ax.plot(dis_df.index, dis_df.loc[:, 'Loki: (Worldwide)'], label='Loki', color='#61b858', linewidth=1.5)
    ax.axvspan(release_df.loc['s1_premiere', 'Loki'], release_df.loc['s1_finale', 'Loki'], alpha=0.25,
               color='#61b858')
    ax.text(pd.to_datetime('06/22/21'), 49, 'Season 1', fontdict={'fontsize': 11, 'fontweight': 'semibold', },
            horizontalalignment='center', color='#265421',
            bbox=dict(facecolor='w', edgecolor='#f0f0f0', boxstyle='round,pad=0.5'))

    ax.plot(dis_df.index, dis_df.loc[:, 'Hawkeye: (Worldwide)'],
            label='Hawkeye', color='#7373bf', linewidth=1.5)
    ax.axvspan(release_df.loc['s1_premiere', 'Hawkeye'],
               release_df.loc['s1_finale', 'Hawkeye'], alpha=0.25, color='#7373bf')
    ax.text(pd.to_datetime('12/04/21'), 49, 'Season 1', fontdict={'fontsize': 11, 'fontweight': 'semibold', },
            horizontalalignment='center', color='#414169',
            bbox=dict(facecolor='w', edgecolor='#f0f0f0', boxstyle='round,pad=0.5'))

    ax.plot(dis_df.index, dis_df.loc[:, 'The Book of Boba Fett: (Worldwide)'],
            label='The Book of Boba Fett', color='#ff4f0a', linewidth=1.5)
    ax.axvspan(release_df.loc['s1_premiere', 'The Book of Boba Fett'],
               release_df.loc['s1_finale', 'The Book of Boba Fett'], alpha=0.25, color='#ff4f0a')
    ax.text(pd.to_datetime('01/13/22'), 60, 'Season 1', fontdict={'fontsize': 11, 'fontweight': 'semibold'},
            horizontalalignment='center', color='#a33307',
            bbox=dict(facecolor='w', edgecolor='#f0f0f0', boxstyle='round,pad=0.5'))
    '''
    Format graph
    '''

    # Set x axis to date format
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.gca().xaxis.set_minor_locator(mdates.MonthLocator(interval=1))
    plt.gcf().autofmt_xdate()

    # Set graph limits
    plt.ylim((0, 100))
    plt.xlim((dis_df.index.tolist()[0], dis_df.index.tolist()[-1]))

    # Create legend
    plt.legend(loc='center left', fontsize=12, title='$\\bf{Search\;Topic}$', bbox_to_anchor=(0.1075, 0.825), title_fontsize=12)

    # Label axis
    plt.xlabel('Month', fontdict={'fontsize': 13}, horizontalalignment="center")
    plt.ylabel('Search Interest', fontdict={'fontsize': 13}, horizontalalignment="center")

    # Set line graph title
    plt.title('Worldwide Interest in Disney+ Originals', fontdict={'fontsize': 16, 'fontweight': 'semibold'},
              horizontalalignment="center", y=1.01)

    # Add bar chart footnotes
    ax.text(pd.to_datetime('10/05/2019'), -17, 'Data Source: Google Trends\nCreated by: Adaora (uploading.substack.com)',
            fontdict={'fontsize': 9, 'fontweight': 'normal'})

    plt.show()

def netflix_graph(nflx_df, release_df):
    '''
    Plot a graph of Google Trends interest in Netflix shows
    :param nflx_df: Pandas dataframe containing tv show interest data
    :param release_df: Pandas dataframe containing tv show release dates
    :return: None
    '''
    # Convert the index to datetime
    nflx_df.index = pd.to_datetime(nflx_df.index)

    # Graph parameters
    txt_bx_fontsize = 9

    # Plot data
    fig, ax = plt.subplots()
    ax.plot(nflx_df.index, nflx_df.loc[:, 'Too Hot to Handle: (Worldwide)'], label='Too Hot to Handle', color='#e83c70',
            linewidth=2.5, zorder=3)
    ax.axvspan(release_df.loc['s1_premiere', 'Too Hot to Handle'], release_df.loc['s1_finale', 'Too Hot to Handle'],
               alpha=0.5, color='#e83c70', linestyle='-', linewidth=2, zorder=4)
    ax.text(pd.to_datetime('03/26/20'), 17.5, 'Season 1\nRelease Day', fontdict={'fontsize': txt_bx_fontsize, 'fontweight': 'semibold', },
            horizontalalignment='center', color='#8a062d', bbox=dict(facecolor='w', edgecolor='#f0f0f0', boxstyle='round,pad=0.5'),
            zorder=5)
    ax.axvspan(release_df.loc['s1_special_1', 'Too Hot to Handle'], release_df.loc['s1_special_1', 'Too Hot to Handle'],
               alpha=0.5, color='#e83c70', linestyle='-', linewidth=2, zorder=4)
    ax.text(pd.to_datetime('05/29/20'), 30, 'Season 1\nBonus Episode\nRelease Day', fontdict={'fontsize': txt_bx_fontsize, 'fontweight': 'semibold', },
            horizontalalignment='center', color='#8a062d', bbox=dict(facecolor='w', edgecolor='#f0f0f0', boxstyle='round,pad=0.5'),
            zorder=5)
    ax.axvspan(release_df.loc['s2_premiere', 'Too Hot to Handle'], release_df.loc['s2_finale', 'Too Hot to Handle'],
               alpha=0.25, color='#e83c70', linestyle='-', linewidth=None, zorder=1)
    ax.text(pd.to_datetime('05/27/21'), 80, 'Season 2\n(Weekly Release)',
            fontdict={'fontsize': txt_bx_fontsize, 'fontweight': 'semibold', },
            horizontalalignment='center', color='#8a062d',
            bbox=dict(facecolor='w', edgecolor='#f0f0f0', boxstyle='round,pad=0.5'), zorder=5)
    ax.axvspan(release_df.loc['s3_premiere', 'Too Hot to Handle'], release_df.loc['s3_finale', 'Too Hot to Handle'],
               alpha=0.5, color='#e83c70', linestyle='-', linewidth=2, zorder=4)
    ax.text(pd.to_datetime('01/01/22'), 90, 'Season 3\nRelease Day',
            fontdict={'fontsize': txt_bx_fontsize, 'fontweight': 'semibold', },
            horizontalalignment='center', color='#ab0234',
            bbox=dict(facecolor='w', edgecolor='#f0f0f0', boxstyle='round,pad=0.5'), zorder=5)

    ax.plot(nflx_df.index, nflx_df.loc[:, 'Love Is Blind: (Worldwide)'], label='Love Is Blind', color='#8a34bf',
            linewidth=2.5, zorder=2)
    ax.axvspan(release_df.loc['s1_premiere', 'Love Is Blind'], release_df.loc['s1_finale', 'Love Is Blind'],
               alpha=0.25, color='#8a34bf', linestyle='-', linewidth=None, zorder=1)
    ax.text(pd.to_datetime('02/23/20'), 80, 'Season 1\n(Weekly Release)', fontdict={'fontsize': txt_bx_fontsize, 'fontweight': 'semibold', },
            horizontalalignment='center', color='#340561', bbox=dict(facecolor='w', edgecolor='#f0f0f0', boxstyle='round,pad=0.5'),
            zorder=4)
    ax.axvspan(release_df.loc['s1_special_1', 'Love Is Blind'], release_df.loc['s1_special_1', 'Love Is Blind'],
               alpha=0.5, color='#8a34bf', linestyle='-', linewidth=2, zorder=4)
    ax.text(pd.to_datetime('08/24/21'), 30, 'Season 1\nBonus Episodes\nRelease Day',
            fontdict={'fontsize': txt_bx_fontsize, 'fontweight': 'semibold', },
            horizontalalignment='center', color='#340561',
            bbox=dict(facecolor='w', edgecolor='#f0f0f0', boxstyle='round,pad=0.5'), zorder=5)

    '''
    Format graph
    '''

    # Set x axis to date format
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.gca().xaxis.set_minor_locator(mdates.MonthLocator(interval=1))
    plt.gcf().autofmt_xdate()

    # Set graph limits
    plt.ylim((0, 100))
    plt.xlim((nflx_df.index.tolist()[0], nflx_df.index.tolist()[-1]))

    # Create legend
    plt.legend(loc='best', fontsize=12, title='$\\bf{Search\;Topic}$', title_fontsize=12)

    # Label axis
    plt.xlabel('Month', fontdict={'fontsize': 13}, horizontalalignment="center")
    plt.ylabel('Search Interest', fontdict={'fontsize': 13}, horizontalalignment="center")

    # Set line graph title
    plt.title('Worldwide Interest in Netflix Reality TV Shows', fontdict={'fontsize': 16, 'fontweight': 'semibold'},
              horizontalalignment="center", y=1.01)

    # Add bar chart footnotes
    ax.text(pd.to_datetime('01/01/2020'), -17, 'Data Source: Google Trends\nCreated by: Adaora (uploading.substack.com)',
            fontdict={'fontsize': 9, 'fontweight': 'normal'})

    plt.show()

def aos_graph(aos_df, release_df):
    '''
    Plot a graph of Google Trends Interest for Agents of S.H.I.E.L.D.
    :param aos_df: Pandas dataframe containing tv show interest data
    :param release_df: Pandas dataframe containing tv show release dates
    :return: None
    '''
    # Convert the index to datetime
    aos_df.index = pd.to_datetime(aos_df.index)

    # Plot data
    fig, ax = plt.subplots()
    ax.plot(aos_df.index, aos_df.loc[:, 'Agents of S.H.I.E.L.D.: (Worldwide)'], label='Agents of S.H.I.E.L.D.', color='#0f4b95',
            linewidth=2.5)
    ax.axvspan(release_df.loc['s1_premiere', 'Agents of S.H.I.E.L.D.'], release_df.loc['s1_finale', 'Agents of S.H.I.E.L.D.'],
               alpha=0.25,color='#0f4b95', linestyle='-', linewidth=None)
    ax.text(pd.to_datetime('04/24/14'), 95, 'Season 1', fontdict={'fontsize': 11, 'fontweight': 'semibold', },
            horizontalalignment='center', color='#0f4b95', bbox=dict(facecolor='w', edgecolor='#f0f0f0', boxstyle='round,pad=0.5'))

    '''
    Format graph
    '''

    # Set x axis to date format
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    plt.gcf().autofmt_xdate()

    # Set graph limits
    plt.ylim((0,100))
    plt.xlim((aos_df.index.tolist()[0], aos_df.index.tolist()[-1]))

    # Label axis
    plt.xlabel('Month', fontdict={'fontsize': 13}, horizontalalignment="center")
    plt.ylabel('Search Interest', fontdict={'fontsize': 13}, horizontalalignment="center")

    # Set line graph title
    plt.title('Worldwide Interest in the Agents of S.H.I.E.L.D. Search Topic',
              fontdict={'fontsize': 16, 'fontweight': 'semibold'}, horizontalalignment="center", y=1.01)

    # Add bar chart footnotes
    ax.text(pd.to_datetime('08/04/2013'), -17, 'Data Source: Google Trends\nCreated by: Adaora (uploading.substack.com)',
            fontdict={'fontsize': 9, 'fontweight': 'normal'})

    plt.show()

if __name__ == "__main__":
    # Load release dates
    release_df = pd.read_csv('data/processed_weekly_release_dates.csv', index_col=0)

    '''
    Plot Netflix Graph
    '''
    # Load data
    nflx_shows_df = pd.read_csv('data/processed_netflix_shows.csv', index_col=0)
    # Plot data
    netflix_graph(nflx_shows_df, release_df)

    '''
    Plot Disney+ Graph
    '''
    # Load data
    dis_df = pd.read_csv('data/processed_disneyplus_shows.csv', index_col=0)
    # Plot data
    disney_graph(dis_df, release_df)

    '''
    Plot Agents of Shield Graph
    '''
    # Load data
    aos_df = pd.read_csv('data/processed_agentsofshield.csv', index_col=0)
    # Plot data
    aos_graph(aos_df, release_df)