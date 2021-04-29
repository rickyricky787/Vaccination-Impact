from flask import Flask, render_template
from database import connectToDatabase
import charts

# Initiating Flask app
app = Flask(__name__)

# Connecting to database
con = connectToDatabase()

# Main page
@app.route("/")
def index():

    # Turn graphs into a long html div string
    plot1 = charts.graph1(con)
    plot2 = charts.graph2(con)
    plot3 = charts.graph3(con)
    plot4 = charts.graph4(con)
    plot5 = charts.graph5(con)
    plot6 = charts.graph6(con)
    plot7 = charts.graph7(con)
    plot8 = charts.graph8(con)

    # #Close database (regardless of method)
    # con.close()
    return render_template(
        "test.html", 
        plot1 = plot1, 
        plot2 = plot2,
        plot3 = plot3,
        plot4 = plot4,
        plot5 = plot5,
        plot6 = plot6,
        plot7 = plot7,
        plot8 = plot8,
    )