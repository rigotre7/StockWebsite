from django.shortcuts import render
import urllib
import json
from django.http import HttpResponse
import matplotlib as mpl
mpl.use('Agg') # Required to redirect locally
import matplotlib.pyplot as plt
from datetime import datetime as dt
import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *
py.sign_in('rtrejo', 's6ZpDxfpUMaP43pil54z')
import pdb

# Come here from home/urls.py
def index(request):
    return render(request, 'home/home.html')

def abt(request):
    return render(request, 'home/about.html')

def get_image(request):
    #get the name and date of the stock below
    stock = request.GET.get("name")
    stockNames = stock.split(",")
    stockNames.sort()
    numStocksToCompare = len(stock.split(','))
    d = request.GET.get('date')
    begDate = dt.strptime(d, '%Y-%m-%d')
    d = d.replace('-', "")

    stock_price_url = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?ticker=+stock+&date.gte=dt&qopts.columns=date,close&api_key=-2H8WyYB8b7FaCshLLTN'

    date = []
    price = []

    stock_price_url = stock_price_url.replace("+stock+", stock)
    stock_price_url = stock_price_url.replace("dt", d)
    source_code = urllib.request.urlopen(stock_price_url).read().decode()

    json_root = json.loads(source_code)
    json_datatable = json_root["datatable"]
    json_data = json_datatable["data"]

    datesFinal = []
    pricesFinal = []

    #if there are more than one stocks to compare
    if numStocksToCompare >1:
        for day in json_data:
            #populate lists with all the data
            date.append(dt.strptime(day[0], '%Y-%m-%d'))
            price.append(day[1])
            dataLength = len(date)


        #day will be the current day in the stock information that we received
        day = date[0]
        dayPrice = price[0]
        i = 1
        #get the stock information for each stock
        for x in range(0, numStocksToCompare):
            datesFinal.append(day)  #store the first date and price
            pricesFinal.append(dayPrice)
            day=date[i]
            while ((abs((day - datesFinal[-1]).days) < 6)):    #if the range between the last date and newest date is larger than 5, we are at a new stock
                datesFinal.append(day)
                dayPrice = price[i]
                pricesFinal.append(dayPrice)
                i+=1
                #if we've reached the end of the data
                if(i == dataLength):
                    break
                day = date[i]


            d = datesFinal
            p = pricesFinal
            plt.plot_date(d, p, '-', label=stockNames[x].upper())    #plot the graph
            #if we've plotted all the stocks, break out of the loop
            if(stockNames[x] == stockNames[len(stockNames)- 1]):
                break
            del datesFinal[:]
            del pricesFinal[:]
            dayPrice = price[i] #store the first price of the next stock



    else:
        #store the price and date information for each day
        for day in json_data:
            date.append(day[0])
            price.append(day[1])

        plt.plot_date(date, price, '-', label=stock.upper())

    #make sure the legend appears when the plotly graph is made
    update = dict(layout=dict(showlegend=True))

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(stock.upper() + " Stock")

    #finally, we create plotly figure
    mpl_fig = plt.gcf()
    py_fig = tls.mpl_to_plotly(mpl_fig, verbose=True)
    py.iplot_mpl(mpl_fig, update=update, filename='graph')

    return render(request, 'home/graph.html')
