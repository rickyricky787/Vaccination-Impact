import pymysql
from database import connectToDatabase

# Import these for method 2
import plotly.graph_objects as go

# Connecting to database
con = connectToDatabase()

# Excecuting query
cur = con.cursor()
cur.execute("SELECT U.country_name, COUNT(T.country_id)FROM vaccine_brand_in_country AS T, country AS U WHERE U.country_id = T.country_id GROUP BY T.country_id")

# Retrieving results
sql_table = cur.fetchall()

# Isolating x and y tables
x_col = []
y_col = []

for row_number in range(len(sql_table)):
    x_col.append(sql_table[row_number][0])
    y_col.append(sql_table[row_number][1])

# Creating chart
fig_two = go.Figure([go.Bar(x=x_col, y=y_col, marker_color="#5BBA6F")])

fig_two.update_layout(
    title = "Number of Vaccine Brands per Country",
    xaxis_title = "Country",
    yaxis_title = "Count",
    dragmode = "pan"
)

fig_two.show()


# # Close database (regardless of method)
con.close()