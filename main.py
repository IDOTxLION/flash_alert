##!<importpandasaspd
##!<importmatplotlib.pyplotasplt
##!<fromdatetimeimportdatetime

#RawPackage
import numpy as np
import pandas as pd

#DataSource
import yfinance as yf

#Dataviz
import plotly.graph_objs as go

#yf.download(tickers="BTC-USD",period="22lasthours",interval="15mins")
data=yf.download(tickers='BTC-USD',period='60m',interval='1m')
#data=yf.download(tickers='BTC-USD',period='22h',interval='1m')

print(data)
print("max:",data['Open'].max(),"min:",data['Open'].min())
print("max:",data['Open'].idxmax(),"min:",data['Open'].idxmin())

highest_open = data['Open'].idxmax()
lowest_open = data['Open'].idxmin()

fig = go.Figure()


fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='market data') )


fig.add_trace(go.Scatter(x=[highest_open], y=[data.loc[highest_open, 'Open']], mode='markers', marker=dict(color='blue'), name='Highest Opening'))
fig.add_trace(go.Scatter(x=[lowest_open], y=[data.loc[lowest_open, 'Open']], mode='markers', marker=dict(color='maroon'), name='Lowest Opening'))



fig.update_xaxes(
rangeslider_visible=True,
rangeselector=dict(
buttons=list([
#dict(count=1,label='1m',step='minute',stepmode='backward'),
dict(count=15,label='15m',step='minute',stepmode='backward'),
dict(count=45,label='45m',step='minute',stepmode='backward'),
#dict(count=60,label='1h',step='minute',stepmode='backward'),
#dict(count=360,label='6h',step='minute',stepmode='backward'),
dict(count=1,label='1h',step='hour',stepmode='backward'),
dict(count=6,label='6h',step='hour',stepmode='backward'),
dict(step='all')
])
)
)

fig.show()