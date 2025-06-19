import pyodbc

# Global variable to store the database connection
_db_connection = None  

def get_db_cursor():
    """Returns a cursor. If no connection exists, create one."""
    global _db_connection
    if _db_connection is None:
        try:
            _db_connection = pyodbc.connect(
            "Driver={ODBC Driver 18 for SQL Server};" 
            "SERVER=DESKTOP-LT3D8HN;"
            "DATABASE=Snazzy;"
            "UID=;"
            "PWD=;"
            "Trusted_Connection=yes;"
        )
            print("Database connection established successfully.")
        except Exception as e:
            print("Database connection error:", e)
            return None  

    return _db_connection.cursor()  # Return the cursor object


  