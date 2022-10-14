# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 05:49:11 2022
@author: Korey

Description:
    This is a script for running test scripts for the economics module. To
    execute this script go to a cli or conda and navigate to this directory.
    Then run the script as follows:
        {python version} -m unittest alpha_test.py
        

"""

import unittest
from core import core_api as a
from core import subplots

# TODO - pass api_key as an arg

class TestAlpha(unittest.TestCase):

    def test_real_gdp_no_df(self):
        econ = a.Economics(api_key='296ULICGSB63VL7A')
        r = econ.real_gdp(dataframe=False)
        self.assertIn('data', r)

    def test_real_gdp_df(self):
        econ = a.Economics(api_key='296ULICGSB63VL7A')
        r = econ.real_gdp(dataframe=True)
        self.assertIsInstance(r.shape, tuple)
        
    def test_retail_sales_df(self):
        econ = a.Economics(api_key='296ULICGSB63VL7A')
        r = econ.retail_sales(dataframe=True)
        self.assertIsInstance(r.shape, tuple)
        
    def test_retail_sales_no_df(self):
        econ = a.Economics(api_key='296ULICGSB63VL7A')
        r = econ.retail_sales(dataframe=False)
        self.assertIsInstance(r, dict)
        
    def test_inflation_df(self):
        econ = a.Economics(api_key='296ULICGSB63VL7A')
        r = econ.retail_sales(dataframe=True)
        self.assertIsInstance(r.shape, tuple)
        
    def test_inflation_no_df(self):
        econ = a.Economics(api_key='296ULICGSB63VL7A')
        r = econ.retail_sales(dataframe=False)
        self.assertIsInstance(r, dict)
        
    def test_cpi_df(self):
        econ = a.Economics(api_key='296ULICGSB63VL7A')
        r = econ.cpi()
        self.assertIsInstance(r.shape, tuple)
           
    def test_cpi_no_df(self):
        econ = a.Economics(api_key='296ULICGSB63VL7A')
        r = econ.cpi(dataframe=False)
        self.assertIsInstance(r, dict)
    
    def test_cpi_semiannual(self):
        econ = a.Economics(api_key='296ULICGSB63VL7A')
        r = econ.cpi(interval='semiannual')
        self.assertIsInstance(r.shape, tuple)
        
    
    
    # TODO add:
        # econ.treasury_yield
        # econ.consumer_sentiment
        # econ.nonfarm_payroll
        # econ.federal_funds_rate
        # econ.real_gdp
        # equities.get_time_series_daily
        # equities.subplot
        
        
    def test_alpha_subplot_rendererror(self):
        with self.assertRaises(ValueError):
            subplots.build_subplots(data='',render_type='error')
    
        


        
if __name__ == '__main__':
    unittest.main()    
