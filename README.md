#Employee Performance Prediction

📌 A Machine Learning-powered web application to predict employee performance based on various factors like job role, experience, compensation, and satisfaction.
This project integrates Streamlit (Frontend), FastAPI (Backend API), PostgreSQL (Database), and Apache Airflow (Workflow Orchestration).

Component	Technology
Frontend  -	Streamlit
Backend	  -  FastAPI
Database  -	PostgreSQL
Orchestration -	Apache Airflow
ML Model  -	Scikit-learn, Pandas, NumPy
Monitoring - Great Expectations, Grafana
Containerization -	Docker, Docker Compose

📌 Features

✅ Employee Performance Prediction
✅ Historical Predictions Storage
✅ Data Ingestion & Validation with Great Expectations
✅ Automated ML Model Training & Deployment
✅ Scheduled Predictions via Airflow
✅ Fully Containerized with Docker

🔧 Setup & Installation

1️⃣ Clone the Repository
bash

git clone https://github.com/your-repo/Employee-Performance-Prediction.git
cd Employee-Performance-Prediction

2️⃣ Set Up Environment Variables

Create a .env file and add the following:

env

POSTGRES_USER=youruser
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=employee_db
AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://youruser:yourpassword@db:5432/airflow_db

3️⃣ Start the Project with Docker
bash

docker-compose up -d

4️⃣ Initialize Airflow
bash

docker exec -it airflow_webserver airflow db init
docker exec -it airflow_webserver airflow users create \
    --username admin --password admin \
    --firstname Air --lastname Flow --role Admin --email admin@example.com

📡 API Endpoints

🚀 FastAPI Backend

Method	Endpoint	Description
POST	/predict	Predicts employee performance
GET	/past-predictions	Retrieves past predictions

Example Request:

json
{
    "age": 30,
    "gender": "Male",
    "job_role": "Engineer",
    "department": "IT",
    "monthly_income": 5000
}
Response:

json
{
    "performance_score": 85
}

🛠️ Airflow DAGs
1️⃣ data_ingestion.py
✅ Extract employee data from CSV
✅ Validate data using Great Expectations
✅ Load data into PostgreSQL

2️⃣ model_training.py
✅ Train the ML model
✅ Save the trained model

3️⃣ prediction_job.py
✅ Load the trained model
✅ Make predictions every 5 minutes
✅ Store results in PostgreSQL

📊 Monitoring & Logs
1️⃣ Check Airflow UI (http://localhost:8080)
2️⃣ Check FastAPI Logs

bash

docker logs -f backend

3️⃣ Check Database Logs

bash

docker logs -f postgres

🛑 Stopping the Project
bash

docker-compose down

📌 Future Improvements
✅ Add Feature Importance Analysis
✅ Improve Model Performance with Hyperparameter Tuning
✅ Deploy to Cloud (AWS/GCP)

🤝 Contributing
🔹 Fork the repository
🔹 Create a new branch (feature-branch)
🔹 Commit changes & open a pull request

📜 License
This project is MIT Licensed.

🚀 Enjoy predicting employee performance! 🚀
