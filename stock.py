import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time as t
from analyze import *
import numpy as np
import yfinance as yf
import plotly.express as px
from plotly.subplots import *
from datetime import *
from pandas_datareader import data as pdr
import streamlit as st

#setting icon and name for the webpage.
st.set_page_config (page_title='Stock Market App',page_icon='st.ico',layout="wide",initial_sidebar_state="expanded")

# Creating the sidebar for Stock Market Data Analysis and Visualization
st.sidebar.markdown('''# :center[Stock Market Data Analysis and Visualization]''')
opt = st.sidebar.selectbox('****', options=('Performance', 'Difference using Facet_Area', 'Moving Averages','Closing Price','Daily Returns','co-relation','Risk'))

if opt == 'Performance':
    with st.spinner('Loading'):
        t.sleep(0.3)
    st.balloons()
    st.sidebar.title("Stock Market Performance")
    st.markdown(opt)
    st.info('''Stock Market Performance''', icon='📌')
    st.plotly_chart(fig)
    st.success('Success!')

elif opt == 'Difference using Facet_Area':
    with st.spinner('Loading'):
        t.sleep(0.3)
    st.balloons()
    st.write(opt)
    st.sidebar.title("Stock Price Difference Using Facet_Area" )
    st.info('''Stock Price Difference Using Facet_Area''', icon='👉')
    st.plotly_chart(fig1)

elif opt == 'Moving Averages':
    st.balloons()
    st.write(opt)
    st.sidebar.title("Moving Averages of Stock")
    st.info('''Moving Averages of Stock''', icon='👉')

    # Iterate over each group
    for company, group in grouped_data:
        # Display the tail of the moving averages
        st.write(f"Moving Averages for {company}")
        st.write(group[['MA10', 'MA20', 'MA30']].tail())

        # Create the line plot for the current company
        fig_line = px.line(group, x='Date', y=['Close', 'MA10', 'MA20', 'MA30'], title=f"{company} Moving Averages")

        # Display the plot using Streamlit
        st.plotly_chart(fig_line)


elif opt == 'Closing Price':
    with st.spinner('Loading'):
        t.sleep(0.3)
    st.balloons()
    st.sidebar.title("Closing Price of All Companies")
    st.markdown(opt)
    st.info('''Closing Price of All Companies.''', icon='📌')
   
# Iterate over each company and plot the closing prices
    for company_name, company_data in company_list:
       fig_l, ax = plt.subplots()
       ax.plot(company_data['Adj Close'])
       ax.set_ylabel('Adj Close',color='white')
       ax.set_title(f"Closing Price of {company_name}",color='white') 
       st.plotly_chart(fig_l)
       st.success('Success!')

elif opt == 'Daily Returns':
    with st.spinner('Loading'):
        t.sleep(0.3)
    st.balloons()
    st.sidebar.title("Daliy Returns of All Companies")
    st.markdown(opt)
    st.info('''Daily Returns of All Companies.''', icon='📌')
    
    # Create a figure with subplots for each company's histogram
    fig_u, axes = plt.subplots(2, 2, figsize=(12, 9))

    # Flatten the axes array
    axes = axes.flatten()

    for i, (company_name, company_data) in enumerate(company_list):
      company_data['Daily Return'] = company_data['Adj Close'].pct_change()
      axes[i].hist(company_data['Daily Return'], bins=50)
      axes[i].set_xlabel('Daily Return')
      axes[i].set_ylabel('Counts')
      axes[i].set_title(company_name)
      axes[i].tick_params()
    
    plt.tight_layout()

    # Display the figure in Streamlit
    st.pyplot(fig_u)

elif opt == 'co-relation':
    with st.spinner('Loading'):
        t.sleep(0.3)
    st.balloons()
    st.sidebar.title("Co-Relation of All Companies")
    st.markdown(opt)
    st.info('''Co-Relation of All Companies.''', icon='📌')
    st.title('Tech Stock Analysis')

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
          st.write("")

    # Make a new tech returns DataFrame
    tech_rets = closing_df.pct_change()

    # Display the tech returns DataFrame
    st.subheader('Tech Returns')
    st.dataframe(tech_rets.head())

    # Create a pair plot using seaborn
    st.subheader('Pair Plot of Co-relation')
    pairplot = sns.pairplot(tech_rets.dropna(), kind='reg')

    # Display the pair plot
    st.pyplot(pairplot.fig)

elif opt == 'Risk':
    with st.spinner('Loading'):
        t.sleep(0.3)
    st.balloons()
    st.sidebar.title("risk by investing")
    st.markdown(opt)
    st.info('''Risk by Investing''', icon='📌')

    # Drop rows with NaN values, if any
    rets = tech_rets.dropna()

    # Calculate area for scatter plot markers
    area = np.pi * 20

   # Create the scatter plot
    fig_p, ax = plt.subplots(figsize=(10, 8))
    ax.scatter(rets.mean(), rets.std(), s=area)

    # Set labels for x and y axes
    ax.set_xlabel('Expected return')
    ax.set_ylabel('Risk')

# Add annotations for each point on the plot
    for label, x, y in zip(rets.columns, rets.mean(), rets.std()):
      ax.annotate(label, xy=(x, y), xytext=(50, 0), textcoords='offset points', ha='right', va='bottom',
                arrowprops=dict(arrowstyle='-', color='blue', connectionstyle='arc3,rad=1'))
      
    st.pyplot(fig_p)
    

