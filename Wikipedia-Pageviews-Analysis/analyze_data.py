import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

def dailypageviews_graph(daily_data, info_df, movie_results):
    '''
    Plot daily pageviews for the Red Notice Wikipedia article
    :param daily_data: (pandas dataframe) Daily Wikipedia pageviews
    :return:
    '''

    '''
    Plot data
    '''

    # Convert dates to datetime
    info_df['release_dt'] = pd.to_datetime(info_df['release_dt'])
    daily_data.index = pd.to_datetime(daily_data.index)
    movie_results['max_pageviews_dt'] = pd.to_datetime(movie_results['max_pageviews_dt'])
    movie_results['1st_mode_dt'] = pd.to_datetime(movie_results['1st_mode_dt'])

    # Filter for Red Notice data
    graph_df = daily_data.loc[(daily_data.index >= pd.to_datetime('2021-10-01')) &
                              (daily_data.index <= pd.to_datetime('2022-06-01')), 'Red Notice (film)']

    # Plot daily pageviews
    fig, ax = plt.subplots()
    ax.plot(graph_df.index, graph_df.values, color='#C0113D', marker='o', markersize=4, lw=1)

    # Annotate the release date
    ax.axvline(info_df.loc['Red Notice (film)', 'release_dt'], alpha=1,
               color='#000000', linestyle='-', linewidth=1)
    ax.text(pd.to_datetime('2021-11-11'), 8e3, 'Release Date',
            fontdict={'fontsize': 9, 'fontweight': 'semibold', },
            horizontalalignment='left', color='#000000',
            bbox=dict(facecolor='w', edgecolor='#f0f0f0', boxstyle='round,pad=0.5'))

    # Annotate the date with the max # of daily pageviews
    ax.add_artist(Line2D((movie_results.loc['Red Notice (film)', 'max_pageviews_dt'],
                          movie_results.loc['Red Notice (film)', 'max_pageviews_dt']),
                         (259.5e3, 280e3), color='#000000', linewidth=1))
    ax.text(movie_results.loc['Red Notice (film)', 'max_pageviews_dt'], 280e3,
            'Max: '+str(format(int(movie_results.loc['Red Notice (film)', 'max_pageviews']),','))+' daily pageviews'
            '\nTime from Release Date to Max: '+str(movie_results.loc['Red Notice (film)', 'days_to_max_pageviews'])+' days',
            fontdict={'fontsize': 9, 'fontweight': 'semibold', },
            horizontalalignment='left', color='#000000',
            bbox=dict(facecolor='w', edgecolor='#f0f0f0', boxstyle='round,pad=0.5'))

    # Annotate the time from the release date to the reversion date
    ax.axvspan(info_df.loc['Red Notice (film)', 'release_dt'],
               movie_results.loc['Red Notice (film)', '1st_mode_dt'], alpha=0.2,
               color='#c75b77', linestyle='-', linewidth=None)
    ax.text(movie_results.loc['Red Notice (film)', '1st_mode_dt'], 30e3,
            'Time from Release Date\nto Reversion Date: ' + str(movie_results.loc['Red Notice (film)', 'days_to_1st_mode_dt'])+' days',
            fontdict={'fontsize': 9, 'fontweight': 'semibold', },
            horizontalalignment='center', color='#9c324e',
            bbox=dict(facecolor='w', edgecolor='#f0f0f0', boxstyle='round,pad=0.5'))

    '''
    Format graph
    '''
    # Set graph limits
    plt.ylim((0, 3e5))
    plt.xlim((pd.to_datetime('2021-10-01'), pd.to_datetime('2022-06-01')))

    # Set x-axis to date format
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%y'))
    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    plt.gcf().autofmt_xdate()

    # Set y-axis format
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x,p: format(int(x),',')))

    # Set line graph title
    plt.title("Daily Pageviews for Red Notice's Wikipedia Article", fontdict={'fontsize': 16, 'fontweight': 'semibold'},
              horizontalalignment="center", y=1.01)

    # Label axis
    ax.text(pd.to_datetime('02/01/2022'), -4e4, 'Date', fontdict={'fontsize': 11, 'fontweight': 'semibold'}, horizontalalignment="center")
    ax.text(pd.to_datetime('09/11/2021'), 1.5e5, 'Total Daily Pageviews', fontdict={'fontsize': 11, 'fontweight': 'semibold'},
               horizontalalignment="center", rotation='vertical', verticalalignment='center')

    # Add bar chart footnotes
    ax.text(pd.to_datetime('10/01/2021'), -7.5e4,
            '$\\bf{Reversion\;Date:}$'' Defined as the day when daily pageviews have reverted back to "normal" levels following a spike.'
            " Mathematically this is defined as the 1st day after the date\nwith the max # of daily pageviews, where total daily pageviews "
            "= the mode of daily pageviews in the 1st year after the film's release date"
            '\n\nData Source: Wikipedia; Created by: Nkemjika (uploading.substack.com)',
            fontdict={'fontsize': 8, 'fontweight': 'normal', 'color': '#848484'})

    plt.show()

