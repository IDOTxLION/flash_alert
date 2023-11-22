from pprint import pprint
import smtplib, ssl
from email.message import EmailMessage



##!<import pandas as pd
##!<import matplotlib.pyplot as plt
##!<from datetime import datetime

# Raw Package
import numpy as np
import pandas as pd


#Data Source
import yfinance as yf

#Data viz
import plotly.graph_objs as go

crypto_list = ['XLM','MKR','BAT','XTZ','DOGE','UNI','CRV','XRP']
#yf.download(tickers="BTC-USD",period="22 last hours",interval="15 mins")
#data = yf.download(tickers='BTC-USD', period = '60m', interval = '1m')
#data = yf.download(tickers = ticker_list ,period='1d', start='2023-07-10')

def data_dl():
  data = [
          yf.download(tickers = 'XLM-USD' ,period='1d', start='2023-01-12'),
          yf.download(tickers = 'MKR-USD' ,period='1d', start='2023-01-06'),
          yf.download(tickers = 'BAT-USD' ,period='1d', start='2023-01-26'),
          yf.download(tickers = 'XTZ-USD' ,period='1d', start='2023-02-02'),
          yf.download(tickers = 'DOGE-USD' ,period='1d', start='2023-07-31'),
          yf.download(tickers = 'UNI-USD' ,period='1d', start='2023-11-12'),
          #yf.download(tickers = 'COMP-USD' ,period='1d', start='2023-01-12'),
          yf.download(tickers = 'CRV-USD' ,period='1d', start='2023-11-12'),
          yf.download(tickers = 'XRP-USD' ,period='1d', start='2023-11-12'),
          ]
  return data


    
def send_email2(first_closing_price, latest_closing_price, price_drop, crypto):
  port = 465  # For SSL
  smtp_server = "smtp.gmail.com"
  sender_email = "aaleensyed20@gmail.com"  # Enter your address
  receiver_email = "abbmir@gmail.com"  # Enter receiver address
  password = "epfb ajgv pzgw rlle"
  
  msg = EmailMessage()
  msg.set_content("Hi \n" + "Your first closing price was " + str(first_closing_price) + ' to '+ str(latest_closing_price))
  msg['Subject'] = crypto + " price drop: " + str(price_drop)
  msg['From'] = sender_email
  msg['To'] = receiver_email
  
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
      server.login(sender_email, password)
      server.send_message(msg, from_addr=sender_email, to_addrs=receiver_email)


# n=0
# for line in data:
#     print(ticker_list[n],line)
#     n+=1


#fig = go.Figure(data = go.Candlestick(x = data[0].index, open = data[0]['Open'], high=data[0], low=data[0], close=data[0], name = 'market data'))
# fig = go.Figure()
# fig.add_trace(go.Candlestick(x = data[0].index, open = data[0]['Open'], high=data[0]['High'], low=data[0]['Low'], close=data[0]['Close'], name = 'HGEN' ))
# fig.add_traces(go.Candlestick(x = data[1].index, open = data[1]['Open'], high=data[1]['High'], low=data[1]['Low'], close=data[1]['Close'], name = 'INGN'))
# fig.add_traces(go.Candlestick(x = data[2].index, open = data[2]['Open'], high=data[2]['High'], low=data[2]['Low'], close=data[2]['Close'], name = 'VSTM'))
# fig.add_traces(go.Candlestick(x = data[3].index, open = data[3]['Open'], high=data[3]['High'], low=data[3]['Low'], close=data[3]['Close'], name = 'KSCP'))
# fig.add_traces(go.Candlestick(x = data[4].index, open = data[4]['Open'], high=data[4]['High'], low=data[4]['Low'], close=data[4]['Close'], name = 'VSTM'))

# fig.show()
t = -1
dip = False
fig = go.Figure()


def main():
  data = data_dl()
  for line, crypto in zip(data,crypto_list):
       # starting_price = line['Close'][0]  
        #ending_price = line['Close'][-1]   
    
        #if ending_price < starting_price:
        first_closing_price = line['Close'][0]
        latest_closing_price = line['Close'][-1]
        if(latest_closing_price < first_closing_price*0.8):
           price_drop = first_closing_price - latest_closing_price
           send_email2( first_closing_price,latest_closing_price,price_drop, crypto)


           


        #print("DEBUG ", ticker , " ", first_closing_price, " ", latest_closing_price)
       
        
        fig.add_trace(go.Candlestick(x = line.index, open = line['Open'], high=line['High'], low=line['Low'], close=line['Close'], name = crypto ))



  
  
  fig.update_layout(title="Candlestick Chart for Multiple Stocks",
                    xaxis_title="Date",
                    yaxis_title="Stock Price",
                    xaxis_rangeslider_visible=True)
  
  
  #fig.show()

if __name__ == "__main__":
     main()
     #send_email()
     #send_email2()



