import pandas as pd
import plotly.express as px
import pymysql
from database import connectToDatabase

# Connecting to database
con = connectToDatabase()

# Excecuting query
cur = con.cursor()
cur.execute("SELECT country_name, pop_size FROM country")

# Retrieving results
rows = cur.fetchall()

# Creating a table
x_name = "country_name"
y_name = "pop_size"
df = pd.DataFrame(rows, columns = [x_name, y_name])

# Creating the figure
fig = px.bar(df, x = x_name, y = y_name)
fig.update_layout(dragmode="pan")
fig.show()  # Displays the figue

# Close database
con.close()