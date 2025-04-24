from app.database import engine
from app import models

# Create all tables defined in models
models.Base.metadata.create_all(bind=engine)

print("Database created successfully")