from flask import Flask, render_template, request, redirect, flash, url_for
app = Flask(__name__, static_url_path="", static_folder="static")
from config import Config
from forms import LoginForm
from nlp import process_query

app.config.from_object(Config)
@app.route('/')
def renders():
    return render_template("Litscan2.html")

@app.route('/techniques')
def techniques():
    return render_template("techniques.html")

@app.route('/about')
def about():
    return render_template("About.html")
@app.route('/results', methods=["POST", "GET"])
def results():
    if request.method == 'POST':
        query = request.form['phrase']
        results = process_query(query)
        overview = ""
        
        pluralization = ""
        if results[0] == 1:
            pluralization = "literary device"
        elif results[0] != 1:
            pluralization = "literary devices"
        
        overview = "Your phrase has " + str(results[0]) + " " + pluralization
        if not results[0]:
            overview = "The phrase you entered contains 0 literary devices. Try another phrase!"

        return render_template("Results.html", phrase=query, overview=overview, listings=results[1])

if __name__ == "__main__":
	app.run()
