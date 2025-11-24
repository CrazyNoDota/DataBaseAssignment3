from flask import Flask, render_template, request, redirect, url_for, flash, session as flask_session
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, joinedload
from models import Base, User, Caregiver, Member, Job, JobApplication, Appointment, Address
from datetime import datetime
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# DATABASE CONFIGURATION
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# MySQL Connection
DATABASE_URL = os.environ.get('DATABASE_URL') or 'mysql+mysqlconnector://root:rootpassword@localhost:3307/caregivers_db'

# Ensure correct driver for SQLAlchemy
if DATABASE_URL.startswith('mysql://'):
    DATABASE_URL = DATABASE_URL.replace('mysql://', 'mysql+mysqlconnector://', 1)

engine = create_engine(DATABASE_URL)

def init_db_from_sql():
    sql_file_path = os.path.join(BASE_DIR, 'part1.sql')
    print(f"Executing SQL script from: {sql_file_path}")
    try:
        with open(sql_file_path, 'r') as file:
            sql_script = file.read()
        
        with engine.connect() as connection:
            # Split statements and execute
            # Note: This simple split might fail on semicolons inside strings, but for this assignment's SQL it should be fine.
            statements = sql_script.split(';')
            for statement in statements:
                if statement.strip():
                    connection.execute(text(statement))
            connection.commit()
        print("Database initialized from SQL script.")
    except Exception as e:
        print(f"Error initializing database: {e}")

# Initialize database
init_db_from_sql()

Session = sessionmaker(bind=engine)

