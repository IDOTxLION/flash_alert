from pprint import pprint
import smtplib, ssl
import sys, re, logging
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



##!<import pandas as pd
##!<import matplotlib.pyplot as plt
from datetime import datetime

# Raw Package
import numpy as np
import pandas as pd
import argparse

#Data Source
import yfinance as yf

#Data viz
import plotly.graph_objs as go
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
t = "    "

ticker_list = ['BTC','XLM','MKR','BAT','DOGE','UNI',
               'XRP','WCFG','AAVE', 'ANKR', 'ANT',
               #'CRV',
               'SPELL', 
               #'COMP'
               #'SAND','XTZ',
             ]
#yf.download(tickers="BTC-USD",period="22 last hours",interval="15 mins")
#data = yf.download(tickers='BTC-USD', period = '60m', interval = '1m')
#data = yf.download(tickers = ticker_list ,period='1d', start='2023-07-10')


def data_dl():
  data = [
          yf.download(tickers = 'XLM-USD' ,period='1d', start='2023-01-13'),
          yf.download(tickers = 'MKR-USD' ,period='1d', start='2023-01-06'),
          yf.download(tickers = 'BAT-USD' ,period='1d', start='2023-01-26'),
          yf.download(tickers = 'DOGE-USD' ,period='1d', start='2023-07-31'),
          yf.download(tickers = 'UNI-USD' ,period='1d', start='2023-11-01'),
          yf.download(tickers = 'XRP-USD' ,period='1d', start='2023-11-13'),
          yf.download(tickers = 'WCFG-USD' ,period='1d', start='2023-11-21'),
          yf.download(tickers = 'AAVE-USD' ,period='1d', start='2023-11-29'),
          yf.download(tickers = 'ANKR-USD' ,period='1d', start='2023-11-29'),
          yf.download(tickers = 'ANT-USD' ,period='1d', start='2023-11-29'),
          #yf.download(tickers = 'CRV-USD' ,period='1d', start='2023-12-01'), #Diamond $0.52
          yf.download(tickers = 'SPELL-USD' ,period='1d', start='2023-12-01'),
          #yf.download(tickers = 'COMP-USD' ,period='1d', start='2023-12-05'), #Diamond $47.84
          #yf.download(tickers = 'SAND-USD' ,period='1d', start='2023-12-22'), 
          #yf.download(tickers = 'XTZ-USD' ,period='1d', start='2023-12-22'), #Diamond $0.92
          ]
  return data
def plot_graph():
  fig = go.Figure() 
  data = data_dl()
  
  for value, ticker in zip(data,ticker_list):
     fig.add_trace(go.Candlestick(x = value.index, open = value['Open'], high=value['High'], low=value['Low'], close=value['Close'], name = ticker ))
  
  
  fig.update_layout(title="Candlestick Chart for drop Multiple Stocks",
                    xaxis_title="Date",
                    yaxis_title="Stock Price",
                    xaxis_rangeslider_visible=True,
                    width=1500,  
                    height=800   
                    )
  
  fig.show()
def plot_graph_drop():
  fig = go.Figure() 
  data = data_dl()
  
  for value, ticker in zip(data,ticker_list):
     first_opening_price = round(value['Open'][0],5)
     latest_market_price = round(value['Close'][-1],5)
     stop_price = round(first_opening_price * 0.85, 5)
     limit_price = round(first_opening_price * 0.8, 5)
     roc = round(((latest_market_price - first_opening_price) / first_opening_price) * 100,5);
     if roc < 0:
        fig.add_trace(go.Candlestick(x = value.index, open = value['Open'], high=value['High'], low=value['Low'], close=value['Close'], name = ticker ))
        fig.add_trace(go.Scatter(x=value.index ,y=[stop_price], mode='markers', marker=dict(size=10), name='stop_price'))
        fig.add_trace(go.Scatter(x=value.index ,y=[limit_price], mode='markers', marker=dict(size=10), name='limit_price'))
  
  fig.update_layout(title="Candlestick Chart for drop Multiple Stocks",
                    xaxis_title="Date",
                    yaxis_title="Stock Price",
                    xaxis_rangeslider_visible=True,
                    width=1500,  
                    height=800   
                    )
  
  fig.show()

