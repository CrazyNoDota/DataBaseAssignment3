from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Caregiver, Member, Job

app = Flask(__name__)

DATABASE_URL = 'sqlite:///caregivers.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@app.route('/')
def index():
    return render_template('index.html')

# --- User CRUD ---
@app.route('/users')
def list_users():
    session = Session()
    users = session.query(User).all()
    session.close()
    return render_template('users.html', users=users)

@app.route('/users/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        session = Session()
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
        session.commit()
        session.close()
        return redirect(url_for('list_users'))
    return render_template('user_form.html', action='Create')

@app.route('/users/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    session = Session()
    user = session.query(User).get(id)
    if request.method == 'POST':
        user.email = request.form['email']
        user.given_name = request.form['given_name']
        user.surname = request.form['surname']
        user.city = request.form['city']
        user.phone_number = request.form['phone_number']
        user.profile_description = request.form['profile_description']
        session.commit()
        session.close()
        return redirect(url_for('list_users'))
    session.close()
    return render_template('user_form.html', action='Edit', user=user)

@app.route('/users/delete/<int:id>')
def delete_user(id):
    session = Session()
    user = session.query(User).get(id)
    if user:
        session.delete(user)
        session.commit()
    session.close()
    return redirect(url_for('list_users'))

# --- Job CRUD ---
@app.route('/jobs')
def list_jobs():
    session = Session()
    jobs = session.query(Job).all()
    session.close()
    return render_template('jobs.html', jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
