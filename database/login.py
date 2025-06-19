import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '')))

from connection import get_db_cursor

curor=get_db_cursor()
def login_user(email, password):
    """Check if the user exists and the password matches."""
    if not email or not password:
        return False, "Email and password are required."

    try:
        query = "SELECT * FROM Users WHERE Email = ? AND Password = ?"
        curor.execute(query, (email, password))
        user = curor.fetchone()
        if user:
            return True, "Login successful."
        else:
            return False, "Invalid email or password."
    except Exception as e:
        return False, f"An error occurred: {e}"