def plot_graph_hike():
  fig = go.Figure() 
  data = data_dl()
  
  for value, ticker in zip(data,ticker_list):
     first_opening_price = round(value['Open'][0],5)
     latest_market_price = round(value['Close'][-1],5)
     limit_price = round(first_opening_price * 1.6, 5)
     roc = round(((latest_market_price - first_opening_price) / first_opening_price) * 100,5);
     if roc > 0:
        print ( "[Crypto( "+ color.BOLD + ticker + color.END + ")] price hike: " + str(roc) + "%")
        fig.add_trace(go.Candlestick(x = value.index, open = value['Open'], high=value['High'], low=value['Low'], close=value['Close'], name = ticker))
        fig.add_trace(go.Scatter(x=value.index ,y=[limit_price], mode='markers', marker=dict(size=10), name='limit_price'))
  
  
  fig.update_layout(title="Candlestick Chart for hike Multiple Stocks",
                    xaxis_title="Date",
                    yaxis_title="Stock Price",
                    xaxis_rangeslider_visible=True,
                    width=1500,  
                    height=800   
                    )
  
  fig.show()
  


def Drop():
    drop_ticker={}
    content = ""
    for ticker, value in zip(ticker_list, data_dl()):
        first_opening_price = round(value['Open'][0],5)
        latest_market_price = round(value['Close'][-1],5)

        stop_price = round(first_opening_price * 0.85, 5)
        limit_price = round(first_opening_price * 0.8, 5)

        #(New Price - Old Price)/Old Price and then multiply that number by 100
        roc = round(((latest_market_price - first_opening_price) / first_opening_price) * 100,5);    

        #if latest_market_price < first_opening_price * 0.8:
        if roc < 0:
            price_drop = round(first_opening_price - latest_market_price,5)
            drop_ticker[ticker] = [roc,price_drop, limit_price,first_opening_price,latest_market_price,stop_price,]
            print ( "[Crypto ( "+ color.BOLD + ticker + color.END + ")] price drop: " + str(roc) + "%")
            content += ( "<p style = 'font-size: 25px;'>[Crypto( <b>" + ticker + "</b>)] price drop: " + str(roc) + "%" +
                  "   <br>"+t+t+"   Your first opening price was " + str(first_opening_price) +
                  "   <br>"+t+t+"   Your latest market price is " + str(latest_market_price) +
                  "   <br>"+t+t+"   Your price drop is " + str(price_drop) +
                  "   <br>"+t+t+"   Your stop price is " + str(stop_price)+
                  "   <br>"+t+t+"   Your limit price is " + str(limit_price)+
                  "<br>"
                  )
    return drop_ticker, content

 

def Hike():
    hike_ticker={}
    content = ""
    for ticker, value in zip(ticker_list, data_dl()):
        first_opening_price = round(value['Open'][0],5)
        latest_market_price = round(value['Close'][-1],5)

        
        limit_price = round(first_opening_price * 1.6, 5)

        #(New Price - Old Price)/Old Price and then multiply that number by 100
        roc = round(((latest_market_price - first_opening_price) / first_opening_price) * 100,5);    
        stop_price=0; #temp measure

        #if latest_market_price < first_opening_price * 0.8:
        if roc > 0:
            print ( "[Crypto( "+ color.BOLD + ticker + color.END + ")] price hike: " + str(roc) + "%")
            price_hike = round(latest_market_price - first_opening_price,5)
            hike_ticker[ticker] = [roc,price_hike, limit_price, first_opening_price,latest_market_price,stop_price]
            content += ("<p style = 'font-size: 25px;'>[Crypto( <b>" + ticker + "</b>)] price hike: " + str(roc) + "%" + 
                  "   <br>"+t+t+"  Your first opening price was " + str(first_opening_price) +
                  "   <br>"+t+t+"  Your latest market price is " + str(latest_market_price) +
                  "   <br>"+t+t+"  Your price hike is " + str(price_hike) +
                  "   <br>"+t+t+"  Your limit price is " + str(limit_price) +
                  "<br>")
    return hike_ticker, content  

