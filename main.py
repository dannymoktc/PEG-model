import yfinance as yf
import requests
from bs4 import BeautifulSoup
from lxml import html as HTMLParser

pe_url = 'http://www.multpl.com/table?f=m'

def get_data_from_multpl_website(url):
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
        )
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text)
    parsed = HTMLParser.fromstring(res.content.decode('utf-8'))
    tr_elems = parsed.cssselect('#datatable tr')
    raw_data = [[td.text.strip() for td in tr_elem.cssselect('td')] for tr_elem in tr_elems[1:]]
    return raw_data

def getLastestSPPe(url):
    pe_data = get_data_from_multpl_website(url)
    return float(pe_data[0][1])

sPPe = getLastestSPPe(pe_url)
print(sPPe)

# Index
indexPe = sPPe
indexG = 16.4

indexG = float(input("What is the G of S&P? :"))
indexPeg = indexPe/float(indexG)
#print(indexPeg)


# Stock
# stock = 'AAPL'

stock = input("Enter your stock code(US): ")
print("searching..." + stock)
stockYfDs = yf.Ticker(stock)

##stockBeta = 1.57
stockBeta = stockYfDs.info.get('beta')
#stockPE = 21.97
stockPE = stockYfDs.info.get('trailingPE')
#stockEPS = 0.17
stockEPS = stockYfDs.info.get('trailingEps')
#stockEstimatedEPS = 0.21
stockEstimatedEPS = stockYfDs.info.get('forwardEps')

##stockYfDs.info
stockCurrentPrice = stockYfDs.info.get('currentPrice')
#print(stockYfDs.info)

#B8
stockG = (stockEstimatedEPS/stockEPS-1)
#print(stockG)

#B9
stockPeg = stockPE/(stockG*100)
#print(stockPeg)

cStockPe = indexPe * stockBeta
#print(cStockPe)

peg = indexPeg * stockBeta
#print(peg)

# Result
pePrice = stockCurrentPrice * ((indexPe * stockBeta)/stockPE)
#print('Result PE price:' + str((indexPe * stockBeta)/stockPE))

pegPrice = stockCurrentPrice * ((indexPeg * stockBeta)/stockPeg)

print('Result PE price:' + str(pePrice))
print('Result PEG price:' + str(pegPrice))

