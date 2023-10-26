import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
import plotly.express as px
from plotly.subplots import *
from datetime import *
from pandas_datareader import data as pdr
import streamlit as st
import pandas as pd
import plotly.express as px

# Load your data into a Pandas DataFrame
f_name=r"C:\Users\RAMYASRI\Downloads\stocks\stocks.csv"
data=pd.read_csv(f_name)
# Calculate moving averages


print("******** FIRST 5 VALUES OF DATA ********")
print(data.head())
print("******** LAST 5 VALUES OF DATA ********")
print(data.tail())
print("******** UNIQUE VALUES IN TICKER CoLUMN ********")
print(data.Ticker.unique())

'''change the values in TIcker to the company Names'''

data['Ticker'].replace(['AAPL','MSFT','NFLX','GOOG'],['APPLE','MICROSOFT','NETFLIX','GOOGLE'],inplace=True)
print("******** UNIQUE VALUES IN TICKER COLUMN ********")
print(data.Ticker.unique())

'''changing Ticker Column name to the Company_Names'''

data.rename(columns={'Ticker':'Company_Name'},inplace=True)
print('******** BREIF INFO OF DATASET********')
print(data.info())




''' to identify trends and patterns in each company’s stock price movements'''

data['MA10'] = data.groupby('Company_Name')['Close'].rolling(window=10).mean().reset_index(0,drop=True)
data['MA20'] = data.groupby('Company_Name')['Close'].rolling(window=20).mean().reset_index(0,drop=True)
data['MA30'] = data.groupby('Company_Name')['Close'].rolling(window=30).mean().reset_index(0,drop=True)
for company, group in data.groupby('Company_Name'):
    print(f'Moving Averages for {company}')
    print(group[['MA10', 'MA20','MA30']])

# Calculate moving averages
data['MA10'] = data.groupby('Company_Name')['Close'].rolling(window=10).mean().reset_index(0, drop=True)
data['MA20'] = data.groupby('Company_Name')['Close'].rolling(window=20).mean().reset_index(0, drop=True)
data['MA30'] = data.groupby('Company_Name')['Close'].rolling(window=30).mean().reset_index(0, drop=True)

# Create the line plot using Plotly Express
fig = px.line(data, x='Date', y='Close', color='Company_Name', title='Stock market performance by last 3 months')

# differece of Stock market performance using facet_Area.
fig1 = px.area(data, x='Date', y='Close', color='Company_Name', facet_col='Company_Name',
               labels={'Date':'Date', 'Close':'Closing_price', 'Company_Name':'Company'})

# Retrieve the adjusted close prices for the tech companies from Yahoo Finance
tech_list = ['AAPL', 'MSFT', 'NFLX', 'GOOGL']
start = data['Date'].min()
end = data['Date'].max()
closing_df = pd.DataFrame()

for ticker in tech_list:
       try:
          stock_data = yf.download(ticker, start=start, end=end)['Adj Close']
          closing_df[ticker] = stock_data
       except Exception as e:
          st.write(f"Failed to download data for {ticker}: {e}")

# Make a new tech returns DataFrame
tech_rets = closing_df.pct_change()

# Group the data by Company_Name
grouped_data = data.groupby('Company_Name')

 # Group the data by company names
company_list = data.groupby('Company_Name')
