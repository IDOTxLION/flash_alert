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
               'NNDM', 'OPTT', 
               # DELISTED 'RWLK', 
               'CLSK', 'LTRX', 'MARA', 'PXLW', 'MOSYX','TXT',
               #'GMDA',
               'SCYX', 
               #'EKSO', 
               'STXS',
               #'HUBC',
               'KSCP','VSTM','INGN','AMSC',
               #'RMBL','ALIM', 
               'DTIL',
               #'ITI',
               'MRAM','ISDR','EYPT',
               #'CASS',
               'BWAY','DCTH',
               #'RELL','CYBN','DAIO', ???, 'WATT','MCRB','SENS','OTLY', 'TVTX', 
               'XOMA',
               #'ANEB', 
               'EVGO', 
               #'CHRS', 'NVTA',
               'MNMD', 'REAL',
               #'MASS', 
               'PHAT', 
               #'APLT','ORIC','ATOS',
               'ESPR',
               #Sell GMDA 
               # DELISTED 'SPWR',
               'RIGL',
               'FVRR',
               'RCAT',
               'PLL',
               'ASPN',
               'AGEN', 'WULF',
               'BTDR',
               #Sell MRAM , PXLW'
               'DM',
               #Sell HUBC, ISDR, RMBL, , TRT'
               'ARBK', 'HUT', 'SDIG',
               #Sell DAIO , MCRB',
               'ABCL', 'MKFG,', 
               # DELISTED 'VLD',
               #Sell LTRX'
               #Sell ALIM'
               'OPAD',
               'ARDX',
               'FLGT', 'LASR',
               #Sell ITI'
               #Sell SPWR'
               'ADPT',
               #Sell SDIG'
               'IRBT',
               #Sell AMSC, KSCP, , WATT'
               'FEIM', 'NEON',
               'UAMY',
               #Sell VLDX'
               #Sell CYBN , MKFG'
               #Sell MNMD , OTLY'
               'ARAY', 'ZVRA,', 'ZYME',
               #Sell ANEB, CHRS, , DTIL'
               #Sell AGEN, ATOS, ORIC, RCAT, , VSTM'
               #Sell MASS'
               'BLND',
               #Sell NEON'
               #Sell BWAY'
               'PPTA',
               'CLOV',
               'EOSE', 'WGS',
               'AXTI',
               #Sell PHAT'
               #Sell ABCL, CASS, EVGO, , FLGT'
               'CHGG',
               #Sell FVRR'
               'LNSR',
               #Sell REAL for a Gain'
               'AMPH',
               #Sell OPTT'
               'ANY',
               'BCOV',
               #Sell ASPN, CLOV, EOSE, , INGN'
               'EXFY', 'XGN',
               #Sell APLT'
               #Sell ARBK'
               'ITRM',
               #Sell AMPH, AXTI, , LASR'
               'MYO', 'XERS',
               #Sell ANY , ARAY'
               'CLPT',
               'BFLY',
               ]

