from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

base_url = "https://finviz.com/quote.ashx?t="
stock_symbols = ["AMD", "NVDA", "INTC"]


news_data = {}
for stock in stock_symbols:
    url = base_url + stock
    
    req = Request(url=url, headers={"user-agent": "market-sentiment"})
    response = urlopen(req)
    
    html = BeautifulSoup(response, "html")
    news_data[stock] = html.find(id="news-table")
    
    break

print(news_data)