import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
from matplotlib.lines import Line2D


if __name__ == "__main__":
    # List of streaming services
    streaming_services = [['netflix_ended','netflix_ongoing'], 'hulu', 'amazon', 'disney', 'apple', 'paramount',
                          'hbo', 'peacock']
    # Initialize dataframe for graphing data
    graphing_df = pd.DataFrame(columns=['% of Reboots', '% of Non-Reboots','% of Reboots Renewed for Season 2',
                                        '% of Non-Reboots Renewed for Season 2'])

    '''
    Determine % of shows that are reboots vs non-reboots 
    '''
    for service in streaming_services:
        # Initialize dictionary
        service_data = {}

        # Load programming data, use datasets that include tv shows with pending renewal status for season 2,
        # as renewal status is irrelevant for this analysis

        if service == ['netflix_ended','netflix_ongoing']:
            # Concatenate netflix ended and ongoing tv show data
            processed_df_1 = pd.read_csv('data/processed_' + service[0] + '_data_incl_pending.csv', index_col=0)
            processed_df_2 = pd.read_csv('data/processed_' + service[1] + '_data_incl_pending.csv', index_col=0)
            processed_df = pd.concat([processed_df_1,processed_df_2], ignore_index=True)
            service = 'netflix'
        else:
            processed_df = pd.read_csv('data/processed_'+service+'_data_incl_pending.csv', index_col=0)

        num_reboots = processed_df['Reboot'].sum()
        num_shows = processed_df['Reboot'].shape[0]
        num_non_reboots = processed_df[processed_df['Reboot'] == False].shape[0]

        service_data['% of Reboots'] = num_reboots/num_shows
        service_data['% of Non-Reboots'] = num_non_reboots/num_shows

        # Load service data into dataframe
        graphing_df.loc[service] = service_data

    '''
    Determine % of shows renewed for season 2 for reboots vs non-reboots 
    '''
    for service in streaming_services:
        # Initialize dictionary
        service_data = {}

        # Load programming data, use datasets that exclude tv shows with pending renewal status for season 2
        if service == ['netflix_ended','netflix_ongoing']:
            # Concatenate netflix ended and ongoing tv show data
            processed_df_1 = pd.read_csv('data/processed_' + service[0] + '_data_excl_pending.csv', index_col=0)
            processed_df_2 = pd.read_csv('data/processed_' + service[1] + '_data_excl_pending.csv', index_col=0)
            processed_df = pd.concat([processed_df_1,processed_df_2], ignore_index=True)
            service = 'netflix'
        else:
            processed_df = pd.read_csv('data/processed_'+service+'_data_excl_pending.csv', index_col=0)

        num_reboots = processed_df['Reboot'].sum()
        num_non_reboots = processed_df[processed_df['Reboot'] == False].shape[0]

        if num_reboots == 0:
            # If the streaming service has no reboots confirmed cancelled or
            # renewed for season 2, set data entry to -1 to flag the data entry as N/A
            service_data['% of Reboots Renewed for Season 2'] = -1
        else:
            service_data['% of Reboots Renewed for Season 2'] = (processed_df[(processed_df['Reboot'] == True) &
                                                          (processed_df['Total Seasons'] > 1)].shape[0]) / num_reboots

        service_data['% of Non-Reboots Renewed for Season 2'] = (processed_df[(processed_df['Reboot'] == False) &
                                                           (processed_df['Total Seasons'] > 1)].shape[0]) / num_non_reboots
        # Load service data into dataframe
        graphing_df.loc[service,
                        ['% of Reboots Renewed for Season 2','% of Non-Reboots Renewed for Season 2']] = service_data

    # Set service names for charting entries
    graphing_df = graphing_df.rename(index={'netflix':'Netflix', 'hulu':'Hulu', 'amazon':'Amazon Prime',
                                            'disney':'Disney+', 'apple':'Apple TV+', 'hbo':'HBO Max',
                                            'peacock':'Peacock', 'paramount':'Paramount+'})

    # Set service logo colours for charting entries
    colours = [('#f0545b', '#e62c35'), ('#87e8b7', '#1ce783'), ('#5bbdde', '#00A8E1'), ('#7493fc', '#0f36b8'),
               ('#d4d4d4', '#c4c4c4'), ('#7794ed', '#2557e8'), ('#bf9be0', '#9845e5'), ('#f7da6f', '#f5d049')]

    '''
    Plot pie charts
    '''
    # Create a separate dataframe for pie chart data, transpose for charting purposes
    pie_chart_df = graphing_df[['% of Reboots','% of Non-Reboots']]
    pie_chart_df.columns = ['Reboots', 'Non-Reboots']
    pie_chart_df = pie_chart_df.transpose()

    fig_pie, ax_pie = plt.subplots(2, 4)

    # Iterate through subplots and plot each pie chart
    for i in range(2):
        for j in range(4):
            wedges, texts, autotexts = ax_pie[i, j].pie(pie_chart_df.iloc[:, 4*i + j], autopct='%1.0f%%',normalize=False,
                                                    startangle=90, colors=colours[4*i + j],
                                                    wedgeprops={'edgecolor':'#FFFFFF'}, pctdistance=0.6,
                                                    textprops={'color':'#000000', 'fontsize':18, 'fontweight':'bold'})
            # Set pattern for pie wedge representing reboot data
            wedges[0].set_hatch('///')
            # Set pie chart as a circle
            ax_pie[i, j].axis('equal')
            # Set pie chart title
            ax_pie[i, j].set_title(pie_chart_df.columns[4*i + j], fontdict={'fontsize':14, 'fontweight':'bold'}, y=0.95)

    # Create pie chart legend
    legend_elements = [Patch(facecolor='w', edgecolor='black', hatch='///', label='TV Show Reboots'),
                       Patch(facecolor='w', edgecolor='black', label='TV Show Non-Reboots')]
    ax_pie[1,1].legend(handles=legend_elements, loc='lower right', bbox_to_anchor=(1.65, -0.25), fontsize=12,
                       title='$\\bf{Legend}$', title_fontsize=12)
    # Add pie chart footnotes
    ax_pie[1,0].text(-0.993, -2, 'Data Source: Wikipedia\nAnalysis by: Adaora at uploading.substack.com')
    # Set overall pie chart title
    ax_pie[0,1].text(1.25, 1.65, "Streaming Service Original TV Shows:\nPercentage of TV Show Reboots",
                     fontdict={'fontsize':18, 'fontweight':'semibold'}, horizontalalignment="center")

    plt.show()

    '''
    Plot Bar Graph
    '''
    # Create a separate dataframe for bar graph data
    bar_graph_df = graphing_df[['% of Reboots Renewed for Season 2','% of Non-Reboots Renewed for Season 2']]

    fig_bar, ax_bar = plt.subplots()

    # Set bar width
    width = 0.35
    # Set bar locations
    bar_loc = np.arange(len(bar_graph_df.index))

    # Plot each bar individually
    for bar_idx in bar_loc:
        #if '% of reboots renewed for season 2' ≠ -1, plot the bar
        if bar_graph_df.iloc[bar_idx, 0] != -1:
            # Assign a pattern to bar for '% of reboots renewed for season 2'
            ax_bar.bar(bar_idx - width/2, bar_graph_df.iloc[bar_idx, 0], width=width, hatch='///', color=colours[bar_idx][0],
                       edgecolor='#FFFFFF')
            # Label bar
            ax_bar.text(bar_idx - width/2, bar_graph_df.iloc[bar_idx, 0] + 0.015,
                        '{:,.0%}'.format(bar_graph_df.iloc[bar_idx, 0]), horizontalalignment="center",
                        fontdict={'fontsize':11, 'fontweight':'semibold','color':'#000000'})

        # Graph '% of non-reboots renewed for season 2'
        ax_bar.bar(bar_idx + width/2, bar_graph_df.iloc[bar_idx, 1], width=width, color=colours[bar_idx][1],
                   edgecolor='#FFFFFF')
        # Label bar
        ax_bar.text(bar_idx + width/2, bar_graph_df.iloc[bar_idx, 1] + 0.015,
                    '{:,.0%}'.format(bar_graph_df.iloc[bar_idx, 1]), horizontalalignment="center",
                    fontdict={'fontsize':11, 'fontweight':'semibold','color':'#000000'})

    # Set x-axis labels
    ax_bar.set_xticks(bar_loc)
    ax_bar.set_xticklabels(bar_graph_df.index, fontdict={'fontsize':11, 'fontweight':'bold'})
    ax_bar.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True)

    # Remove frame
    ax_bar.set_frame_on(False)
    # Remove y-axis
    ax_bar.axes.get_yaxis().set_visible(False)
    # Redraw x-axis line
    xmin, xmax = ax_bar.get_xaxis().get_view_interval()
    ymin, ymax = ax_bar.get_yaxis().get_view_interval()
    ax_bar.add_artist(Line2D((xmin, xmax), (ymin, ymin), color='black', linewidth=1.5))

    # Create bar chart legend
    legend_elements = [Patch(facecolor='w', edgecolor='black', hatch='///', label='TV Show Reboots'),
                       Patch(facecolor='w', edgecolor='black', label='TV Show Non-Reboots')]
    ax_bar.legend(handles=legend_elements,loc='lower right', bbox_to_anchor=(0.5, 0.05, 0.5, 0.5), fontsize=12,
                        title='$\\bf{Legend}$', title_fontsize=12)
    # Add bar chart footnotes
    ax_bar.text(-0.75, -0.1, 'Data Source: Wikipedia\nAnalysis by: Adaora at uploading.substack.com')
    # Add N/A note
    ax_bar.text(4 - width/2, 0.015, 'N/A', horizontalalignment="center",
                    fontdict={'fontsize':11, 'fontweight':'semibold','color':'#000000'})
    # Set bar chart title
    ax_bar.text(3 + width, 1.1, "Streaming Service Original Programming:"
                                "\nPercentage of TV Shows Renewed for Season 2",
                fontdict={'fontsize': 16, 'fontweight': 'semibold'}, horizontalalignment="center")

    plt.show()