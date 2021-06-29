# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%


# %% [markdown]
#

# %%
import pandas_datareader.data as web
import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import seaborn as sns
import matplotlib

sns.set_theme()

# %% [markdown]
# Set start and end time. It is one year by default

# %%


# %% [markdown]
# Stock class

# %%
class Stock:
    def __init__(self,  label, start=None, end=None,priceScoreWeight=0.5):
        self.label = label
        self.start = start
        self.end = end
        if priceScoreWeight >1 or priceScoreWeight <0:
            priceScoreWeight=0.5
        self.priceScoreWeight=priceScoreWeight
        self.stockData = self.getStockData()

    def getStockData(self):
        if self.start is None or self.end is None:
            self.end = datetime.date.today()
            self.start = self.end - datetime.timedelta(700)
        stock = web.DataReader(self.label, 'yahoo', self.start, self.end)[
            ['Close', 'Volume']].round(2)
        addMAData(stock)
        addMAScore(stock)
        addPriceScore(stock)
        addSumScore(stock,self.priceScoreWeight)
        addPriceDelta(stock)
        return stock
    def updateSumScore(self,priceScoreWeight):
        addSumScore(self.stockData,priceScoreWeight)
        return self
# %% [markdown]
# function to calculate MA and EMA, Score

# %%


def caculateEMA(prices, days, smoothing=2):
    if len(prices) < days:
        return [np.nan]*len(prices)
    ema = [sum(prices[:days]) / days]
    for price in prices[days:]:
        ema.append((price * (smoothing / (1 + days))) +
                   ema[-1] * (1 - (smoothing / (1 + days))))
    return [np.nan]*(days-1)+ema


def caculateMA(prices, days):
    if len(prices) < days:
        return [np.nan]*len(prices)
    return prices.rolling(days).mean()


def addMAData(prices_df):
    prices_df['MA20'] = caculateMA(prices_df['Close'], 20)
    prices_df['MA60'] = caculateMA(prices_df['Close'], 60)
    prices_df['MA120'] = caculateMA(prices_df['Close'], 120)
    prices_df['MA250'] = caculateMA(prices_df['Close'], 250)
    prices_df['EMA20'] = caculateEMA(prices_df['Close'], 20)
    prices_df['EMA60'] = caculateEMA(prices_df['Close'], 60)
    prices_df['EMA120'] = caculateEMA(prices_df['Close'], 120)
    prices_df['EMA250'] = caculateEMA(prices_df['Close'], 250)


def caculateOneDayPriceScore(prices):
    score = 0
    fullScore = 200
    dummy = {'Close': np.nan,
             'MA20': np.nan,
             'MA60': np.nan,
             'MA120': np.nan,
             'MA250': np.nan,
             'EMA20': np.nan,
             'EMA60': np.nan,
             'EMA120': np.nan,
             'EMA250': np.nan,
             }
    priceToday = prices.iloc[-1] if(len(prices) > 0) else dummy
    price20 = prices.iloc[-20] if len(prices) >= 20 else dummy
    price60 = prices.iloc[-60] if len(prices) >= 60 else dummy
    price120 = prices.iloc[-120] if len(prices) >= 120 else dummy
    price250 = prices.iloc[-250]if len(prices) >= 250 else dummy
    if priceToday['Close'] >= priceToday['EMA250']:
        score += 40
    if priceToday['Close'] >= priceToday['EMA120']:
        score += 30
    if priceToday['Close'] >= priceToday['EMA60']:
        score += 20
    if priceToday['Close'] >= priceToday['EMA20']:
        score += 10
    if priceToday['Close'] >= price250['Close']:
        score += 40
    if priceToday['Close'] >= price120['Close']:
        score += 30
    if priceToday['Close'] >= price60['Close']:
        score += 20
    if priceToday['Close'] >= price20['Close']:
        score += 10
    # pass score  180=>90
    return score*100/fullScore


def addPriceDelta(pricesDF):
    pricesDeltaList = ['']
    pricesDeltaPercentageList = [0]
    for i in range(1, len(pricesDF)):
        delta = pricesDF.iloc[i]['Close']-pricesDF.iloc[i-1]['Close']
        pricesDeltaList.append(round(delta, 2))
        pricesDeltaPercentageList .append(
            str(round(delta*100/pricesDF.iloc[i-1]['Close'], 2))+'%'
        )
    pricesDF['Chg'] = pricesDeltaList
    pricesDF['%Chg'] = pricesDeltaPercentageList


def caculateOneDayMAScore(oneDayPrices):
    score = 0
    fullScore = 420
    # compare with 250
    if oneDayPrices['EMA120'] > oneDayPrices['EMA250']:
        score += 60
    if oneDayPrices['MA120'] > oneDayPrices['MA250']:
        score += 60
    if oneDayPrices['EMA60'] > oneDayPrices['EMA250']:
        score += 50
    if oneDayPrices['MA60'] > oneDayPrices['MA250']:
        score += 50
    if oneDayPrices['EMA20'] > oneDayPrices['EMA250']:
        score += 40
    if oneDayPrices['MA20'] > oneDayPrices['MA250']:
        score += 40

    # compare with 120
    if oneDayPrices['EMA60'] > oneDayPrices['EMA120']:
        score += 30
    if oneDayPrices['MA60'] > oneDayPrices['MA120']:
        score += 30
    if oneDayPrices['EMA20'] > oneDayPrices['EMA120']:
        score += 20
    if oneDayPrices['MA20'] > oneDayPrices['MA120']:
        score += 20
    # compare with 60
    if oneDayPrices['EMA20'] > oneDayPrices['EMA60']:
        score += 10
    if oneDayPrices['MA20'] > oneDayPrices['MA60']:
        score += 10
    # pass score: MA60 must higher MA120==> 360 ==> 85
    return score*100/fullScore


def addMAScore(pricesDF):
    score = []
    for i in range(len(pricesDF)):
        score.append(caculateOneDayMAScore(pricesDF.iloc[i, :]))
    pricesDF['MAScore'] = score


def addPriceScore(pricesDF):
    score = []
    for i in range(len(pricesDF)):
        score.append(caculateOneDayPriceScore(
            pricesDF.iloc[max(i-250, 0):i+1, :]))
    pricesDF['PriceScore'] = score


def addSumScore(pricesDF,priceScoreWeight):
    score = []
    for i in range(len(pricesDF)):
        score.append(
            (pricesDF.iloc[i]['PriceScore']*priceScoreWeight)
            + (pricesDF.iloc[i]['MAScore']*(1-priceScoreWeight)))

    pricesDF['SumScore'] = score

