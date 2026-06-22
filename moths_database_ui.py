
# Import the libraries to connect to the database and present the information in tables
import sqlite3
from tabulate import tabulate

# This is the filename of the database to be used
DB_NAME = 'moths_database.db'

# This is the SQL to connect to all the tables in the database - only needed if you are using a parameter query (Excellence)
TABLES = (" moths "
           "LEFT JOIN origin ON moths.origin_id = origin.origin_id "
            "LEFT JOIN endemic ON moths.endemic_id = endemic.endemic_id "
            "LEFT JOIN lifespan ON moths.lifespan_id ")




def print_query(view_name:str):
    ''' Prints the specified view from the database in a table '''
    # Set up the connection to the database
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    # Get the results from the view
    sql = "SELECT * FROM '" + view_name + "'"
    cursor.execute(sql)
    results = cursor.fetchall()
    # Get the field names to use as headings
    field_names = "SELECT name from pragma_table_info('" + view_name + "') AS tblInfo"
    cursor.execute(field_names)
    headings = list(sum(cursor.fetchall(),()))
    # Print the results in a table with the headings
    print(tabulate(results,headings))
    db.close()

def print_parameter_query(fields:str, where:str, parameter):
    """ Prints the results for a parameter query in tabular form. 
        Only required for Excellence """
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    sql = ("SELECT " + fields + " FROM " + TABLES + " WHERE " + where)
    cursor.execute(sql,(parameter,))
    results = cursor.fetchall()
    print(tabulate(results,fields.split(",")))
    db.close()  



# A IN COMMON NAME
# LIFESPAN BELOW 9
# LIFESPAN TOP 5
# max_wing_offset_and_limit5
# north_america_lifespan7
# not_europe_has_e
# wingspan_over100
# wingspan_sortby_scientifitc
# wingspans

print_query('all')

# make = input('TXTTXT MOTHS TXT: ')
# print_parameter_query("model, top_speed", "make = ? ORDER BY top_speed DESC", make)

a_in_common_name = input('Please type which letter you would like to filter by in common name: ')
print_parameter_query("common_name, max_wingspan - min_wingspan AS difference, average_wingspan, lifespan, origin", "common_name LIKE %?% ORDER BY difference", a_in_common_name)