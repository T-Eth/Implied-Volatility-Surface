import requests
from datetime import datetime, timedelta
import json

class optionsChain:
    def __init__(self, underlyingSymbol='AAPL', strikeFrom=100, strikeTo=100):
        self.underlyingSymbol = underlyingSymbol
        
        #Get options expiring from today to two years from now
        self.dateFrom = datetime.today().date().isoformat()
        #self.dateTo = datetime.today().date().replace(year=datetime.today().date().year+2).isoformat()
        self.dateTo = datetime.today().date().isoformat()
        #Select range of strikes based on last traded price
        self.quoteUrl = 'https://api.marketdata.app/v1/stocks/quotes/AAPL/'
        self.quoteResponse = requests.request("GET", self.quoteUrl)
        self.quote = json.loads(self.quoteResponse.text)
        self.strikeFrom = round(self.quote['last'][0]*strikeFrom/100)
        self.strikeTo = round(self.quote['last'][0]*strikeTo/100)
        self.url = f'https://api.marketdata.app/v1/options/chain/{underlyingSymbol}/?strike={strikeFrom}-{strikeTo}&from={self.dateFrom}&to={self.dateTo}/'
        self.get_access_token()
        self.headers = {
                            'Accept': 'application/json',
                            'Authorization': f'Bearer {self.token}'
                        }
        self.chain = requests.request("GET", self.url, headers=self.headers)
        self.optionsChain = json.loads(self.chain.text)

    def get_access_token(self):
        with open('md.token', 'r') as file:
            self.token = file.read()
