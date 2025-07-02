# api/database/create_tables.py

from database.db import Base, engine
from database.models import Prediction

print("✅ Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Done.")
