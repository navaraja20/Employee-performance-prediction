import os
import random
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.exceptions import AirflowFailException, AirflowSkipException

# Constants and paths
PROJECT_ROOT = "/opt/airflow"
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw_data")
GOOD_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "good_data")
BAD_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "bad_data")
GE_DATA_CONTEXT_ROOT = os.path.join(PROJECT_ROOT, "great_expectations")
SUITE_NAME = "employee_data_suite"

@dag(
    dag_id="employee_ingestion_dag",
    description="Employee performance data ingestion and validation pipeline",
    schedule_interval=timedelta(minutes=1),
    start_date=days_ago(1),
    catchup=False,
    max_active_runs=1,
    tags=["employee", "validation", "data-quality"],
)
def employee_ingestion_dag():

    @task(task_id="read_data")
    def read_data() -> str:
        files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith(".csv")]
        if not files:
            raise AirflowSkipException("No CSV files found in raw-data folder")
        return os.path.join(RAW_DATA_DIR, random.choice(files))

    @task(task_id="validate_data")
    def validate_data(filepath: str) -> dict:
        import pandas as pd
        import os

        try:
            print(f"Validating file: {filepath}")
            df = pd.read_csv(filepath)
            total_rows = len(df)
            
            # Simple validation checks instead of Great Expectations
            required_columns = ["Age", "Monthly Income", "Job Satisfaction", "Job Role"]
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Check for data quality issues
            missing_values = df.isnull().sum()
            duplicate_count = df.duplicated().sum()
            
            # Identify bad rows (rows with missing values or duplicates)
            bad_row_indices = []
            if missing_values.sum() > 0:
                bad_row_indices.extend(df[df.isnull().any(axis=1)].index.tolist())
            if duplicate_count > 0:
                bad_row_indices.extend(df[df.duplicated()].index.tolist())
            
            bad_row_indices = list(set(bad_row_indices))  # Remove duplicates
            invalid_rows = len(bad_row_indices)
            valid_rows = total_rows - invalid_rows
            
            # Determine criticality
            error_ratio = invalid_rows / total_rows if total_rows > 0 else 0
            criticality = "low" if error_ratio < 0.1 else "medium" if error_ratio < 0.5 else "high"
            
            # Create error summary
            errors = []
            for col, count in missing_values.items():
                if count > 0:
                    errors.append(f"{col}: {count} missing values")
            if duplicate_count > 0:
                errors.append(f"Duplicate rows: {duplicate_count}")
            
            validation_results = {
                "filepath": filepath,
                "total_rows": total_rows,
                "valid_rows": valid_rows,
                "invalid_rows": invalid_rows,
                "criticality": criticality,
                "errors_summary": "; ".join(errors) if errors else "No issues found",
                "error_counts": missing_values.to_dict(),
                "created_on": datetime.now().isoformat(),
                "bad_row_indices": bad_row_indices,
                "validation_status": "PASSED" if invalid_rows == 0 else "FAILED"
            }
            
            print(f"Validation completed: {validation_results}")
            return validation_results

        except Exception as e:
            raise AirflowFailException(f"Validation failed: {str(e)}")

    @task(task_id="save_statistics")
    def save_statistics(results: dict) -> None:
        from airflow.providers.postgres.hooks.postgres import PostgresHook
        import json

        try:
            hook = PostgresHook(postgres_conn_id="processed_files_db")
            conn = hook.get_conn()
            cursor = conn.cursor()

            query = """
                INSERT INTO validation_statistics (
                    filepath, total_rows, valid_rows, invalid_rows, criticality,
                    errors_summary, error_counts, created_on, bad_row_indices
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                results["filepath"],
                results["total_rows"],
                results.get("valid_rows", results["total_rows"]),
                results.get("invalid_rows", 0),
                results.get("criticality", "low"),
                results.get("errors_summary", "Basic validation passed"),
                json.dumps(results.get("error_counts", {})),
                results.get("created_on", datetime.now().isoformat()),
                json.dumps(results.get("bad_row_indices", []))
            ))
            conn.commit()
            print(f"Statistics saved successfully for {results.get('filepath', 'unknown file')}")
        except Exception as e:
            raise AirflowFailException(f"Database error: {str(e)}")
        finally:
            if conn:
                cursor.close()
                conn.close()

    @task(task_id="send_alerts")
    def send_alerts(results: dict) -> None:
        import requests
        import logging
        from airflow.models import Variable
        import json
        import os

        try:
            # Get Teams webhook URL
            try:
                webhook_url = Variable.get("TEAMS_WEBHOOK_URL")
                if webhook_url == "https://outlook.office.com/webhook/your-webhook-url-here":
                    logging.warning("Teams webhook URL is not configured properly. Please update TEAMS_WEBHOOK_URL variable with your actual Teams webhook URL.")
                    webhook_url = None
            except Exception:
                logging.warning("TEAMS_WEBHOOK_URL not configured, skipping Teams alert")
                webhook_url = None

            # Generate simple HTML report
            html_report_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Data Validation Report</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .header {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px; }}
                    .critical {{ color: #d9534f; }}
                    .medium {{ color: #f0ad4e; }}
                    .low {{ color: #5cb85c; }}
                    .details {{ margin: 20px 0; }}
                    table {{ border-collapse: collapse; width: 100%; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Employee Data Validation Report</h1>
                    <p><strong>File:</strong> {os.path.basename(results['filepath'])}</p>
                    <p><strong>Validation Time:</strong> {results['created_on']}</p>
                    <p><strong>Status:</strong> <span class="{results['criticality']}">{results['criticality'].upper()}</span></p>
                </div>
                
                <div class="details">
                    <h2>Summary</h2>
                    <table>
                        <tr><th>Metric</th><th>Value</th></tr>
                        <tr><td>Total Rows</td><td>{results['total_rows']}</td></tr>
                        <tr><td>Valid Rows</td><td>{results['valid_rows']}</td></tr>
                        <tr><td>Invalid Rows</td><td>{results['invalid_rows']}</td></tr>
                        <tr><td>Error Rate</td><td>{(results['invalid_rows']/results['total_rows']*100):.2f}%</td></tr>
                    </table>
                    
                    <h2>Issues Found</h2>
                    <p>{results['errors_summary']}</p>
                    
                    <h2>Error Details</h2>
                    <table>
                        <tr><th>Column</th><th>Missing Values</th></tr>
            """
            
            for col, count in results['error_counts'].items():
                if count > 0:
                    html_report_content += f"<tr><td>{col}</td><td>{count}</td></tr>"
            
            html_report_content += """
                    </table>
                </div>
            </body>
            </html>
            """
            
            # Save HTML report to uncommitted folder for access
            report_dir = f"{GE_DATA_CONTEXT_ROOT}/uncommitted/data_docs/local_site/validations"
            os.makedirs(report_dir, exist_ok=True)
            report_filename = f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            report_path = os.path.join(report_dir, report_filename)
            
            with open(report_path, 'w') as f:
                f.write(html_report_content)
            
            # Create accessible URL (assuming Airflow webserver can serve these files)
            docs_url = f"http://localhost:8080/static/validation_reports/{report_filename}"
            
            logging.info(f"HTML report generated: {report_path}")

            # Send Teams notification if webhook is configured
            if webhook_url and webhook_url != "https://outlook.office.com/webhook/your-webhook-url-here":
                try:
                    # Determine color based on criticality
                    color_map = {"low": "Good", "medium": "Warning", "high": "Attention"}
                    theme_color = {"low": "00FF00", "medium": "FFA500", "high": "FF0000"}
                    
                    alert = {
                        "@type": "MessageCard",
                        "@context": "http://schema.org/extensions",
                        "themeColor": theme_color.get(results['criticality'], "0076D7"),
                        "summary": f"Data Validation Alert - {results['criticality'].upper()}",
                        "sections": [{
                            "activityTitle": "🚨 Employee Data Validation Alert",
                            "activitySubtitle": f"File: {os.path.basename(results['filepath'])}",
                            "activityImage": "https://adaptivecards.io/content/cats/1.png",
                            "facts": [
                                {"name": "Status", "value": f"{results['criticality'].upper()}"},
                                {"name": "Total Rows", "value": str(results['total_rows'])},
                                {"name": "Invalid Rows", "value": f"{results['invalid_rows']} ({(results['invalid_rows']/results['total_rows']*100):.1f}%)"},
                                {"name": "Issues", "value": results['errors_summary'][:100] + "..." if len(results['errors_summary']) > 100 else results['errors_summary']}
                            ],
                            "markdown": True
                        }],
                        "potentialAction": [{
                            "@type": "OpenUri",
                            "name": "View Detailed Report",
                            "targets": [{"os": "default", "uri": docs_url}]
                        }]
                    }
                    
                    response = requests.post(webhook_url, json=alert, timeout=10)
                    response.raise_for_status()
                    logging.info("Teams alert sent successfully")
                except Exception as e:
                    logging.error(f"Failed to send Teams alert: {e}")
            else:
                logging.info("Teams webhook not configured or using placeholder URL - alert not sent")
            
            # Always log the alert locally
            logging.info(f"""
            🚨 DATA VALIDATION ALERT 🚨
            File: {os.path.basename(results['filepath'])}
            Total Rows: {results['total_rows']}
            Valid Rows: {results['valid_rows']}
            Invalid Rows: {results['invalid_rows']}
            Criticality: {results['criticality'].upper()}
            Issues: {results['errors_summary']}
            Report: {docs_url}
            """)
            
        except Exception as e:
            # Don't fail the DAG if alerting fails, just log it
            logging.error(f"Alerting failed: {str(e)}")
            logging.info(f"Validation completed for {os.path.basename(results.get('filepath', 'unknown'))}: {results.get('invalid_rows', 0)}/{results.get('total_rows', 0)} issues")

    @task(task_id="split_and_save_data")
    def split_and_save_data(results: dict) -> None:
        import pandas as pd
        try:
            df = pd.read_csv(results["filepath"])
            base_name = os.path.basename(results["filepath"])
            
            print(f"Processing file: {base_name}")
            print(f"Total rows: {results['total_rows']}, Invalid rows: {results['invalid_rows']}")
            
            if results["invalid_rows"] == 0:
                # No data quality issues - move to good_data
                good_path = os.path.join(GOOD_DATA_DIR, base_name)
                df.to_csv(good_path, index=False)
                print(f"File moved to good_data: {good_path}")
            elif results["valid_rows"] == 0:
                # All rows have problems - move to bad_data
                bad_path = os.path.join(BAD_DATA_DIR, base_name)
                df.to_csv(bad_path, index=False)
                print(f"File moved to bad_data: {bad_path}")
            else:
                # Split the file - some good, some bad rows
                bad_indices = results["bad_row_indices"]
                bad_rows = df.iloc[bad_indices]
                good_rows = df.drop(index=bad_indices)
                
                good_path = os.path.join(GOOD_DATA_DIR, base_name)
                bad_path = os.path.join(BAD_DATA_DIR, base_name)
                
                good_rows.to_csv(good_path, index=False)
                bad_rows.to_csv(bad_path, index=False)
                print(f"File split - Good rows: {good_path}, Bad rows: {bad_path}")
            
            # Remove original file from raw_data after processing
            os.remove(results["filepath"])
            print(f"Original file removed: {results['filepath']}")
            
        except Exception as e:
            raise AirflowFailException(f"File split and save error: {str(e)}")

    # DAG wiring
    data_file = read_data()
    validation_results = validate_data(data_file)

    data_file >> validation_results >> [
        save_statistics(validation_results),
        send_alerts(validation_results),
        split_and_save_data(validation_results)
    ]

employee_ingestion_dag = employee_ingestion_dag()
