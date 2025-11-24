from sqlalchemy import create_engine, func, select, update, delete, and_
from sqlalchemy.orm import sessionmaker
from models import Base, User, Caregiver, Member, Address, Job, JobApplication, Appointment
import os


DATABASE_URL = 'mysql+mysqlconnector://root:rootpassword@localhost:3307/caregivers_db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def run_queries():
    print("--- Part 2: Queries and Updates ---\n")

    
    print("3.1 Updating phone number of Arman Armanov...")
    arman = session.query(User).filter_by(given_name="Arman", surname="Armanov").first()
    if arman:
        arman.phone_number = "+77773414141"
        session.commit()
        print(f"Updated phone number: {arman.phone_number}")
    else:
        print("Arman Armanov not found.")
    print("-" * 20)

    
    print("3.2 Updating hourly rates...")
    caregivers = session.query(Caregiver).all()
    for c in caregivers:
        old_rate = c.hourly_rate
        if c.hourly_rate < 10:
            c.hourly_rate += 0.3
        else:
            c.hourly_rate += c.hourly_rate * 0.10
        print(f"Caregiver {c.caregiver_user_id}: {old_rate} -> {c.hourly_rate}")
    session.commit()
    print("-" * 20)

    
    print("4.1 Deleting jobs posted by Amina Aminova...")
    amina = session.query(User).filter_by(given_name="Amina", surname="Aminova").first()
    if amina:
        
        jobs_to_delete = session.query(Job).filter_by(member_user_id=amina.user_id).all()
        count = len(jobs_to_delete)
        for job in jobs_to_delete:
            session.delete(job)
        session.commit()
        print(f"Deleted {count} jobs posted by Amina Aminova.")
    else:
        print("Amina Aminova not found.")
    print("-" * 20)

    
    print("4.2 Deleting members on Kabanbay Batyr street...")
    
    addresses = session.query(Address).filter(Address.street.like("%Kabanbay Batyr%")).all()
    deleted_count = 0
    for addr in addresses:
        member = session.query(Member).filter_by(member_user_id=addr.member_user_id).first()
        if member:
            
            
            
            
            
            
            user_to_delete = session.query(User).filter_by(user_id=member.member_user_id).first()
            if user_to_delete:
                session.delete(user_to_delete)
                deleted_count += 1
    session.commit()
    print(f"Deleted {deleted_count} members living on Kabanbay Batyr street.")
    print("-" * 20)

    
    print("5.1 Caregiver and Member names for accepted appointments:")
    
    from sqlalchemy.orm import aliased
    CaregiverUser = aliased(User)
    MemberUser = aliased(User)

    results = session.query(
        CaregiverUser.given_name, CaregiverUser.surname,
        MemberUser.given_name, MemberUser.surname
    ).select_from(Appointment)\
     .join(Caregiver, Appointment.caregiver_user_id == Caregiver.caregiver_user_id)\
     .join(CaregiverUser, Caregiver.caregiver_user_id == CaregiverUser.user_id)\
     .join(Member, Appointment.member_user_id == Member.member_user_id)\
     .join(MemberUser, Member.member_user_id == MemberUser.user_id)\
     .filter(Appointment.status == "Confirmed").all()

    for row in results:
        print(f"Caregiver: {row[0]} {row[1]}, Member: {row[2]} {row[3]}")
    print("-" * 20)

    
    print("5.2 Job IDs with 'soft-spoken' requirement:")
    jobs = session.query(Job.job_id).filter(Job.other_requirements.like("%soft-spoken%")).all()
    for j in jobs:
        print(f"Job ID: {j.job_id}")
    print("-" * 20)

    
    
    
    
    
    
    print("5.3 Work hours of all babysitter appointments:")
    hours = session.query(Appointment.work_hours)\
        .join(Caregiver, Appointment.caregiver_user_id == Caregiver.caregiver_user_id)\
        .filter(Caregiver.caregiving_type == "babysitter").all()
    for h in hours:
        print(f"Hours: {h.work_hours}")
    print("-" * 20)

    
    print("5.4 Members looking for Elderly Care in Astana with 'No pets.' rule:")
    
    
    
    
    
    members = session.query(User.given_name, User.surname)\
        .join(Member, User.user_id == Member.member_user_id)\
        .join(Address, Member.member_user_id == Address.member_user_id)\
        .join(Job, Member.member_user_id == Job.member_user_id)\
        .filter(
            Address.town == "Astana",
            Member.house_rules.like("%No pets%"),
            Job.required_caregiving_type == "caregiver for elderly"
        ).distinct().all()
    
    for m in members:
        print(f"Member: {m.given_name} {m.surname}")
    print("-" * 20)

    
    print("6.1 Number of applicants for each job:")
    
    results = session.query(Job.job_id, func.count(JobApplication.caregiver_user_id))\
        .outerjoin(JobApplication, Job.job_id == JobApplication.job_id)\
        .group_by(Job.job_id).all()
    for r in results:
        print(f"Job {r[0]}: {r[1]} applicants")
    print("-" * 20)

    
    print("6.2 Total hours spent by caregivers for accepted appointments:")
    total_hours = session.query(func.sum(Appointment.work_hours))\
        .filter(Appointment.status == "Confirmed").scalar()
    print(f"Total Hours: {total_hours}")
    print("-" * 20)

    
    print("6.3 Average pay of caregivers (hourly rate) based on accepted appointments:")
    
    
    
    avg_rate = session.query(func.avg(Caregiver.hourly_rate))\
        .join(Appointment, Caregiver.caregiver_user_id == Appointment.caregiver_user_id)\
        .filter(Appointment.status == "Confirmed").scalar()
    print(f"Average Hourly Rate: {avg_rate}")
    print("-" * 20)

    
    print("6.4 Caregivers earning above average:")
    
    subquery = session.query(func.avg(Caregiver.hourly_rate))\
        .join(Appointment, Caregiver.caregiver_user_id == Appointment.caregiver_user_id)\
        .filter(Appointment.status == "Confirmed").scalar_subquery()
    
    caregivers = session.query(User.given_name, User.surname, Caregiver.hourly_rate)\
        .join(Caregiver, User.user_id == Caregiver.caregiver_user_id)\
        .join(Appointment, Caregiver.caregiver_user_id == Appointment.caregiver_user_id)\
        .filter(Appointment.status == "Confirmed")\
        .filter(Caregiver.hourly_rate > subquery)\
        .distinct().all()
    
    for c in caregivers:
        print(f"{c.given_name} {c.surname}: {c.hourly_rate}")
    print("-" * 20)

    
    print("Derived Attribute: Total cost for all accepted appointments:")
    
    total_cost = session.query(func.sum(Caregiver.hourly_rate * Appointment.work_hours))\
        .join(Appointment, Caregiver.caregiver_user_id == Appointment.caregiver_user_id)\
        .filter(Appointment.status == "Confirmed").scalar()
    print(f"Total Cost: {total_cost}")
    print("-" * 20)

    
    print("View Operation: Job Applications and Applicants:")
    
    results = session.query(
        Job.job_id, 
        Job.required_caregiving_type, 
        User.given_name, 
        User.surname, 
        JobApplication.date_applied
    ).join(JobApplication, Job.job_id == JobApplication.job_id)\
     .join(Caregiver, JobApplication.caregiver_user_id == Caregiver.caregiver_user_id)\
     .join(User, Caregiver.caregiver_user_id == User.user_id).all()
    
    for r in results:
        print(f"Job {r.job_id} ({r.required_caregiving_type}): Applicant {r.given_name} {r.surname} on {r.date_applied}")
    print("-" * 20)

if __name__ == "__main__":
    run_queries()
