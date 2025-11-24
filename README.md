# Online Caregivers Platform

This project implements a database system for an Online Caregivers Platform using Python, SQLAlchemy, and Flask with a MySQL database.

## Project Structure

- `src/models.py`: SQLAlchemy models defining the database schema.
- `src/seed_data.py`: Script to create tables and insert initial data (Part 1).
- `src/part2_queries.py`: Script to execute queries and updates (Part 2).
- `src/app.py`: Flask web application for CRUD operations (Part 3).
- `src/templates/`: HTML templates for the web application.
- `requirements.txt`: Python dependencies.

## Setup Instructions

1.  **Prerequisites:**
    - Ensure you have MySQL installed and running.
    - Create a database named `caregivers_db` (or update the connection string in the scripts to match your database name).
    - Create a user `root` with password `password` (or update the connection string in the scripts to match your credentials).

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Database Connection:**
    Update the `DATABASE_URL` in `src/seed_data.py`, `src/part2_queries.py`, and `src/app.py` with your MySQL connection details:
    `mysql+mysqlconnector://username:password@localhost/dbname`

4.  **Initialize Database:**
    Run the seed script to create the tables and populate them with data.
    ```bash
    cd src
    python seed_data.py
    ```

5.  **Run Queries (Part 2):**
    Execute the script to perform the requested updates and queries.
    ```bash
    cd src
    python part2_queries.py
    ```

6.  **Run Web Application (Part 3):**
    Start the Flask server.
    ```bash
    cd src
    python app.py
    ```
    Open your browser and navigate to `http://127.0.0.1:5000`.

## Database Configuration

This project is configured to use MySQL. You must update the `DATABASE_URL` in `src/seed_data.py`, `src/part2_queries.py`, and `src/app.py` to match your MySQL server configuration.

Format: `mysql+mysqlconnector://username:password@localhost/dbname`
