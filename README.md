# 🚀 Employee Performance Prediction System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)
[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.0+-red.svg)](https://airflow.apache.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)](https://streamlit.io/)
[![Grafana](https://img.shields.io/badge/Grafana-Latest-orange.svg)](https://grafana.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://www.postgresql.org/)
[![Great Expectations](https://img.shields.io/badge/Great%20Expectations-Latest-purple.svg)](https://greatexpectations.io/)
[![Redis](https://img.shields.io/badge/Redis-Latest-red.svg)](https://redis.io/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-Latest-orange.svg)](https://scikit-learn.org/)
[![pandas](https://img.shields.io/badge/pandas-Latest-blue.svg)](https://pandas.pydata.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-Latest-pink.svg)](https://pydantic-docs.helpmanual.io/)
[![JSON](https://img.shields.io/badge/JSON-Latest-lightgrey.svg)](https://www.json.org/)

A comprehensive end-to-end machine learning pipeline for predicting employee performance and attrition using Apache Airflow, FastAPI, and Streamlit with built-in data quality monitoring, validation, and visualization capabilities.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Data Pipeline](#data-pipeline)
- [Monitoring & Alerting](#monitoring--alerting)
- [Contributing](#contributing)

## 🎯 Overview

This system provides a complete solution for:
- **Employee Performance Prediction**: ML-powered predictions on whether an employee will stay or leave
- **Data Quality Monitoring**: Automated data validation and quality checks
- **Real-time Predictions**: Both single and batch prediction capabilities
- **Pipeline Orchestration**: Automated data ingestion and processing workflows
- **Interactive Dashboard**: User-friendly web interface for predictions and analytics
- **Comprehensive Monitoring**: Grafana dashboards for system and data monitoring

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │────│  Apache Airflow │────│  Data Validation│
│                 │    │                 │    │  (Great Expect.)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │◄───│  Data Storage   │────│   FastAPI       │
│   Database      │    │                 │    │   ML Service    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Grafana      │    │   Streamlit     │────│   Web Interface │
│   Monitoring    │    │   Frontend      │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## ✨ Features

### 🤖 Machine Learning
- **Random Forest Classifier** for employee attrition prediction
- **Feature Engineering** with label encoding for categorical variables
- **Model Validation** with confidence scoring
- **Batch & Real-time Predictions** support

### 📊 Data Pipeline
- **Automated Data Ingestion** from CSV files
- **Data Quality Validation** using Great Expectations
- **Smart Data Routing** (good/bad data separation)
- **Error Handling & Recovery** mechanisms
- **Duplicate Detection** and data cleansing

### 🎯 Real-time Processing
- **RESTful API** for predictions
- **Asynchronous Processing** for large datasets
- **Database Integration** with PostgreSQL
- **Request Source Tracking** for audit trails

### 📈 Monitoring & Alerting
- **Data Quality Metrics** tracking
- **Pipeline Health Monitoring**
- **Microsoft Teams Integration** for alerts
- **HTML Report Generation** for validation results
- **Grafana Dashboards** for system metrics

### 🌐 User Interface
- **Interactive Web App** built with Streamlit
- **Single & Batch Prediction** modes
- **Historical Data Analysis**
- **CSV Import/Export** functionality
- **Real-time Results Visualization**

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Orchestration** | Apache Airflow 2.0+ | Workflow management and scheduling |
| **API Backend** | FastAPI | High-performance REST API |
| **Frontend** | Streamlit | Interactive web application |
| **Database** | PostgreSQL 13 | Data storage and management |
| **ML Framework** | Scikit-learn | Machine learning models |
| **Data Validation** | Great Expectations | Data quality and validation |
| **Monitoring** | Grafana | System and data monitoring |
| **Containerization** | Docker & Docker Compose | Environment management |
| **Message Broker** | Redis | Task queue management |
| **Web Server** | Nginx | Static file serving |

## 📁 Project Structure

```
Employee-performance-prediction/
├── 🐳 docker-compose.yml          # Multi-service orchestration
├── 📊 airflow/                    # Airflow workflows and configurations
│   ├── dags/                     # DAG definitions
│   │   ├── ingestion_pipeline.py # Data ingestion and validation
│   │   └── prediction_job.py     # Automated prediction jobs
│   ├── data/                     # Data storage
│   │   ├── raw_data/            # Incoming data files
│   │   ├── good_data/           # Validated data
│   │   └── bad_data/            # Invalid data
│   └── great_expectations/       # Data validation rules
├── 🚀 FastApi/                   # ML API service
│   ├── api.py                   # Main API endpoints
│   ├── ml_model_training.py     # Model training script
│   └── *.pkl                    # Trained models and encoders
├── 🌐 Webapp/                    # Streamlit frontend
│   └── main.py                  # Web application
├── 📊 Grafana/                   # Monitoring queries
├── 🗄️ Database/                  # Database setup scripts
├── 📓 NoteBook/                  # Data generation and analysis
└── 🔧 data_generation/           # Synthetic data creation
```

## 🚀 Installation

### Prerequisites
- Docker & Docker Compose
- Python 3.8+
- 8GB+ RAM recommended

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/navaraja20/Employee-performance-prediction.git
   cd Employee-performance-prediction
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your configurations
   ```

3. **Launch the complete system**
   ```bash
   docker-compose up -d
   ```

4. **Wait for services to initialize** (2-3 minutes)

5. **Access the applications**
   - 🌐 **Streamlit App**: http://localhost:8501
   - 🔧 **Airflow UI**: http://localhost:8080 (admin/admin)
   - 📊 **Grafana**: http://localhost:3001 (dsp/project)
   - 🚀 **FastAPI Docs**: http://localhost:8000/docs
   - 🗄️ **PgAdmin**: http://localhost:5050

## 💻 Usage

### 🎯 Making Predictions

#### Single Prediction
1. Navigate to the Streamlit app (http://localhost:8501)
2. Select "Single Prediction" tab
3. Input employee details:
   - Age, Gender, Job Role
   - Monthly Income, Job Satisfaction
4. Click "Predict" to get results

#### Batch Predictions
1. Select "Multiple Predictions" tab
2. Upload a CSV file with required columns:
   ```csv
   Gender,Age,JobRole,MonthlyIncome,JobSatisfaction
   Male,25,Technology,60000,High
   Female,30,Finance,75000,Medium
   ```
3. Review predictions and download results

### 📊 Data Pipeline Management

#### Automated Ingestion
- Place CSV files in `airflow/data/raw_data/`
- Pipeline runs every minute automatically
- Data validation occurs automatically
- Valid data flows to prediction pipeline

#### Manual Pipeline Trigger
1. Access Airflow UI (http://localhost:8080)
2. Navigate to "employee_ingestion_dag"
3. Click "Trigger DAG" button

### 📈 Monitoring & Analytics

#### System Health
- **Grafana Dashboards**: http://localhost:3001
- **Data Quality Metrics**: Real-time validation statistics
- **Prediction Performance**: API response times and accuracy

#### Historical Analysis
1. Use "Past Predictions" in Streamlit app
2. Select date range and prediction source
3. Analyze trends and patterns
4. Export data for further analysis

## 📚 API Documentation

### Prediction Endpoint
```http
POST /predict
Content-Type: application/json
X-Request-Source: "API Client"

{
  "data": [
    {
      "Gender": "Male",
      "Age": 30,
      "JobRole": "Technology",
      "MonthlyIncome": 65000,
      "JobSatisfaction": "High"
    }
  ]
}
```

**Response:**
```json
{
  "predictions": ["Stayed"],
  "confidence_scores": [0.85],
  "database_status": "success",
  "total_predictions": 1
}
```

### Historical Data Endpoint
```http
GET /past-predictions?start_date=2025-01-01&end_date=2025-01-31&source=All
```

## 🔄 Data Pipeline

### Ingestion Workflow
1. **Data Discovery**: Scan raw data directory
2. **Validation**: Check data quality using Great Expectations
3. **Classification**: Route to good/bad data folders
4. **Statistics**: Store validation metrics
5. **Alerting**: Send notifications for quality issues
6. **Processing**: Trigger prediction jobs for valid data

### Data Validation Rules
- ✅ Required columns presence
- ✅ Data type validation
- ✅ Range checks (Age: 18-70, Income: 1K-100K)
- ✅ Categorical value validation
- ✅ Duplicate detection
- ✅ Missing value analysis

### Quality Metrics
- **Data Quality Score**: Percentage of valid records
- **Error Classification**: Missing values, invalid categories, out of range
- **Trend Analysis**: Quality degradation over time
- **Alert Thresholds**: Configurable quality gates

## 📊 Monitoring & Alerting

### Grafana Dashboards
- **Data Quality Dashboard**: Validation metrics and trends
- **Prediction Performance**: API metrics and model accuracy
- **System Health**: Infrastructure monitoring

### Alert Channels
- **Microsoft Teams**: Real-time notifications
- **Email Reports**: Daily/weekly summaries
- **HTML Reports**: Detailed validation results

### Key Metrics
- Data validation pass/fail rates
- Prediction API response times
- Model prediction confidence scores
- System resource utilization

## 🔧 Configuration

### Environment Variables
```bash
# Database Configuration
DATABASE_URL=postgresql://postgres:piggy@db:5432/employee_app_db
AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@airflow-db/airflow

# API Configuration
PREDICTION_API_URL=http://fastapi:8000/predict
PAST_PREDICTIONS_API_URL=http://fastapi:8000/past-predictions

# Airflow Configuration
AIRFLOW_UID=50000
_AIRFLOW_WWW_USER_USERNAME=admin
_AIRFLOW_WWW_USER_PASSWORD=admin

# Teams Integration (Optional)
TEAMS_WEBHOOK_URL=your_teams_webhook_url_here
```

### Model Configuration
- **Algorithm**: Random Forest Classifier
- **Features**: Age, Gender, Job Role, Monthly Income, Job Satisfaction
- **Target**: Employee Attrition (Stayed/Left)
- **Encoding**: Label encoding for categorical variables

## 🐛 Troubleshooting

### Common Issues

**Services not starting:**
```bash
# Check system resources
docker system prune -f
docker-compose down && docker-compose up -d
```

**Database connection errors:**
```bash
# Reset database
docker-compose down -v
docker-compose up -d
```

**Airflow DAGs not appearing:**
```bash
# Check DAG syntax
docker-compose exec airflow-scheduler airflow dags list
```

**Prediction errors:**
```bash
# Verify model files exist
docker-compose exec fastapi ls -la *.pkl
```

### Logs Access
```bash
# Application logs
docker-compose logs fastapi
docker-compose logs airflow-scheduler
docker-compose logs webapp

# Database logs
docker-compose logs db
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make changes and test thoroughly
4. Submit a pull request

### Code Standards
- Follow PEP 8 for Python code
- Add tests for new features
- Update documentation
- Ensure Docker builds succeed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Apache Airflow community for workflow orchestration
- FastAPI team for the excellent web framework
- Streamlit for rapid UI development
- Great Expectations for data validation
- Scikit-learn for machine learning capabilities

## 📞 Support

For support and questions:
- 📧 Create an issue in this repository
- 💬 Join our discussions
- 📖 Check the documentation

---

**⭐ Star this repository if you find it helpful!**

*Built with ❤️ for the data science and ML engineering community*