from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from app.database import engine, SessionLocal
from fastapi.responses import JSONResponse
from sqlalchemy import text
from pydantic import BaseModel
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import HiredEmployee

app = FastAPI()

@app.get("/")
def read_root():
    return{"message": "Globant Data Engineering Challenge API"}

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(pd.io.common.BytesIO(contents))

        filename = file.filename.lower()
        if "department" in filename:
            table_name = "departments"
        elif "job" in filename:
            table_name = "jobs"
        elif "employee" in filename:
            table_name = "hired_employees"
        else:
            raise HTTPException(status_code=400, detail="File name not recognized")

        # Check if the ids already exist in the database
        if table_name == "departments":
            # Extract the ids that come in the CSV
            department_ids = df['id'].tolist()
            with engine.connect() as connection:
                # Retrieve existing IDs from the Departments table
                existing_ids = [row[0] for row in connection.execute(text("SELECT id FROM departments")).fetchall()]
                # Filter out data that is not duplicated
                df = df[~df['id'].isin(existing_ids)]

        df.to_sql(table_name, engine, if_exists="replace", index=False)
        return {"message": f"File {file.filename} successfully loaded into the table {table_name}."}

    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Error parsing CSV")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error inserting into the database: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/report/hires-per-quarter/")
def hires_per_quarter():
    try:
        query = text("""
            SELECT 
                d.department AS department,
                CASE
                    WHEN CAST(strftime('%m', he.datetime) AS INTEGER) BETWEEN 1 AND 3 THEN 'Q1'
                    WHEN CAST(strftime('%m', he.datetime) AS INTEGER) BETWEEN 4 AND 6 THEN 'Q2'
                    WHEN CAST(strftime('%m', he.datetime) AS INTEGER) BETWEEN 7 AND 9 THEN 'Q3'
                    WHEN CAST(strftime('%m', he.datetime) AS INTEGER) BETWEEN 10 AND 12 THEN 'Q4'
                END AS quarter,
                COUNT(*) AS hired_count
            FROM hired_employees he
            JOIN departments d ON he.department_id = d.id
            WHERE strftime('%Y', he.datetime) = '2021'
            GROUP BY d.department, quarter
            ORDER BY d.department, quarter
        """)
        with engine.connect() as conn:
            result = conn.execute(query)
            data = [dict(row._mapping) for row in result]
            print(data)  # Imprimir los resultados para depurar
            return JSONResponse(content=data)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/report/above-average-hires/")
def above_average_hires():
    try:
        query = text("""
            WITH hires_2021 AS (
                SELECT 
                    department_id, 
                    COUNT(*) AS hires
                FROM hired_employees
                WHERE strftime('%Y', datetime) = '2021'
                GROUP BY department_id
            ),
            avg_hires AS (
                SELECT AVG(hires) AS avg_hires FROM hires_2021
            )
            SELECT 
                d.id, 
                d.department, 
                h.hires
            FROM hires_2021 h
            JOIN departments d ON h.department_id = d.id
            WHERE h.hires > (SELECT avg_hires FROM avg_hires)
            ORDER BY h.hires DESC
        """)
        with engine.connect() as conn:
            result = conn.execute(query)
            data = [dict(row._mapping) for row in result]
            print(data)  
            return JSONResponse(content=data)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

class HiredEmployeeCreate(BaseModel):
    id: int
    name: str
    datetime: datetime
    department_id: int
    job_id: int

@app.post("/batch-insert-employees/")
def batch_insert_employees(employees: List[HiredEmployeeCreate]):
    if not (1 <= len(employees) <= 1000):
        raise HTTPException(status_code=400, detail="You must insert between 1 and 1000 records")

    db: Session = SessionLocal()
    try:
        new_employees = [HiredEmployee(**e.dict()) for e in employees]
        db.add_all(new_employees)
        db.commit()
        return {"message": f"{len(new_employees)} employees inserted successfully."}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error inserting into the database: {str(e)}")
    finally:
        db.close()