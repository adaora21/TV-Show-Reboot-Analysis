import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter
from scipy import stats
import seaborn as sns

def round_int_or_zero(x):
    '''
    Round the float input (x) to an integer if it's > 100, 1 decimal point if it's between 10 and 100
    and 2 decimal points if it's below 10
    :param x: float
    :return: integer or float
    '''
    if x >= 100:
        return int(x)
    elif x >= 10 and x < 100:
        return round(x,1)
    else:
        return round(x,2)


def density_scatter_plot_insta(df):
    '''
    Plot Instagram data points in a scatter plot, colouring the data points based on density
    :param df: (pandas dataframe) Contains personal account and brand account follower data for Instagram
    :return: None
    '''

    # Load data
    x = df.iloc[:, 2]
    y = df.iloc[:, 3]

    # Calculate the point density
    xy = np.vstack([x, y])
    z = gaussian_kde(xy)(xy)

    # Sort the points by density, so that the densest points are plotted last
    idx = z.argsort()
    x, y, z = x[idx], y[idx], z[idx]

    fig, ax = plt.subplots()

    # Plot data points, coloured based on density
    ax.scatter(x, y, c=z, s=50, cmap=sns.color_palette("Spectral", as_cmap=True), edgecolor=None)

    '''
    Format graph
    '''

    # Customize x and y ticks
    plt.xticks(np.arange(0, 475, 25))
    plt.yticks(np.arange(0, 35, 5))

    # Label axis
    plt.xlabel('# of Personal Account Followers (millions)', fontdict={'fontsize': 13}, horizontalalignment="center")
    plt.ylabel('# of Brand Account Followers (millions)', fontdict={'fontsize': 13}, horizontalalignment="center")

    # Add title
    plt.title('Instagram Followers\non Celebrity Personal Accounts vs Brand Accounts',
              fontdict={'fontsize': 16, 'fontweight': 'semibold'},
              horizontalalignment="center")

    # Add footnotes
    ax.text(-21, -5,
            "Instagram follower count as of 5/31/2024.\n"
            'Data Source: Instagram. Analysis by: Nkemjika at uploading.substack.com',
            fontdict={'fontsize': 9, 'fontweight': 'normal', 'color': '#000000'})

    '''
    Annotate scatter plot
    '''
    # Add the indices of the rows with the 2 largest personal follower counts
    max_followers_indices = df.iloc[:, 2].nlargest(2, keep='last').index.to_list()
    j = 0

    # For each celebrity, annotate the data point with the celebrity name and the brand name
    for i in max_followers_indices:
        # Add annotation box
        ax.text(df.iloc[i, 2] - 30, df.iloc[i, 3] + 3.5 - j,
                df.loc[i, 'celebrity'] + ": " + str(round_int_or_zero(df.iloc[i, 2])) + "M\n" + df.loc[
                    i, 'brand'] + ": " + str(round_int_or_zero(df.iloc[i, 3])) + "M",
                fontdict={'fontsize': 10, 'fontweight': 'light', 'color': '#303030'},
                bbox=dict(facecolor='#FFFFFF', edgecolor='#303030', boxstyle='round, pad=0.25'))
        # Add annotation line
        ax.add_artist(Line2D((df.iloc[i, 2], df.iloc[i, 2]), (df.iloc[i, 3] + 0.3, df.iloc[i, 3] + 3.5 - j),
                             color='#303030', linewidth=1))
        # Increase the label's y position so that each annotation is visible
        j = j + 0.5

    # Add the indices of notable data points
    notable_indices = df[(df['celebrity'] == 'Rihanna') & (df['brand'] == 'Fenty Beauty')].index.to_list() \
                      + df[(df['brand'] == 'Papatui')].index.to_list()
    j = 0

    # For each celebrity, annotate the data point with the celebrity name and the brand name
    for i in notable_indices:
        # Verify that the data point is not being annotated twice
        if i not in max_followers_indices:
            # Add annotation box
            ax.text(df.iloc[i, 2] - 30, df.iloc[i, 3] + 2.5 + j,
                    df.loc[i, 'celebrity'] + ": " + str(round_int_or_zero(df.iloc[i, 2])) + "M\n" + df.loc[
                        i, 'brand'] + ": " + str(round_int_or_zero(df.iloc[i, 3])) + "M",
                    fontdict={'fontsize': 10, 'fontweight': 'light', 'color': '#303030'},
                    bbox=dict(facecolor='#FFFFFF', edgecolor='#303030', boxstyle='round, pad=0.25'))
            # Add annotation line
            ax.add_artist(
                Line2D((df.iloc[i, 2], df.iloc[i, 2]), (df.iloc[i, 3] + 0.3, df.iloc[i, 3] + 2.5 + j), color='#303030',
                       linewidth=1))
            # Increase the label's y position so that each annotation is visible
            j = j + 0.65

    plt.show()


