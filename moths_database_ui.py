
# Import the libraries to connect to the database and present the information in tables
import sqlite3
from tabulate import tabulate

# This is the filename of the database to be used
DB_NAME = 'moths_database.db'

# This is the SQL to connect to all the tables in the database - only needed if you are using a parameter query (Excellence)
TABLES = (" moths "
           "LEFT JOIN origin ON moths.origin_id = origin.origin_id "
            "LEFT JOIN endemic ON moths.endemic_id = endemic.endemic_id "
            "LEFT JOIN lifespan ON moths.lifespan_id = lifespan.lifespan_id ")




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

# MENU
menu_choice = ''
while menu_choice != 'Z':
    menu_choice = input('Welcome to the moths database.'
                        'Type the letter of the information you want to see: \n'
                        'A: All Moths.\n'
                        'B: Shows moths with specific letter in their common name.\n'
                        'C: Shows moths with a lifespan below a specified number.\n'
                        'D: Shows the top five moths with the longest lifespan.\n'
                        'E: Shows the top five runner ups for the biggest wingspan.\n'
                        'F: Shows moths with a lifespan above 7 and from a specific continent.\n'
                        'G:\n'
                        'H:\n'
                        'I:\n'
                        'J:\n' \
                        'Z: Exit\n\n' \
                        'Type choice here: ')
    menu_choice = menu_choice.upper()
    if menu_choice == 'A':
        print_query('all')
    elif menu_choice == 'B':
        a_in_common_name = input('Please type which letter you would like to filter by in common name: ')
        print_parameter_query("common_name, max_wingspan - min_wingspan AS difference, average_wingspan, lifespan, origin", "common_name LIKE '%'||?||'%' ORDER BY difference", a_in_common_name)
    elif menu_choice == 'C':
        lifespan_below9 = int(input('Please type the number you would like to see lifespans of non-endemic moths below: '))
        print_parameter_query("scientific_name, common_name, origin, lifespan, min_wingspan, max_wingspan, endemic", "lifespan < ? AND endemic = 'No' ORDER BY lifespan", lifespan_below9)
    elif menu_choice == 'D':
        print_query('lifespan_top5')
    elif menu_choice == 'E':
        print_query('max_wing_offset_limit5')
    elif menu_choice == 'F':
        north_america_lifespan7 = input('Please type the continent of which moths you would like to see with a lifespan above 7. Your options are:\n'
        'North America, Oceania, Europe, Asia, Africa.\n'
        'Type option here: ').title()
        print_parameter_query("common_name, lifespan", "origin = ? AND lifespan > 7", north_america_lifespan7)
    elif menu_choice == 'G':
        not_europe_has_e = input('Please which letter you would like to filter by, excluding moths from Europe:')
        print_parameter_query("common_name, scientific_name, origin, endemic, lifespan, average_wingspan, max_wingspan, min_wingspan, max_wingspan - min_wingspan AS difference", "origin <> Europe AND (common_name LIKE '%'||?||'%' OR (scientific_name LIKE '%'||?||'%' AND average_wingspan <= 100))", not_europe_has_e)
    elif menu_choice == 'H':
        print_query('wingspan_over100')
    elif menu_choice == 'I':
        print_query('wingspan_sortby_scientific')
    elif menu_choice == 'J':
        print_query('wingspans')
    


# A IN COMMON NAME done
# LIFESPAN BELOW 9 done
# LIFESPAN TOP 5 done
# max_wing_offset_and_limit5
# north_america_lifespan7
# not_europe_has_e
# wingspan_over100
# wingspan_sortby_scientifitc
# wingspans


# make = input('TXTTXT MOTHS TXT: ')
# print_parameter_query("model, top_speed", "make = ? ORDER BY top_speed DESC", make)