def maxpageviews_graph(summary_df):
    '''
    Given data for the maximum, average and minimum values for films' maximum number of daily pageviews,
    across netflix and theatrical releases, plot the data on a bar graph
    :param summary_df: (pandas dataframe) contains the max data that will be plotted
    :return:
    '''
    '''
    Plot Bar Graph
    '''
    # Initialize variable for indexing multiindex dataframes
    idx = pd.IndexSlice

    # Create lists for various inputs that are needed to extract data and generate graphs
    summary_datapts = ['min','average', 'max']
    categories = ['streaming', '2019 theatrical', '2022 theatrical']
    colours = ['#e62c35', '#3256a8', '#32a867']

    # Create 3 subplots for each subset of data
    fig, ax = plt.subplots(1, 3)

    # Set bar width
    width = 0.35

    # Set y-axis units
    yunits = 1e6

    # Iterate through subplots and plot each bar chart
    for i in range(3):

        # Plot each bar individually
        for j in range(3):
            # Get the value to plot
            value = summary_df.loc[idx[categories[i], summary_datapts[j]], 'max_pageviews']

            # Preset the data label height
            if value/yunits < 0.15:
                datalabel_height = value + 0.04*yunits
            else:
                datalabel_height = 0.95/2*value

            # Plot the bar
            ax[i].bar(j, value, width=width, color=colours[i], edgecolor='#FFFFFF')
            # Label bar
            ax[i].text(j, datalabel_height, readable_format(num=value, magnitude=2, prec=2),
                        horizontalalignment="center", fontdict={'fontsize': 9, 'fontweight': 'semibold',
                        'color': colours[i]}, bbox=dict(facecolor='w', edgecolor=colours[i], boxstyle='round, pad=0.25'))

            # Add annotations with film names
            if summary_datapts[j] == 'max':
                # Get a list of film names
                film_names = summary_df.loc[idx[categories[i], 'max_movie'], 'max_pageviews'].strip(']')\
                                                                    .strip('[').replace("'", "").replace(',',',\n')\
                                                                    .replace('Doctor Strange in the', 'Doctor Strange\nin the') \
                                                                    .replace(' (film)', '')
                # Annotate max bar with film names
                ax[i].text(j, value + 0.2*yunits,
                            'Film:\n' + film_names, horizontalalignment="center",
                            fontdict={'fontsize': 8, 'fontweight': 'semibold', 'color': '#848484'},
                            bbox=dict(facecolor='#FFFFFF', edgecolor='#9D9D9D', boxstyle='round, pad=0.25'))
                # Add annotation line
                ax[i].add_artist(Line2D((j, j), (value, value + 0.2*yunits), color='#9D9D9D', linewidth=1))

            elif summary_datapts[j] == 'min':
                # Get a list of film names
                film_names = summary_df.loc[idx[categories[i], 'min_movie'], 'max_pageviews'].strip(']')\
                                                                    .strip('[').replace("'", "").replace(',',',\n')\
                                                                    .replace(' (film)', '').replace(' (2022 film)', '')
                # Annotate min bar with film names
                ax[i].text(j, value + 0.2*yunits,
                            'Film:\n' + film_names, horizontalalignment="center",
                            fontdict={'fontsize': 8, 'fontweight': 'demibold', 'color': '#848484'},
                            bbox=dict(facecolor='#FFFFFF', edgecolor='#9D9D9D', boxstyle='round, pad=0.25'))
                # Add annotation line
                ax[i].add_artist(Line2D((j, j), (value, value + 0.2*yunits), color='#9D9D9D', linewidth=1))

        # Set x-axis labels
        ax[i].set_xticks(np.arange(3))
        ax[i].set_xticklabels(['Minimum', 'Average', 'Maximum'], fontdict={'fontsize': 10, 'fontweight': 'semibold'},
                              color='black')
        ax[i].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True)

        # Set y-axis limits
        overall_ymax = summary_df.loc[idx[:, 'max'], 'max_pageviews'].max()
        overall_ymax = (np.ceil(overall_ymax/yunits)+0.5)*yunits
        ax[i].set_ylim(0, overall_ymax)

        # Remove frame
        ax[i].set_frame_on(False)

        # Remove y-axis
        ax[i].axes.get_yaxis().set_visible(False)

        # Redraw x-axis line
        xmin, xmax = ax[i].get_xaxis().get_view_interval()
        ax[i].add_artist(Line2D((xmin, xmax), (0, 0), color='black', linewidth=1.5))

    # Set bar chart title
    ax[1].text(1, overall_ymax*1.05, "Maximum Number of Daily Pageviews\n""$\\bf{for\;a\;Film’s\;Wikipedia\;Article^1}$",
              fontdict={'fontsize': 16, 'fontweight': 'semibold'},
              horizontalalignment="center")

    # Set bar chart subtitles
    ax[0].text(1, overall_ymax*0.95, 'Top 10 Most Popular English\nNetflix Films (All Time)', fontdict={'fontsize': 14, 'fontweight': 'semibold'},
               horizontalalignment="center", color=colours[0])
    ax[1].text(1, overall_ymax*0.95, "2019 Top 10 Grossing Films\n (US Domestic Box Office)",
               fontdict={'fontsize': 14, 'fontweight': 'semibold'},
               horizontalalignment="center", color=colours[1])
    ax[2].text(1, overall_ymax*0.95, "2022 YTD Top 10 Grossing Films\n (US Domestic Box Office)",
               fontdict={'fontsize': 14, 'fontweight': 'semibold'},
               horizontalalignment="center", color=colours[2])

    # Add x-axis subtitles
    ax[0].text(1, -1.5e5, '(of Top 10 Netflix Films)', horizontalalignment='center', fontdict={'fontsize': 10, 'fontweight': 'semibold'},
               color=colours[0])
    ax[1].text(1, -1.5e5, '(of Top 10 2019 Theatrical Films)', horizontalalignment='center',
               fontdict={'fontsize': 10, 'fontweight': 'semibold'},
               color=colours[1])
    ax[2].text(1, -1.5e5, '(of Top 10 2022 YTD Theatrical Films)', horizontalalignment='center',
               fontdict={'fontsize': 10, 'fontweight': 'semibold'},
               color=colours[2])

    # Add bar chart footnotes
    ax[0].text(-0.3, -3.25e5, "$^1$""Maximum number of daily Wikipedia article pageviews following each film's release date, as of 11/30/22;\n"
                            'Top 10 most popular Netflix films by total hours viewed in first 28 days as of 11/30/22; '
                            '2022 YTD top 10 grossing films (in-year releases) by US domestic box office as of 11/30/22;'
                            '\nData Sources: Wikipedia, Netflix, Box Office Mojo; Analysis by: Nkemjika at uploading.substack.com',
                            fontdict={'fontsize': 8, 'fontweight': 'normal', 'color': '#848484'})

    plt.show()

