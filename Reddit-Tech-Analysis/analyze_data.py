import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as grid_spec
import numpy as np
from sklearn.neighbors import KernelDensity
from matplotlib.ticker import FuncFormatter
from matplotlib.patches import Patch


def ridge_plots(processed_df):
    '''
    Plots the distribution of reddit posts' upvote ratios for various streaming services by topic
    :param processed_df: Pandas dataframe with reddit post data
    :return: None
    '''

    # List out preset inputs for each streaming service's graph
    service_txt_colours = ['#00B554', '#8243BC', '#D6B200']
    service_graph_colours = ['#18D778','#9645E0', '#F3CE12']
    service_names = ['Hulu', 'HBO Max', 'Peacock']
    service_keys = ['Hulu', 'HBOMAX', 'peacock']
    topics = ['Other', 'Tech Support']

    # For each service (3 total), create a ridge plot
    for n in range(3):
        # Initialize the plot
        gs = (grid_spec.GridSpec(2, 1))
        fig = plt.figure(figsize=(6, 6))
        ax_objs = []

        # Select the colours and subreddit name for the given service
        graph_colours = ['#D6D6D6', service_graph_colours[n]]
        label_colours = ['#7A7A7A', service_txt_colours[n]]
        service_key = service_keys[n]

        #For each topic (2 total), plot a distribution plot
        for i in range(2):
            # Create a new axes object and append it to ax_objs
            ax_objs.append(fig.add_subplot(gs[i:i + 1, 0:]))

            # Get upvote ratio data and distribution data
            x = np.array(processed_df[(processed_df.service == service_key) & (processed_df.tech_flag == i)].upvote_ratio)
            x_d = np.linspace(0, 1, 1000)
            kde = KernelDensity(bandwidth=0.03, kernel='gaussian')
            kde.fit(x[:, None])
            logprob = kde.score_samples(x_d[:, None])

            # Plot the distribution
            ax_objs[i].plot(x_d, np.exp(logprob), color="#000000", lw=0.75)
            ax_objs[i].fill_between(x_d, np.exp(logprob), alpha=0.5, color=graph_colours[i])

            # Format the graph

            # Limit the x and y axis
            ax_objs[i].set_xlim(0, 1)
            ax_objs[i].set_ylim(0, 8)

            # Make the background transparent
            rect = ax_objs[i].patch
            rect.set_alpha(0)

            # Remove borders and y-axis ticks
            ax_objs[i].tick_params(
                axis='y',
                which='both',
                left=False,
                right=False,
                labelleft=False,
                labelright=False)
            ax_objs[i].axes.get_yaxis().get_label().set_visible(False)

            # On the last graph, set formatting parameters that only need to be done once
            if i == 1:
                # Label the ticks on the x-axis
                ax_objs[i].tick_params(
                    axis='x',
                    which='both',
                    bottom=False,
                    top=False,
                    labelbottom=True)
                ax_objs[i].xaxis.set_major_formatter(FuncFormatter(lambda x, pos: '{0:.0f}%'.format(x*100)))

                # Add a title
                ax_objs[i].text(-0.015, 5, 'Distribution of Upvote Ratios for Top r/' + service_keys[n] + ' posts by Topic',
                                fontweight="bold", fontsize=16, ha="left", color='#000000')

                # Label the x-axis
                ax_objs[i].set_xlabel("Upvote Ratio", fontsize=12, fontweight="bold")

                # Add a legend
                legend_elements = [Patch(facecolor=graph_colours[0], edgecolor='black', label=topics[0]),
                                   Patch(facecolor=graph_colours[1], edgecolor='black', label=topics[1])]
                ax_objs[i].legend(handles=legend_elements, loc='lower left', fontsize=12,
                                     ncol=1, edgecolor='white')

                # Add footnotes
                plt.text(-0.015, -0.7,
                         'Definition: The Upvote Ratio is the % of upvotes out of all votes on a post; '
                         'Data Source: Top 1000 posts on r/' + service_keys[n] + ' in the last year, as of 9/25/2022'
                                                                                  '\nCreated by: Adaora (uploading.substack.com)',
                         verticalalignment='top')
            else:
                # Remove the ticks on the x-axis for the first graph (since it will be overlayed)
                ax_objs[i].tick_params(
                    axis='x',
                    which='both',
                    bottom=False,
                    top=False,
                    labelbottom=False)

            # Remove the border on the overall graph
            spines = ["top", "right", "left", "bottom"]
            for s in spines:
                ax_objs[i].spines[s].set_visible(False)

        # Set the two graphs to sit directly ontop of each other
        gs.update(hspace=-1)

        plt.show()

