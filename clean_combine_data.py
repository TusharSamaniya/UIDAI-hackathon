import pandas as pd
import numpy as np

df = pd.read_csv("combined.csv")
print(df.shape)
df.head()

df.info()
df.describe(include = "all")

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

df["date"] = pd.to_datetime(
    df["date"],
    format="%d-%m-%Y",
    errors="coerce"
)
df = df.dropna(subset=["date"])

df["state"] = df["state"].str.strip().str.title()
df["district"] = df["district"].str.strip().str.title()

age_cols = ["age_0_5", "age_5_17", "age_18_greater"]

for col in age_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    df[col] = df[col].astype(int)


df = df[df["pincode"].between(100000, 999999)]

df["enrolment_count"] = (
    df["age_0_5"] +
    df["age_5_17"] +
    df["age_18_greater"]
)
df = df[df["enrolment_count"] > 0]
df = df.drop_duplicates()

df.to_csv("cleaned_aadhar_data.csv", index=False)
print("data clean successfully")
df.info()