from flask import Flask, render_template, request
from model_search import search_model
from n_days_search import n_days_search

app = Flask(__name__)
app.jinja_env.filters['zip'] = zip

@app.route("/")

def root():
    
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
    list_of_offers_url = n_days_search(my_days, soup_list)
    help(search_model)
    help(n_days_search)
    ###tady konci kod z jupyteru na scraping
    ############################################################

    ############################################################
    ### tady zacina data mining part
        # DATA/TEXT MINING PART
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
            print(i)
            add_page = requests.get(i)
            soup_add = BeautifulSoup(add_page.text, 'html')
            add = modify_text(soup_add.find('div', {'class':'popisdetail'}).get_text())
            price = soup_add.find('table').find_all('b')[-1].get_text()
            all_numbers = get_numbers_from_text(add)
            context_got = get_context(add, all_numbers)
            result = [i, context_got[0], context_got[1], price.replace(" ", "").replace("Kč", "")]
            results_temp.append(result)
            time.sleep(0.2)
        results = ResultTable(results_temp)
        results.columns = ['link', 'year_of_manuf', 'mileage', 'price']
        results = results[(results["price"] != "Dohodou") & (results["price"] != "Vtextu") & (results["price"] != "Nabídněte")]
        return results
    result = get_info(list_of_offers_url)


    pd.options.display.max_colwidth = 120
    test = ResultTable(result)
    test.show_results(min_price = 50000, max_price = 350000, min_year = 2013, max_year = 2018, min_mileage = 100000, max_mileage = 200000)
    test.show_best(n = 10)
    ### tady konci data mining part
    ############################################################
    ############################################################

    input = request.args.get('input')
    if not input:
        return render_template("index.j2")


    #todo - dodat scrapovani a data mining code, output spravit tak, ze sa nacitaju .py scripty a potom ten output ktory by mi normalne isiel do tabulky 
    order = []
    date = []
    price = []
    mileage = []
    yom = []
    url = []

    page_data = {
        'order-values': ["1","2","3"], #order,
        'date-values': ["2022-8-11","2022-8-12","2022-8-13"], #date,
        'price-values': [250000, 275000, 265000], #price,
        'mileage-values': ["mileage 1", "mileage 2", "mileage 3"], #mileage,
        'yom-values': ["1","2","3"], #yom,
        'url-values': ["1","2","3"], #url,
        'input': input
    }

    return render_template("index.j2", page_data=page_data)

if __name__ == "__main__":
    app.run(port=8080)