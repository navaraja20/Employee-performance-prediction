# airflow/db_operations.py
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
import os

DATABASE_URL = os.getenv("DB_URL", "postgresql://mlops_user:mlops_pass@postgres:5432/mlops_db")

engine = create_engine(DATABASE_URL)
metadata = MetaData()

data_stats = Table(
    'data_quality_stats', metadata,
    Column('id', Integer, primary_key=True),
    Column('filename', String),
    Column('row_count', Integer),
    Column('valid', Integer),
    Column('invalid', Integer),
    Column('summary', String)
)

metadata.create_all(engine)

def log_data_stats(df, result, file_path):
    filename = os.path.basename(file_path)
    total = len(df)
    valid = int(result['success']) * total
    invalid = total - valid
    summary = str([r['expectation_type'] for r in result['results']])
    
    with engine.connect() as conn:
        conn.execute(
            data_stats.insert().values(
                filename=filename,
                row_count=total,
                valid=valid,
                invalid=invalid,
                summary=summary
            )
        )
