from Classes import *
from selenium import webdriver
from googlesearch import search
import requests
from bs4 import BeautifulSoup


# load the different indexes and scrap for tickers to later iterate over the tickers
sandp = Sandp500()
sandp.scrap_tickers()

# calculate crv of sandp-index and make a dictionary which includes all stockes with crv > 3
dic_crv = {}
for ticker in sandp.tickers:
    try:
        df = sandp.load_stock(ticker)
        crv = sandp.calculate_crv(df)
        if crv >= 3:
            dic_crv[ticker] = crv
    except KeyError:
        pass

crv_names = []
crv_tickers = []
for ticker in dic_crv.keys():
    index = sandp.tickers.index(ticker)
    crv_names.append(sandp.names[index])
    crv_tickers.append(ticker)

# Ersten 5 Googleergebnisse als links speichern und dann per Email senden
links = []
for count, name in enumerate(crv_names):
    links.append([])
    for j in search(term=name, num_results=5):
        links[count].append(j)

# Write the mail
body = f'Here are todays recomendations:\r'
for count, name in enumerate(crv_names):
    body += f'{name}: CRV = {dic_crv[crv_tickers[count]]}\r'
    for i in links[count]:
        body += f'{i}\r'
body += '\r'
body += 'Hope the mail is useful!'

sandp.send_mail(email='zenz.finanzen@gmail.com', subject='Good stocks', body=body)
