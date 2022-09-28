from flask import Flask, render_template, request
from model_search import search_model
from n_days_search import n_days_search, DATE_DICT

from data_mining import *
from cache import cache

import re
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
import time
import pandas as pd

app = Flask(__name__)
app.jinja_env.filters['zip'] = zip

@app.route("/")

def root():
    
    print(f'{cache=}')
    input = request.args.get('input')
    if not input:
        return render_template("index.j2")
    
    input2 = request.args.get('input2')
    input2 = input2 if input2 else 4
    my_days = int(input2)

    ############################################################
    ###tady zacina kod na scraping
    #soup_list = search_model('octavia 3')
    soup_list = search_model(input)

    if soup_list is None:
        return "Bazos does not respond, please try again later.", 503
    list_of_offers_url = n_days_search(my_days, soup_list)
    
    # help(search_model)
    # help(n_days_search)
    ###tady konci kod na scraping
    
    ############################################################
    ### tady zacina data mining part

    result = get_info(list_of_offers_url)

    pd.options.display.max_colwidth = 120
    test = ResultTable(result)
    test.show_results(min_price = 50000, max_price = 350000, min_year = 2013, max_year = 2018, min_mileage = 100000, max_mileage = 200000)
    test.show_best(n = 10)
    ### tady konci data mining part
    ############################################################
    

    # NOTE: v pripade ze bazos nechce povolit/blokuje scrapovani muzeme nacist
    # 'result_filtered_backup.csv' a natahnout promenne below z daneho dataframe-u

    order = list(range(1, len(result['link'].values.tolist())))
    price = result['price'].values.tolist()
    mileage = result['mileage'].values.tolist()
    yom = result['year_of_manuf'].values.tolist()
    url = result['link'].values.tolist()
    
    date = []
    for link in url:
        if link in DATE_DICT.keys():
            date.append(DATE_DICT[link])

    page_data = {
            'order-values': order,
            'date-values': date,
            'price-values': price,
            'mileage-values': mileage,
            'yom-values': yom,
            'url-values': url,
            'input': input
        }

    return render_template("index.j2", page_data=page_data)

if __name__ == "__main__":
    app.run(port=8080)
