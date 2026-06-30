import os
import subprocess
import sys
from dagster import Definitions, job, op, schedule

# Dynamic path to the current virtual environment's Python executable
PYTHON_EXE = sys.executable

# =========================================================
# OP 1: Scrape Telegram Data
# =========================================================

@op
def scrape_telegram_data():
    print("Running Telegram scraper...")

    result = subprocess.run(
        [PYTHON_EXE, os.path.join("src", "scraper.py")],
        capture_output=True,
        text=True
    )

    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise Exception(f"Scraper failed: {result.stderr}")

    return "scrape_complete"


# =========================================================
# OP 2: Load Raw Data into PostgreSQL
# =========================================================

@op
def load_raw_to_postgres(upstream_status):
    # upstream_status captures the "scrape_complete" string
    print(f"Upstream status: {upstream_status}")
    print("Loading raw data into PostgreSQL...")

    result = subprocess.run(
        [PYTHON_EXE, os.path.join("src", "load_to_postgres.py")],
        capture_output=True,
        text=True
    )

    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise Exception(f"Load step failed: {result.stderr}")

    return "load_complete"


# =========================================================
# OP 3: Run dbt Transformations
# =========================================================

@op
def run_dbt_transformations(upstream_status):
    print("Running dbt models...")

    # Ensure the 'dbt' directory exists relative to current working directory
    dbt_cwd = os.path.abspath("dbt")

    result = subprocess.run(
        ["dbt", "run"],
        cwd=dbt_cwd,
        capture_output=True,
        text=True,
        shell=True # Required on Windows for CLI tools like dbt if not globally mapped
    )

    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise Exception(f"dbt run failed: {result.stderr}")

    return "dbt_complete"


# =========================================================
# OP 4: Run YOLO Enrichment
# =========================================================

@op
def run_yolo_enrichment(upstream_status):
    print("Running YOLO object detection...")

    result = subprocess.run(
        [PYTHON_EXE, os.path.join("src", "yolo_detect.py")],
        capture_output=True,
        text=True
    )

    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise Exception(f"YOLO step failed: {result.stderr}")

    return "yolo_complete"


# =========================================================
# DAG / JOB GRAPH
# =========================================================

@job
def telegram_analytics_pipeline():
    raw = scrape_telegram_data()
    loaded = load_raw_to_postgres(raw)
    dbt_out = run_dbt_transformations(loaded)
    run_yolo_enrichment(dbt_out)


# =========================================================
# SCHEDULER (Daily Run)
# =========================================================

@schedule(
    job=telegram_analytics_pipeline,
    cron_schedule="0 2 * * *",  # every day at 2 AM
    execution_timezone="Africa/Addis_Ababa"
)
def daily_schedule(_context):
    return {}
    

# =========================================================
# DEFINITIONS (Dagster Entry Point)
# =========================================================

defs = Definitions(
    jobs=[telegram_analytics_pipeline],
    schedules=[daily_schedule]
)