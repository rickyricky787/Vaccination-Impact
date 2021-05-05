from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.io import to_html
from helpers import formatString

# Graph 6  

def graph6(con, country):
    # Excecuting query
    cur = con.cursor()
    cur.execute('WITH T AS ( SELECT country_name, country_id FROM country WHERE country_name = ' +  formatString(country) + '), U AS ( SELECT country_id, date_recorded, total_cases, total_deaths, new_cases, new_deaths FROM covid_data ) SELECT U.date_recorded, U.total_cases, U.total_deaths, U.new_cases, U.new_deaths FROM T, U WHERE T.country_id = U.country_id')

    # Retrieving results
    sql_table = cur.fetchall()

    # Isolating x and y tables
    date_recorded = []
    total_cases = []
    total_deaths = []
    new_cases = []
    new_deaths = []


    for row_number in range(len(sql_table)):
        date_recorded.append(sql_table[row_number][0])
        total_cases.append(sql_table[row_number][1])
        total_deaths.append(sql_table[row_number][2])
        new_cases.append(sql_table[row_number][3])
        new_deaths.append(sql_table[row_number][4])


    # Creating chart
    fig = make_subplots(rows=1, cols=2)

    fig.add_trace(go.Scatter(
        x = date_recorded,
        y = total_cases,
        name = 'Total Cases',
        fill='tozeroy'
        ), 
        row=1, col=1)

    fig.add_trace(go.Scatter(
        x = date_recorded,
        y = total_deaths,
        name = 'Total Deaths',
        fill='tozeroy'
        ), 
        row=1, col=1)

    fig.add_trace(go.Scatter(
        x = date_recorded,
        y = new_cases,
        name = 'New Cases',
        fill='tozeroy'
        ), 
        row=1, col=2)

    fig.add_trace(go.Scatter(
        x = date_recorded,
        y = new_deaths,
        name = 'New Deaths',
        fill='tozeroy',
        line_color="orange"
        ), 
        row=1, col=2)

    

    fig.update_layout(
        title = country + " COVID-19 Cases and Deaths",
        xaxis_title = "Date Recorded",
        yaxis_title = "Number of People",
        dragmode = "pan",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
        modebar_activecolor="white"
    )

    return to_html(fig, include_plotlyjs = False, full_html=False)