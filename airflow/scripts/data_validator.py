import pandas as pd
import great_expectations as ge
from sqlalchemy import create_engine
from pymsteams import connectorcard
import os
import uuid
from datetime import datetime


def validate_data(file_path, good_data_path, bad_data_path, report_path):
    df = pd.read_csv(file_path)
    ge_df = ge.dataset.PandasDataset(df)

    expectations = [
        ge_df.expect_column_to_exist("Age"),
        ge_df.expect_column_values_to_not_be_null("MonthlyIncome"),
        ge_df.expect_column_values_to_be_in_set("EducationField", ["Life Sciences", "Medical", "Marketing", "Technical Degree", "Other", "Human Resources"]),
        ge_df.expect_column_values_to_be_between("Age", min_value=18, max_value=100),
        ge_df.expect_column_values_to_be_in_set("Gender", ["Male", "Female"]),
        ge_df.expect_column_values_to_be_of_type("DailyRate", "int64"),
        ge_df.expect_column_values_to_be_between("MonthlyRate", min_value=0)
    ]

    validation_results = ge_df.validate()
    criticality = "high" if not validation_results['success'] else "low"

    stats = {
        "filename": os.path.basename(file_path),
        "nb_rows": len(df),
        "nb_valid_rows": sum([res['success'] for res in expectations]),
        "nb_invalid_rows": sum([not res['success'] for res in expectations]),
        "errors": [res['expectation_config']['expectation_type'] for res in expectations if not res['success']],
        "timestamp": datetime.now().isoformat()
    }

    # Save stats to PostgreSQL
    engine = create_engine("postgresql+psycopg2://user:password@postgres:5432/employee_db")
    pd.DataFrame([stats]).to_sql('data_quality_stats', engine, if_exists='append', index=False)

    # Save HTML report
    report_file = os.path.join(report_path, f'report_{uuid.uuid4()}.html')
    with open(report_file, "w") as f:
        f.write(validation_results.to_html())

    # Send Microsoft Teams alert
    webhook = connectorcard("https://epitafr.webhook.office.com/webhookb2/fe98d8f4-571d-4986-9ea5-f04e7702ab25@3534b3d7-316c-4bc9-9ede-605c860f49d2/IncomingWebhook/5afac3a2888f4489af0f4c23439eb970/500a5448-3bbc-4150-a404-a45848e7baee/V21bSas1fsUanrFXS_UW9qnQKVV9fqf09ZFFCDm0oQV6M1")
    webhook.text(f"Data Quality Alert\nCriticality: {criticality}\nErrors: {', '.join(stats['errors'])}\nReport: file://{report_file}")
    webhook.send()

    # Separate valid and invalid rows
    invalid_rows = pd.DataFrame()
    valid_rows = df.copy()

    for res in expectations:
        if not res['success']:
            col = res['expectation_config']['kwargs'].get('column')
            if col:
                if 'value_set' in res['expectation_config']['kwargs']:
                    invalid_mask = ~df[col].isin(res['expectation_config']['kwargs']['value_set'])
                elif 'min_value' in res['expectation_config']['kwargs']:
                    invalid_mask = df[col] < res['expectation_config']['kwargs']['min_value']
                elif 'type_' in res['expectation_config']['kwargs']:
                    invalid_mask = df[col].map(lambda x: not isinstance(x, int))
                else:
                    invalid_mask = df[col].isna()

                invalid_rows = pd.concat([invalid_rows, df[invalid_mask]])
                valid_rows = valid_rows.drop(df[invalid_mask].index)

    # Save valid/invalid rows
    os.makedirs(good_data_path, exist_ok=True)
    os.makedirs(bad_data_path, exist_ok=True)

    if not valid_rows.empty:
        valid_rows.to_csv(os.path.join(good_data_path, os.path.basename(file_path)), index=False)
    if not invalid_rows.empty:
        invalid_rows.to_csv(os.path.join(bad_data_path, os.path.basename(file_path)), index=False)

    os.remove(file_path)
    return stats
