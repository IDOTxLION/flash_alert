from pprint import pprint
import smtplib, ssl
from email.message import EmailMessage
##!<import pandas as pd
##!<import matplotlib.pyplot as plt
##!<from datetime import datetime

# Raw Package
import numpy as np

#Data Source
import yfinance as yf

#Data viz
import plotly.graph_objs as go

ticker_list = ['DCTH', 'RELL', 'WATT','MCRB','SENS']

def data_dl():
  '''
  data2 = [
          yf.download(tickers = 'RWLK' ,period='1d', start='2020-08-25'), 
          yf.download(tickers = 'ITI'  ,period='1d', start='2023-08-24'), 
          yf.download(tickers = 'MRAM' ,period='1d', start='2023-08-28'), 
          yf.download(tickers = 'ISDR' ,period='1d', start='2023-08-29'), 
          yf.download(tickers = 'EYPT' ,period='1d', start='2023-08-30'), 
          yf.download(tickers = 'CASS' ,period='1d', start='2023-09-08'), 
          yf.download(tickers = 'BWAY' ,period='1d', start='2023-09-15'), 
          yf.download(tickers = 'DAIO' ,period='1d', start='2022-09-15'), 
          yf.download(tickers = 'CYBN' ,period='1d', start='2023-11-01'), 
                                                                          
          yf.download(tickers = 'DCTH' ,period='1d', start='2023-09-25'),          
          yf.download(tickers = 'RELL' ,period='1d', start='2023-10-04'), 
          yf.download(tickers = 'WATT' ,period='1d', start='2023-11-02'), 
          yf.download(tickers = 'MCRB' ,period='1d', start='2023-11-03'), 
          yf.download(tickers = 'SENS' ,period='1d', start='2023-11-14'), 
          ]
  '''
  data = [
          yf.download(tickers = 'DCTH' ,period='1d', start='2023-09-25'),          
          yf.download(tickers = 'RELL' ,period='1d', start='2023-10-04'), 
          yf.download(tickers = 'WATT' ,period='1d', start='2023-11-02'), 
          yf.download(tickers = 'MCRB' ,period='1d', start='2023-11-03'), 
          yf.download(tickers = 'SENS' ,period='1d', start='2023-11-14'), 
          ]
  return data

def send_email2(first_opening_price, latest_market_price, price_drop, roc, ticker):
  port = 465  # For SSL
  smtp_server = "smtp.gmail.com"
  sender_email = "aaleensyed20@gmail.com"  # Enter your address
  receiver_email = "abbmir@gmail.com"  # Enter receiver address
  password = "txpw qshd uhvk fdgu"
  
  stop_price = round(first_opening_price * 0.85, 2)
  limit_price = round(first_opening_price * 0.8, 2)

  msg = EmailMessage()
  msg.set_content("Hi \n" + "Your first opening price was " + str(first_opening_price) +
                  "   \n" + "Your latest market price is " + str(latest_market_price) +
                  "   \n" + "Your price drop is " + str(price_drop) +
                  "   \n" + "Your stop price is " + str(stop_price) +
                  "   \n" + "Your limit price is " + str(limit_price))

  msg['Subject'] = "[Uncovered Diamond(" + ticker + ")] price drop: " + str(roc) + "%"
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
  
  stop_price = round(first_opening_price * 1.6, 2)
  limit_price = round(first_opening_price * 1.7, 2)

  msg = EmailMessage()
  msg.set_content("Hi \n" + "Your first opening price was " + str(first_opening_price) +
                  "   \n" + "Your latest market price is " + str(latest_market_price) +
                  "   \n" + "Your price hike is " + str(price_hike) +
                  "   \n" + "Your stop price is " + str(stop_price) +
                  "   \n" + "Your limit price is " + str(limit_price))
  msg['Subject'] = "[Uncovered(" + ticker + ")] price hike: " + str(roc) + "%"
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
        first_opening_price = line['Open'][0]
        latest_market_price = line['Close'][-1]
        
        #(New Price - Old Price)/Old Price and then multiply that number by 100
        roc = ((latest_market_price - first_opening_price) / first_opening_price) * 100;    

        #if(latest_market_price < first_opening_price*0.8):
        if roc < 0:
           print("Opening price drop found on ticker ", ticker)
           price_drop = first_opening_price - latest_market_price
           send_email2( round(first_opening_price,3),round(latest_market_price,3),round(price_drop,3), round(roc,3), ticker)
        #if(latest_market_price * 0.90 > first_opening_price):
        if roc >= 0:
           print("Opening price hike found on ticker ", ticker)
           price_hike = latest_market_price - first_opening_price
           send_email3( round(first_opening_price,3),round(latest_market_price,3),round(price_hike,3), round(roc,3), ticker)
        
        #fig.add_trace(go.Candlestick(x = line.index, open = line['Open'], high=line['High'], low=line['Low'], close=line['Open'], name = ticker ))

      # fig.add_trace(go.Candlestick(
      #     x=list.index[n:],  
      #     open=list['Open'], 
      #     high=list['High'], 
      #     low=list['Low'], 
      #     close=list['Close'], 
      #     name=ticker
      
      # ))
      
  
  
  
#   fig.update_traces(selector=dict(name = 'APRN'),  increasing_line=dict(color='indigo'),   increasing_fillcolor = 'indigo',    decreasing_line=dict(color='firebrick'),  decreasing_fillcolor = 'firebrick')
                    
  
  
  
  #fig.update_layout(title="Candlestick Chart for Multiple Stocks",
  #                  xaxis_title="Date",
  #                  yaxis_title="Stock Price",
  #                  xaxis_rangeslider_visible=True)
  
  
  #fig.show()

if __name__ == "__main__":
     main()
     #send_email()
     #send_email2()



