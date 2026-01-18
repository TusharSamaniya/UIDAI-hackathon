import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

input_path = os.path.join(BASE_DIR, "working_with_csv", "combined.csv")
output_path = os.path.join(BASE_DIR, "working_with_csv", "cleaned_aadhar_data.csv")

df = pd.read_csv(input_path)
print(df.shape)

df.columns = (
    df.columns.str.strip()
              .str.lower()
              .str.replace(" ", "_")
)

df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")
df = df.dropna(subset=["date"])

df["state"] = df["state"].str.strip().str.title()
df["district"] = df["district"].str.strip().str.title()

age_cols = ["age_0_5", "age_5_17", "age_18_greater"]
for col in age_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

df = df[df["pincode"].between(100000, 999999)]

df["enrolment_count"] = df[age_cols].sum(axis=1)
df = df[df["enrolment_count"] > 0].drop_duplicates()

df.to_csv(output_path, index=False)
print("✅ Data cleaned successfully")