def Sort():
    drop_ticker, _ = Drop() 
    hike_ticker, _ = Hike() 

    combined_data = {**drop_ticker, **hike_ticker}

    sorted_tickers = sorted(combined_data.items(), key=lambda x: x[1][0], reverse=True)

    content = ""
    for ticker, values in sorted_tickers:
        roc, price_change, limit_price, first_opening_price, latest_market_price, stop_limit = values
        change_type = "price hike" if roc >= 0 else "price drop"
        # Construct the content for each ticker
        content += ("<p style='font-size: 25px;'>[Uncovered Diamond( <b>{}</b>)] {}: {}%".format(ticker, change_type, roc) +
                    "<br>&nbsp;&nbsp;Your first opening price was " + str(first_opening_price) +
                    "<br>&nbsp;&nbsp;Your latest market price is " + str(latest_market_price) +
                    "<br>&nbsp;&nbsp;Your {} is ".format(change_type) + str(price_change) +
                    "<br>&nbsp;&nbsp;Your limit price is " + str(limit_price))
        if change_type == "price drop":
            content += "<br>&nbsp;&nbsp;Your stop price is " + str(stop_limit)
        content += "<br>" 
    return content



    

# fig.add_traces(go.Candlestick(x = data[4].index, open = data[4]['Open'], high=data[4]['High'], low=data[4]['Low'], close=data[4]['Close'], name = 'VSTM'))

# fig.show()

def RightNow():
    import datetime
    #current_time = datetime.datetime.now().strftime('%H:%M:%S')
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    return current_time

def send_email(email):  
  port = 465  # For SSL
  smtp_server = "smtp.gmail.com"
  sender_email = "aaleensyed20@gmail.com"  # Enter your address
  receiver_email = email  # Enter receiver address
  password = "xxmg qaps ojvn tmtg"
  
  msg = MIMEMultipart()
  msg['Subject'] = "[Uncovered Platinum(Crypto)] " + RightNow()
  msg['From'] = sender_email
  msg['To'] = receiver_email

  content = ""
  content += Hike() + "<br>"
  
  content += Drop()
  

   
  msg.attach(MIMEText(content, 'html'))
  context = ssl.create_default_context()

  with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
      server.login(sender_email, password)
      server.send_message(msg, from_addr=sender_email, to_addrs=receiver_email)


def main():
  parser = argparse.ArgumentParser(epilog="additional position arguments:\n  Specify variable overrides using <NAME>:<VALUE> syntax on command line.",description="Email or Plot Stock hike and drop",formatter_class=argparse.RawDescriptionHelpFormatter)
  #parser.add_argument("flow",metavar="FLOW",help="Required. Specify desired flow. Use --list_flows to see available flows",default="UNSPECIFIED",nargs="?")
  parser.add_argument("--email","-e",help="Specify your e-mail address", default=None)
  parser.add_argument("--plot","-p",help="Plot tickers on browser",action='store_true',default=False)
  parser.add_argument("--plot_drop","-pd",help="Plot tickers of drop on browser",action='store_true',default=False)
  parser.add_argument("--plot_hike","-ph",help="Plot tickers of hike on browser",action='store_true',default=False)

  args,option_overrides = parser.parse_known_args()
  logger = logging.getLogger("logger")
  # Check the option overrides array for any unknown arguments. Anything starting with a dash (-) is an unknown switch, not 
  # an override
  for o in option_overrides:
    if re.match(r'^-',o):
      logger.error("Unknown command line argument \"{}\"".format(o))
      parser.print_help()
      sys.exit(1)
  if args.plot:
     plot_graph()
  elif args.plot_drop:
     plot_graph_drop()
  elif args.plot_hike:
     plot_graph_hike()
  elif args.email:
     send_email(args.email)
     

  

if __name__ == "__main__":
     main()
     #send_email()
     #send_email2()



