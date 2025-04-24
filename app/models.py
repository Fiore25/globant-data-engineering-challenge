from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base

class Department(Base):
    __tablename__="departments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    department = Column(String, index=True)

class Job(Base):
    __tablename__="jobs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    job = Column(String, index=True)

class HiredEmployee(Base):
    __tablename__="hired_employees"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    datetime = Column(DateTime)
    department_id = Column(Integer, ForeignKey("departments.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))