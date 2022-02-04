import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import matplotlib as mpl
import matplotlib.gridspec as grid_spec
from scipy.interpolate import LinearNDInterpolator

def generate_cts_density_grid(df, startyear, endyear):
    '''
    Generates grid points for runtime density, using triangular interpolation
    :param df: Pandas dataframe with movie runtime and release year data
    :param startyear: Start year of analysis
    :param endyear: End year of analysis
    :return: (X, Y, Z): Set of grid points
    '''

    # Initialize lists for all x, y, and z points
    all_z = []
    all_x = []
    all_y = []

    # Calculate point density (z) at each point (x,y)
    for year in range(startyear, endyear + 1):
        x = df.loc[df['release year'] == year, 'release year'].to_numpy()
        y = df.loc[df['release year'] == year, 'runtime'].to_numpy()

        # Calculate the point density
        z = gaussian_kde(y)(y)

        # Normalize z values
        mean = np.mean(z)
        std = np.std(z)
        norm_z = (z - mean) / std

        # Append (x,y,z) to lists
        all_z.extend(norm_z)
        all_x.extend(x)
        all_y.extend(y)

    # Set parameters for x & y axis on the graph
    xx_interval = 0.1
    yy_min = 85
    yy_max = 125
    yy_interval = 0.1

    # Generate a mesh of points on the graph
    xx = np.arange(startyear, endyear + xx_interval, xx_interval)
    yy = np.arange(yy_min, yy_max, yy_interval)

    # Use triangular interpolation to approximate z points
    tri_interp = LinearNDInterpolator(list(zip(all_x, all_y)), all_z)

    # Generate mesh
    X, Y = np.meshgrid(xx, yy)
    Z = tri_interp(X, Y)

    # Replace any np.nan values (arise when mesh points are outside of the interpolation boundaries,
    # so they'd require extrapolation to be approximated) with min value in mesh
    Z = np.where(np.isnan(Z), np.nanmin(Z), Z)

    return X, Y, Z

def density_plots(bo_df, s_df, startyear, endyear):
    '''
    Plot runtime density graphs for theatrical releases and streaming films
    :param bo_df: Pandas dataframe of theatrical releases with runtime and release year data
    :param s_df: Pandas dataframe of streaming films with runtime and release year data
    :param startyear: Start year of analysis
    :param endyear: End year of analysis
    '''

    '''
    Create density plots
    '''
    # Create subplots for the theatrical release and streaming graphs
    gs = (grid_spec.GridSpec(1, 2, width_ratios=[5, 1]))
    fig = plt.figure()
    bo_ax = fig.add_subplot(gs[0:, 0])
    s_ax = fig.add_subplot(gs[0:, 1])

    bo_X, bo_Y, bo_Z = generate_cts_density_grid(bo_df, startyear, endyear)
    s_X, s_Y, s_Z = generate_cts_density_grid(s_df, 2016, endyear)

    # Initialize parameters for contour graph
    plot_levels = 4

    # Create custom colour palettes for contour graphs
    bo_norm = plt.Normalize(np.min(bo_Z), np.max(bo_Z))
    bo_cmap = mpl.colors.LinearSegmentedColormap.from_list("", ["#ffffff", "#93d3f5", "#5db4e3", "#2891c9", "#036396"])
    s_norm = plt.Normalize(np.min(s_Z), np.max(s_Z))
    s_cmap = mpl.colors.LinearSegmentedColormap.from_list("", ["#ffe8e9", "#f7a8ad", "#fa898f", "#f56971", "#d92932"])

    # Plot graph
    bo_ax.contourf(bo_X, bo_Y, bo_Z, cmap=bo_cmap, alpha=0.95, levels=plot_levels, norm=bo_norm)
    s_ax.contourf(s_X, s_Y, s_Z, cmap=s_cmap, alpha=1, levels=plot_levels, norm=s_norm)

    '''
    Create line graphs for the median
    '''
    # Calculate median
    bo_graphing_df = bo_df.groupby('release year')['runtime'].agg(Median='median')
    s_graphing_df = s_df.groupby('release year')['runtime'].agg(Median='median')

    # Plot line graph
    bo_ax.plot(bo_graphing_df.index, bo_graphing_df['Median'], label='Median',
            color='#000000', marker='o', linestyle='-', linewidth=2.5, markersize=8)
    s_ax.plot(s_graphing_df.index, s_graphing_df['Median'], label='Median',
            color='#000000', marker='o', linestyle='-', linewidth=2.5, markersize=8)

    '''
    Format graph
    '''
    for ax in [bo_ax, s_ax]:
        # Add gridlines
        ax.grid(axis='y', color='#000000', linestyle='-', alpha=0.3)
        # Create legend
        ax.legend(loc='best', fontsize=12)

    # Set horizontal space between the subplots
    gs.update(wspace=0.1)

    # Customize x ticks
    bo_ax.set_xticks(np.arange(startyear, endyear + 1, 2))
    s_ax.set_xticks(np.arange(2016, endyear + 1, 2))

    # Label axis
    bo_ax.text(2009, 82, 'Release Year', fontdict={'fontsize': 14}, horizontalalignment="center")
    bo_ax.set_ylabel('Runtime (min)', fontdict={'fontsize': 14}, horizontalalignment="center")

    # Add subtitles
    bo_ax.set_title('Films Released in Theaters', fontdict={'fontsize': 14, 'fontweight':'normal'})
    s_ax.set_title('Films Released\nExclusively on Streaming', fontdict={'fontsize': 14, 'fontweight':'normal'})

    # Add title
    bo_ax.text(2009, 128,'Feature Film Runtime by Release Year',
                fontdict={'fontsize': 18, 'fontweight': 'semibold'}, horizontalalignment="center")

    # Add bar chart footnotes
    bo_ax.text(1991, 80, 'Data Sources: Box Office Mojo, IMDb, Wikipedia\nCreated by: Adaora (uploading.substack.com)')

    plt.show()

if __name__ == "__main__":
    # Load box office data
    bo_df = pd.read_csv('../data/processed_boxoffice_films_runtime.csv', index_col=0)
    bo_df = bo_df.drop(columns='title')

    # Load streaming data
    s_df = pd.read_csv('../data/processed_streaming_films_runtime.csv', index_col=0)
    s_df = s_df.drop(columns='title')
    # Drop rows for titles with release year = 2015, since there's only 2 titles (too little data)
    s_df = s_df[s_df['release year'] != 2015]

    density_plots(bo_df, s_df, 1991, 2021)
