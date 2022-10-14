# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 09:03:12 2022
@author: Korey
"""
import requests
import pandas as pd
import plotly as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np

def build_subplots(data, render_type='browser', subplot_height=375, title=''):
    ''' Outputs a figure object which is a subplot of the different data sets and series   provided.   

    Parameters
    ----------
    data : List, required 
        This is a list of dictionaries where each dictionary contains a list of series
        and parameters for subplots.Each subplot can have one or more series. Each series
        will have specific parameters that include: 
            'series' - a pandas series 
            'legend-name' - the name that series should be represented as on the chart legend
            'max-trendline' - whether to include a max-trendline
            'min-trendline' - whether to include a min-trendline
        
       EXAMPLE:
           
       [{'subplot': [{'series': series_df,
                                'legend-name': t,
                                'max-trendline': {},
                                'min-trendline': {}}],
                   'title': t}]
        
    render_type : str, optional
        This is the render type that is used by plotly to determine how to view the figure. More 
        information can be found here: https://plotly.com/python/renderers/
        The default is 'browser'.
        
    subplot_height : int, optional
        This is the height of each subplot. The default is 375.

    title : str, optional
        Title for the figure, not the individual subplot title

    Returns
    -------
    Plotly figure

    '''

    # these are the render types that are available by default in plotly,
    # default is browser, if an incorrect value is passed throw an exception
    render_type_options = ['plotly_mimetype', 'jupyterlab', 'nteract', 'vscode',
                           'notebook', 'notebook_connected', 'kaggle', 'azure', 'colab',
                           'cocalc', 'databricks', 'json', 'png', 'jpeg', 'jpg', 'svg',
                           'pdf', 'browser', 'firefox', 'chrome', 'chromium', 'iframe',
                           'iframe_connected', 'sphinx_gallery', 'sphinx_gallery_png']

    if render_type in render_type_options:
        plt.io.renderers.default = render_type
    else:
        raise ValueError(
            f"render_type={render_type} is not a valid option. Valid options are {render_type_options}")

    # based on how much data passed, determine the row_count
    row_count = (len(data) + 1) // 2

    # control the height of the figure based on the number of rows
    fig_height = row_count * subplot_height

    # build a list of plot titles
    titles = [d['title'] for d in data]

    # create the fig object by calling make subplots, pass in row count, col count, and titles
    fig = make_subplots(rows=row_count, cols=2, subplot_titles=titles)

    # iterate through items in data array and build subplots
    for i, k in enumerate(data, start=1):

        # data should be an array containing dictionaries
        # where each key is used to define an aspect of the subplot
        subplot_data = k['subplot']

        # determine which row and column the subplot should be placed on
        row_place = (i+1) // 2
        col_place = 1

        # we have two columns, place graph on column based on integer even or odd
        if i % 2 != 0:
            col_place = 1
        else:
            col_place = 2

        # each subplot can have one or many series, for each series add a trace to that subplot
        
        # TODO - this should be rewritten to be consistent with using a pandas series, 
        # regardless of whether a dataframe is submitted or a series. We are only adding a trace
        # with a single feature, selecting from multiple columns shouldn't be required
        
        for s in subplot_data:
            #print(s)
            #breakpoint()
            
            trace_data = None
            
            # if dataframe convert to series
            if isinstance(s['series'],pd.DataFrame):
                trace_data = s['series']['value'].squeeze()
            
            # if series set trace data to series
            elif isinstance(s['series'],pd.Series):
                trace_data = s['series']
            
            # if we do not have a dataframe and we don't have a series throw error
            else:
                raise ValueError(
                    f"Series data is not a pandas dataframe or series.")
            
            #current_val = s['series']['value'][0]
            current_val = trace_data[0]
            
            # if a color is passed - use it
            line_dict = {}
            if 'line-color' in s:
                line_dict['color']=s['line-color']
            
            
            fig.add_trace(go.Scatter(x=trace_data.index, #s['series'].index,
                                     y=trace_data, #s['series']['value'],
                                     name=s['legend-name'],
                                     showlegend=False,
                                     line=line_dict,# TODO - fix this so subplots legends can be shown
                                     ),
                          row=row_place,
                          col=col_place)

            if 'max-trendline' in s or 'min-trendline' in s:

                # TODO - break this out, you only get current if you want a trendline
                fig.add_annotation(xref='x domain',
                                   yref='y domain',
                                   x=1.0,
                                   y=1.09,
                                   text='Current:' + str(current_val),
                                   showarrow=False,
                                   row=row_place,
                                   col=col_place)

            if 'max-trendline' in s:

                # from dataframe col get max and create a list where every element is the max number
                max_val = round(trace_data.max(), 2)
                max_line = [max_val]*trace_data.shape[0]

                delta_max = round(((1 - (max_val/current_val))*100), 2)

                fig.add_trace(go.Scatter(x=trace_data.index,
                                         y=max_line,
                                         name='Max Value',
                                         line=dict(color='white', width=.5),
                                         showlegend=False,  # TODO - fix this so subplots legends can be shown
                                         ),
                              row=row_place,
                              col=col_place)

                fig.add_annotation(xref='x domain',
                                   yref='y domain',
                                   x=0.01,
                                   y=1.2,
                                   text=f'Max: {str(max_val)}({str(delta_max)}%)',
                                   showarrow=False,
                                   row=row_place,
                                   col=col_place)

            if 'min-trendline' in s:

                # from dataframe col get min and create a list where every element is the max number
                min_val = round(trace_data.min(), 2)
                min_line = [min_val]*trace_data.shape[0]

                delta_min = round(((1 - (min_val/current_val))*100), 2)

                fig.add_trace(go.Scatter(x=trace_data.index,
                                         y=min_line,
                                         name='Min Value',
                                         line=dict(color='white', width=.5),
                                         showlegend=False,  # TODO - fix this so subplots legends can be shown
                                         ),
                              row=row_place,
                              col=col_place)

                fig.add_annotation(xref='x domain',
                                   yref='y domain',
                                   x=0.01,
                                   y=1.1,
                                   text=f'Min: {str(min_val)}({str(delta_min)}%)',
                                   showarrow=False,
                                   row=row_place,
                                   col=col_place)

    fig.update_layout(
        template="plotly_dark",
        height=fig_height,
        title_text=title)
    fig.update_yaxes(side='right')

    return fig
