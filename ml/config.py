# Configuration file for ML model
MODEL_PATH = "/app/ml/model.pkl"  # Path to save the trained model
TEST_SIZE = 0.2  # 20% of the data will be used for testing
RANDOM_STATE = 42  # Ensures reproducibility
TARGET_COLUMN = "Attrition"
DATABASE_URL = "postgresql+psycopg2://postgres:password@postgres_db:5432/employee_db"
