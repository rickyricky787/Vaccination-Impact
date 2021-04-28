import pymysql
from database import connectToDatabase

# Import these for method 2
import plotly.graph_objects as go

# Connecting to database
con = connectToDatabase()

# Excecuting query
cur = con.cursor()
cur.execute(
    "WITH V AS ( WITH T AS (SELECT country_id, vaccine_id, MAX(date_recorded) AS latest_date FROM total_vaccination_by_brand GROUP BY country_id, vaccine_id) SELECT U.country_id, U.vaccine_id, T.latest_date, U.vaccination_total FROM total_vaccination_by_brand AS U, T WHERE U.date_recorded = T.latest_date AND U.vaccine_id = T.vaccine_id AND U.country_id = T.country_id ) SELECT W.country_name, X.vaccine_name, V.vaccination_total FROM V, country AS W, vaccine AS X WHERE V.country_id = W.country_id AND V.vaccine_id = X.vaccine_id ORDER BY W.country_name"
)

# Retrieving results
sql_table = cur.fetchall()
sql_table = list(sql_table)

# Filling countries with no vaccine of a certain brand with zeroes
vaccine_name = []

for row_number in range(len(sql_table)):
    vaccine_name.append(sql_table[row_number][1])

vaccine_brands = sorted(list(set(vaccine_name)))

country_to_brand = dict()

for item in sql_table:
    if item[0] not in country_to_brand.keys():
        country_to_brand[item[0]] = [item[1]]
    else:
        country_to_brand[item[0]].append(item[1])

country_name = list(country_to_brand.keys())

for pos in range(len(country_to_brand)):
    for brand in vaccine_brands:
        if brand not in country_to_brand[country_name[pos]]:
            sql_table.append((country_name[pos], brand, 0))

sql_table = sorted(sql_table)

vaccination_total = [[] for i in range(len(country_name))]

count = 0
for i in range(len(country_name)):
    for j in range(len(vaccine_brands)):
        vaccination_total[i].append(sql_table[count][2])
        count = count + 1


bar_data = []
for i in range(len(country_name)):
    bar_data.append(go.Bar(
        name=country_name[i], 
        y=vaccine_brands, 
        x=vaccination_total[i], 
        orientation = "h"
        ))

# Creating chart
fig = go.Figure(data=bar_data)

# Change the bar mode
fig.update_layout(
    title = "People Vaccinated per Brand Globally",
    yaxis_title = "Vaccine Brand",
    xaxis_title = "People Vaccinated",
    dragmode = "pan",
    barmode = "group",
    legend_traceorder="reversed"
)
fig.show()

# # Close database (regardless of method)
con.close()