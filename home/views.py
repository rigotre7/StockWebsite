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
py.sign_in('rigotre', 'sjqnnlbl6v')
import io
import pdb

# Come here from home/urls.py
def index(request):
    return render(request, 'home/home.html')

def get_image(request):
    #get the name and date of the stock below

    stock = request.GET.get("name")
    stockNames = stock.split(",")
    numStocksToCompare = len(stock.split(','))
    d = request.GET.get('date')

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

    d = json_data[0]
    startDate = dt.strptime(d[0], '%Y-%m-%d')

    #if there are more than one stocks to compare
    if numStocksToCompare >1:
        for day in json_data:
            #populate lists with all the data
            date.append(dt.strptime(day[0], '%Y-%m-%d'))
            price.append(day[1])

        end = len(date)/numStocksToCompare
        start = 0

        for x in range (0, numStocksToCompare):
            #split the list data for the respective
            datesFinal = date[int(start):int(end)]
            pricesFinal = price[int(start):int(end)]

            #pdb.set_trace()
            plt.plot_date(datesFinal, pricesFinal, '-')
            start = end
            end = end+end



    else:
        #store the price and date information for each day
        for day in json_data:
            date.append(dt.strptime(day[0], '%Y-%m-%d'))
            price.append(day[1])

        plt.plot_date(date, price, '-', label = "Google")


    #plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(stock.upper() + " Stock")





    #finally, we create plotly figure
    mpl_fig = plt.gcf()
    py_fig = tls.mpl_to_plotly(mpl_fig, verbose=True)
    py.iplot_mpl(mpl_fig, filename='graph')

    return render(request, 'home/graph.html')
