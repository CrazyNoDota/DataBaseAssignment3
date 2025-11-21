# Online Caregivers Platform

This project implements a database system for an Online Caregivers Platform using Python, SQLAlchemy, and Flask.

## Project Structure

- `src/models.py`: SQLAlchemy models defining the database schema.
- `src/seed_data.py`: Script to create tables and insert initial data (Part 1).
- `src/part2_queries.py`: Script to execute queries and updates (Part 2).
- `src/app.py`: Flask web application for CRUD operations (Part 3).
- `src/templates/`: HTML templates for the web application.
- `requirements.txt`: Python dependencies.

## Setup Instructions

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Initialize Database:**
    Run the seed script to create the database (`caregivers.db`) and populate it with data.
    ```bash
    cd src
    python seed_data.py
    ```

3.  **Run Queries (Part 2):**
    Execute the script to perform the requested updates and queries.
    ```bash
    cd src
    python part2_queries.py
    ```

4.  **Run Web Application (Part 3):**
    Start the Flask server.
    ```bash
    cd src
    python app.py
    ```
    Open your browser and navigate to `http://127.0.0.1:5000`.

## Database Configuration

By default, the project uses SQLite (`caregivers.db`) for simplicity. To use PostgreSQL or MySQL, update the `DATABASE_URL` in `src/models.py`, `src/seed_data.py`, `src/part2_queries.py`, and `src/app.py`.

Example for PostgreSQL:
`postgresql://username:password@localhost/dbname`

Example for MySQL:
`mysql+mysqlconnector://username:password@localhost/dbname`
