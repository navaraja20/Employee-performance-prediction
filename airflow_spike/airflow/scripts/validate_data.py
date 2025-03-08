import pandas as pd
import os
import great_expectations as ge
from sqlalchemy import create_engine
from datetime import datetime

DATABASE_URL = "postgresql://postgres:password@postgres_db:5432/employee_db"
engine = create_engine(DATABASE_URL)

def validate_data(file_path):
    df = pd.read_csv(file_path)
    gdf = ge.from_pandas(df)

    # Define expectations
    expectations = {
        "EmployeeNumber": {"expect_column_values_to_be_unique": True},
        "Age": {"expect_column_values_to_be_between": {"min_value": 18, "max_value": 65}},
        "MonthlyIncome": {"expect_column_values_to_be_non_null": True},
    }

    errors = []
    for column, checks in expectations.items():
        for check, params in checks.items():
            result = getattr(gdf, check)(column, **params)
            if not result.success:
                errors.append({"column": column, "error": check})

    if errors:
        with engine.connect() as conn:
            for err in errors:
                conn.execute(
                    f"INSERT INTO data_issues (timestamp, file_name, column, error_type) VALUES "
                    f"('{datetime.utcnow()}', '{os.path.basename(file_path)}', '{err['column']}', '{err['error']}');"
                )
        return False

    return True

if __name__ == "__main__":
    import sys
    file_path = sys.argv[1]
    if validate_data(file_path):
        print(f"{file_path} is valid")
    else:
        print(f"{file_path} has validation issues")
