from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
#@app.route("/")
#@app.before_first_request
def _run_on_start():

   return "Hello, I am your bazos.cz car searching engine. \n Please insert the name of your desired car model below."

#@app.route("/")
def root():
    input = request.args.get('input')
    if not input:
        return render_template("index.j2")

    page_data = {
        'x-values': ["2022-8-11","2022-8-12","2022-8-13"],
        'y-values': [250000, 275000, 265000],
        'input': input
    }

    return render_template("index.j2", page_data=page_data)

#ap@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('action1') == 'VALUE1':
            pass # do something

        elif  request.form.get('action2') == 'VALUE2':
            pass # do something else
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('index.html')#, form=form)
    
    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=8080)