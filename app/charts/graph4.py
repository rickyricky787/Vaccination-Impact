import plotly.graph_objects as go
from plotly.io import to_html

# Graph 4

def graph4(con):
    # Excecuting query
    cur = con.cursor()
    cur.execute("WITH T AS ( SELECT country_id, MAX(vaccination_total) AS latest_num FROM daily_vaccination GROUP BY country_id ), U AS ( SELECT country_name, country_id, pop_size FROM country ) SELECT U.country_name, ((T.latest_num / U.pop_size) * 100) AS percent FROM T, U WHERE T.country_id = U.country_id")

    # Retrieving results
    sql_table = cur.fetchall()

    # Isolating x and y tables
    x_col = []
    y_col = []

    for row_number in range(len(sql_table)):
        x_col.append(sql_table[row_number][0])
        y_col.append(sql_table[row_number][1])

    # Creating chart
    fig = go.Figure([go.Bar(
        x=x_col, 
        y=y_col, 
        marker=dict(
            cmax=100,
            cmin=0,
            color=y_col,
            colorbar=dict(
                title=""
            ),
            colorscale="Viridis"
            )
        )])

    fig.update_layout(
        title = "Percentage of Population Vaccinated",
        xaxis_title = "Country",
        yaxis_title = "People Vaccinated (%)",
        dragmode = "pan",
    )

    return to_html(fig, include_plotlyjs = False, full_html=False)