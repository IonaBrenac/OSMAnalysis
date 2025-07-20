"""Module of functions for plot of results of BSO data analysis.

ToDo: Wright functions docstrings.
"""

__all__ = ['plot_bar_df',
           'plot_bar_nbs_dict',
           'plot_nbs_dict',
           'plot_pareto_df',
           'plot_pie_df',
           'show_wordcloud_dict',
          ]


# 3rd party imports
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# Local imports
import bso_analysis.plot_globals as pg

def _add_trace_to_fig(fig, years, mentions_nbs, articles_nbs, name, error_y=None):    
    fig.add_trace(go.Scatter(x=years, y=mentions_nbs*100/articles_nbs,
                             name=name, error_y=error_y))


def _upd_layout(fig, fig_name, legend_type):
    fig_title = ""
    if fig_name in pg.TITLES_DICT.keys():
        fig_title = pg.TITLES_DICT[fig_name]
    fig.update_layout(xaxis_tickfont_size=pg.TICKS_FONT_SIZE,
                      yaxis=pg.YAXIS_DICT[fig_name],
                      legend=pg.LEGENDS_DICT[legend_type],
                      title=fig_title,
                  )


def plot_nbs_dict(fig_name, years, mentions_dict, articles_nbs,
                  errors_y_dict=None, mentions_add_tup=None):
    fig = go.Figure()
    for key, mentions_nbs in mentions_dict.items():
        error_y = None
        if errors_y_dict:
            error_y = errors_y_dict[key]
        _add_trace_to_fig(fig, years, mentions_nbs, articles_nbs,
                          pg.NAMES_DICT[key], error_y=error_y)
    if mentions_add_tup:
        mentions_nbs, mentions_key= mentions_add_tup
        _add_trace_to_fig(fig, years, mentions_nbs, articles_nbs,
                          pg.NAMES_DICT[mentions_key])
    _upd_layout(fig, fig_name, 'go')
    fig.show()


def plot_pie_df(fig_name, df, cols):
    fig = go.Figure(data=[go.Pie(labels=df[cols[0]],
                                 values=df[cols[1]],
                                 hole=.3)])
    _upd_layout(fig, fig_name, 'go')
    fig.show()


def plot_bar_df(fig_name, df, x_col):
    fig = px.bar(df, x=x_col, y=df.columns)
    _upd_layout(fig, fig_name, 'px')
    fig.show()


def show_wordcloud_dict(wordcloud_dict):
    for key, wordcloud_tup in wordcloud_dict.items():
        fig, axs = plt.subplots(1, 2, constrained_layout=True)
        for wc_num in [0, 1]:
            axs[wc_num].imshow(wordcloud_tup[wc_num],
                               interpolation='bilinear')
            axs[wc_num].set_title(key)
            axs[wc_num].axis("off")
        plt.show()


def plot_pareto_df(fig_name, full_df, y_col, freq_max):
    plot_df = full_df[full_df[y_col]>=freq_max]
    fig = go.Figure(go.Scatter(x=plot_df.index, y=plot_df[y_col]))    
    _upd_layout(fig, fig_name, 'go')
    fig.show()


def _add_bar_to_fig(fig, df, cols, name, color):    
    fig.add_trace(go.Bar(x=df[cols[0]], y=df[cols[1]],
                         name=name, marker_color=color))


def plot_bar_nbs_dict(fig_name, plot_dict, plot_keys, cols):
    fig = go.Figure()
    for key in plot_keys:
        df = plot_dict[key]
        _add_bar_to_fig(fig, df, cols, pg.NAMES_DICT[key],
                        pg.BAR_COLORS_DICT[key])
    _upd_layout(fig, fig_name, 'go')
    fig.show()
