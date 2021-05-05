import plotly.graph_objects as go
from plotly.io import to_html

# Graph 9

def graph9(con):
    # Excecuting query
    cur = con.cursor()
    cur.execute("WITH V AS ( WITH T AS ( SELECT country_id, MAX(date_recorded) AS latest_date FROM covid_data GROUP BY country_id ) SELECT U.country_id, T.latest_date, U.new_cases, U.new_deaths FROM covid_data AS U, T WHERE U.date_recorded = T.latest_date AND U.country_id = T.country_id ) SELECT W.country_name, V.new_cases, V.new_deaths FROM V, country AS W WHERE V.country_id = W.country_id")

    # Retrieving results
    sql_table = cur.fetchall()

    # Isolating x and y tables
    country_names = []
    total_cases = []
    total_deaths = []

    for row_number in range(len(sql_table)):
        country_names.append(sql_table[row_number][0])
        total_cases.append(sql_table[row_number][1])
        total_deaths.append(sql_table[row_number][2])


    # Creating chart
    fig = go.Figure(data=[
        go.Bar(name='Total Cases', x=country_names, y=total_cases),
        go.Bar(name='Total Deaths', x=country_names, y=total_deaths)
    ])

    fig.update_layout(
        title = "Newest Total Cases and Deaths per Country",
        dragmode = "pan",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
        modebar_activecolor="white"
    )

    return to_html(fig, include_plotlyjs = False, full_html=False)