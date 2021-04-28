import pymysql
from database import connectToDatabase

# Import these for method 2
import plotly.graph_objects as go

# Connecting to database
con = connectToDatabase()

# Excecuting query
cur = con.cursor()
cur.execute("WITH T AS ( SELECT country_id, MAX(vaccination_total) AS latest_num FROM daily_vaccination GROUP BY country_id), U AS ( SELECT country_id, continent_id FROM country ), V AS ( SELECT continent_name, continent_id FROM continent ) SELECT V.continent_name, SUM(T.latest_num)FROM T, U, V WHERE T.country_id = U.country_id AND U.continent_id = V.continent_id GROUP BY U.continent_id")

# Retrieving results
sql_table = cur.fetchall()

### METHOD 2 ### (Easier to understand my opinion) 

# Isolating x and y tables
continent_name = []
vax_number = []

for row_number in range(len(sql_table)):
    continent_name.append(sql_table[row_number][0])
    vax_number.append(sql_table[row_number][1])

# Creating chart
fig_two = go.Figure([go.Bar(x=continent_name, y=vax_number, marker_color="#F9A620")])

fig_two.update_layout(
    title = "Vaccinations per Continent",
    xaxis_title = "Continent",
    yaxis_title = "Number of People",
    dragmode = "pan"
)

fig_two.show()


# # Close database (regardless of method)
con.close()