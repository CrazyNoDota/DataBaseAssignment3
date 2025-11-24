
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from app import app, init_db_from_sql, User, Caregiver, Member

# Override DATABASE_URL for local testing if needed, but app.py logic should handle it.
# We want to test the exact logic in app.py

def test_login():
    print("Testing login...")
    with app.app_context():
        # Initialize DB
        init_db_from_sql()
        
        # Create session
        engine = create_engine('mysql+mysqlconnector://root:rootpassword@localhost:3307/caregivers_db')
        Session = sessionmaker(bind=engine)
        session = Session()
        
        email = 'arman@example.com'
        print(f"Querying user with email: {email}")
        try:
            user = session.query(User).filter_by(email=email).first()
            if user:
                print(f"User found: {user.given_name} {user.surname}")
                print(f"Password: {user.password}")
                if user.caregiver_profile:
                    print("User is a caregiver")
                if user.member_profile:
                    print("User is a member")
            else:
                print("User not found")
        except Exception as e:
            print(f"Error querying user: {e}")
            import traceback
            traceback.print_exc()
        finally:
            session.close()

if __name__ == "__main__":
    test_login()
