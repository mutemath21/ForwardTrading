# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 14:37:10 2018

@author: Bornok
"""
import winsound
from pygame import mixer # Load the required library

mixer.init()
mixer.music.load('ragnarok-online-level-up-sound.mp3')


from binance.client import Client
import talib
from talib.abstract import * 
import numpy
from IPython import display

import matplotlib.pyplot as plt
from matplotlib.finance import candlestick2_ohlc

import time

import logging
LOG_LEVEL = logging.DEBUG
LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
from colorlog import ColoredFormatter
logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(LOGFORMAT)
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
log = logging.getLogger('pythonConfig')
log.setLevel(LOG_LEVEL)
log.addHandler(stream)

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

import sys
sys.stdout = Unbuffered(sys.stdout)


#C:\Users\Bornok\Downloads\Music\service-bell_daniel_simion.wav
graphOn = False;
commission = 0.001

if(graphOn):
    plt.ion() 
    f1 = plt.figure();
    axesList = {};

pairs = [
             "BTC",
             "ETH",
             "EOS",
             "BNB",
             "TRX",
             "BCC",
             "LTC",
             "XRP",
             "ETC",
             "ONT",
             "ADA",
             "IOTA",
             "NEO",
             "ICX",
             "VEN",
             "XLM",
             "QTUM"];

totalcolumns = 5;
plotPerRow = int(len(pairs) / totalcolumns);
excess = len(pairs) % totalcolumns;
    
if (plotPerRow <= 0 and excess > 0):
    totalcolumns = excess;
    
if(excess > 0):
    plotPerRow += 1;    

print("total rows: " , plotPerRow)    ;
print("total columns: ", totalcolumns)    
plotCounter = 1;


if(graphOn):
    for pairx in pairs:
        #2 rows 1 column
        ax1 = f1.add_subplot(plotPerRow,totalcolumns,plotCounter);
        ax1.set_autoscale_on(True) # enable autoscale
        ax1.autoscale_view(True,True,True)    
        axesList[pairx + 'USDT'] = ax1;
        plotCounter += 1;
            

def main(): 
    previousGain = 0.00;
    patternList = [
                    "CDL2CROWS",
                    "CDL3BLACKCROWS",
                    "CDL3INSIDE",
                    "CDL3LINESTRIKE",
                    "CDL3OUTSIDE",
                    "CDL3STARSINSOUTH",
                    "CDL3WHITESOLDIERS",
                    "CDLABANDONEDBABY",
                    "CDLADVANCEBLOCK",
                    "CDLBELTHOLD",
                    "CDLBREAKAWAY",
                    "CDLCLOSINGMARUBOZU",
                    "CDLCONCEALBABYSWALL",
                    "CDLCOUNTERATTACK",
                    "CDLDARKCLOUDCOVER",
                    "CDLDOJI",
                    "CDLDOJISTAR",
                    "CDLDRAGONFLYDOJI",
                    "CDLENGULFING",
                    "CDLEVENINGDOJISTAR",
                    "CDLEVENINGSTAR",
                    "CDLGAPSIDESIDEWHITE",
                    "CDLGRAVESTONEDOJI",
                    "CDLHAMMER",
                    "CDLHANGINGMAN",
                    "CDLHARAMI",
                    "CDLHARAMICROSS",
                    "CDLHIGHWAVE",
                    "CDLHIKKAKE",
                    "CDLHIKKAKEMOD",
                    "CDLHOMINGPIGEON",
                    "CDLIDENTICAL3CROWS",
                    "CDLINNECK",
                    "CDLINVERTEDHAMMER",
                    "CDLKICKING",
                    "CDLKICKINGBYLENGTH",
                    "CDLLADDERBOTTOM",
                    "CDLLONGLEGGEDDOJI",
                    "CDLLONGLINE",
                    "CDLMARUBOZU",
                    "CDLMATCHINGLOW",
                    "CDLMATHOLD",
                    "CDLMORNINGDOJISTAR",
                    "CDLMORNINGSTAR",
                    "CDLONNECK",
                    "CDLPIERCING",
                    "CDLRICKSHAWMAN",
                    "CDLRISEFALL3METHODS",
                    "CDLSEPARATINGLINES",
                    "CDLSHOOTINGSTAR",
                    "CDLSHORTLINE",
                    "CDLSPINNINGTOP",
                    "CDLSTALLEDPATTERN",
                    "CDLSTICKSANDWICH",
                    "CDLTAKURI",
                    "CDLTASUKIGAP",
                    "CDLTHRUSTING",
                    "CDLTRISTAR",
                    "CDLUNIQUE3RIVER",
                    "CDLUPSIDEGAP2CROWS",
            
                    ]
    
    api_key = "Q3sZBei1LKWiUxLCGnUUhVoFDcaXV0BD19J35bltp4pWEkBNHbEw7jLC2MJaTNhP"
    api_secret = "57rLGuHMy2VhvgyWQCyWudtyW9L7ARAZ7XWZ9hbI78x1iTsRga5MwnoxhF6KUPEM";
    
    startingBalance = 10000.00; # USD
    portfolio = {};
    portfolio['USDT'] = startingBalance;
    
    client = Client(api_key, api_secret)
#    print(client.get_all_tickers());
    
    against = "USDT";
    
    while(True):
#        latestCandle = 0;
        
        log.debug("");
        log.error("+=================== RESCANNING MARKET =====================+");
        klinesDictionary = {};
        for pair1 in pairs:
            klines = client.get_historical_klines(pair1 + against, Client.KLINE_INTERVAL_3MINUTE, '2 hours ago UTC');
#            latestCandle = klines[-1];
            
#            del(klines[-1]);
            klinesDictionary[pair1+against] = (klines);
        
        
        # KLINES STRUCTURE:
        # [
        #     [
        #         1499040000000,      # Open time
        #         "0.01634790",       # Open
        #         "0.80000000",       # High
        #         "0.01575800",       # Low
        #         "0.01577100",       # Close
        #         "148976.11427815",  # Volume
        #         1499644799999,      # Close time
        #         "2434.19055334",    # Quote asset volume
        #         308,                # Number of trades
        #         "1756.87402397",    # Taker buy base asset volume
        #         "28.46694368",      # Taker buy quote asset volume
        #         "17928899.62484339" # Can be ignored
        #     ]
        # ]
        
        # Pattern recognition strategy;
    #        suggestions = decisionAgent_candle_strategy(scanBullishPatterns(patternList, klinesDictionary, talib), klinesDictionary);
        
        # Moving average strategy;
#        suggestions = decisionAgent_movingAverage_strategy(klinesDictionary);
        
        # High last sell strategy:
        suggestions = decisionAgent_movingAverage_strategy(klinesDictionary);
        
        portfolio = initiateTrade(suggestions, portfolio, client);
        previousGain = showBalance(portfolio, startingBalance, client, previousGain);
        
        if(graphOn):
            f1.canvas.blit();
            
        if(graphOn):
            f1.tight_layout();
            f1.canvas.draw()            
        
        for pair1 in pairs:
            klines = klinesDictionary[pair1+against];
            while(True):
                current_time = client.get_server_time()['serverTime']
                if(int(current_time) >= int(float(klines[len(klines) - 1][6]))):
                    break;
                else:
                    print("Waiting...");
                    time.sleep(2);


    
        
def plotCandles(o, h, l, c, ema8, ema13, ema21, ema55, pair, ax1):
    # MAIN FRAME.
    # =============================================================
    # - CANDLESTICK SUB-PLOT.
    # =============================================================
    ax1.clear();
    ax1.set_title(pair)
    ax1.set_facecolor('black')
    candlestick2_ohlc(ax1, o, h, l, c, width=0.6, colorup='g', colordown='r')
    
    ax1.plot(ema8, linewidth=1, color='cyan');
    ax1.plot(ema13, linewidth=1, color='purple');
    ax1.plot(ema21, linewidth=1, color='orange');
    ax1.plot(ema55, linewidth=1, color='yellow');
    
    lastclose = c[len(c) - 1];
    lastopen = o[len(o) - 1];
    
    if(lastclose > lastopen):
        ax1.axhline(y=lastclose, color='g', linestyle='--')    
    elif(lastclose < lastopen):
        ax1.axhline(y=lastclose, color='r', linestyle='--')    
    else:
        ax1.axhline(y=lastclose, color='b', linestyle='--')
        
    plt.gcf();
    
def scanBullishPatterns(patternList, klinesList, talib):
    allPairsAnalysis = {};
    for klinesPairKey in klinesList.keys():
        dict = {};
        o = numpy.empty(0)
        h = numpy.empty(0)
        l = numpy.empty(0)
        c = numpy.empty(0)
        v = numpy.empty(0)
        
        klineData = klinesList[klinesPairKey];
        
        klineCounter = 0;
        for line in klineData:
            o = numpy.append(o, float(line[1]));
            h = numpy.append(h, float(line[2]));
            l = numpy.append(l, float(line[3]));
            c = numpy.append(c, float(line[4])); 
            v = numpy.append(v, float(line[5]));
           
            klineCounter += 1;
            
        for pattern in patternList:
            resultData = getattr(talib, pattern)(o, h, l, c);
            
            candleCount= 0;
            for matchUnit in resultData:
                if(matchUnit == 100):
                    dict[pattern + " @ candle " + str(candleCount + 1)] = resultData;
                elif(matchUnit == -100):
                    dict[pattern + " @ candle " + str(candleCount + 1)] = resultData;
                
                candleCount += 1;
                
        allPairsAnalysis[klinesPairKey] = dict;
    
    
    return allPairsAnalysis;

def decisionAgent_gain_strategy(klinesDictionary):
    suggestions = {};
    
    for keyOfPairs in klinesDictionary.keys():    
        kline = klinesDictionary[keyOfPairs];
        prices = getFactor(kline, 'c');
        rsi = talib.RSI(prices, timeperiod=14);
        last = len(prices) - 2;
       
        if(rsi[last] < 30):
            message = keyOfPairs + ': suggestion ===> BUY ';
            suggestions[keyOfPairs.replace('USDT', '')] = 'BUY';
            log.info(message);
        elif(prices[last] < prices[last + 1]):
            message = keyOfPairs + ': suggestion ===> SELL ';
            suggestions[keyOfPairs.replace('USDT', '')] = 'SELL';
            log.error(message);
        
    return suggestions;

def decisionAgent_movingAverage_strategy(klinesDictionary):
    suggestions = {};
    for keyOfPairs in klinesDictionary.keys():    
        kline = klinesDictionary[keyOfPairs];
        prices = getFactor(kline, 'c');
        highs = getFactor(kline, 'h');
        opens = getFactor(klinesDictionary[keyOfPairs], 'o');
        lows = getFactor(kline, 'l');
        
        ema8 =  talib.EMA(prices, timeperiod=8);
        ema13 =  talib.EMA(prices, timeperiod=13);
        ema21 =  talib.EMA(prices, timeperiod=21);
        ema55 =  talib.EMA(prices, timeperiod=55);
        rsi = talib.RSI(prices, timeperiod=14);
        macd, macdsignal, macdhist = talib.MACD(prices, fastperiod=12, slowperiod=26, signalperiod=9)
        
        if(graphOn):
            plotCandles(opens, highs, lows, prices, ema8, ema13, ema21, ema55, keyOfPairs, axesList[keyOfPairs]);
            plt.pause(0.05);
        
        last = len(prices) - 2;
        
        if(macdhist[last] > macdhist[last - 1]):
#           aboveAllEMAs(ema8[last], ema13[last], ema21[last], ema55[last], prices[last], highs[last], lows[last])):
#        if(rsi[last] < 30):
            message = keyOfPairs + ': suggestion ===> BUY ';
            log.info(message);
            suggestions[keyOfPairs.replace('USDT', '')] = 'BUY';
#        elif(belowAllEMAs(ema8[last], ema13[last], ema21[last], ema55[last], prices[last], highs[last], lows[last]) and
#             rsi[last] >= 70):
        elif(macdhist[last] < macdhist[last - 1]):
#             belowAllEMAs(ema8[last], ema13[last], ema21[last], ema55[last], prices[last], highs[last], lows[last]) and
#             rsi[last] > 70):            
            message = keyOfPairs + ': suggestion ===> SELL ';
            log.error(message);
            suggestions[keyOfPairs.replace('USDT', '')] = 'SELL';
        else:
            message = keyOfPairs + ': suggestion ===> HOLD ';
            log.debug(message);
            suggestions[keyOfPairs.replace('USDT', '')] = 'HOLD';
        
        
        
        
    return suggestions;            

def getFactor(kline, factor):
    factors = numpy.empty(0);
    for line in kline:
        if(factor == 'o'):
            factors = numpy.append(factors, float(line[1]));
        elif(factor == 'h'):
            factors = numpy.append(factors, float(line[2]));
        elif(factor == 'l'):
            factors = numpy.append(factors, float(line[3]));
        elif(factor == 'c'):
            factors = numpy.append(factors, float(line[4]));   
            
    return factors;
    

    
def decisionAgent_candle_strategy(allPairsAnalysis, klinesDictionary):
    suggestions = {};
    for keyOfPairs in allPairsAnalysis.keys():
        patternData = allPairsAnalysis[keyOfPairs];
        
        cumulativeRating = 0;
        keepPatterns = [];
        for patternName in patternData.keys():
            patternEvaluations = patternData[patternName];
            
            candlePosition = 0;
            for evaluations in patternEvaluations:
                cumulativeRating = cumulativeRating + evaluations;
                kline = klinesDictionary[keyOfPairs];
                
                try:
                    # Given the pattern, confirm the there's a spike on volume.
                    if(kline[candlePosition][5] > kline[candlePosition - 1][5] and cumulativeRating > 0):
                        cumulativeRating += 100;
                except:
                    continue
                    
                candlePosition += 1;
                
            keepPatterns.append(patternName);
            
        
        message = '';
        if(cumulativeRating > 0):
            message = keyOfPairs + ': Rating ('+ str(cumulativeRating) + ') suggestion ===> BUY ' , keepPatterns;
            log.info(message);
            suggestions[keyOfPairs.replace('USDT', '')] = 'BUY';
        elif(cumulativeRating == 0):
            message = (keyOfPairs + ': Rating ('+ str(cumulativeRating) + ') suggestion ===> NO ACTIONS ' , keepPatterns);
            log.debug(message);
            suggestions[keyOfPairs.replace('USDT', '')] = 'HOLD';
        elif(cumulativeRating < 0):
            message = (keyOfPairs + ': Rating ('+ str(cumulativeRating) + ') suggestion ===> SELL or NO ACTIONS ' , keepPatterns);
            log.error(message);
            suggestions[keyOfPairs.replace('USDT', '')] = 'SELL';
            
    return suggestions;

def initiateBuying(currentPortfolio, instrumentPricePerUnit, instrumentSymbol, maximumInvestment):
    log.info("------------- BUYING POWER [" + str(maximumInvestment) + "] ----------------");
    getUSDBalance = currentPortfolio['USDT'];
    
    if (round(getUSDBalance, 2) == 0 or round(maximumInvestment, 2) <= 0):
        log.warn("Unable to purchase " + str(instrumentSymbol) + " due to an insufficient balance.");
        return currentPortfolio;
    
    maximumInvestment = maximumInvestment - (maximumInvestment * commission);
    
    # Compute maximum units that can be bought.
    totalUnitsToBuy = round(maximumInvestment, 4) / float(instrumentPricePerUnit);
    totalPrice = round(float(instrumentPricePerUnit) * totalUnitsToBuy, 2);
    totalPrice = round(totalPrice + (totalPrice * commission), 2);
    
    if(instrumentSymbol in currentPortfolio):
        # Put the entry on the portfolio
        currentPortfolio[instrumentSymbol] = round(currentPortfolio[instrumentSymbol] + totalUnitsToBuy, 4);
    else:
        currentPortfolio[instrumentSymbol] = round(totalUnitsToBuy, 4);
        
    # Deduct total price of purchased item
    log.debug("Maximum investment: " + str(maximumInvestment));
    log.debug("Commission: " + str(totalPrice * commission));
    log.debug("Total expense: " + str(maximumInvestment + (totalPrice * commission)));
    log.debug("Total Price: " + str(totalPrice));
    currentPortfolio['USDT'] = round(getUSDBalance - totalPrice, 2);
    
#    playBell();
    
    log.info('Successful purchase of [' + instrumentSymbol + '] with total units of ' + str(totalUnitsToBuy));
    return currentPortfolio;




def initiateSelling(currentPortfolio, instrumentPricePerUnit, instrumentSymbol, totalOfferCoin):
    log.info("------------- SELLING ----------------");
    instrumentQuantity = currentPortfolio[instrumentSymbol];
    
    if(instrumentQuantity == 0):
        log.warn("Nothing to sell for " + str(instrumentSymbol));
        return currentPortfolio;
    
    finalInstrumentQuantity = round(float(totalOfferCoin), 4) - round(instrumentQuantity, 4);
    
    if(finalInstrumentQuantity >= 0):
        totalOfferCoin = instrumentQuantity;
    
    totalSellingPrice = float(instrumentPricePerUnit) * float(totalOfferCoin);
    totalSellingPrice = totalSellingPrice + (totalSellingPrice * commission);
    currentBalance = currentPortfolio['USDT'];
    
    currentPortfolio['USDT'] = round(currentBalance + totalSellingPrice, 2);
    
#    playBell();
    
    log.info('Successful selling of [' + instrumentSymbol + '] with total units of ' + str(instrumentQuantity));
    # Zero out remaining instrument; (for the sake of it);
    if(finalInstrumentQuantity >= 0):
        currentPortfolio[instrumentSymbol] = 0.00;
    else:
        currentPortfolio[instrumentSymbol] = instrumentQuantity - round(float(totalOfferCoin), 4);
    
    return currentPortfolio;

# Based on total signal of buy, calculate the distribution of investment equally.
def calculatePurchaseDistribution(suggestions):
    totalForecastedPurchase = 0;
    for coin in suggestions.keys():
        if(suggestions[coin] == 'BUY'):
            totalForecastedPurchase += 1;
    
    return totalForecastedPurchase;

def initiateTrade(suggestions, portfolio, binanceClient):
    
    riskDistribution = calculatePurchaseDistribution(suggestions);
    
    maximumInvestment = 0;
    
    if(riskDistribution > 0):
        maximumInvestment = portfolio['USDT'] / riskDistribution;
    
    
    for coin in suggestions.keys():
        coinPair = coin + 'USDT';
        
        if(suggestions[coin] == 'BUY' and round(maximumInvestment, 2) > 0):
            # Pull order book and find any transaction you want to purchase that can be covered by your balance.
            orderConfiguration = nominatePurchase(round(maximumInvestment, 2), binanceClient.get_order_book(symbol=coinPair)['asks']);
            
            if(len(orderConfiguration) == 0):
                log.warn('Unable to make purchase. No order satisfies for purchase due to insufficient quantity.');
            else:                
                currentPriceOfInstrument = orderConfiguration[0];    
                
                portfolio = initiateBuying(portfolio, currentPriceOfInstrument, coin, maximumInvestment);
        elif(suggestions[coin] == 'SELL'):
            if(coin not in portfolio):
                log.warn('No assets found to sell for ' + str(coin) + '. Bypass selling.');            
            elif(coin in portfolio and portfolio[coin] > 0):
                # Pull order book and find any transaction you want to purchase that can be covered by your balance.
                bids = binanceClient.get_order_book(symbol=coinPair)['bids'];
                while(portfolio[coin] != 0):
                    orderConfiguration = nominateSell(portfolio[coin], bids, coin);
                    
                    currentPriceOfInstrument = orderConfiguration[0];    
                    totalCoinToSell = orderConfiguration[1];
                    
                    portfolio = initiateSelling(portfolio, currentPriceOfInstrument, coin, totalCoinToSell);
    
    # default;    
    return portfolio;

def nominatePurchase(currentBalance, asks):
    finalOrder = [];
    for order in asks:
        askingPrice = order[0];
        totalUnits = order[1];
        
        # Meaning we can take from this order some partial coins.
        if(currentBalance <= (float(askingPrice) * float(totalUnits))):
            finalOrder = order;
            break;
            
    return finalOrder;
        
        
def nominateSell(coinToSellBalance, bids, coinLabel):
    finalOrder = [];
    for order in bids:
        totalUnits = order[1];
        
        # Meaning we can sell our coins to that buyer because they are bidding 
        # enough quantity that we have.
        log.debug("Matching bid with count for [" +coinLabel+ "] of [" + totalUnits + "] = Current coin count [" + str(coinToSellBalance) + "]");
        finalOrder = order;
        bids.remove(order);
        break;        
            
    return finalOrder;    
    

def showBalance(portfolio, startingBalance, binanceClient, previousGain):
    portfolioValue = calculatePortfolioValue(portfolio, binanceClient.get_all_tickers());
    log.info('Buying power: ' + str(portfolio['USDT']));
    log.info('Total balance: ' + str(portfolioValue));
    
    gain = round(portfolioValue - startingBalance, 2);
    
    if(gain > 0):   
        log.info('Gain/Loss: ' + "+" + str(gain));
        if(previousGain < gain):
            playBell();
        previousGain = gain;
    else:
        log.error('Gain/Loss: ' + str(gain));
        
    return previousGain;

def calculatePortfolioValue(portfolio, latestPrices):
    totalValuation = 0;
    for asset in portfolio.keys():
        coinPair = asset + 'USDT';
        
        for coin in latestPrices:
            if(coin['symbol'] == coinPair):
                perCoinValue = round(float(coin['price']), 4);
                assetPrice = round(portfolio[asset] * perCoinValue, 4);
                log.critical(asset + ' => ' + str(portfolio[asset]) + " USD value: " + str(assetPrice) + " (" + str(perCoinValue) + ")");
                totalValuation += assetPrice;
                break;
    
    totalValuation += portfolio['USDT'];
    
    
    log.critical('USDT' + ' => ' + str(portfolio['USDT']))
    log.critical("---------------------------------------------");
    log.critical("Total valuation of your portfolio: " + str(totalValuation));
    return round(totalValuation, 2);
                
def aboveAllEMAs(ema8, ema13, ema21, ema55, price, high, low):
    if ((ema8 < price and ema13 < price and ema21 < price and ema55 < price) and 
       (ema8 < high and ema13 < high and ema21 < high and ema55 < high) and
       (ema8 < low and ema13 < low and ema21 < low and ema55 < low)):
    # if (ema8 < price and ema21 < price) and (ema8 < high and ema21 < high) and (ema8 < low and ema21 < low):
    #         if (ema13 < price and ema21 < price and ema55 < price) and (ema13 < high and ema21 < high and ema55 < high):            
    # if (ema55 < price) and (ema55 < high) and (ema55 < low):
        return True;
    return False;

def belowAllEMAs(ema8, ema13, ema21, ema55, price, high, low):
    if ((ema8 > price and ema13 > price and ema21 > price and ema55 > price) and 
       (ema8 > high and ema13 > high and ema21 > high and ema55 > high) and
       (ema8 > low and ema13 > low and ema21 > low and ema55 > low)):
#        if (ema8 > price and ema13 > price and ema21 > price and ema55 > price) and (ema8 > low and ema13 > low and ema21 > low and ema55 > low):            
        # if (ema8 > price and ema21 > price) and (ema8 > high and ema21 > high) and (ema8 > low and ema21 > low):
        # if (ema13 > price and ema21 > price and ema55 > price) and (ema13 > high and ema21 > high and ema55 > high) and (ema13 > low and ema21 > low and ema55 > low):
        # if (ema55 > price) and (ema55 > high) and (ema55 > low):
        return True;
    return False;

def playBell():
    mixer.music.play()
    
if __name__ == '__main__':
    main()    