# Alpha

A python module for interacting with alpha vantage and building basic plots with plotly, with a long term goal of becoming a robust investment anlaysis module.

## Equities
***
Construct the equities class like so:

```python
api_key = 'your premium api key'

tickers = ['AMZN', 'GOOG', 'AAPL','VB']

equities = a.Equities(api_key=api_key, tickers=tickers)
```

Note: some methods only work with a premium apikey.


### Get cashflow data
```python
cf = equities.get_cashflow()
```

### Build cashflow subplot
```python
fig = equities.cashflow_subplot()
fig.show()
```

### Get timeseries adjusted data
```python
fig = equities.cashflow_subplot()
fig.show()
```

### Build equity subplot
```python
start_end_dates = ('2018-01-01', '2022-10-07')
fig = equities.daily_adjusted_subplot(start_end_dates=start_end_dates, output_size='full')
fig.show()
```


## Economics
***
Construct the economics class like so:

```python
econ = a.Economics(api_key)
```

### Get 10-year treasury yield data
```python
ty_ten = econ.treasury_yield()
```

### Get 7-year treasury yield data
```python
ty_seven = econ.treasury_yield(maturity='7year')
```

### Get 2-year treasury yield data
```python
ty_two = econ.treasury_yield(maturity='2year')
```

### Get real gdp
```python
rgdp = econ.real_gdp()
```

### Get nonfarm payroll
```python
nfpr = econ.nonfarm_payroll()
```

### Get federal funds rate
```python
ffr = econ.federal_funds_rate()
```

### Get consumer price index
```python
cpi = econ.cpi()
```