def daystomax_graph(summary_df):
    '''
    Given data for the maximum, average and minimum numbers of days between a film's release date
    and its maximum number of daily pageviews, across netflix and theatrical releases, plot the data on a bar graph
    :param summary_df: (pandas dataframe) contains the days to max data that will be plotted
    :return:
    '''

    '''
    Plot Bar Graph
    '''
    # Initialize variable for indexing multiindex dataframes
    idx = pd.IndexSlice

    # Create lists for various inputs that are needed to extract data and generate graphs
    summary_datapts = ['min', 'average', 'max']
    categories = ['streaming', '2019 theatrical', '2022 theatrical']
    colours = ['#e62c35', '#3256a8', '#32a867']
    annotation_heights = [14, 0, 4, 8, 0, 3, 19, 0, 6]

    # Create 3 subplots for each subset of data
    fig, ax = plt.subplots(1, 3)

    # Set bar width
    width = 0.35

    # Iterate through subplots and plot each bar chart
    for i in range(3):

        # Plot each bar individually
        for j in range(3):
            # Get the value to plot
            value = summary_df.loc[idx[categories[i], summary_datapts[j]], 'days_to_max_pageviews']

            # Preset the data label height
            if value < 4:
                datalabel_height = value + 1
            else:
                datalabel_height = 0.95 / 2 * value

            # Plot bar
            ax[i].bar(j, value, width=width, color=colours[i], edgecolor='#FFFFFF')

            # Create data label
            if value == 1:
                datalabel = str(int(value)) + str(' day')
            else:
                if summary_datapts[j] != 'average':
                    datalabel = str(int(value)) + str(' days')
                else:
                    datalabel = str(round(value, 1)) + str(' days')

            # Label bar
            ax[i].text(j, datalabel_height, datalabel,
                       horizontalalignment="center", fontdict={'fontsize': 9, 'fontweight': 'semibold',
                                                               'color': colours[i]},
                       bbox=dict(facecolor='w', edgecolor=colours[i], boxstyle='round, pad=0.25'))

            # Add annotations with film names
            if summary_datapts[j] == 'max':
                # Get a list of film names
                film_names = summary_df.loc[idx[categories[i], 'max_movie'], 'days_to_max_pageviews'].strip(']') \
                    .strip('[').replace("'", "").replace(',', ',\n') \
                    .replace(' (film)', '').replace(' (2022 film)', '')
                # Annotate max bar with film names
                ax[i].text(j, value + annotation_heights[i*3 + j],
                           'Film(s):\n' + film_names, horizontalalignment="center",
                           fontdict={'fontsize': 8, 'fontweight': 'semibold', 'color': '#848484'},
                           bbox=dict(facecolor='#FFFFFF', edgecolor='#9D9D9D', boxstyle='round, pad=0.25'))
                # Add annotation line
                ax[i].add_artist(Line2D((j, j), (value, value + annotation_heights[i*3 + j]), color='#9D9D9D', linewidth=1))

            elif summary_datapts[j] == 'min':
                # Get a list of film names
                film_names = summary_df.loc[idx[categories[i], 'min_movie'], 'days_to_max_pageviews'].strip(']') \
                    .strip('[').replace("'", "").replace(',', ',\n') \
                    .replace('(film)', '').replace('Doctor Strange in the', 'Doctor Strange\nin the') \
                # Annotate min bar with  film names
                ax[i].text(j, value + annotation_heights[i*3 + j],
                           'Film(s):\n' + film_names, horizontalalignment="center",
                           fontdict={'fontsize': 8, 'fontweight': 'demibold', 'color': '#848484'},
                           bbox=dict(facecolor='#FFFFFF', edgecolor='#9D9D9D', boxstyle='round, pad=0.25'))
                # Add annotation line
                ax[i].add_artist(Line2D((j, j), (value, value + annotation_heights[i*3 + j]), color='#9D9D9D', linewidth=1))

        # Set x-axis labels
        ax[i].set_xticks(np.arange(3))
        ax[i].set_xticklabels(['Minimum', 'Average', 'Maximum'],
                              fontdict={'fontsize': 10, 'fontweight': 'semibold'},
                              color='black')
        ax[i].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True)

        # Set y-axis limits
        overall_ymax = summary_df.loc[idx[:, 'max'], 'days_to_max_pageviews'].max()
        overall_ymax = (np.ceil(overall_ymax) + 20)
        ax[i].set_ylim(0, overall_ymax)

        # Remove frame
        ax[i].set_frame_on(False)

        # Remove y-axis
        ax[i].axes.get_yaxis().set_visible(False)

        # Redraw x-axis line
        xmin, xmax = ax[i].get_xaxis().get_view_interval()
        ax[i].add_artist(Line2D((xmin, xmax), (0, 0), color='black', linewidth=1.5))

    # Set bar chart title
    ax[1].text(1, overall_ymax * 1.05,
               "Days between a Film's Release Date &\nMaximum Number of Daily Pageviews ""$\\bf{for\;a\;Film’s\;Wikipedia\;Article^1}$",
               fontdict={'fontsize': 16, 'fontweight': 'semibold'},
               horizontalalignment="center")

    # Set bar chart subtitles
    ax[0].text(1, overall_ymax * 0.95, 'Top 10 Most Popular English\nNetflix Films (All Time)',
               fontdict={'fontsize': 14, 'fontweight': 'semibold'},
               horizontalalignment="center", color=colours[0])
    ax[1].text(1, overall_ymax * 0.95, "2019 Top 10 Grossing Films\n (US Domestic Box Office)",
               fontdict={'fontsize': 14, 'fontweight': 'semibold'},
               horizontalalignment="center", color=colours[1])
    ax[2].text(1, overall_ymax * 0.95, "2022 YTD Top 10 Grossing Films\n (US Domestic Box Office)",
               fontdict={'fontsize': 14, 'fontweight': 'semibold'},
               horizontalalignment="center", color=colours[2])

    # Add x-axis subtitles
    ax[0].text(1, -6, '(of Top 10 Netflix Films)', horizontalalignment='center',
               fontdict={'fontsize': 10, 'fontweight': 'semibold'},
               color=colours[0])
    ax[1].text(1, -6, '(of Top 10 2019 Theatrical Films)', horizontalalignment='center',
               fontdict={'fontsize': 10, 'fontweight': 'semibold'},
               color=colours[1])
    ax[2].text(1, -6, '(of Top 10 2022 YTD Theatrical Films)', horizontalalignment='center',
               fontdict={'fontsize': 10, 'fontweight': 'semibold'},
               color=colours[2])

    # Add bar chart footnotes
    ax[0].text(-0.3, -12.5,
               "$^1$""Maximum number of daily Wikipedia article pageviews following each film's release date, as of 11/30/22;\n"
               'Top 10 most popular Netflix films by total hours viewed in first 28 days as of 11/30/22; '
               '2022 YTD top 10 grossing films (in-year releases) by US domestic box office as of 11/30/22;'
               '\nData Sources: Wikipedia, Netflix, Box Office Mojo; Analysis by: Nkemjika at uploading.substack.com',
               fontdict={'fontsize': 8, 'fontweight': 'normal', 'color': '#848484'})

    plt.show()