# Login Required Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in flask_session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in flask_session:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        session = Session()
        # Eager load profiles to determine role
        user = session.query(User).options(
            joinedload(User.caregiver_profile),
            joinedload(User.member_profile)
        ).filter_by(email=email).first()
        session.close()
        
        if user and user.password == password: # In production, use password hashing!
            flask_session['user_id'] = user.user_id
            flask_session['user_name'] = user.given_name
            
            # Determine Role
            if user.caregiver_profile:
                flask_session['role'] = 'caregiver'
            elif user.member_profile:
                flask_session['role'] = 'member'
            else:
                flask_session['role'] = 'unknown'

            flash(f'Welcome back, {user.given_name}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    flask_session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# --- User CRUD ---
@app.route('/users')
@login_required
def list_users():
    role = flask_session.get('role')
    
    # Caregivers should not see the list of other caregivers or members
    if role == 'caregiver':
        flash('Access denied. Caregivers cannot browse the user list.', 'warning')
        return redirect(url_for('index'))

    session = Session()
    # If Member, show only Caregivers
    if role == 'member':
        # Join User to get names and filter
        query = session.query(Caregiver).join(User).options(joinedload(Caregiver.user))
        
        # Filtering
        caregiving_type = request.args.get('caregiving_type')
        city = request.args.get('city')
        
        if caregiving_type:
            query = query.filter(Caregiver.caregiving_type == caregiving_type)
        if city:
            query = query.filter(User.city.ilike(f'%{city}%'))
            
        caregivers = query.all()
        # Transform to list of users for the template compatibility
        users = [c.user for c in caregivers]
    else:
        # Fallback or Admin view (if existed)
        users = session.query(User).all()
        
    session.close()
    return render_template('users.html', users=users)

@app.route('/users/create', methods=['GET', 'POST'])
def create_user():
    if 'user_id' in flask_session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        session = Session()
        try:
            # Check if email exists first to give a clean error
            existing_user = session.query(User).filter_by(email=request.form['email']).first()
            if existing_user:
                flash('Email already registered. Please use a different email.', 'danger')
                return render_template('user_form.html', action='Create')

            new_user = User(
                email=request.form['email'],
                given_name=request.form['given_name'],
                surname=request.form['surname'],
                city=request.form['city'],
                phone_number=request.form['phone_number'],
                password=request.form['password'],
                profile_description=request.form['profile_description']
            )
            session.add(new_user)
            session.flush() # Get the user_id

            role = request.form.get('role')
            if role == 'caregiver':
                caregiver = Caregiver(
                    caregiver_user_id=new_user.user_id,
                    photo=request.form.get('photo'),
                    gender=request.form.get('gender'),
                    caregiving_type=request.form.get('caregiving_type'),
                    hourly_rate=float(request.form.get('hourly_rate') or 0)
                )
                session.add(caregiver)
            elif role == 'member':
                member = Member(
                    member_user_id=new_user.user_id,
                    house_rules=request.form.get('house_rules'),
                    dependent_description=request.form.get('dependent_description')
                )
                session.add(member)
                
                # Add Address if provided
                if request.form.get('street'):
                    address = Address(
                        member_user_id=new_user.user_id,
                        house_number=request.form.get('house_number'),
                        street=request.form.get('street'),
                        town=request.form.get('town')
                    )
                    session.add(address)

            session.commit()
            flash('User created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            session.rollback()
            flash('Error: This email is already registered.', 'danger')
            return render_template('user_form.html', action='Create')
        except Exception as e:
            session.rollback()
            flash(f'Error creating user: {str(e)}', 'danger')
            return render_template('user_form.html', action='Create')
        finally:
            session.close()
    return render_template('user_form.html', action='Create')

@app.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    # Security check: only allow editing own profile
    if flask_session.get('user_id') != id:
        flash('You can only edit your own profile.', 'danger')
        return redirect(url_for('view_profile', id=id))

    session = Session()
    user = session.query(User).options(
        joinedload(User.caregiver_profile),
        joinedload(User.member_profile).joinedload(Member.address)
    ).get(id)
    if request.method == 'POST':
        user.email = request.form['email']
        user.given_name = request.form['given_name']
        user.surname = request.form['surname']
        user.city = request.form['city']
        user.phone_number = request.form['phone_number']
        user.profile_description = request.form['profile_description']
        
        # Update Caregiver/Member details
        if user.caregiver_profile:
            user.caregiver_profile.photo = request.form.get('photo')
            user.caregiver_profile.gender = request.form.get('gender')
            user.caregiver_profile.caregiving_type = request.form.get('caregiving_type')
            user.caregiver_profile.hourly_rate = float(request.form.get('hourly_rate') or 0)
        
        if user.member_profile:
            user.member_profile.house_rules = request.form.get('house_rules')
            user.member_profile.dependent_description = request.form.get('dependent_description')
            
            if user.member_profile.address:
                user.member_profile.address.house_number = request.form.get('house_number')
                user.member_profile.address.street = request.form.get('street')
                user.member_profile.address.town = request.form.get('town')
            elif request.form.get('street'): # Create address if it didn't exist but fields are filled
                address = Address(
                    member_user_id=user.user_id,
                    house_number=request.form.get('house_number'),
                    street=request.form.get('street'),
                    town=request.form.get('town')
                )
                session.add(address)

        session.commit()
        session.close()
        return redirect(url_for('list_users'))
    session.close()
    return render_template('user_form.html', action='Edit', user=user)

@app.route('/users/delete/<int:id>')
@login_required
def delete_user(id):
    # Security check
    if flask_session.get('user_id') != id:
        flash('You can only delete your own account.', 'danger')
        return redirect(url_for('list_users'))

    session = Session()
    user = session.query(User).get(id)
    if user:
        session.delete(user)
        session.commit()
        flask_session.clear() # Logout after delete
        flash('Your account has been deleted.', 'info')
        return redirect(url_for('index'))
    session.close()
    return redirect(url_for('list_users'))

# --- Job CRUD ---
@app.route('/jobs')
@login_required
def list_jobs():
    role = flask_session.get('role')
    user_id = flask_session.get('user_id')
    
    session = Session()
    query = session.query(Job)
    
    # Members should only see their own jobs (or maybe none if they only post?)
    # Requirement: "Caregivers can then search through these announcements"
    # Requirement: "Members can view the profiles of applicants..." (implies they see their jobs to click on them)
    if role == 'member':
        query = query.filter(Job.member_user_id == user_id)
    
    # Filtering (mostly for Caregivers)
    caregiving_type = request.args.get('caregiving_type')
    if caregiving_type:
        query = query.filter(Job.required_caregiving_type.ilike(f'%{caregiving_type}%'))
        
    jobs = query.all()
    session.close()
    return render_template('jobs.html', jobs=jobs)

@app.route('/users/<int:id>')
@login_required
def view_profile(id):
    session = Session()
    user = session.query(User).options(
        joinedload(User.caregiver_profile),
        joinedload(User.member_profile).joinedload(Member.address)
    ).get(id)
    session.close()
    return render_template('profile.html', user=user)

@app.route('/jobs/create', methods=['GET', 'POST'])
@login_required
def create_job():
    if request.method == 'POST':
        session = Session()
        try:
            new_job = Job(
                member_user_id=flask_session.get('user_id'), # Use logged in user
                required_caregiving_type=request.form['required_caregiving_type'],
                other_requirements=request.form['other_requirements'],
                person_age=request.form.get('person_age'),
                time_interval=request.form.get('time_interval'),
                frequency=request.form.get('frequency'),
                date_posted=datetime.strptime(request.form['date_posted'], '%Y-%m-%d').date()
            )
            session.add(new_job)
            session.commit()
            flash('Job posted successfully!', 'success')
            return redirect(url_for('list_jobs'))
        except Exception as e:
            session.rollback()
            flash(f'Error posting job: {str(e)}', 'danger')
        finally:
            session.close()
    
    return render_template('job_form.html')

@app.route('/jobs/<int:id>/apply', methods=['POST'])
@login_required
def apply_job(id):
    session = Session()
    try:
        caregiver_id = flask_session.get('user_id') # Use logged in user
        
        # Check if already applied
        existing = session.query(JobApplication).filter_by(job_id=id, caregiver_user_id=caregiver_id).first()
        if existing:
            flash('You have already applied to this job.', 'warning')
            return redirect(url_for('list_jobs'))

        application = JobApplication(
            job_id=id,
            caregiver_user_id=caregiver_id,
            date_applied=datetime.now().date()
        )
        session.add(application)
        session.commit()
        flash('Applied to job successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error applying to job: {str(e)}', 'danger')
    finally:
        session.close()
    return redirect(url_for('list_jobs'))

@app.route('/my_applications')
@login_required
def my_applications():
    # Use logged in user
    user_id = flask_session.get('user_id')
    session = Session()
    
    # Prepare query with eager loading to avoid DetachedInstanceError after session close
    query = session.query(JobApplication).options(
        joinedload(JobApplication.job),
        joinedload(JobApplication.caregiver).joinedload(Caregiver.user)
    )

    try:
        if user_id:
            # Check if user is caregiver or member
            caregiver = session.query(Caregiver).get(user_id)
            if caregiver:
                applications = query.filter_by(caregiver_user_id=user_id).all()
                return render_template('my_applications.html', applications=applications, user_type='caregiver')
            
            member = session.query(Member).get(user_id)
            if member:
                # Find jobs posted by this member, then applications to those jobs
                jobs = session.query(Job).filter_by(member_user_id=user_id).all()
                job_ids = [j.job_id for j in jobs]
                applications = query.filter(JobApplication.job_id.in_(job_ids)).all()
                return render_template('my_applications.html', applications=applications, user_type='member')
                
        # Fallback
        return render_template('my_applications.html', applications=[], user_type='unknown')
    finally:
        session.close()

@app.route('/appointments')
@login_required
def list_appointments():
    session = Session()
    # Filter appointments for the logged in user
    user_id = flask_session.get('user_id')
    
    appointments = session.query(Appointment).options(
        joinedload(Appointment.caregiver).joinedload(Caregiver.user),
        joinedload(Appointment.member).joinedload(Member.user)
    ).filter((Appointment.caregiver_user_id == user_id) | (Appointment.member_user_id == user_id)).all()
    
    session.close()
    return render_template('appointments.html', appointments=appointments)

@app.route('/appointments/create', methods=['GET', 'POST'])
@login_required
def create_appointment():
    if request.method == 'POST':
        session = Session()
        try:
            new_appointment = Appointment(
                caregiver_user_id=request.form['caregiver_user_id'],
                member_user_id=flask_session.get('user_id'), # Logged in user is the member booking
                appointment_date=datetime.strptime(request.form['appointment_date'], '%Y-%m-%d').date(),
                appointment_time=datetime.strptime(request.form['appointment_time'], '%H:%M').time(),
                work_hours=int(request.form['work_hours']),
                status='Pending'
            )
            session.add(new_appointment)
            session.commit()
            flash('Appointment booked successfully!', 'success')
            return redirect(url_for('list_appointments'))
        except Exception as e:
            session.rollback()
            flash(f'Error booking appointment: {str(e)}', 'danger')
        finally:
            session.close()
    
    # Get caregivers for dropdown
    session = Session()
    caregivers = session.query(Caregiver).options(joinedload(Caregiver.user)).all()
    session.close()
    return render_template('appointment_form.html', caregivers=caregivers)

@app.route('/appointments/<int:id>/update', methods=['POST'])
@login_required
def update_appointment(id):
    session = Session()
    try:
        appointment = session.query(Appointment).get(id)
        # Security check: only involved parties can update
        user_id = flask_session.get('user_id')
        if appointment.caregiver_user_id != user_id and appointment.member_user_id != user_id:
             flash('Unauthorized action.', 'danger')
             return redirect(url_for('list_appointments'))

        if 'status' in request.form:
            appointment.status = request.form['status']
        session.commit()
        flash('Appointment updated successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error updating appointment: {str(e)}', 'danger')
    finally:
        session.close()
    return redirect(url_for('list_appointments'))

@app.route('/appointments/<int:id>/delete', methods=['POST'])
@login_required
def delete_appointment(id):
    session = Session()
    try:
        appointment = session.query(Appointment).get(id)
        # Security check
        user_id = flask_session.get('user_id')
        if appointment and (appointment.caregiver_user_id == user_id or appointment.member_user_id == user_id):
            session.delete(appointment)
            session.commit()
            flash('Appointment cancelled successfully!', 'success')
        else:
             flash('Unauthorized action or appointment not found.', 'danger')
    except Exception as e:
        session.rollback()
        flash(f'Error cancelling appointment: {str(e)}', 'danger')
    finally:
        session.close()
    return redirect(url_for('list_appointments'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
