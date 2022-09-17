from flask import Flask, render_template, request

app = Flask(__name__)
app.jinja_env.filters['zip'] = zip

@app.route("/")

def root():
    
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