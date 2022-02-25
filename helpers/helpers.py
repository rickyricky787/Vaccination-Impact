def getCountries(con):
    cur = con.cursor()
    cur.execute("SELECT DISTINCT country_name FROM country")

    # Retrieving results
    sql_table = cur.fetchall()
    country_name = []

    for row_number in range(len(sql_table)):
        country_name.append(sql_table[row_number][0])
    
    return country_name

def formatString(string):
    return "\"" + string + "\""

