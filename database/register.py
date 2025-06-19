import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '')))

from connection import get_db_cursor
curor=get_db_cursor()
def register_user(name,email, password):
    try:
        # Check if the user already exists
        query = "SELECT * FROM Users WHERE Email = ?"
        curor.execute(query, (email,))
        existing_user = curor.fetchone()
        
        if existing_user:
            return False, "User already exists."

        # Insert the new user into the database
        insert_query = "INSERT INTO Users (Name, Email, Password) VALUES (?, ?, ?)"
        curor.execute(insert_query, (name, email, password))
          # Commit the transaction        
        return True, "User registered successfully."
    except Exception as e:
        return False, f"An error occurred: {e}"