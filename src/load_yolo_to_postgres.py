import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/medical_db"
)

df = pd.read_csv("data/processed/yolo_detections.csv")

df.to_sql(
    "stg_yolo_detections",
    engine,
    if_exists="replace",
    index=False
)

print("YOLO detections uploaded successfully!")