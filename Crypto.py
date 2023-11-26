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

ticker_list = ['XLM','MKR','BAT','XTZ','DOGE','UNI','CRV','XRP','WCFG']
#yf.download(tickers="BTC-USD",period="22 last hours",interval="15 mins")
#data = yf.download(tickers='BTC-USD', period = '60m', interval = '1m')
#data = yf.download(tickers = ticker_list ,period='1d', start='2023-07-10')

def data_dl():
  data = [
          yf.download(tickers = 'XLM-USD' ,period='1d', start='2023-01-13'),
          yf.download(tickers = 'MKR-USD' ,period='1d', start='2023-01-06'),
          yf.download(tickers = 'BAT-USD' ,period='1d', start='2023-01-26'),
          yf.download(tickers = 'XTZ-USD' ,period='1d', start='2023-02-02'),
          yf.download(tickers = 'DOGE-USD' ,period='1d', start='2023-01-12'),
          yf.download(tickers = 'UNI-USD' ,period='1d', start='2023-01-12'),
          #yf.download(tickers = 'COMP-USD' ,period='1d', start='2023-01-12'),
          yf.download(tickers = 'CRV-USD' ,period='1d', start='2023-01-12'),
          yf.download(tickers = 'XRP-USD' ,period='1d', start='2023-01-12'),
        
        
          
          
          ]
  return data


    
def send_email2(first_closing_price, price_drop, crypto):
  port = 465  # For SSL
  smtp_server = "smtp.gmail.com"
  sender_email = "aaleensyed20@gmail.com"  # Enter your address
  receiver_email = "abbmir@gmail.com"  # Enter receiver address
  #password = 'stct gxna upbz hofd'
  password = "txpw qshd uhvk fdgu"
  
  stop_price = round(first_opening_price * 0.85, 2)
  limit_price = round(first_opening_price * 0.8, 2)

  msg = EmailMessage()
  msg.set_content("Hi \n" + "Your first closing price was " + str(first_closing_price))
  msg['Subject'] = crypto + " price drop: " + str(price_drop)
  msg['From'] = sender_email
  msg['To'] = receiver_email
  
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
      server.login(sender_email, password)
      server.send_message(msg, from_addr=sender_email, to_addrs=receiver_email)

def send_email3(first_opening_price, latest_market_price, price_hike, roc, ticker):
  port = 465  # For SSL
  smtp_server = "smtp.gmail.com"
  sender_email = "aaleensyed20@gmail.com"  # Enter your address
  receiver_email = "abbmir@gmail.com"  # Enter receiver address
  password = "txpw qshd uhvk fdgu"
  
  limit_price = round(first_opening_price * 1.6, 2)

  msg = EmailMessage()
  msg.set_content("Hi \n" + "Your first opening price was " + str(first_opening_price) +
                  "   \n" + "Your latest market price is " + str(latest_market_price) +
                  "   \n" + "Your price hike is " + str(price_hike) +
                  "   \n" + "Your sell limit price is " + str(limit_price))
  msg['Subject'] = "[Crypto(" + ticker + ")] price hike: " + str(roc) + "%"
  msg['From'] = sender_email
  msg['To'] = receiver_email
  
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
      server.login(sender_email, password)
      server.send_message(msg, from_addr=sender_email, to_addrs=receiver_email)

# fig.add_traces(go.Candlestick(x = data[4].index, open = data[4]['Open'], high=data[4]['High'], low=data[4]['Low'], close=data[4]['Close'], name = 'VSTM'))

# fig.show()
t = -1
dip = False
fig = go.Figure()


def main():
  data = data_dl()
  for line, ticker in zip(data,ticker_list):
       # starting_price = line['Close'][0]  
        #ending_price = line['Close'][-1]   

        #for o in line['Open']:
        #   print (str(o) + " for " + ticker)

        #if ending_price < starting_price:
        first_closing_price = line['Close'][0]
        latest_closing_price = line['Close'][-1]
        if(latest_closing_price < first_closing_price*0.8):
           price_drop = first_closing_price - latest_closing_price
           send_email2( first_closing_price,price_drop, crypto)


           


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



