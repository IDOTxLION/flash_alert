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


ticker_list = [
               'VIGAX', 'VTSAX', 'VLCAX',
               #'EYPT',
              #  'ISDR',
               #'RWLK', 
               #  'MRAM',
               'CASS',
               #'BWAY',
               'ITI','CYBN','MCRB','RMBL',
               #  'INGN','GMDA',
               'HUBC','OTLY', 'SENS','WATT','DAIO','CHRS',
              #  'NVTA',
              #  'MNMD',
               'TVTX','EKSO','ALIM','MASS',
               'ANEB','RSKD','ORIC','APLT','ATOS','ESPR','SPWR','RIGL','FVRR',
              ]


def data_dl():
  data = [
          # Note: Check the analyst price before selling 
          yf.download(tickers = 'VIGAX' ,period='1d', start='2021-12-30'), 
          yf.download(tickers = 'VTSAX' ,period='1d', start='2021-12-30'), 
          yf.download(tickers = 'VLCAX' ,period='1d', start='2023-12-08'), 
          #yf.download(tickers = 'EYPT' ,period='1d', start='2023-09-19'),  #sold on 11/27 at $5.90
          # yf.download(tickers = 'ISDR' ,period='1d', interval='1h', start=datetime(2023, 9, 20, 15, 30, 0)),  #$19.32, $19.32
          #yf.download(tickers = 'RWLK' ,period='1d', start='2023-09-21'), 
          # yf.download(tickers = 'MRAM' ,period='1d', start='2023-09-21'),  #$9.20, $9.15
          yf.download(tickers = 'CASS' ,period='1d', interval='1h', start=datetime(2023, 10, 2, 11, 30, 0)),  #$34.04, $36.52
          #yf.download(tickers = 'BWAY' ,period='1d', start='2023-10-03'), #sold on 11/20 at $4.87
          #yf.download(tickers = 'DAIO' ,period='1d', start='2023-10-16'), #sold on 11/30 at $2.90
          yf.download(tickers = 'ITI'  ,period='1d', interval='1h', start=datetime(2023, 10, 23, 11, 30, 0)),  #$4.05, $4.05
          yf.download(tickers = 'CYBN' ,period='1d', start='2023-11-10'),  #$0.64, $0.44
          yf.download(tickers = 'MCRB' ,period='1d', interval='1h', start=datetime(2023, 12, 1, 9, 32, 0)),  #$1.24, $0.99 
          yf.download(tickers = 'RMBL' ,period='1d', interval='1h', start=datetime(2023, 12, 4, 15, 35, 0)),  #$10.58, $5.67
          # yf.download(tickers = 'INGN' ,period='1d', interval='1h', start=datetime(2023, 12, 5, 14, 44, 0)),  #$10.30, $5.00
          #yf.download(tickers = 'GMDA' ,period='1d', interval='1h', start=datetime(2023, 12, 5, 14, 44, 0)),  #$3.30, $0.32
          yf.download(tickers = 'HUBC' ,period='1d', interval='1h', start=datetime(2023, 12, 6, 14, 44, 0)),  #$2.39, $0.25
          yf.download(tickers = 'OTLY' ,period='1d', interval='1h', start=datetime(2023, 12, 6, 12, 44, 0)),  #$0.87, $1.24
          yf.download(tickers = 'SENS' ,period='1d', interval='1h', start=datetime(2023, 12, 6, 14, 33, 0)),  #$0.52, $0.63
          yf.download(tickers = 'WATT' ,period='1d',  interval='1h', start=datetime(2023, 12, 12, 12, 11, 0)),  #$1.84
          yf.download(tickers = 'DAIO' ,period='1d',  interval='1h', start=datetime(2023, 12, 20, 11, 40, 0)), #$2.88
          yf.download(tickers = 'CHRS' ,period='1d',  interval='1h', start=datetime(2024, 1, 5, 9, 30, 0)),  #$2.76
          # yf.download(tickers = 'NVTA' ,period='1d',  interval='5m', start=datetime(2024, 1, 8, 9, 30, 0)),  #$0.49
          # yf.download(tickers = 'MNMD' ,period='1d',  interval='5m', start=datetime(2024, 1, 11, 9, 30, 0)),#$3.96
          yf.download(tickers = 'TVTX' ,period='1d',  interval='5m', start=datetime(2024, 2, 22, 9, 30, 0)),  #$7.79
          yf.download(tickers = 'EKSO' ,period='1d',  interval='5m', start=datetime(2024, 2, 28, 9, 30, 0)),  #$1.98
          yf.download(tickers = 'ALIM' ,period='1d',  interval='5m', start=datetime(2024, 2, 28, 9, 30, 0)),  #$3.38
          yf.download(tickers = 'MASS' ,period='1d',  interval='5m', start=datetime(2024, 2, 29, 9, 30, 0)),  #$7.42
          yf.download(tickers = 'ANEB' ,period='1d',  interval='5m', start=datetime(2024, 3, 5, 9, 30, 0)),   #2.73
          yf.download(tickers = 'RSKD' ,period='1d',  interval='5m', start=datetime(2024, 3, 6, 9, 30, 0)),   #5.32
          yf.download(tickers = 'ORIC' ,period='1d',  interval='5m', start=datetime(2024, 3, 27, 9, 30, 0)),   #13.35
          yf.download(tickers = 'APLT' ,period='1d',  interval='5m', start=datetime(2024, 3, 28, 9, 30, 0)),   #6.83
          yf.download(tickers = 'ATOS' ,period='1d',  interval='5m', start=datetime(2024, 3, 28, 9, 30, 0)),   #1.83
          yf.download(tickers = 'ESPR' ,period='1d',  interval='5m', start=datetime(2024, 4, 2, 9, 30, 0)),   #2.85
          yf.download(tickers = 'SPWR' ,period='1d',  interval='5m', start=datetime(2024, 4, 8, 9, 30, 0)),   #2.65
          yf.download(tickers = 'RIGL' ,period='1d',  interval='5m', start=datetime(2024, 4, 9, 9, 30, 0)),   #1.23
          yf.download(tickers = 'FVRR' ,period='1d',  interval='5m', start=datetime(2024, 4, 12, 9, 30, 0)),   #20.09
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
     first_opening_price = round(value['Open'][0],2)
     latest_market_price = round(value['Close'][-1],2)
     stop_price = round(first_opening_price * 0.85, 2)
     limit_price = round(first_opening_price * 0.8, 2)
     roc = round(((latest_market_price - first_opening_price) / first_opening_price) * 100,2);
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
     first_opening_price = round(value['Open'][0],2)
     latest_market_price = round(value['Close'][-1],2)
     limit_price = round(first_opening_price * 1.6, 2)
     roc = round(((latest_market_price - first_opening_price) / first_opening_price) * 100,2);
     if roc > 0:
        print ( "[Vanguard( "+ color.BOLD + ticker + color.END + ")] price hike: " + str(roc) + "%")
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
        first_opening_price = round(value['Open'][0],2)
        latest_market_price = round(value['Close'][-1],2)

        stop_price = round(first_opening_price * 0.85, 2)
        limit_price = round(first_opening_price * 0.8, 2)

        #(New Price - Old Price)/Old Price and then multiply that number by 100
        roc = round(((latest_market_price - first_opening_price) / first_opening_price) * 100,2);    

        #if latest_market_price < first_opening_price * 0.8:
        if roc < 0:
            price_drop = round(first_opening_price - latest_market_price,2)
            drop_ticker[ticker] = [roc,price_drop, limit_price,first_opening_price,latest_market_price,stop_price,]
            print ( "[Vanguard ( "+ color.BOLD + ticker + color.END + ")] price drop: " + str(roc) + "%")
            content += ( "<p style = 'font-size: 25px;'>[Vanguard( <b>" + ticker + "</b>)] price drop: " + str(roc) + "%" +
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
        first_opening_price = round(value['Open'][0],2)
        latest_market_price = round(value['Close'][-1],2)
        
        #if 'ISDR' in ticker:
        #print(ticker, value)
        
        limit_price = round(first_opening_price * 1.6, 2)
        stop_price=0; #temp measure

        #(New Price - Old Price)/Old Price and then multiply that number by 100
        roc = round(((latest_market_price - first_opening_price) / first_opening_price) * 100,2);    
        
        #if latest_market_price < first_opening_price * 0.8:
        if roc >= 0:
            print ( "[Vanguard( "+ color.BOLD + ticker + color.END + ")] price hike: " + str(roc) + "%")
            price_hike = round(latest_market_price - first_opening_price,2)
            hike_ticker[ticker] = [roc,price_hike, limit_price, first_opening_price,latest_market_price,stop_price]
            content += ("<p style = 'font-size: 25px;'>[Vanguard( <b>" + ticker + "</b>)] price hike: " + str(roc) + "%" + 
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
    content = ""
    for ticker,values in sorted(combined_data.items(), key=lambda x: x[1][0], reverse=True): #(k,v) tuple
       #print ("DEBUG TICKER", k)
       #print ("DEBUG V",v)

    #sorted_tickers = sorted(combined_data.items(), key=lambda x: x[1][0], reverse=True)
    
    
    #for ticker, values in sorted_tickers:
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
  msg['Subject'] = "[Vanguard(tickers)] " + RightNow() 
  msg['From'] = sender_email
  msg['To'] = receiver_email

  content = ""
  #content += Hike() + "<br>"
  #content += Drop()
  content += Sort()
  

   
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



