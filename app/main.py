from flask import Flask, render_template, request
from database import connectToDatabase
import charts
import helpers

# Initiating Flask app
app = Flask(__name__)

# Connecting to database
con = connectToDatabase()

# Main page
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # Turn graphs into a long html div string
        plots = []
        plots.append(charts.graph1(con))
        plots.append(charts.graph2(con))
        plots.append(charts.graph3(con))
        plots.append(charts.graph4(con))
        plots.append(charts.graph5(con))
        plots.append(charts.graph6(con, "Afghanistan"))
        plots.append(charts.graph7(con, "Afghanistan"))
        plots.append(charts.graph8(con))

        # Get list of country names
        country_names = helpers.getCountries(con)

        return render_template("test.html", plots=plots, country_names = country_names)
    
    elif request.method == 'POST':
        selection = request.form.get('country')
        
        # Turn graphs into a long html div string
        plots = []
        plots.append(charts.graph1(con))
        plots.append(charts.graph2(con))
        plots.append(charts.graph3(con))
        plots.append(charts.graph4(con))
        plots.append(charts.graph5(con))
        plots.append(charts.graph6(con, selection))
        plots.append(charts.graph7(con, selection))
        plots.append(charts.graph8(con))

        # Get list of country names
        country_names = helpers.getCountries(con)

        return render_template("test.html", plots=plots, country_names = country_names, selection = selection)