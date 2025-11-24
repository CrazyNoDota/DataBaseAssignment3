from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, time
from models import Base, User, Caregiver, Member, Address, Job, JobApplication, Appointment
import os

# MySQL Connection
DATABASE_URL = 'mysql+mysqlconnector://root:rootpassword@localhost:3307/caregivers_db'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    # Tables are created via part1.sql in app.py or manually
    # Base.metadata.create_all(engine)
    print("Assuming tables are created via SQL script.")

def seed_data():
    # Check if data already exists to avoid duplicates if run multiple times
    if session.query(User).count() > 0:
        print("Data already exists. Skipping seed.")
        return

    print("Seeding data...")

    # --- 1. Users ---
    users = [
        # Caregivers
        User(email="c1@example.com", given_name="Alice", surname="Smith", city="Astana", phone_number="1111111111", password="pass", profile_description="Experienced babysitter"),
        User(email="c2@example.com", given_name="Bob", surname="Brown", city="Almaty", phone_number="2222222222", password="pass", profile_description="Elderly care specialist"),
        User(email="c3@example.com", given_name="Charlie", surname="Davis", city="Astana", phone_number="3333333333", password="pass", profile_description="Playmate for kids"),
        User(email="c4@example.com", given_name="Diana", surname="Evans", city="Shymkent", phone_number="4444444444", password="pass", profile_description="Nurse"),
        User(email="c5@example.com", given_name="Evan", surname="Foster", city="Astana", phone_number="5555555555", password="pass", profile_description="Babysitter"),
        
        # Members
        User(email="m1@example.com", given_name="Arman", surname="Armanov", city="Astana", phone_number="6666666666", password="pass", profile_description="Need help"),
        User(email="m2@example.com", given_name="Amina", surname="Aminova", city="Almaty", phone_number="7777777777", password="pass", profile_description="Busy mom"),
        User(email="m3@example.com", given_name="Berik", surname="Bolatov", city="Astana", phone_number="8888888888", password="pass", profile_description="Looking for care"),
        User(email="m4@example.com", given_name="Dana", surname="Dauletova", city="Astana", phone_number="9999999999", password="pass", profile_description="Need elderly care"),
        User(email="m5@example.com", given_name="Erlan", surname="Ermekov", city="Almaty", phone_number="0000000000", password="pass", profile_description="Family man"),
        
        # Extra for padding
        User(email="c6@example.com", given_name="Fiona", surname="Green", city="Astana", phone_number="1212121212", password="pass", profile_description="Student"),
        User(email="m6@example.com", given_name="Gani", surname="Gani", city="Astana", phone_number="1313131313", password="pass", profile_description="Dad"),
    ]
    session.add_all(users)
    session.commit()

    # Retrieve users to link them
    u_c1 = session.query(User).filter_by(email="c1@example.com").first()
    u_c2 = session.query(User).filter_by(email="c2@example.com").first()
    u_c3 = session.query(User).filter_by(email="c3@example.com").first()
    u_c4 = session.query(User).filter_by(email="c4@example.com").first()
    u_c5 = session.query(User).filter_by(email="c5@example.com").first()
    u_c6 = session.query(User).filter_by(email="c6@example.com").first()

    u_m1 = session.query(User).filter_by(email="m1@example.com").first() # Arman
    u_m2 = session.query(User).filter_by(email="m2@example.com").first() # Amina
    u_m3 = session.query(User).filter_by(email="m3@example.com").first()
    u_m4 = session.query(User).filter_by(email="m4@example.com").first() # Dana (Astana, Elderly Care)
    u_m5 = session.query(User).filter_by(email="m5@example.com").first()
    u_m6 = session.query(User).filter_by(email="m6@example.com").first()

    # --- 2. Caregivers ---
    caregivers = [
        Caregiver(caregiver_user_id=u_c1.user_id, photo="p1.jpg", gender="Female", caregiving_type="babysitter", hourly_rate=15.0),
        Caregiver(caregiver_user_id=u_c2.user_id, photo="p2.jpg", gender="Male", caregiving_type="caregiver for elderly", hourly_rate=20.0),
        Caregiver(caregiver_user_id=u_c3.user_id, photo="p3.jpg", gender="Male", caregiving_type="playmate for children", hourly_rate=12.0),
        Caregiver(caregiver_user_id=u_c4.user_id, photo="p4.jpg", gender="Female", caregiving_type="caregiver for elderly", hourly_rate=25.0),
        Caregiver(caregiver_user_id=u_c5.user_id, photo="p5.jpg", gender="Male", caregiving_type="babysitter", hourly_rate=9.0), # < 10 for update test
        Caregiver(caregiver_user_id=u_c6.user_id, photo="p6.jpg", gender="Female", caregiving_type="babysitter", hourly_rate=11.0),
    ]
    session.add_all(caregivers)
    session.commit()

    # --- 3. Members ---
    members = [
        Member(member_user_id=u_m1.user_id, house_rules="No smoking", dependent_description="2 kids"),
        Member(member_user_id=u_m2.user_id, house_rules="Cleanliness", dependent_description="1 baby"),
        Member(member_user_id=u_m3.user_id, house_rules="Quiet", dependent_description="Grandfather"),
        Member(member_user_id=u_m4.user_id, house_rules="No pets.", dependent_description="Grandmother needs help"), # Matches query 5.4
        Member(member_user_id=u_m5.user_id, house_rules="No shoes", dependent_description="3 kids"),
        Member(member_user_id=u_m6.user_id, house_rules="Be on time", dependent_description="Twins"),
    ]
    session.add_all(members)
    session.commit()

    # --- 4. Addresses ---
    addresses = [
        Address(member_user_id=u_m1.user_id, house_number="10", street="Main St", town="Astana"),
        Address(member_user_id=u_m2.user_id, house_number="5", street="Abay St", town="Almaty"),
        Address(member_user_id=u_m3.user_id, house_number="12", street="Kabanbay Batyr street", town="Astana"), # For delete 4.2
        Address(member_user_id=u_m4.user_id, house_number="33", street="Dostyk", town="Astana"),
        Address(member_user_id=u_m5.user_id, house_number="7", street="Kabanbay Batyr street", town="Almaty"), # For delete 4.2
        Address(member_user_id=u_m6.user_id, house_number="1", street="Saryarka", town="Astana"),
    ]
    session.add_all(addresses)
    session.commit()

    # --- 5. Jobs ---
    jobs = [
        Job(member_user_id=u_m1.user_id, required_caregiving_type="babysitter", other_requirements="Must be patient", date_posted=date(2025, 10, 1)),
        Job(member_user_id=u_m2.user_id, required_caregiving_type="babysitter", other_requirements="soft-spoken person", date_posted=date(2025, 10, 2)), # Matches query 5.2, posted by Amina
        Job(member_user_id=u_m2.user_id, required_caregiving_type="playmate for children", other_requirements="Energetic", date_posted=date(2025, 10, 3)), # Posted by Amina
        Job(member_user_id=u_m3.user_id, required_caregiving_type="caregiver for elderly", other_requirements="Strong", date_posted=date(2025, 10, 4)),
        Job(member_user_id=u_m4.user_id, required_caregiving_type="caregiver for elderly", other_requirements="Medical background", date_posted=date(2025, 10, 5)),
        Job(member_user_id=u_m5.user_id, required_caregiving_type="babysitter", other_requirements="soft-spoken", date_posted=date(2025, 10, 6)), # Matches query 5.2
        Job(member_user_id=u_m6.user_id, required_caregiving_type="babysitter", other_requirements="Weekend only", date_posted=date(2025, 10, 7)),
        Job(member_user_id=u_m1.user_id, required_caregiving_type="playmate for children", other_requirements="Fun", date_posted=date(2025, 10, 8)),
        Job(member_user_id=u_m3.user_id, required_caregiving_type="caregiver for elderly", other_requirements="Night shift", date_posted=date(2025, 10, 9)),
        Job(member_user_id=u_m4.user_id, required_caregiving_type="caregiver for elderly", other_requirements="Day shift", date_posted=date(2025, 10, 10)),
    ]
    session.add_all(jobs)
    session.commit()

    # Retrieve jobs
    job_list = session.query(Job).all()

    # --- 6. Job Applications ---
    applications = [
        JobApplication(caregiver_user_id=u_c1.user_id, job_id=job_list[0].job_id, date_applied=date(2025, 10, 2)),
        JobApplication(caregiver_user_id=u_c5.user_id, job_id=job_list[0].job_id, date_applied=date(2025, 10, 3)),
        JobApplication(caregiver_user_id=u_c1.user_id, job_id=job_list[1].job_id, date_applied=date(2025, 10, 4)),
        JobApplication(caregiver_user_id=u_c3.user_id, job_id=job_list[2].job_id, date_applied=date(2025, 10, 5)),
        JobApplication(caregiver_user_id=u_c2.user_id, job_id=job_list[3].job_id, date_applied=date(2025, 10, 6)),
        JobApplication(caregiver_user_id=u_c4.user_id, job_id=job_list[3].job_id, date_applied=date(2025, 10, 7)),
        JobApplication(caregiver_user_id=u_c2.user_id, job_id=job_list[4].job_id, date_applied=date(2025, 10, 8)),
        JobApplication(caregiver_user_id=u_c5.user_id, job_id=job_list[5].job_id, date_applied=date(2025, 10, 9)),
        JobApplication(caregiver_user_id=u_c6.user_id, job_id=job_list[6].job_id, date_applied=date(2025, 10, 10)),
        JobApplication(caregiver_user_id=u_c3.user_id, job_id=job_list[7].job_id, date_applied=date(2025, 10, 11)),
    ]
    session.add_all(applications)
    session.commit()

    # --- 7. Appointments ---
    appointments = [
        Appointment(caregiver_user_id=u_c1.user_id, member_user_id=u_m1.user_id, appointment_date=date(2025, 11, 1), appointment_time=time(9, 0), work_hours=4, status="Confirmed"),
        Appointment(caregiver_user_id=u_c2.user_id, member_user_id=u_m3.user_id, appointment_date=date(2025, 11, 2), appointment_time=time(10, 0), work_hours=5, status="Confirmed"),
        Appointment(caregiver_user_id=u_c3.user_id, member_user_id=u_m2.user_id, appointment_date=date(2025, 11, 3), appointment_time=time(14, 0), work_hours=2, status="Pending"),
        Appointment(caregiver_user_id=u_c4.user_id, member_user_id=u_m4.user_id, appointment_date=date(2025, 11, 4), appointment_time=time(8, 0), work_hours=8, status="Confirmed"),
        Appointment(caregiver_user_id=u_c5.user_id, member_user_id=u_m5.user_id, appointment_date=date(2025, 11, 5), appointment_time=time(18, 0), work_hours=3, status="Declined"),
        Appointment(caregiver_user_id=u_c1.user_id, member_user_id=u_m6.user_id, appointment_date=date(2025, 11, 6), appointment_time=time(12, 0), work_hours=4, status="Confirmed"),
        Appointment(caregiver_user_id=u_c2.user_id, member_user_id=u_m4.user_id, appointment_date=date(2025, 11, 7), appointment_time=time(9, 0), work_hours=6, status="Confirmed"),
        Appointment(caregiver_user_id=u_c3.user_id, member_user_id=u_m1.user_id, appointment_date=date(2025, 11, 8), appointment_time=time(15, 0), work_hours=2, status="Confirmed"),
        Appointment(caregiver_user_id=u_c4.user_id, member_user_id=u_m3.user_id, appointment_date=date(2025, 11, 9), appointment_time=time(10, 0), work_hours=5, status="Pending"),
        Appointment(caregiver_user_id=u_c5.user_id, member_user_id=u_m2.user_id, appointment_date=date(2025, 11, 10), appointment_time=time(11, 0), work_hours=3, status="Confirmed"),
    ]
    session.add_all(appointments)
    session.commit()

    print("Data seeded successfully.")

if __name__ == "__main__":
    init_db()
    seed_data()
