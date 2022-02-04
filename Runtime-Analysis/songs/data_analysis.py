import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import matplotlib as mpl
import matplotlib.gridspec as grid_spec
import math
from scipy.interpolate import LinearNDInterpolator



def continuous_density(sp_df, startyear, endyear):
    '''
    Plot song duration density, using triangular interpolation to make the graph continuous
    :param sp_df: Pandas dataframe with song duration and release year data
    :param startyear: Start year of analysis
    :param endyear: End year of analysis
    '''

    '''
    Plot song duration density scatter plot
    '''
    # Initialize container for figure
    fig2, ax = plt.subplots()

    # Initialize lists for all x, y, and z points
    all_z = []
    all_x = []
    all_y = []

    # Calculate point density (z) at each point (x,y)
    for year in range(startyear, endyear+1):
        x = sp_df.loc[sp_df['release year'] == year, 'release year'].to_numpy()
        y = sp_df.loc[sp_df['release year'] == year, 'duration'].to_numpy()

        # Calculate the point density
        z = gaussian_kde(y)(y)

        # Normalize z values
        mean = np.mean(z)
        std = np.std(z)
        norm_z = (z - mean)/std

        # Append (x,y,z) to lists
        all_z.extend(norm_z)
        all_x.extend(x)
        all_y.extend(y)

    # Set parameters for x & y axis on the graph
    xx_interval = 0.1
    yy_min = 160
    yy_max = 300

    # Generate a mesh of points on the graph
    xx = np.arange(startyear, endyear + xx_interval, xx_interval)
    yy = np.arange(yy_min, yy_max, 1)

    # Approximate z points using triangular interpolation
    tri_interp = LinearNDInterpolator(list(zip(all_x, all_y)), all_z)

    # Generate mesh
    X, Y = np.meshgrid(xx, yy)
    Z = tri_interp(X, Y)

    # Replace any np.nan values (arise when mesh points are outside of the interpolation boundaries,
    # so they'd require extrapolation to be approximated) with min value in mesh
    Z = np.where(np.isnan(Z), np.nanmin(Z), Z)

    # Initialize parameters for contour graph
    plot_levels = 2
    norm = plt.Normalize(np.min(all_z), np.max(all_z))
    cmap = mpl.colors.LinearSegmentedColormap.from_list("", ["#ffffff", "#85d97e", "#159429"])

    # Plot graph
    plt.contourf(X, Y, Z, cmap=cmap, alpha=0.875, levels=plot_levels, norm=norm)


    '''
    Add line graph for the median
    '''
    # Calculate median
    sp_graphing_df = sp_df.groupby('release year')['duration'].agg(Median='median')

    # Plot line graph
    ax.plot(sp_graphing_df.index, sp_graphing_df['Median'], label='Median',
            color='#000000', marker='o', linestyle='-', linewidth=2.5, markersize=8)

    '''
    Format graph
    '''
    # Customize x and y ticks
    plt.xticks(np.arange(startyear, endyear + 1, 2))
    plt.yticks(np.arange(yy_min, yy_max, 20))

    # Add gridlines
    plt.grid(axis='y', color='#000000', linestyle='-', alpha=0.5)

    # Add legend
    plt.legend(loc='lower left', fontsize=14)

    # Label axis
    plt.xlabel('Release Year', fontdict={'fontsize': 16}, horizontalalignment="center")
    plt.ylabel('Song Duration (s)', fontdict={'fontsize': 16}, horizontalalignment="center")

    # Add title
    plt.title('Duration of Hit Songs by Release Year', fontdict={'fontsize': 18, 'fontweight': 'semibold'},
              horizontalalignment="center")

    # Add bar chart footnotes
    ax.text(1991, 142.5, 'Data Source: Spotify\nCreated by: Adaora (uploading.substack.com)')

    plt.show()



if __name__ == "__main__":
    # Load Spotify data
    sp_df = pd.read_csv('../data/processed_spotify_songs_duration.csv', index_col=0)
    sp_df = sp_df.drop(columns=['playlist_url', 'track_uri', 'title'])

    plt.show()

    continuous_density(sp_df, 1991, 2021)
