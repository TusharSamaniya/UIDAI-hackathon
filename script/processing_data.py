import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

input_path = os.path.join(BASE_DIR, "working_with_csv", "cleaned_aadhar_data.csv")
output_path = os.path.join(BASE_DIR, "working_with_csv", "aadhaar_enrolment_standardized.csv")

df = pd.read_csv(input_path, parse_dates=["date"])

df["state"] = df["state"].str.strip().str.upper()
df["district"] = df["district"].str.strip().str.upper()

df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["quarter"] = df["date"].dt.quarter
df["week_number"] = df["date"].dt.isocalendar().week

df["financial_year"] = np.where(
    df["month"] >= 4,
    df["year"].astype(str) + "-" + (df["year"] + 1).astype(str),
    (df["year"] - 1).astype(str) + "-" + df["year"].astype(str)
)

df["pct_age_0_5"] = df["age_0_5"] / df["enrolment_count"] * 100
df["pct_age_5_17"] = df["age_5_17"] / df["enrolment_count"] * 100
df["pct_age_18_plus"] = df["age_18_greater"] / df["enrolment_count"] * 100

df["pin_category"] = np.where(
    df["pincode"] >= 700000, "URBAN",
    np.where(df["pincode"] >= 400000, "SEMI-URBAN", "RURAL")
)

df.to_csv(output_path, index=False)
print("✅ Processing completed")
