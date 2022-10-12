# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 15:46:17 2022

@author: Korey

Alpha is a module used to access data from alpha vantage and perform various common tasks
such as building subplots of various economic and equity based data. 
"""

import requests
import pandas as pd
import plotly as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np


_colors = plt.colors.DEFAULT_PLOTLY_COLORS


def _build_dataframe(data, columns: list = ['value'], set_index: bool = True):
    '''Private. Takes a list of dicts or dataframe and builds a dataframe while converting values to numeric,
    and setting the index to date.
      
    Parameters
    ----------
    data : dataframe or list of dicts
        holds data that should be converted into dataframe or used for converting to numeric.

    columns: list
        A list of columns that should be converted to numeric.
        
    set_index: boolean
        if True set the date columne to the index
        
    Returns
    -------
    df : pandas.DataFrame
        Returns a pandas dataframe.

    '''
    if isinstance(data,list):
        data = pd.DataFrame(data)

    data[columns] = data[columns].apply(pd.to_numeric, errors='coerce')

    if set_index == True:
        data.set_index('date', inplace=True)

    return data


def alpha_subplots(data, render_type='browser', subplot_height=375, title=''):
    ''' Outputs a figure object which is a subplot of the different data sets and series provided.   

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


class Equities():

    """
    A class used to represent common equity data available in alphavantage. For more
    information on the data returned by alpha vantage go here: https://www.alphavantage.co/documentation/
    
    ...
    Attributes
    ----------
    api_key : str
        alpha_vantage api key
    
    tickers : list
        list of stock symbols to be retrieved
    
    Methods
    -------
    get_time_series_daily_adusted(output_size: str='compact')    
        returns a dataframe of daily open/high/low/close/volume values with an adjusted close column that 
        shows the value of the stock adjusted for stock splits
    
    subplot(series_type: str='daily_adjusted',output_size: str='compact', start_end_dates: tuple=())
        creates a subplot of for each equity that as retrieved using plotly
    """

    def __init__(self, api_key: str, tickers: list):
        self.api_key = api_key
        self.tickers = tickers
        self.base_url = 'https://www.alphavantage.co/query?'

    # TODO - add income statement
    def get_income_statement(self):
        pass

    # TODO - add get overview
    def get_overview(self):
        pass

    # TODO - add balance sheet
    def get_balance_sheet(self):
        pass

    def get_cashflow(self):

        return_obj = []
        for t in self.tickers:
            url = f'{self.base_url}function=CASH_FLOW&symbol={t}&apikey={self.api_key}'
            r = requests.get(url)
            data = r.json()
            if 'annualReports' in data:
                df = pd.DataFrame(data['annualReports'])
                df['ticker'] = t

                return_obj.append(df)

            df = pd.concat(return_obj)

            columns = df.columns[2:-1]

            df[columns] = df[columns].apply(pd.to_numeric, errors='coerce')

            df.set_index('fiscalDateEnding', inplace=True)

        return df

    # TODO - add earnings
    def get_earnings(self):
        pass

    def get_time_series_daily_adjusted(self, dataframe: bool = True, output_size: str = 'compact'):
        '''
        Gets daily stock value data with a adjusted column, showing the value adjusted for stock splits

        Parameters
        ----------
        dataframe : bool, optional
            If true the function returns a dataframe. The default is True.
        
        output_size : str, optional
            Controls the size of the data returned.
            output_size = 'compact' returns the last 100 days of data
            output_size = 'full' returns all available data 
            
        Returns
        -------
        Dataframe or List of Dictionaries    

        '''
        return_obj = []
        for t in self.tickers:
            url = f'{self.base_url}function=TIME_SERIES_DAILY_ADJUSTED&symbol={t}&outputsize={output_size}&apikey={self.api_key}'
            r = requests.get(url)
            data = r.json()

            if dataframe:
                df = pd.DataFrame(data['Time Series (Daily)']).T
                columns = df.columns
                df = _build_dataframe(df, columns=columns, set_index=False)
                df['ticker'] = t
                return_obj.append(df)
            else:
                return_obj.append(data)

        if dataframe:
            return_df = pd.concat(return_obj)
            return return_df
        else:
            return return_obj

    def cashflow_subplot(self, columns: list = ['operatingCashflow', 'netIncome', 'changeInCashAndCashEquivalents']):
        # TODO add docstring
        cf = self.get_cashflow()
        
        subplot_data = []
        for t in self.tickers:
            df = cf[cf['ticker']==t]
            if not df.empty:               
                subplot = {'subplot': [],
                           'title': t}
                
                for i,v in enumerate(columns):
                    series = df[v]
                    series = series.rename('value')
                    subplot['subplot'].append({'series':series,
                                               'legend-name':v,
                                               'line-color':_colors[i],
                                               },
                                              )
                subplot_data.append(subplot)
                
        fig = alpha_subplots(subplot_data)
            
        return fig
        

    def daily_adjusted_subplot(self, series_type: str = 'daily_adjusted', output_size: str = 'compact', start_end_dates=()):
        
        '''
        Uses the get_time_series_daily_adjusted method to generate data for stocks and create a 
        subplot of different stocks. Currently only supports daily close values by using the 
        daily adjusted values or non-adjusted values.

        Parameters
        ----------
        series_type : str, optional
            if daily_adjusted will return the adjusted close value, else it return
            the un-adjusted close values. Default is daily_adjusted
        
        output_size : str, optional
           controls how much data per equity is returned, compact is the last 100 data points, full all data available
           default is 'compact'
        
        start_end_dates : Tuple, optional
            for each series selects sub selects between the start date and the end date.
            First tuple element is start date, second is end date().

        Returns
        -------
        fig : TYPE
            DESCRIPTION.

        '''

        # TODO add docstring
        price = self.get_time_series_daily_adjusted(output_size=output_size)

        if start_end_dates:
            price = price[(price.index > start_end_dates[0]) &
                          (price.index <= start_end_dates[1])]

        if series_type == 'daily_adjusted':
            price_df = price[['5. adjusted close', 'ticker']]
            price_df = price_df.rename(columns={"5. adjusted close": "value"})

        else:
            price_df = price[['4. close', 'ticker']]
            price_df = price_df.rename(columns={"4. close": "value"})

        price_df = price_df.rename(columns={"1. open": "value"})

        subplot_data = []
        for t in self.tickers:
            # each subplot will have one series which is the equity
            series_df = price_df[price_df['ticker'] == t]
            subplot = {'subplot': [{'series': series_df,
                                    'legend-name': t,
                                    'max-trendline': {},
                                    'min-trendline': {}}],
                       'title': t}
            subplot_data.append(subplot)

        fig = alpha_subplots(subplot_data)
        return fig


class Economics:

    """
    A class used to represent common economic data available in alphavantage. For more
    information on the data returned by alpha vantage go here: https://www.alphavantage.co/documentation/
    
    ...
    Attributes
    ----------
    api_key : str
        alpha_vantage api key
    
    Methods
    -------
    retail_sales(dataframe: bool = True)
        returns either a dataframe or a dictionary of monthly US retail sales data
        
    inflation(dataframe: bool = True)
        returns either a dataframe or a dictionary of monthly US inflation data
        
    cpi(dataframe: bool = True, interval: str = 'monthly')
        returns either a dataframe or a dictionary of monthly us inflation data
    
    treasury_yield(interval: str = 'monthly', maturity: str = '10year', dataframe: bool = True)
        returns either a dataframe or a dictionary of treasury yield for a defined maturity time e.g., 2,5,7 years
    
    consumer_sentiment(dataframe: bool = True)
        returns either a dataframe or a dictionary consumer sentiment data for US
        
    nonfarm_payroll(dataframe: bool = True)
        returns either a dataframe or a dictionary for nonfarm payroll data for the US
    
    federal_funds_rate(interval: str = 'monthly', dataframe: bool = True)
        returns either a dataframe or a dictionary of federal funds rate data based on FOMC decisions
        
    real_gdp(interval: str = 'quarterly', dataframe: bool = True)
        returns either a dataframe or a dictionary of real gdp data 
    
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://www.alphavantage.co/query?'

    def retail_sales(self, dataframe: bool = True):
        ''' retrieves monthly US retail sales data via alphavantage 
        
        Parameters
        ----------
        dataframe : bool, optional
            if True the method will return a dataframe
            if False the method will return a dictionary
            
        Returns
        -------
        Dictionary or Dataframe of US monthly US retails sales data.
        '''
        # build url and call request
        # https://www.alphavantage.co/query?function=REAL_GDP&interval=annual&apikey=demo'
        url = f'{self.base_url}function=RETAIL_SALES&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()

        if dataframe:
            df = _build_dataframe(data['data'])
            return df
        else:
            return data

    def inflation(self, dataframe: bool = True):
        ''' retrieves monthly US inflation data via alphavantage 
        
        Parameters
        ----------
        dataframe : bool, optional | default = True
            if True the method will return a dataframe
            if False the method will return a dictionary
            
        Returns
        -------
        Dictionary or Dataframe of US monthly US inflation data.
        '''
        # build url and call request
        # https://www.alphavantage.co/query?function=REAL_GDP&interval=annual&apikey=demo'
        url = f'{self.base_url}function=INFLATION&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()

        if dataframe:
            df = _build_dataframe(data['data'])
            return df
        else:
            return data

    def cpi(self, dataframe: bool = True, interval: str = 'monthly'):
        ''' retrieves monthly or semiannual consumer price index (CPI) for the US 
        
        Parameters
        ----------
        dataframe : bool, optional | default = True
            if True the method will return a dataframe
            if False the method will return a dictionary
            
        interval : str, optional | default = 'monthly'
            if 'monthly' returns monthly cpi data
            if 'semiannual' returns data for twice a year
            
        Returns
        -------
        Dictionary or Dataframe of US monthly US inflation data.
        '''
        # build url and call request
        # https://www.alphavantage.co/query?function=REAL_GDP&interval=annual&apikey=demo'
        url = f'{self.base_url}function=CPI&interval={interval}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()

        if dataframe:
            df = _build_dataframe(data['data'])
            return df
        else:
            return data

    def treasury_yield(self, interval: str = 'monthly', maturity: str = '10year', dataframe: bool = True):
        ''' retrieves monthly, daily, or weekly US yield given maturity of 3 months or 2,5,7,10,30 years 
        
        Parameters
        ----------
        dataframe : bool, optional | default = True
            if True the method will return a dataframe
            if False the method will return a dictionary
            
        interval : str, optional | default = 'monthly'
            if 'monthly' returns monthly treasury yield data
            if 'weekly' returns weekly treasury yield data
            if 'monthly' returns monthly treasury yield data
            
        maturity : str, optional | default = '10year'
            '3month' 
            '2year' 
            '5year' 
            '10year'
            '30year'
            
        Returns
        -------
        Dictionary or Dataframe of treasury yield data.
        '''

        # build url and call request
        # https://www.alphavantage.co/query?function=REAL_GDP&interval=annual&apikey=demo'
        url = f'{self.base_url}function=TREASURY_YIELD&interval={interval}&maturity={maturity}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()
        if dataframe:
            df = _build_dataframe(data['data'])
            return df
        else:
            return data

    def consumer_sentiment(self, dataframe: bool = True):
        ''' TODO - Update docstring
        Parameters
        ----------
        dataframe : bool, optional
            DESCRIPTION. The default is True.
    
        Returns
        -------
        None.
        '''
        # build url and call request
        # https://www.alphavantage.co/query?function=REAL_GDP&interval=annual&apikey=demo'
        url = f'{self.base_url}function=CONSUMER_SENTIMENT&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()

        if dataframe:
            df = _build_dataframe(data['data'])
            return df
        else:
            return data

    def nonfarm_payroll(self, dataframe: bool = True):
        ''' TODO - Update docstring
        Parameters
        ----------
        dataframe : bool, optional
            DESCRIPTION. The default is True.
    
        Returns
        -------
        None.
        '''
        # build url and call request
        # https://www.alphavantage.co/query?function=REAL_GDP&interval=annual&apikey=demo'
        url = f'{self.base_url}function=NONFARM_PAYROLL&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()

        if dataframe:
            df = _build_dataframe(data['data'])
            return df
        else:
            return data

    def federal_funds_rate(self, interval: str = 'monthly', dataframe: bool = True):
        ''' TODO - Update docstring
        Parameters
        ----------
        dataframe : bool, optional
            DESCRIPTION. The default is True.
    
        Returns
        -------
        None.
        '''
        # build url and call request
        # https://www.alphavantage.co/query?function=REAL_GDP&interval=annual&apikey=demo'
        # https://www.alphavantage.co/query?function=REAL_GDP&interval=annual&apikey=demo'
        url = f'{self.base_url}function=FEDERAL_FUNDS_RATE&interval={interval}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()

        if dataframe:
            df = _build_dataframe(data['data'])
            return df
        else:
            return data

    def real_gdp(self, interval: str = 'quarterly', dataframe: bool = True):
        '''
        Retrieves real quarterly or annual gdp using alphavantage api.
        
        Parameters
        ----------
        interval: str, optional
            quarterly or annual (default is annual)
         
        dataframe: bool, optional
            if True return a pandas dataframe else return a dictionary
         
        
        Returns
        --------
        dictionary or dataframe of real gdp data
        
        '''
        # build url and call request
        # https://www.alphavantage.co/query?function=REAL_GDP&interval=annual&apikey=demo'
        url = f'{self.base_url}function=REAL_GDP&interval={interval}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()

        if dataframe:
            df = _build_dataframe(data['data'])
            return df
        else:
            return data


if __name__ == "__main__":
    print(__name__)
