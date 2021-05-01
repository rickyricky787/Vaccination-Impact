import plotly.graph_objects as go
from plotly.io import to_html

def table2(con):
    # Excecuting query
    cur = con.cursor()
    cur.execute("WITH V AS ( WITH T AS ( SELECT country_id, MAX(date_recorded) AS latest_date FROM covid_data GROUP BY country_id ) SELECT U.country_id, T.latest_date, U.total_deaths FROM covid_data AS U, T WHERE U.date_recorded = T.latest_date AND U.country_id = T.country_id ) SELECT W.country_name, V.total_deaths FROM V, country AS W WHERE V.country_id = W.country_id ORDER BY V.total_deaths DESC LIMIT 10")

    # Retrieving results
    sql_table = cur.fetchall()

    # Isolating x and y tables
    country_names = []
    total_deaths = []

    for row_number in range(len(sql_table)):
        country_names.append(sql_table[row_number][0])
        total_deaths.append(sql_table[row_number][1])
    
    # Making table
    fig = go.Figure(data=[go.Table(header=dict(values=['Rank', 'Country', 'Total Deaths']),
                 cells=dict(values=[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], country_names, total_deaths]))
                     ])
    
    fig.update_layout(
        title = "Top 10 Total COVID-19 Deaths Globally"
    )

    return to_html(fig, include_plotlyjs = False, full_html=False)