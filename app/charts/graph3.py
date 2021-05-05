import plotly.graph_objects as go
from plotly.io import to_html

# Graph 3

def graph3(con):
    # Excecuting query
    cur = con.cursor()
    cur.execute("WITH T AS (SELECT country_id, MAX(vaccination_total) AS latest_num FROM daily_vaccination GROUP BY country_id ), U AS ( SELECT country_name, country_id, pop_size FROM country )SELECT U.country_name, T.latest_num, U.pop_size FROM T, U WHERE T.country_id = U.country_id")

    # Retrieving results
    sql_table = cur.fetchall()

    # Isolating x and y tables
    country_names = []
    vax_num = []
    pop_size = []

    for row_number in range(len(sql_table)):
        country_names.append(sql_table[row_number][0])
        vax_num.append(sql_table[row_number][1])
        pop_size.append(sql_table[row_number][2])


    # Creating chart
    fig = go.Figure(data=[
        go.Bar(name='People Vaccinated', x=country_names, y=vax_num, marker_color="#0FA3B1"),
        go.Bar(name='Population', x=country_names, y=pop_size, marker_color="#EAD2AC")
    ])

    fig.update_layout(
        title = "Population vs. Vaccinations",
        dragmode = "pan",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white")
    )

    return to_html(fig, include_plotlyjs = False, full_html=False)