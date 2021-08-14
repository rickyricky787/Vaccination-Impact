from flask import Flask, render_template, request
from database import connectToDatabase
import charts
import helpers

# Initiating Flask app
app = Flask(__name__)

# Connecting to database
con = connectToDatabase()

# Fetching info to be used in each webpage
country_names = helpers.getCountries(con)
last_update_date = helpers.getLastUpdateDate(con)

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
        plots.append(charts.graph8(con))
        plots.append(charts.graph9(con))
        
        # Same thing with tables
        tables = []
        tables.append(charts.table1(con))
        tables.append(charts.table2(con))
        tables.append(charts.table3(con))
        tables.append(charts.table4(con))

        return render_template(
            "index.html", 
            plots=plots, 
            tables=tables, 
            country_names=country_names,
            last_update_date=last_update_date
        )
    
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
        plots.append(charts.graph8(con))
        plots.append(charts.graph9(con))

        # Same thing with tables
        tables = []
        tables.append(charts.table1(con))
        tables.append(charts.table2(con))
        tables.append(charts.table3(con))
        tables.append(charts.table4(con))

        return render_template(
            "index.html", 
            plots=plots, 
            tables=tables, 
            country_names=country_names, 
            selection = selection,
            last_update_date=last_update_date
        )

if __name__ == '__main__':
    app.run()