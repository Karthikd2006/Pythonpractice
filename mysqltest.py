import mysql.connector

# Establish a connection to the MySQL database
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="karthik",
    password="welcome2024",
    database="rfpai" 
)

# # Create a cursor object to execute SQL queries
# cursor = connection.cursor()

# # Define the query to retrieve table names
# table_query = "SHOW TABLES"

# # Execute the query
# cursor.execute(table_query)

# # Fetch all the table names
# tables = cursor.fetchall()

# # Loop through the tables
# for table in tables:
#     table_name = table[0]
#     print("Table:", table_name)
#     # Query to select all data from the table
#     select_query = "SELECT * FROM {}".format(table_name)
#     # Execute the query
#     cursor.execute(select_query)
#     # Fetch all the rows from the table
#     rows = cursor.fetchall()
#     # Print each row
#     for row in rows:
#         print(row)

# # Close the cursor and connection
# cursor.close()
# connection.close()
