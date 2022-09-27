import pandas as pd
from cache import cache
import re
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
import time
import pandas as pd

def modify_text(text):
    """ Internal function modifying the text of the add to better suit for text mining. """
    return text.replace(" ", "").replace(".", "").replace("xxx", "000").replace("-", "")

def get_numbers_from_text(text):
    """ Internal function for finding all numbers in the text. """
    text = modify_text(text)
    pattern = '[.]?[\d]+[\.]?\d*(?:[eE][-+]?\d+)?'
    list_of_numbers = re.findall(pattern, text)
    return list_of_numbers

def find_years(numbers):
    """ Internal function picking numbers which might be years from all numbers in text. """
    numbers = [x for x in numbers if (float(x) > 1980) and (float(x) < 2023)]
    return numbers

def find_km(numbers):
    """ Internal function picking numbers which might be mileage from all numbers in text. """
    numbers = [x for x in numbers if (float(x) > 3000) and (float(x) < 500000)]
    return numbers

def get_context(text, list_of_tokens, year_dictionary = ['egistr', 'rv', 'RV', 'yrob', 'ýrob', 'prov', 'rok', 'Rok'], km_dictionary = ['km', 'Km', 'KM', 'ilomet', 'ajet', 'ájez', 'achom', 'atoč'], context_span=20):
    """ Internal function looking into surroundings of each year and mileage candidate and searching for parts of words defined in dictionaries. """
    #import re
    context = []
    year = 'No match'
    km = 'No match'
    for token in find_years(list_of_tokens):
        all_occurences_indices = [m.start() for m in re.finditer(token, text)]
        for index in all_occurences_indices:
            left_index = max(index - context_span, 0)
            right_index = min(index + context_span, len(text))
            substring = text[left_index: right_index].strip()
            for s in year_dictionary:
                year_find = [m.start() for m in re.finditer(s, substring)]
                if len(year_find) > 0:
                    year = token
    for token in find_km(list_of_tokens):
        all_occurences_indices = [m.start() for m in re.finditer(token, text)]
        for index in all_occurences_indices:
            left_index = max(index - context_span, 0)
            right_index = min(index + context_span, len(text))
            substring = text[left_index: right_index].strip()
            for s in km_dictionary:
                km_find = [m.start() for m in re.finditer(s, substring)]
                if len(km_find) > 0:
                    km = token
    return [year, km]

class ResultTable(pd.core.frame.DataFrame):
    def show_results(self, min_price = 0, max_price = 10000000, min_year = 1950, max_year = 2022, min_mileage = 0, max_mileage = 500000):
        temp_table = self[(self["mileage"] != "No match") & (self["year_of_manuf"] != "No match")]
        temp_table2 = temp_table[(pd.to_numeric(temp_table["price"]) > min_price) & (pd.to_numeric(temp_table["price"]) < max_price) &
                (pd.to_numeric(temp_table["year_of_manuf"]) > min_year) & (pd.to_numeric(temp_table["year_of_manuf"]) < max_year) &
                    (pd.to_numeric(temp_table["mileage"]) > min_mileage) & (pd.to_numeric(temp_table["mileage"]) < max_mileage)].sort_values(by = "price")
        print(temp_table2)
    def show_best(self, n = 5, penalty = 5000):
        temp_table = self[(self["mileage"] != "No match") & (self["year_of_manuf"] != "No match")]
        temp_table = temp_table.assign(score=lambda x: ((2022 - pd.to_numeric(x.year_of_manuf))*penalty +
                                    pd.to_numeric(x.mileage)) / pd.to_numeric(x.price))
        temp_table = temp_table.sort_values(by = "score").head(n)
        print(temp_table)

def get_info(links):
    """ Get_info is a final function performing text mining and creating results in form of ResultTable class. """
    results_temp = []

    for i in links:
        if i in cache:
            add_page = cache[i]
            print("Loaded", i, 'from cache')
        else:
            add_page = requests.get(i)
            if not add_page.status_code == 200:
                print(i, add_page.status_code)
                continue
            cache[i] = add_page

        print(i, add_page)
        
            
        soup_add = BeautifulSoup(add_page.text, 'html')
        #print(f"soup_add=") # looking for a bug
        add = modify_text(soup_add.find('div', {'class':'popisdetail'}).get_text())
        #print(f"add=") # looking for a bug
        price = soup_add.find('table').find_all('b')[-1].get_text()
        #print(f"price=") # looking for a bug
        all_numbers = get_numbers_from_text(add)
        #print(f"all_numbers=") # looking for a bug
        context_got = get_context(add, all_numbers)
        #print(f"context_got=") # looking for a bug
        result = [i, context_got[0], context_got[1], price.replace(" ", "").replace("Kč", "")]
        #print(f"result=") # looking for a bug
        results_temp.append(result)
        time.sleep(0.1)
    results = ResultTable(results_temp)
    results.columns = ['link', 'year_of_manuf', 'mileage', 'price']
    results = results[(results["price"] != "Dohodou") & (results["price"] != "Vtextu") & (results["price"] != "Nabídněte")]
    return results
