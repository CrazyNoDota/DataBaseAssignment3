from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

DATABASE_URL = 'mysql+mysqlconnector://caregiver_app:password@localhost/caregivers_db'

try:
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    print("Connection successful!")
    connection.close()
except OperationalError as e:
    print(f"Connection failed: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
