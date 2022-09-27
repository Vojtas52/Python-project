from flask import Flask, render_template, request
from model_search import search_model
from n_days_search import n_days_search

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
    ############################################################
    ############################################################
    ###tady zacina kod z jupyteru na scraping
    #from model_search import search_model
    #from n_days_search import n_days_search
    
    #print("Enter your desired car model here:")
    #my_search = input()
    #soup_list = search_model(my_search)
    #print("Enter the number of past days (max. 5) that you want to include in your search here:")
    #my_days = input()
    #my_days = int(my_days)
    soup_list = search_model("octavia 3")
    my_days = 4
    if soup_list is None:
        return "Bazos does not respond.", 503
    list_of_offers_url = n_days_search(my_days, soup_list)
    #help(search_model)
    #help(n_days_search)
    ###tady konci kod z jupyteru na scraping
    ############################################################

    ############################################################
    ### tady zacina data mining part
        # DATA/TEXT MINING PART

    result = get_info(list_of_offers_url)

    

    pd.options.display.max_colwidth = 120
    test = ResultTable(result)
    test.show_results(min_price = 50000, max_price = 350000, min_year = 2013, max_year = 2018, min_mileage = 100000, max_mileage = 200000)
    test.show_best(n = 10)
    ### tady konci data mining part
    ############################################################
    ############################################################

    ### TODO
    ###ZISTIT CO TO HADZE AKO OUTPUT - PANDAS, a ci to je dobry output do listu
    ###Prerobit ze output octavia 3 z jinja-e pojde rovno ako vstup do search_model
    ### dorobit date - stlpec
    #dorobit graficky output a filter na dni...
    # nejako ulozit dni do listu a hodit to nizsie do date = ...
    #zapracovat filter tlacidlo na pocet dni (najprv napisat kod na filter a potom zapracovat jinja)
    # vyriesit chybove hlasky co hadze pandas
    
    
    #na konci updateovat readme popis + maybe diagram?_ 

    #todo - dodat scrapovani a data mining code, output spravit tak, ze sa nacitaju .py scripty a potom ten output ktory by mi normalne isiel do tabulky 
    order = list(range(1, len(result['link'].values.tolist())))
    date = list(range(1, len(result['link'].values.tolist())))
    price = result['price'].values.tolist()
    mileage = result['mileage'].values.tolist()
    yom = result['year_of_manuf'].values.tolist()
    url = result['link'].values.tolist()

    # page_data = {
    #     'order-values': ["1","2","3"], #order,
    #     'date-values': ["2022-8-11","2022-8-12","2022-8-13"], #date,
    #     'price-values': [250000, 275000, 265000], #price,
    #     'mileage-values': ["mileage 1", "mileage 2", "mileage 3"], #mileage,
    #     'yom-values': ["1","2","3"], #yom,
    #     'url-values': ["1","2","3"], #url,
    #     'input': input
    # }
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