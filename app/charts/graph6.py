import plotly.graph_objects as go
from plotly.io import to_html
from helpers import formatString

# Graph 6  

def graph6(con, country):
    # Excecuting query
    cur = con.cursor()
    cur.execute('WITH T AS ( SELECT country_name, country_id FROM country WHERE country_name = ' +  formatString(country) + '), U AS ( SELECT country_id, date_recorded, total_cases, total_deaths FROM covid_data ) SELECT U.date_recorded, U.total_cases, U.total_deaths FROM T, U WHERE T.country_id = U.country_id')

    # Retrieving results
    sql_table = cur.fetchall()

    # Isolating x and y tables
    date_recorded = []
    cases_per_day = []
    deaths_per_day = []


    for row_number in range(len(sql_table)):
        date_recorded.append(sql_table[row_number][0])
        cases_per_day.append(sql_table[row_number][1])
        deaths_per_day.append(sql_table[row_number][2])

    # Creating chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x = date_recorded,
        y = cases_per_day,
        name = 'Total Cases',
        fill='tozeroy'
    ))

    fig.add_trace(go.Scatter(
        x = date_recorded,
        y = deaths_per_day,
        name = 'Total Deaths',
        fill='tozeroy'
    ))

    fig.update_layout(
        title = country + " Total COVID-19 Cases and Deaths",
        xaxis_title = "Date Recorded",
        yaxis_title = "Number of People",
        dragmode = "pan",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white")
    )

    return to_html(fig, include_plotlyjs = False, full_html=False)