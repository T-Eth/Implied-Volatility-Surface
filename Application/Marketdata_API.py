import requests
from datetime import datetime, timedelta
import json
import pandas as pd

class optionsChain:
    def __init__(self, underlyingSymbol='AAPL', strikeFrom=80, strikeTo=120, side='call'):
        self.underlyingSymbol = underlyingSymbol
        self.side = side
        #Get options expiring from today to two years from now
        self.dateFrom = datetime.today().date().isoformat()
        self.dateTo = datetime.today().date().replace(year=datetime.today().date().year+1).isoformat()
        #Select range of strikes based on last traded price
        self.quoteUrl = 'https://api.marketdata.app/v1/stocks/quotes/AAPL/'
        self.quoteResponse = requests.request("GET", self.quoteUrl)
        self.quote = json.loads(self.quoteResponse.text)
        self.strikeFrom = round(self.quote['last'][0]*strikeFrom/100)
        self.strikeTo = round(self.quote['last'][0]*strikeTo/100)
        self.url = f'https://api.marketdata.app/v1/options/chain/{underlyingSymbol}/?strike={self.strikeFrom}-{self.strikeTo}&from={self.dateFrom}&to={self.dateTo}&side={self.side}'
        self.get_access_token()
        self.headers = {
                            'Accept': 'application/json',
                            'Authorization': f'Bearer {self.token}'
                        }
        self.chain = requests.request("GET", self.url, headers=self.headers)
        self.optionsChain = pd.DataFrame(json.loads(self.chain.text))
        self.optionsChain = self.optionsChain.where(self.optionsChain['strike']%10 == 0).dropna()

    def get_access_token(self):
        with open('md.token', 'r') as file:
            self.token = file.read()

def main():
    chain = optionsChain()
    print(chain.optionsChain.head())
    print(chain.optionsChain.tail())
    print(chain.optionsChain['iv'].head())

if __name__ == '__main__':
    main()