def pie_chart(ml_df):
    '''
    Plots pie charts of sentiment analysis results for tech/other reddit posts for each service
    :param ml_df: Pandas dataframe with sentiment analysis results
    :return: None
    '''

    # List out preset inputs for each streaming service's graph
    service_keys = ['Hulu', 'HBOMAX', 'peacock']
    service_graph_colours = [['#18D778','#8BEBBB','#C5F5DD'], ['#9645E0','#BD8BEC','#E5D1F7'], ['#F3CE12', '#F9E789','#FDF6D3']]
    topics = ['Tech Support Posts', 'Other Posts']

    # Initialize the plot
    fig_pie, ax_pie = plt.subplots(2, 3)

    # Iterate through subplots and plot each pie chart
    for i in range(2):
        for j in range(3):
            # Plot pie chart
            wedges, texts, autotexts = ax_pie[i, j].pie(ml_df[(ml_df.service == service_keys[j]) & (ml_df.tech_flag == 1-i)].new_pct,
                                                        autopct='%1.0f%%',
                                                        normalize=False,
                                                        startangle=90,
                                                        colors=service_graph_colours[j],
                                                        wedgeprops={'edgecolor': '#ffffff'}, pctdistance=0.6,
                                                        textprops={'color': '#000000', 'fontsize': 18,
                                                                   'fontweight': 'bold'})
            # Set pie chart as a circle
            ax_pie[i, j].axis('equal')
            # Add pie chart title
            ax_pie[i, j].set_title(topics[i], fontdict={'fontsize': 12, 'fontweight': 'ultralight'}, y=0.9)
            if i == 0:
                # Add subreddit name
                ax_pie[0, j].text(0, 1.4, 'r/' + service_keys[j], horizontalalignment='center',
                                  fontdict={'fontsize': 14, 'fontweight': 'semibold'})

    # Create pie chart legend
    legend_elements = [Patch(facecolor='#202020', edgecolor='black', label='Negative Posts'),
                       Patch(facecolor='#9F9F9F', edgecolor='black', label='Neutral Posts'),
                       Patch(facecolor='#EDEDED', edgecolor='black', label='Positive Posts')]
    ax_pie[1, 1].legend(handles=legend_elements, loc='lower center', fontsize=12, bbox_to_anchor=(0.5, -0.15),
                        title='$\\bf{Legend}$', title_fontsize=12, ncol=3)

    # Set overall title
    ax_pie[0, 1].text(0, 1.8, "Streaming Service Subreddits: Sentiment of Top Reddit Posts by Topic",
                      fontdict={'fontsize': 18, 'fontweight': 'semibold'}, horizontalalignment="center")

    # Add footnotes
    ax_pie[1, 1].text(0, -2, 'Data Sources: Top 1000 subreddit posts in the last year, as of 9/25/2022'
                                  ', roBERTa base model for Sentiment Analysis\n'
                                  '(huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest); '
                                  'Created by: Adaora at uploading.substack.com', horizontalalignment='center')
    plt.show()

if __name__ == "__main__":
    # Load data
    processed_df = pd.read_csv('data/processed_posts.csv', index_col=0)
    ml_df = pd.read_csv('data/ml_results.csv', index_col=0)

    # Create ridge plot
    ridge_plots(processed_df)

    # Create pie chart
    pie_chart(ml_df)