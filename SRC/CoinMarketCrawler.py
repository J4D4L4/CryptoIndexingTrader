from coinmarketcap import Market
import matplotlib.pyplot as plt
import json
import copy
class coin:
    def __init__(self, prozent, symbol, price):
        self.prozent = prozent
        self.symbol = symbol
        self.price = price
        self.amt = 0
        self.worth =0


class portfolio:
    #fuellungsGrad=0
    #coins = list()
    #market = dict()

    def __init__(self, marketSize, maxSlize, investmentSize):
        self.market=getMarket(marketSize)
        self.fuellungsGrad = 0
        self.coins = list()
        self.maxSlize = maxSlize
        self.investmentSize = investmentSize

def getMarket(nrOfPositions):

    coinmarketcap = Market()
    linstings = coinmarketcap.listings()
    ticker = coinmarketcap.ticker(start=0, limit=nrOfPositions, convert='USD')
    return ticker

def getMarketWorth(ticker, symbol):
    marketCounter=0
    symbolReached = 0
    for tick in ticker['data'].items():
        if tick[1]['symbol'] == symbol:
            symbolReached=1
        if symbolReached == 1:
            marketCounter += tick[1]['quotes']['USD']['market_cap']
    return marketCounter



def getCoin(coin, ticker):
    for tick in ticker['data'].items():
        if str(tick[1]['symbol']) == coin:
            return tick[1]

    return 0
#def calcRestMarketWorth(portfolio, symbol)
 #   symbolReached = 0
  #  for symbol in portfolio.market.items

def calcSlize(portfolio, symbol):
    prozentLeft = 100 - calcProzentVergeben(portfolio.coins)
    marketWorthfromSymbol = getMarketWorth(portfolio.market, symbol)
    infoCoin = getCoin(symbol, portfolio.market)
    marketCap = infoCoin['quotes']['USD']['market_cap']
    price  = infoCoin['quotes']['USD']['price']
    prozent= (prozentLeft/marketWorthfromSymbol)*marketCap
    if prozent > portfolio.maxSlize:
        prozent = portfolio.maxSlize
    #print(prozent)
    nCoin = coin(prozent, symbol, price)
    nCoin = calcCoinAmt(nCoin, portfolio.investmentSize)
    return nCoin

def calcProzentVergeben(coinList):
    cProzent = 0
    for eCoin in coinList:
       cProzent += eCoin.prozent
    #print(eCoin.symbol)
    return cProzent

def calcPortfolio(portfolio):

    for symbol in portfolio.market['data'].items():
        portfolio.coins.append(calcSlize(portfolio,symbol[1]["symbol"]))
    return portfolio

def listSymbols(portfolio):
    symbols =list()
    for symbol in portfolio.market['data'].items():
        symbols.append(symbol[1]["symbol"])

    return symbols
def calcCoinAmt(coin, portfolioSize):
    coin.worth = ((portfolioSize/100)*coin.prozent)
    coin.amt = coin.worth/coin.price
    return coin

def removeSymbol(market, symbols):
    nMarket= copy.deepcopy(market)
    for key, symbol in market['data'].items():
        if symbol['symbol']  in symbols:
            nMarket['data'].pop(key)
    return nMarket

def consoleInterface():
    print('Create your Crypto Index')
    print('-------------------------')
    try:
        investSize = int(input('How much do you want to invest? (In $)'))
    except ValueError:
        print("thats not a number")
        return



    print('-------------------------')
    try:
        amtOfSymbols = int(input('The index can include the top x Symbols. What should x be? '))
    except ValueError:
        print("thats not a number")
        return

    print('-------------------------')
    try:
        highestPortfolioProzentage = int(input('What should be the highes prozentage allocation to a single Coin?(the lower the number the higher the focus on smaller alt coins'))
    except ValueError:
        print("thats not a number")
        return
    print('-------------------------')
    myPortfolio = portfolio(int(amtOfSymbols), int(highestPortfolioProzentage), int(investSize))
    print ("the current Symbols are:")

    repeat=1
    symbols = list()
    while True:
        print(listSymbols(myPortfolio))
        try:
            exclude = input('enter the symbol you want to exclude. If you do not want to exclude anything enter: 0')
            if exclude=='0':
                break
            else:
                symbols.append(exclude)
                myPortfolio.market = removeSymbol(myPortfolio.market, symbols)
        except ValueError:
            print("thats not a number")
            return

    print('-------------------------')
    print('Creating Portfolio')
    myPortfolio = calcPortfolio(myPortfolio)
    #for coin in myPortfolio.coins:
        #print(str(coin.symbol) + ": "+ str(coin.prozent)+"%")
    return myPortfolio
def getListofSymbols(coins):
    symbols=list()
    for coin in coins:
        symbols.append(coin.symbol)
    return symbols
def getListofProzent(coins):
    prozent=list()
    for coin in coins:
        prozent.append(coin.prozent)
    return prozent
def getListOfValues(coins):
    values=list()
    for coin in coins:
        values.append(coin.worth)
    return values
def getListOfAmtCoins(coins):
    amtCoins=list()
    for coin in coins:
        amtCoins.append(coin.amt)
    return amtCoins
#myPortfolio = portfolio(50, 5, 10000)
#symbols=listSymbols(myPortfolio)
#symbols=['BTC']
#myPortfolio.market = removeSymbol(myPortfolio.market, symbols)
#myPortfolio.market =getMarket(20)
#marketWorth=getMarketWorth(myPortfolio.market,'XRP')
#print(calcSlize(myPortfolio,"BTC"))
#print(marketWorth)
#myPortfolio = calcPortfolio(myPortfolio)
#for coin in myPortfolio.coins:
#    print(str(coin.symbol) + ": "+ str(coin.prozent))

#for coin in myPortfolio.coins:
#    print (coin)
myPortfolio = consoleInterface()
label = getListofSymbols(myPortfolio.coins)
prozent=getListofProzent(myPortfolio.coins)
values=getListOfValues(myPortfolio.coins)
amtCoins=getListOfAmtCoins(myPortfolio.coins)

for coin in myPortfolio.coins:
    print(str(coin.symbol)+":"+ str(coin.amt)+" Worth: "+str(coin.worth) +"$ Portfolio Slize: "+ str(coin.prozent))


