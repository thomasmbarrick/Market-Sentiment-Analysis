from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
import datetime

base_url = "https://finviz.com/quote.ashx?t="
stock_symbols = ["AMD", "NVDA", "INTC"]


news_data = {}
stock_data = []
for stock in stock_symbols:
    url = base_url + stock
    
    req = Request(url=url, headers={"user-agent": "market-sentiment"})
    response = urlopen(req)
    
    html = BeautifulSoup(response, features="html.parser")
    news_data[stock] = html.find(id="news-table")
    data_rows = news_data[stock].findAll("tr")
    
    for index, row in enumerate(data_rows):
        
        article_title = row.a.text 
        
        timestamp_raw = row.td.text
        timestamp = timestamp_raw.replace("\r\n", "")
        timestamp_split = timestamp.split(" ")
        
        timestamp_split = list(filter(None, timestamp_split))
        
        if len(timestamp_split) == 1:
            article_time = timestamp_split[0]
        else:
            article_date = timestamp_split[0]
            article_time = timestamp_split[1]

            
        stock_data.append([stock, article_date, article_time, article_title])
        
    
df = pd.DataFrame(stock_data, columns=["stock", "article_date", "article_time", "article_title"])

vader = SentimentIntensityAnalyzer()

compound_function = lambda title: vader.polarity_scores(title)["compound"]

df["compound"] = df["article_title"].apply(compound_function)

print("hey")

plt.figure(figsize=(10,8))
df = df.drop(columns=['article_time', 'article_title'])
mean_df = df.groupby(["stock", "article_date"]).mean()
mean_df = mean_df.unstack()
mean_df = mean_df.xs("compound" , axis="columns").transpose()
mean_df.plot(kind="bar")
plt.show()