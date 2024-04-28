#function to get Tickers from yahoo finance and return the open, close values
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
import csv
#Data Source
import yfinance as yf


#function that reads the tickers from a csv file
#mostly done by me
def get_stock_data():
    ticker_list = read_tickers()
    stock_data = []
    for ticker in ticker_list:
        ticker_symbol = ticker  
        data = yf.download(ticker_symbol, start="2024-01-01")
        for index, row in data.iterrows():
            stock_data.append({'Ticker': ticker_symbol, 'Open': round(row['Open'], 2), 'Close': round(row['Close'], 2), 'Date': index})
    return stock_data
#function that reads the tickers from a csv file
#mostly done by me
def read_tickers():
    with open('tickers.csv', 'r') as file:
        reader = csv.reader(file)
        tickers = [ticker[0].lstrip("ï»¿") for ticker in reader]
    return tickers

#function that formats the stock data into a pandas dataframe
#mostly done by copilot by me telling it what to do each LINE
def stock_data_formatted():
    data = get_stock_data()
    formatted_data = pd.DataFrame()
    for ticker in set(stock['Ticker'] for stock in data):
        stock_df = pd.DataFrame([stock for stock in data if stock['Ticker'] == ticker])
        formatted_data = pd.concat([formatted_data, stock_df[['Ticker', 'Open', 'Close', 'Date']]])
    return formatted_data


#function for me to send an email to anyone
#mostly by Copilot(guided by me)
def send_email(stock_df, email):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "aaleensyed20@gmail.com"  # Enter your address
    receiver_email = email  # Enter receiver address
    password = "xxmg qaps ojvn tmtg"

    EmailMessage = MIMEMultipart()
    EmailMessage['From'] = sender_email
    EmailMessage['To'] = receiver_email
    EmailMessage['Subject'] = "Stock Data assisted by Copilot"
    EmailMessage.attach(MIMEText(stock_df.to_string(index=False), 'plain'))
    text = EmailMessage.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

def main():
    #mostly done Copilot
    parser = argparse.ArgumentParser()
    parser.add_argument('-email', type=str, help='Email address')
    args = parser.parse_args()
    print("")
    tickers = read_tickers()
    data = get_stock_data()
    send_email(stock_data_formatted(), args.email)

   
    

if __name__ == '__main__':
    main()


    