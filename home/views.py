from django.shortcuts import render
import urllib
import json
from django.http import HttpResponse
import matplotlib as mpl
mpl.use('Agg') # Required to redirect locally
import matplotlib.pyplot as plt
import datetime as dt
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
    #pdb.set_trace()
    stock = request.GET.get("stockName")
    stock_price_url = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?ticker=+stock+&date.gte=20151101&qopts.columns=date,close&api_key=-2H8WyYB8b7FaCshLLTN'

    date = []
    price = []

    stock_price_url = stock_price_url.replace("+stock+", stock)
    source_code = urllib.request.urlopen(stock_price_url).read().decode()

    json_root = json.loads(source_code)
    json_datatable = json_root["datatable"]
    json_data = json_datatable["data"]

    for day in json_data:
        date.append(dt.datetime.strptime(day[0], '%Y-%m-%d'))
        price.append(day[1])

    plt.plot_date(date, price, '-')

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(stock.upper() + " Stock")

    mpl_fig = plt.gcf()
    py_fig = tls.mpl_to_plotly(mpl_fig, verbose=True)
    py.iplot_mpl(mpl_fig, filename='graph')

    return render(request, 'home/graph.html')


    #f = io.BytesIO()
    #plt.savefig(j, format="png")    #save the plot to the BytesIO stream implementation
    #plt.clf()

    ##Add the contents of the cStringIO object to the response, matching the
    #mime type with the plot format (in this case, PNG) and return
    #return HttpResponse(f.getvalue(), content_type="image/png")