def reversiontime_graph(summary_df):
    '''
    Given data for the maximum, average and minimum numbers of days between a film's release date
    and its reversion date, for netflix and theatrical releases, plot the data on a bar graph
    :param summary_df: (pandas dataframe) contains the reversion data that will be plotted
    :return:
    '''

    '''
    Plot Bar Graph
    '''
    # Initialize variable for indexing multiindex dataframes
    idx = pd.IndexSlice

    # Create lists for various inputs that are needed to extract data and generate graphs
    summary_datapts = ['min', 'average', 'max']
    categories = ['streaming', '2019 theatrical']
    colours = ['#e62c35', '#3256a8']

    # Create 3 subplots for each subset of data
    fig, ax = plt.subplots(1, 2)

    # Set bar width
    width = 0.2

    # Iterate through subplots and plot each bar chart
    for i in range(2):

        # Plot each bar individually
        for j in range(3):
            # Get the value to plot
            value = summary_df.loc[idx[categories[i], summary_datapts[j]], 'days_to_1st_mode_dt']

            # Preset the data label height
            if value < 4:
                datalabel_height = value + 1
            else:
                datalabel_height = 0.95 / 2 * value

            # Plot bar
            ax[i].bar(j, value, width=width, color=colours[i], edgecolor='#FFFFFF')

            # Create data label
            if value == 1:
                datalabel = str(int(value)) + str(' day')
            else:
                datalabel = str(int(value)) + str(' days')

            # Label bar
            ax[i].text(j, datalabel_height, datalabel,
                       horizontalalignment="center", fontdict={'fontsize': 9, 'fontweight': 'semibold',
                                                               'color': colours[i]},
                       bbox=dict(facecolor='w', edgecolor=colours[i], boxstyle='round, pad=0.25'))

            # Add annotations with film names
            if summary_datapts[j] == 'max':
                # Get a list of film names
                film_names = summary_df.loc[idx[categories[i], 'max_movie'], 'days_to_1st_mode_dt'].strip(']') \
                    .strip('[').replace("'", "").replace(',', ',\n') \
                    .replace(' (film)', '').replace(' (2022 film)', '')
                # Annotate max bar with film names
                ax[i].text(j, value + 6,
                           'Film:\n' + film_names, horizontalalignment="center",
                           fontdict={'fontsize': 8, 'fontweight': 'semibold', 'color': '#848484'},
                           bbox=dict(facecolor='#FFFFFF', edgecolor='#9D9D9D', boxstyle='round, pad=0.25'))
                # Add annotation line
                ax[i].add_artist(Line2D((j, j), (value, value + 6), color='#9D9D9D', linewidth=1))
            elif summary_datapts[j] == 'min':
                # Get a list of film names
                film_names = summary_df.loc[idx[categories[i], 'min_movie'], 'days_to_1st_mode_dt'].strip(']') \
                    .strip('[').replace("'", "").replace(',', ',\n') \
                    .replace('(film)', '').replace(' (2022 film)', '')\
                    .replace('Panther: Wakanda', 'Panther:\nWakanda').replace('Spider-Man: Far', 'Spider-Man:\nFar')
                # Annotate min bar with film names
                ax[i].text(j, value + 6,
                           'Film:\n' + film_names, horizontalalignment="center",
                           fontdict={'fontsize': 8, 'fontweight': 'demibold', 'color': '#848484'},
                           bbox=dict(facecolor='#FFFFFF', edgecolor='#9D9D9D', boxstyle='round, pad=0.25'))
                # Add annotation line
                ax[i].add_artist(Line2D((j, j), (value, value + 6), color='#9D9D9D', linewidth=1))

        # Set x-axis labels
        ax[i].set_xticks(np.arange(3))
        ax[i].set_xticklabels(['Minimum', 'Average', 'Maximum'],
                              fontdict={'fontsize': 10, 'fontweight': 'semibold'},
                              color='black')
        ax[i].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True)

        # Set y-axis limits
        overall_ymax = summary_df.loc[idx[:, 'max'], 'days_to_1st_mode_dt'].max()
        overall_ymax = (np.ceil(overall_ymax) + 50)
        ax[i].set_ylim(0, overall_ymax)

        # Remove frame
        ax[i].set_frame_on(False)

        # Remove y-axis
        ax[i].axes.get_yaxis().set_visible(False)

        # Redraw x-axis line
        xmin, xmax = ax[i].get_xaxis().get_view_interval()
        ax[i].add_artist(Line2D((xmin, xmax), (0, 0), color='black', linewidth=1.5))

    # Set bar chart title
    ax[0].text(2.5, overall_ymax * 1.05,
               "Days between a Film's Release Date &\nDaily Pageviews Reversion Date for a Film's Wikipedia Article",
               fontdict={'fontsize': 16, 'fontweight': 'semibold'},
               horizontalalignment="center")

    # Set bar chart subtitles
    ax[0].text(1, overall_ymax * 0.95, 'Top 10 Most Popular English\nNetflix Films (All Time)',
               fontdict={'fontsize': 14, 'fontweight': 'semibold'},
               horizontalalignment="center", color=colours[0])
    ax[1].text(1, overall_ymax * 0.95, "2019 Top 10 Grossing Films\n (US Domestic Box Office)",
               fontdict={'fontsize': 14, 'fontweight': 'semibold'},
               horizontalalignment="center", color=colours[1])

    # Add x-axis subtitles
    ax[0].text(1, -20, '(of Top 10 Netflix Films)', horizontalalignment='center',
               fontdict={'fontsize': 10, 'fontweight': 'semibold'},
               color=colours[0])
    ax[1].text(1, -20, '(of Top 10 2019 Theatrical Films)', horizontalalignment='center',
               fontdict={'fontsize': 10, 'fontweight': 'semibold'},
               color=colours[1])

    # Add bar chart footnotes
    ax[0].text(-0.25, -45,
                '$\\bf{Reversion\;Date:}$'' Defined as the day when daily pageviews have reverted back to "normal" levels following a spike.'
                " Mathematically this is defined as the 1st day after the date with the max #\nof daily pageviews, where total daily pageviews "
                "= the mode of daily pageviews in the 1st year after the film's release date."
                ' Top 10 most popular Netflix films by total hours viewed in first\n28 days as of 11/30/22; '
                'Data Sources: Wikipedia, Netflix, Box Office Mojo; Analysis by: Nkemjika at uploading.substack.com',
                fontdict={'fontsize': 8, 'fontweight': 'normal', 'color': '#848484'})

    plt.show()

