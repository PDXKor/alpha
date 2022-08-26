# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 13:08:21 2022

@author: Korey
"""

import requests
import pandas as pd


class Equities:
    
    # any variables defined here are considered class variables

    # init is a constructor method and is automatically called to allocate memory when a new object/instance
    # is created. All classes have an __init__ method. It helps in distinguising a class variable 
    # from a local variable
    
    # sometime the init method is just referred to as constructor
    def __init__(self, api_key, tickers):
        
        # any variables defined here are considered instance variables
        self.api_key = api_key
        self.tickers = tickers
        
    
    def alpha_vantage_get(self,function=None,symbol=None):
        
        url = 'https://www.alphavantage.co/query?function='+function+'&symbol='+symbol+'&apikey='+self.api_key
        r = requests.get(url)
        data = r.json()
        
        return data

    def get_overview(self):
        
        return_dict = {}
        
        for t in self.tickers:
            data = self.alpha_vantage_get(function="OVERVIEW",symbol=t)
            return_dict[t] = data
            
        self.overview = return_dict
            
        #return return_dict
        
         
    def get_balance_sheets(self):
        
        # list to store dataframes in
        dfs = []
        
        # for each ticker make a request
        # TODO add timer between requests based on level of alpha vantage API call volume allowed per minute
        for t in self.tickers:    
                        
            data = self.alpha_vantage_get(function='BALANCE_SHEET',symbol=t)
            
            # create a dataframe
            # TODO check for empty return
            df = pd.DataFrame.from_dict(data['annualReports'])
            
            # add symbol as field in dataframe
            df['ticker'] = t
            dfs.append(df)

        return_df = pd.concat(dfs)

        self.balance_sheets = return_df

        #return return_df
    
    


api_key = '296ULICGSB63VL7A'
sbs = Stonks(api_key, ['INTC', 'AMD']).get_balance_sheets()

print(sbs.get_overview().overview['AMD'])

#print(sbs['ticker'])

#sbo = Stonks(api_key,['INTC','AMD']).get_overview()
#print(sbo['AMD'])


