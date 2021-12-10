import bs4 as bs
import requests
import numpy as np
import pandas_datareader as web
import ezgmail


class Index:
    def __init__(self):
        self.tickers = None
        self.names = None
        self.webside = None
        self.index_tickers = None
        self.index_names = None
        self.strip_tickers = None
        self.strip_names = None

    def scrap_tickers(self):
        response = requests.get(self.webside)
        soup = bs.BeautifulSoup(response.text, "lxml")
        tabelle = soup.find("table", {"class": "wikitable sortable"})
        tickers = []
        names = []
        for reihe in tabelle.findAll("tr")[1:]:
            ticker = reihe.findAll("td")[self.index_tickers].text
            tickers.append(ticker)
            name = reihe.findAll("td")[self.index_names].text
            names.append(name)
        self.tickers = [ticker for ticker in tickers]
        self.names = [name for name in names]
        self.strip_tickers()
        self.strip_names()

    def strip_tickers(self):
        pass

    def strip_names(self):
        pass

    def return_tickers(self):
        return self.tickers

    def return_names(self):
        return self.names

    def load_stock(self, ticker):
        df = web.DataReader(ticker, "yahoo")
        return df

    def calculate_crv(self, df):
        highest = df["Close"].max()
        lowest = df["Close"].min()
        today = df["Close"][-1]
        crv = np.abs((highest - today) / (lowest - today))
        return crv

    def send_mail(self, email, subject, body, attachments=None):
        ezgmail.send(email, subject, body, attachments)


class Sandp500(Index):
    """Class to load S&P 500 data."""

    def __init__(self):
        super(Index).__init__()
        self.webside = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        self.index_tickers = 0
        self.index_names = 1

    def strip_tickers(self):
        self.tickers = [ticker[:-1] for ticker in self.tickers]


class DAX(Index):
    """Class to load DAX data."""

    def __init__(self):
        super(Index).__init__()
        self.webside = "https://de.wikipedia.org/wiki/DAX#Unternehmen_im_DAX"
        self.index_tickers = 1
        self.index_names = 0

    def strip_names(self):
        self.names = [name[:-1] for name in self.names]
