from django.shortcuts import render
import urllib
import json
from django.http import HttpResponse
import matplotlib as mpl
mpl.use('Agg') # Required to redirect locally
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import io
import pdb

# Come here from home/urls.py
def index(request):
    return render(request, 'home/home.html')

def get_image(request):
    stock_price_url = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?ticker=GOOGL&date.gte=20151101&qopts.columns=date,close&api_key=-2H8WyYB8b7FaCshLLTN'

    date = []
    price = []

    #pdb.set_trace()
    #stock_price_url = stock_price_url.replace("+stock+", stock)
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
    plt.title("Google Stock")

    #pdb.set_trace()
    f = io.BytesIO()
    plt.savefig(f, format="png")
    plt.clf()

    return HttpResponse(f.getvalue(), content_type="image/png")