def readable_format(num, magnitude, prec):
    '''
    Take in a number (num) and convert it to a string representation of the number,
    where the output is num/10^(3*magnitude) rounded to (prec) decimal points
    :param num: (float) number that will be formatted
    :param magnitude: (int) number representing the magnitude of the output
    :param prec: (int) number of decimal points in the output
    :return:
    '''
    # Convert num to 10^(3*magnitude) units
    form_num = num / 10 ** (3*magnitude)
    # Convert num to readable string form
    return '{}{}'.format('{:.{prec}f}'.format(form_num, prec=prec), ['', 'K', 'M'][magnitude])

if __name__ == "__main__":
    # Load data
    summary_df = pd.read_csv('data/processed_summarized_data.csv', index_col=[0,1])
    info_df = pd.read_csv('data/release_dates_v2.csv', index_col=0)
    daily_data = pd.read_csv('data/netflix top 10 films - daily wikipedia pageviews.csv', index_col=0)
    movie_results = pd.read_csv('data/processed_movie_data.csv', index_col=0)

    # Convert numeric entries in dataframe to floats
    summary_df.loc[pd.IndexSlice[:, ['max','min','average']], :] \
                                            = summary_df.loc[pd.IndexSlice[:, ['max','min','average']], :].astype(float)

    # Generate a graph of Red Notice daily pageviews over time
    dailypageviews_graph(daily_data, info_df, movie_results)

    # Generate max pageviews bar graph
    maxpageviews_graph(summary_df)

    # Generate days to max bar graph
    daystomax_graph(summary_df)

    # Generate reversion time bar graph
    reversiontime_graph(summary_df)