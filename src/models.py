from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Time, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'USER'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), nullable=False, unique=True)
    given_name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    city = Column(String(50))
    phone_number = Column(String(20))
    profile_description = Column(Text)
    password = Column(String(100), nullable=False)

    # Relationships
    caregiver_profile = relationship("Caregiver", back_populates="user", uselist=False, cascade="all, delete-orphan")
    member_profile = relationship("Member", back_populates="user", uselist=False, cascade="all, delete-orphan")

class Caregiver(Base):
    __tablename__ = 'CAREGIVER'
    
    caregiver_user_id = Column(Integer, ForeignKey('USER.user_id'), primary_key=True)
    photo = Column(String(255)) # Path to photo
    gender = Column(String(10))
    caregiving_type = Column(String(50)) # babysitter, caregiver for elderly, playmate for children
    hourly_rate = Column(Float)

    user = relationship("User", back_populates="caregiver_profile")
    job_applications = relationship("JobApplication", back_populates="caregiver")
    appointments = relationship("Appointment", back_populates="caregiver")

class Member(Base):
    __tablename__ = 'MEMBER'
    
    member_user_id = Column(Integer, ForeignKey('USER.user_id'), primary_key=True)
    house_rules = Column(Text)
    dependent_description = Column(Text)

    user = relationship("User", back_populates="member_profile")
    address = relationship("Address", back_populates="member", uselist=False, cascade="all, delete-orphan")
    jobs = relationship("Job", back_populates="member", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="member")

class Address(Base):
    __tablename__ = 'ADDRESS'
    
    member_user_id = Column(Integer, ForeignKey('MEMBER.member_user_id'), primary_key=True)
    house_number = Column(String(20))
    street = Column(String(100))
    town = Column(String(50))

    member = relationship("Member", back_populates="address")

class Job(Base):
    __tablename__ = 'JOB'
    
    job_id = Column(Integer, primary_key=True, autoincrement=True)
    member_user_id = Column(Integer, ForeignKey('MEMBER.member_user_id'))
    required_caregiving_type = Column(String(50))
    other_requirements = Column(Text)
    date_posted = Column(Date)

    member = relationship("Member", back_populates="jobs")
    applications = relationship("JobApplication", back_populates="job", cascade="all, delete-orphan")

class JobApplication(Base):
    __tablename__ = 'JOB_APPLICATION'
    
    caregiver_user_id = Column(Integer, ForeignKey('CAREGIVER.caregiver_user_id'), primary_key=True)
    job_id = Column(Integer, ForeignKey('JOB.job_id'), primary_key=True)
    date_applied = Column(Date)

    caregiver = relationship("Caregiver", back_populates="job_applications")
    job = relationship("Job", back_populates="applications")

class Appointment(Base):
    __tablename__ = 'APPOINTMENT'
    
    appointment_id = Column(Integer, primary_key=True, autoincrement=True)
    caregiver_user_id = Column(Integer, ForeignKey('CAREGIVER.caregiver_user_id'))
    member_user_id = Column(Integer, ForeignKey('MEMBER.member_user_id'))
    appointment_date = Column(Date)
    appointment_time = Column(Time)
    work_hours = Column(Integer)
    status = Column(String(20)) # e.g., 'Confirmed', 'Declined', 'Pending'

    caregiver = relationship("Caregiver", back_populates="appointments")
    member = relationship("Member", back_populates="appointments")
