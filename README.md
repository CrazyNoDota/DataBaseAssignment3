# Online Caregivers Platform

This project implements a database system for an Online Caregivers Platform using Python, SQLAlchemy, and Flask with a MySQL database.

## Project Structure

- `part1.sql`: SQL script for schema creation and initial data seeding.
- `src/models.py`: SQLAlchemy models defining the database schema.
- `src/part2_queries.py`: Script to execute queries and updates (Part 2).
- `src/app.py`: Flask web application for CRUD operations (Part 3).
- `src/templates/`: HTML templates for the web application.
- `requirements.txt`: Python dependencies.

## Setup Instructions

### 1. Prerequisites
- Python 3.x
- Docker (for running the MySQL database)

### 2. Environment Setup

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Database Setup (Docker)

Start the MySQL container using Docker. This command runs a MySQL 8.0 instance on port 3307 with the required credentials.

```bash
docker run --name caregivers-mysql-3307 -e MYSQL_ROOT_PASSWORD=rootpassword -e MYSQL_DATABASE=caregivers_db -p 3307:3306 -d mysql:8.0
```

*Note: The application is configured to connect to `localhost:3307` with user `root` and password `rootpassword`.*

### 4. Initialize Database & Run Web Application (Part 3)

The application is designed to automatically initialize the database using the `part1.sql` file when it starts.

Run the Flask application:

```bash
cd src
python app.py
```

- The database tables will be created and seeded automatically.
- Open your browser and navigate to `http://127.0.0.1:5000`.

### 5. Run Queries (Part 2)

To execute the specific queries and updates required for Part 2 of the assignment:

```bash
cd src
python part2_queries.py
```

This script connects to the same MySQL database and performs the required operations, printing the results to the console.

## Database Configuration

This project is configured to use MySQL. You must update the `DATABASE_URL` in `src/seed_data.py`, `src/part2_queries.py`, and `src/app.py` to match your MySQL server configuration.

Format: `mysql+mysqlconnector://username:password@localhost/dbname`
