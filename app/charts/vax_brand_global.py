import pymysql
from database import connectToDatabase

# Import these for method 2
import plotly.graph_objects as go

# Connecting to database
con = connectToDatabase()

# Excecuting query
cur = con.cursor()
cur.execute(
    "WITH V AS ( WITH T AS (SELECT country_id, vaccine_id, MAX(date_recorded) AS latest_date FROM total_vaccination_by_brand GROUP BY country_id, vaccine_id) SELECT U.country_id, U.vaccine_id, T.latest_date, U.vaccination_total FROM total_vaccination_by_brand AS U, T WHERE U.date_recorded = T.latest_date AND U.vaccine_id = T.vaccine_id AND U.country_id = T.country_id ) SELECT W.country_name, X.vaccine_name, V.vaccination_total FROM V, country AS W, vaccine AS X WHERE V.country_id = W.country_id AND V.vaccine_id = X.vaccine_id ORDER BY X.vaccine_name"
)

# Retrieving results
sql_table = cur.fetchall()

### METHOD 2 ### (Easier to understand my opinion) 

# Isolating x and y tables
country_name = []
vaccine_name = []
vaccination_total = []

for row_number in range(len(sql_table)):
    country_name.append(sql_table[row_number][0])
    vaccine_name.append(sql_table[row_number][1])
    vaccination_total.append(sql_table[row_number][2])

country_vax = []
for i in range(len(country_name)):
    country_vax.append(country_name[i] + "-" + vaccine_name[i])


# Creating chart
fig_two = go.Figure([go.Bar(x=country_vax, y=vaccination_total)])

fig_two.update_layout(
    title = "Population",
    xaxis_title = "country_name",
    yaxis_title = "pop_size",
    dragmode = "pan"
)

fig_two.show()

# bar_data = []
# for i in range(len(country_name)):
#     bar_data.append(go.Bar(x=[country_name[i] + "-" + vaccine_name[i]], y=[vaccination_total[i]]))

# # Creating chart
# fig = go.Figure(data=bar_data)
# # Change the bar mode

# fig.show()

# # Creating chart
# fig_two = go.Figure([go.Bar(x=x_col, y=y_col)])

# fig_two.update_layout(
#     title = "Population",
#     xaxis_title = "country_name",
#     yaxis_title = "pop_size",
#     dragmode = "pan"
# )

# fig_two.show()


# # Close database (regardless of method)
con.close()