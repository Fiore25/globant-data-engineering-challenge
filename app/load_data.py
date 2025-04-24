import pandas as pd
from sqlalchemy import create_engine
import os

# Absolute path to the .db file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "employees.db")

engine = create_engine(f"sqlite:///{DB_PATH}")

# Upload and save each CSV
def load_csv_to_db():
    # Upload departments
    departments = pd.read_csv(os.path.join(BASE_DIR, "data", "departments.csv"))
    departments.to_sql("departments", engine, if_exists="append", index=False)

    # Upload jobs
    jobs = pd.read_csv(os.path.join(BASE_DIR, "data", "jobs.csv"))
    jobs.to_sql("jobs", engine, if_exists="append", index=False)

    # Upload empleados
    employees = pd.read_csv(os.path.join(BASE_DIR, "data", "hired_employees.csv"))
    employees.to_sql("hired_employees", engine, if_exists="append", index=False)

    print("Data successfully loaded into the database")

if __name__ == "__main__":
    load_csv_to_db()