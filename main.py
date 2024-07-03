from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

base_url = "https://finviz.com/quote.ashx?t="
stock_symbols = ["AMD", "NVDA", "INTC"]


news_data = {}
final_data = []
for stock in stock_symbols:
    url = base_url + stock
    
    req = Request(url=url, headers={"user-agent": "market-sentiment"})
    response = urlopen(req)
    
    html = BeautifulSoup(response, features="html.parser")
    news_data[stock] = html.find(id="news-table")
    data_rows = news_data[stock].findAll("tr")
    
    stock_data = []
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
        
    final_data.append(stock_data)
    

        
print(final_data)