def data_dl():
  data = [
          yf.download(tickers = 'NNDM' ,period='1d', start='2020-06-02'),  #$1.79
          yf.download(tickers = 'OPTT' ,period='1d', start='2020-06-16'),  #$1.79
          #DELISTED yf.download(tickers = 'RWLK' ,period='1d', start='2020-08-25'),  #$1.79
          yf.download(tickers = 'CLSK' ,period='1d', start='2020-09-08'),  #$1.79
          yf.download(tickers = 'LTRX' ,period='1d', start='2020-09-23'),  #$1.79
          yf.download(tickers = 'MARA' ,period='1d', start='2020-09-25'),  #$1.79
          yf.download(tickers = 'PXLW' ,period='1d', start='2020-11-06'),  #$1.79
          yf.download(tickers = 'MOSYX' ,period='1d', start='2020-08-04'),  #$1.79
          yf.download(tickers = 'TXT' ,period='1d', start='2021-12-22'),  #$1.79
          #yf.download(tickers = 'GMDA' ,period='1d', start='2022-03-01'),  #$3.30, $0.32
          yf.download(tickers = 'SCYX' ,period='1d', start='2022-03-16'),  #$1.79
          #yf.download(tickers = 'EKSO' ,period='1d', start='2023-01-10'),  #$1.79
          yf.download(tickers = 'STXS' ,period='1d', start='2023-02-17'),  #$1.79
          #yf.download(tickers = 'HUBC' ,period='1d', start='2023-03-20'),  #$2.39, $0.25
          yf.download(tickers = 'KSCP' ,period='1d', start='2023-05-26'),  #$1.79
          yf.download(tickers = 'VSTM' ,period='1d', start='2020-06-20'),  #$1.79
          yf.download(tickers = 'INGN' ,period='1d', start='2023-06-27'),  #$10.30, $5.00
          yf.download(tickers = 'AMSC' ,period='1d', start='2023-07-27'),  #$1.79
          #yf.download(tickers = 'RMBL' ,period='1d', start='2023-08-01'),  #$10.58, $5.67
          #yf.download(tickers = 'ALIM' ,period='1d', start='2023-08-15'),  #$3.22
          yf.download(tickers = 'DTIL' ,period='1d', start='2023-08-18'),  #$1.79
          #yf.download(tickers = 'ITI' ,period='1d',  interval='1h', start=datetime(2023, 11, 2, 15, 30, 0)),  #$1.84
          yf.download(tickers = 'MRAM' ,period='1d', start=datetime(2023, 11, 2, 15, 30, 0)),  #$1.84
          yf.download(tickers = 'ISDR' ,period='1d', start=datetime(2023, 11, 2, 15, 30, 0)),  #$1.84
          yf.download(tickers = 'EYPT' ,period='1d', start=datetime(2023, 9, 19, 15, 30, 0)),  #sold on 11/27 at $5.90
          #yf.download(tickers = 'CASS' ,period='1d',  interval='1h', start=datetime(2023, 11, 2, 15, 30, 0)),  #$1.84
          yf.download(tickers = 'BWAY' ,period='1d', start=datetime(2023, 10, 3, 15, 30, 0)), #sold on 11/20 at $4.87
          yf.download(tickers = 'DCTH' ,period='1d', start=datetime(2023, 9, 25, 15, 30, 0)),  #$3.87, $2.61        
          #yf.download(tickers = 'RELL' ,period='1d',  interval='1h', start=datetime(2023, 10, 4, 15, 30, 0)),  #$9.84, $10.84 -- SELL on 1/11/24
          #yf.download(tickers = 'CYBN' ,period='1d',  interval='1h', start=datetime(2023, 10, 4, 15, 30, 0)),  #$9.84, $10.84
          #yf.download(tickers = 'DAIO' ,period='1d',  interval='1h', start=datetime(2023, 10, 16, 15, 30, 0)), #sold on 11/30 at $2.90
                                                                          #placed on 12/4 at $2.88 
          #yf.download(tickers = 'WATT' ,period='1d',  interval='1h', start=datetime(2023, 11, 2, 15, 30, 0)),  #$1.84
          #yf.download(tickers = 'MCRB' ,period='1d', start='2023-11-03'), #$1.24, $0.99
          #yf.download(tickers = 'SENS' ,period='1d', start='2023-11-14'),  #$0.52, $0.63
          #yf.download(tickers = 'OTLY' ,period='1d', start='2023-12-01'),  #$0.87, $1.24
          #yf.download(tickers = 'TVTX' ,period='1d',  interval='1h', start=datetime(2023, 12, 6, 11, 8, 0)),  #$7.96
          yf.download(tickers = 'XOMA' ,period='1d', start=datetime(2023, 12, 12, 11, 8, 0)),  #$14.72
          #yf.download(tickers = 'ANEB' ,period='1d',  interval='1h', start=datetime(2023, 12, 19, 9, 30, 0)),  #$1.84
          yf.download(tickers = 'EVGO' ,period='1d', start=datetime(2024, 1, 2, 9, 30, 0)),  #$3.22
          #yf.download(tickers = 'CHRS' ,period='1d',  interval='5m', start=datetime(2024, 1, 5, 9, 30, 0)),  #$2.76
          #yf.download(tickers = 'NVTA' ,period='1d',  interval='5m', start=datetime(2024, 1, 8, 9, 30, 0)),  #$0.49 -- SELL on 2/16/24
          yf.download(tickers = 'MNMD' ,period='1d', start=datetime(2024, 1, 11, 9, 30, 0)),  #$3.96
          yf.download(tickers = 'REAL' ,period='1d', start=datetime(2024, 1, 17, 9, 30, 0)),  #$1.56
          #yf.download(tickers = 'MASS' ,period='1d',  interval='5m', start=datetime(2024, 2, 13, 9, 30, 0)),  #$6.67
          yf.download(tickers = 'PHAT' ,period='1d', start=datetime(2024, 2, 13, 9, 30, 0)),  #$5.98
          #yf.download(tickers = 'APLT' ,period='1d',  interval='5m', start=datetime(2024, 3, 11, 9, 30, 0)),  #$5.80
          #yf.download(tickers = 'ORIC' ,period='1d',  interval='5m', start=datetime(2024, 3, 13, 9, 30, 0)),  #$14.08
          #yf.download(tickers = 'ATOS' ,period='1d',  interval='5m', start=datetime(2024, 3, 19, 9, 30, 0)),  #$1.24
          yf.download(tickers = 'ESPR' ,period='1d', start=datetime(2024, 3, 26, 9, 30, 0)),  #$2.39
          #Sell GMDA [Stock] — 4/1/24
          #Buy SPWR [Stock] — 4/5/24
          # DELISTED yf.download(tickers = 'SPWR' ,period='1d', start=datetime(2024, 4, 5, 9, 30, 0)),  #$2.39
          #Buy RIGL [Stock] — 4/8/24
          yf.download(tickers = 'RIGL' ,period='1d', start=datetime(2024, 4, 8, 9, 30, 0)),  #$2.39
          #Buy FVRR [Stock] — 4/11/24
          yf.download(tickers = 'FVRR' ,period='1d', start=datetime(2024, 4, 11, 9, 30, 0)),  #$2.39
          #Buy RCAT [Stock] — 4/15/24
          yf.download(tickers = 'RCAT' ,period='1d', start=datetime(2024, 4, 15, 9, 30, 0)),  #$2.39
          #Buy PLL [Stock] — 4/19/24
          yf.download(tickers = 'PLL' ,period='1d', start=datetime(2024, 4, 15, 9, 30, 0)),  #$2.39
          #Buy ASPN [Stock] — 5/2/24
          yf.download(tickers = 'ASPN' ,period='1d', start=datetime(2024, 5, 2, 9, 30, 0)),  #$2.39
          #Buy AGEN & WULF [Stock] — 5/31/24
          yf.download(tickers = 'AGEN' ,period='1d', start=datetime(2024, 5, 31, 9, 30, 0)),  #$2.39
          yf.download(tickers = 'WULF' ,period='1d', start=datetime(2024, 5, 31, 9, 30, 0)),  #$2.39
          #Buy BTDR [Stock] — 6/3/24
          yf.download(tickers = 'BTDR' ,period='1d', start=datetime(2024, 6, 3, 9, 30, 0)),  #$2.39
          #Sell MRAM & PXLW [Stock] — 6/4/24
          #Buy DM [Stock] — 6/10/24
          yf.download(tickers = 'DM' ,period='1d', start=datetime(2024, 6, 10, 9, 30, 0)),  #$2.39
          #Sell HUBC, ISDR, RMBL, & TRT [Stock] — 6/10/24
          #Buy ARBK, HUT, & SDIG [Stock] — 6/11/24
          yf.download(tickers = 'ARBK' ,period='1d', start=datetime(2024, 6, 11, 9, 30, 0)),  #$2.39
          yf.download(tickers = 'HUT' ,period='1d', start=datetime(2024, 6, 11, 9, 30, 0)),  #$2.39
          yf.download(tickers = 'SDIG' ,period='1d', start=datetime(2024, 6, 11, 9, 30, 0)),  #$2.39
          #Sell DAIO & MCRB [Stock] — 6/11/24
          #Buy ABCL, MKFG, & VLD [Stock] — 6/12/24
          yf.download(tickers = 'ABCL' ,period='1d', start=datetime(2024, 6, 12, 9, 30, 0)),  #$2.39
          yf.download(tickers = 'MKFG' ,period='1d', start=datetime(2024, 6, 12, 9, 30, 0)),  #$2.39
          #DELISTED yf.download(tickers = 'VLD' ,period='1d', start=datetime(2024, 6, 12, 9, 30, 0)),  #$2.39
          #Sell LTRX [Stock] — 6/12/24
          #Sell ALIM [Stock] — 6/24/24
          #Buy OPAD — 7/12/24
          yf.download(tickers = 'OPAD' ,period='1d', start=datetime(2024, 7, 12, 9, 30, 0)),  #$2.39
          #Buy ARDX [Stock] — 7/29/24
          yf.download(tickers = 'ARDX' ,period='1d', start=datetime(2024, 7, 12, 9, 30, 0)),  #$2.39
          #Buy FLGT & LASR [Stock] — 8/2/24
          yf.download(tickers = 'FLGT' ,period='1d', start=datetime(2024, 8, 2, 9, 30, 0)),  #$2.39
          yf.download(tickers = 'LASR' ,period='1d', start=datetime(2024, 8, 2, 9, 30, 0)),  #$2.39
          #Sell ITI [Stock] — 8/9/24
          #Sell SPWR [Stock] — 8/13/24
          #Buy ADPT [Stock] — 8/16/24
          yf.download(tickers = 'ADPT' ,period='1d', start=datetime(2024, 8, 16, 9, 30, 0)),  #$2.39
          #Sell SDIG [Stock] — 8/21/24
          #Buy IRBT [Stock] — 8/21/24
          yf.download(tickers = 'IRBT' ,period='1d', start=datetime(2024, 8, 21, 9, 30, 0)),  #$2.39
          #Sell AMSC, KSCP, & WATT [Stock] — 8/29/24
          #Buy FEIM & NEON [Stock] — 8/29/24
          yf.download(tickers = 'FEIM' ,period='1d', start=datetime(2024, 8, 29, 9, 30, 0)),  #$2.39
          yf.download(tickers = 'NEON' ,period='1d', start=datetime(2024, 8, 29, 9, 30, 0)),  #$2.39
          #Buy UAMY [Stock] — 9/5/24
          yf.download(tickers = 'UAMY' ,period='1d', start=datetime(2024, 9, 5, 9, 30, 0)),  #$2.39
          #Sell VLDX [Stock] — 9/17/24
          #Sell CYBN & MKFG [Stock] — 9/19/24
          #Sell MNMD & OTLY [Stock] — 9/20/24
          #Buy ARAY, ZVRA, & ZYME [Stock] — 9/23/24
          yf.download(tickers = 'ARAY' ,period='1d', start=datetime(2024, 9, 23, 9, 30, 0)),  #$2.39
          yf.download(tickers = 'ZVRA' ,period='1d', start=datetime(2024, 9, 23, 9, 30, 0)),  #$2.39
          yf.download(tickers = 'ZYME' ,period='1d', start=datetime(2024, 9, 23, 9, 30, 0)),  #$2.39
          #Sell ANEB, CHRS, & DTIL [Stock] — 9/23/24
          #Sell AGEN, ATOS, ORIC, RCAT, & VSTM [Stock] — 9/24/24
          #Sell MASS [Stock] — 9/25/24
          #Buy BLND [Stock] — 9/26/24
          yf.download(tickers = 'BLND' ,period='1d', start=datetime(2024, 9, 26, 9, 30, 0)),  #$2.39
          #Sell NEON [Stock] — 9/26/24
          #Sell BWAY [Stock] — 9/30/24
          #Buy PPTA [Stock] — 10/2/24
          yf.download(tickers = 'PPTA' ,period='1d', start=datetime(2024, 10, 2, 9, 30, 0)),  #$2.39
          #Buy CLOV [Stock] — 10/3/24
          yf.download(tickers = 'CLOV' ,period='1d', start=datetime(2024, 10, 3, 9, 30, 0)),  #$2.39
          #Buy EOSE & WGS [Stock] — 10/4/24
          yf.download(tickers = 'EOSE' ,period='1d', start=datetime(2024, 10, 4, 9, 30, 0)),  #$2.39
          yf.download(tickers = 'WGS' ,period='1d', start=datetime(2024, 10, 4, 9, 30, 0)),  #$2.39
          #Buy AXTI [Stock] — 10/7/24
          yf.download(tickers = 'AXTI' ,period='1d', start=datetime(2024, 10, 7, 9, 30, 0)),  #$2.39
          #Sell PHAT [Stock] — 10/7/24
          #Sell ABCL, CASS, EVGO, & FLGT [Stock] — 10/9/24
          #Buy CHGG [Stock] — 10/10/24
          yf.download(tickers = 'CHGG' ,period='1d', start=datetime(2024, 10, 10, 9, 30, 0)),  #$2.39
          #Sell FVRR [Stock] — 10/11/24
          #Buy LNSR [Stock] — 10/16/24
          yf.download(tickers = 'LNSR' ,period='1d', start=datetime(2024, 10, 16, 9, 30, 0)),  #$2.39
          #Sell REAL for a Gain [Stock] — 10/17/24
          #Buy AMPH [Stock] — 10/17/24
          yf.download(tickers = 'AMPH' ,period='1d', start=datetime(2024, 10, 17, 9, 30, 0)),  #$2.39
          #Sell OPTT [Stock] — 10/29/24
          #Buy ANY [Stock] — 11/11/24
          yf.download(tickers = 'ANY' ,period='1d', start=datetime(2024, 11, 11, 9, 30, 0)),  #$2.39
          #Buy BCOV [Stock] — 11/15/24
          yf.download(tickers = 'BCOV' ,period='1d', start=datetime(2024, 11, 15, 9, 30, 0)),  #$2.39
          #Sell ASPN, CLOV, EOSE, & INGN [Stocks] — 11/22/24
          #Buy EXFY & XGN [Stock] — 11/22/24
          yf.download(tickers = 'EXFY' ,period='1d', start=datetime(2024, 11, 22, 9, 30, 0)),  #$2.39
          yf.download(tickers = 'XGN' ,period='1d', start=datetime(2024, 11, 22, 9, 30, 0)),  #$2.39
          #Sell APLT [Stock] — 12/3/24
          #Sell ARBK [Stock] — 12/3/24
          #Buy ITRM [Stock] — 12/4/24
          yf.download(tickers = 'ITRM' ,period='1d', start=datetime(2024, 12, 4, 9, 30, 0)),  #$2.39
          #Sell AMPH, AXTI, & LASR [Stock] — 12/4/24
          #Buy MYO & XERS [Stock] — 12/6/24
          yf.download(tickers = 'MYO' ,period='1d', start=datetime(2024, 12, 6, 9, 30, 0)),  #$2.39
          yf.download(tickers = 'XERS' ,period='1d', start=datetime(2024, 12, 6, 9, 30, 0)),  #$2.39
          #Sell ANY & ARAY [Stock] — 12/10/24
          #Buy CLPT [Stock] — 12/10/24
          yf.download(tickers = 'CLPT' ,period='1d', start=datetime(2024, 12, 10, 9, 30, 0)),  #$2.39
          #Buy BFLY [Stock] — 12/11/24   
          yf.download(tickers = 'BFLY' ,period='1d', start=datetime(2024, 12, 11, 9, 30, 0)),  #$2.39
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
        print ( "[Uncovered Diamond( "+ color.BOLD + ticker + color.END + ")] price hike: " + str(roc) + "%")
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
            #print(ticker + " "+ str(first_opening_price)+" "+ str(latest_market_price)+ " " + str(roc))
            print ( "[Uncovered Diamond ( "+ color.BOLD + ticker + color.END + ")] price drop: " + str(roc) + "%")
            content += ( "<p style = 'font-size: 25px;'>[Uncovered Diamond( <b>" + ticker + "</b>)] price drop: " + str(roc) + "%" +
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

        
        limit_price = round(first_opening_price * 1.6, 2)
        stop_price=0; #temp measure

        #(New Price - Old Price)/Old Price and then multiply that number by 100
        roc = round(((latest_market_price - first_opening_price) / first_opening_price) * 100,2);    
        
        #if latest_market_price < first_opening_price * 0.8:
        if roc >= 0:
            #print(ticker + " "+ str(first_opening_price)+" "+ str(latest_market_price)+ " " + str(roc))
            print ( "[Uncovered Diamond( "+ color.BOLD + ticker + color.END + ")] price hike: " + str(roc) + "%")
            price_hike = round(latest_market_price - first_opening_price,2)
            hike_ticker[ticker] = [roc,price_hike, limit_price, first_opening_price,latest_market_price,stop_price]
            content += ("<p style = 'font-size: 25px;'>[Uncovered Diamond( <b>" + ticker + "</b>)] price hike: " + str(roc) + "%" + 
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
  msg['Subject'] = "[Uncovered Diamond(tickers)] " + RightNow()
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
   #   for value, ticker in zip(data_dl(),ticker_list):
   #       first_opening_price = round(value['Open'][0],2)
   #       latest_market_price = round(value['Close'][-1],2)
   #       roc = round(((latest_market_price - first_opening_price) / first_opening_price) * 100,2); 
   #       print(ticker + " "+ str(first_opening_price)+" "+ str(latest_market_price)+ " " + str(roc))
     #send_email()
     #send_email2()