def density_scatter_plot_tiktok(df):
    '''
    Plot TikTok data points in a scatter plot, colouring the data points based on density
    :param df: (pandas dataframe) Contains personal account and brand account follower data for TikTok
    :return:
    '''

    # Load data
    x = df.iloc[:, 2]
    y = df.iloc[:, 3]

    # Calculate the point density
    xy = np.vstack([x, y])
    z = gaussian_kde(xy)(xy)

    # Sort the points by density, so that the densest points are plotted last
    idx = z.argsort()
    x, y, z = x[idx], y[idx], z[idx]

    fig, ax = plt.subplots()

    # Create scatter plot
    ax_ = ax.scatter(x, y, c=z, s=50, cmap=sns.color_palette("Spectral", as_cmap=True), edgecolor=None)

    '''
    Format graph
    '''

    # Customize x and y ticks
    plt.xticks(np.arange(0, 85, 5))
    plt.yticks(np.arange(0, 5, 0.5))

    # Label axis
    plt.xlabel('# of Personal Account Followers (millions)', fontdict={'fontsize': 13}, horizontalalignment="center")
    plt.ylabel('# of Brand Account Followers (millions)', fontdict={'fontsize': 13}, horizontalalignment="center")

    # Add title
    plt.title('TikTok Followers\non Celebrity Brand Accounts vs Personal Accounts',
              fontdict={'fontsize': 16, 'fontweight': 'semibold'},
              horizontalalignment="center")

    # Add footnotes
    ax.text(-3.8, -0.75,
            "TikTok follower count as of 5/31/2024.\n"
            'Data Source: TikTok. Analysis by: Nkemjika at uploading.substack.com',
            fontdict={'fontsize': 9, 'fontweight': 'normal', 'color': '#000000'})

    '''
    Annotate scatter plot
    '''
    # Add the indices of the 5 largest personal follower counts
    max_followers_indices = df.iloc[:, 2].nlargest(5, keep='all').index.to_list()

    # For each celebrity, annotate the data point with the celebrity name and the brand name
    for i in max_followers_indices:
        k = 0.25  # Parameter for the vertical position of the annotation
        l = 0.04  # Parameter for the horizontal position of the annotation line,
        # so that it doesn't overlap with the data point

        if df.loc[i, 'celebrity'] == 'Kylie Jenner':
            # For this specific annotation, place the annotation below the data point instead of above it
            k = -0.4
            l = -1 * l

        # Add annotation box
        ax.text(df.iloc[i, 2] - 7.5, df.iloc[i, 3] + k,
                df.loc[i, 'celebrity'] + ": " + str(round_int_or_zero(df.iloc[i, 2])) + "M\n" + df.loc[
                    i, 'brand'] + ": " + str(round_int_or_zero(df.iloc[i, 3])) + "M",
                fontdict={'fontsize': 10, 'fontweight': 'light', 'color': '#303030'},
                bbox=dict(facecolor='#FFFFFF', edgecolor='#4f4f4f', boxstyle='round, pad=0.25'))

        # Add annotation line
        ax.add_artist(
            Line2D((df.iloc[i, 2], df.iloc[i, 2]), (df.iloc[i, 3] + l, df.iloc[i, 3] + k), color='#303030',
                   linewidth=1))

    # Add the indices of notable data points
    notable_indices = df[(df['celebrity'] == 'Rihanna') & (df['brand'] == 'Fenty Beauty')].index.to_list() \
                      + df[(df['celebrity'] == 'Kim Kardashian') & (df['brand'] == 'SKIMS')].index.to_list()
    j = 0

    # For each celebrity, annotate the data point with the celebrity name and the brand name
    for i in notable_indices:
        # Verify that the data point is not being annotated twice
        if i not in max_followers_indices:
            l = 0.04

            # Add annotation box
            ax.text(df.iloc[i, 2] - 7.5, df.iloc[i, 3] + 0.25,
                    df.loc[i, 'celebrity'] + ": " + str(round_int_or_zero(df.iloc[i, 2])) + "M\n" + df.loc[
                        i, 'brand'] + ": " + str(round_int_or_zero(df.iloc[i, 3])) + "M",
                    fontdict={'fontsize': 10, 'fontweight': 'light', 'color': '#303030'},
                    bbox=dict(facecolor='#FFFFFF', edgecolor='#4f4f4f', boxstyle='round, pad=0.25'))
            # Add annotation line
            ax.add_artist(
                Line2D((df.iloc[i, 2], df.iloc[i, 2]), (df.iloc[i, 3] + l, df.iloc[i, 3] + 0.25), color='#303030',
                       linewidth=1))

    plt.show()

def density_scatter_plot(df, app, max, footnote):
    '''
    Plots a scatter plot and a linear fit line for the given dataframe
    :param df: (pandas dataframe) Contains celebrity personal & brand follower counts
    :return: None
    '''

    # Load data
    x = df.iloc[:,2]
    y = df.iloc[:,3]

    fig, ax = plt.subplots()

    # Calculate linear fit
    res = stats.linregress(x, y)
    ax.plot(x, res.intercept + res.slope * x, label = f"$R^2 =${round((res.rvalue**2)*100, 2)}%", c='#bd2b61',
            linewidth=2.25)

    # Plot data points
    ax.scatter(x, y, s=60, c='#493b92', edgecolor=None)

    '''
    Format graph
    '''
    # Customize x ticks
    plt.xticks(np.arange(0, max + max/10, max/10))

    # Label axis
    plt.xlabel('# of Personal Account Followers (millions)', fontdict={'fontsize': 13}, horizontalalignment="center")
    plt.ylabel('# of Brand Account Followers (millions)', fontdict={'fontsize': 13}, horizontalalignment="center")

    # Show Legend
    plt.legend(loc='upper left', fontsize=12, title='$\\bf{Linear\;Fit}$', title_fontsize=12)

    # Add title
    plt.title(app+' Followers on Celebrity Personal Accounts vs Brand Accounts:\n<'+str(max)+'M Personal Account Followers',
              fontdict={'fontsize': 16, 'fontweight': 'semibold'}, horizontalalignment="center")

    # Add bar chart footnotes
    ax.text(footnote[0], footnote[1],
               app+" follower count as of 5/31/2024.\n"
               'Data Source: TikTok. Analysis by: Nkemjika at uploading.substack.com',
               fontdict={'fontsize': 9, 'fontweight': 'normal', 'color': '#000000'})

    plt.show()