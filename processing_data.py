import pandas as pd
import numpy as np

df = pd.read_csv("cleaned_aadhar_data.csv", parse_dates=["date"])

#convert to uppercase
df["state"] = df["state"].str.upper()
df["district"] = df["district"].str.upper()

#remove the special characters
df["state"] = df["state"].str.replace(r"[A-Z]", "", regex=True)
df["district"] = df["district"].str.replace(r"[A-Z]", "", regex=True)

#remove the extra space
df["state"] = df["state"].str.replace(r"\s+", " ", regex= True).str.strip()
df["district"] = df["district"].str.replace(r"\s+", " ", regex= True).str.strip()


#update the year, month, quarter, week_number, financial_year
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["quarter"] = df["date"].dt.quarter
df["week_number"] = df["date"].dt.isocalendar().week


#update the financial year start to april
df["financial_year"] = np.where(
    df["month"] >= 4,
    df["year"].astype(str) + "-" + (df["year"] + 1).astype(str),
    (df["year"] - 1).astype(str) + "-" + df["year"].astype(str)
)


#create meaning ratios and growth
df["pct_age_0_5"] = (df["age_0_5"]/df["enrolment_count"]) * 100
df["pct_age_5_17"] = (df["age_5_17"]/df["enrolment_count"]) * 100
df["pct_age_18_plus"] = (df["age_18_greater"] / df["enrolment_count"]) * 100


#monthly aggregation
monthly = (
    df.groupby(["state", "district", "year", "month"], as_index = False)
    .agg({"enrolment_count": "sum"})
    .sort_values(["state", "district", "year", "month"])
)

#month growth rate
monthly["monthly_growth_rate"] = (
    monthly.groupby(["state", "district"])["enrolment_count"]
           .pct_change() * 100
)

#YoY growth rate
monthly["yoy_growth_rate"] = (
    monthly.groupby(["state", "district"])["enrolment_count"]
           .pct_change(periods=12) * 100
)

#pin category
df["pin_category"] = np.where(
    df["pincode"] >= 700000, "URBAN",
    np.where(df["pincode"] >= 400000, "SEMI-URBAN", "RURAL")
)

#district and state codes
df["state_code"] = df["state"].astype("category").cat.codes
df["district_code"] = df["district"].astype("category").cat.codes

#enrolment saturation index
population = df.groupby(["state", "district"], as_index=False)\
               .agg({"enrolment_count": "sum"})

population["estimated_population"] = population["enrolment_count"] * 1.2

#esi calculation
population["esi"] = (
    population["enrolment_count"] /
    population["estimated_population"]
) * 100

#coverage buckets
population["coverage_level"] = pd.cut(
    population["esi"],
    bins=[0, 60, 85, 100],
    labels=["Low Coverage", "Medium Coverage", "High Coverage"]
)

#trends and momentum features
monthly["rolling_3m_avg"] = (
    monthly.groupby(["state", "district"])["enrolment_count"]
           .rolling(3).mean().reset_index(level=[0,1], drop=True)
)

monthly["momentum"] = monthly["enrolment_count"] - monthly["rolling_3m_avg"]

#acceleration flag
monthly["acceleration_flag"] = np.where(
    monthly["momentum"] > 0, "INCREASING",
    np.where(monthly["momentum"] < 0, "DECLINING", "STABLE")
)

#policy bucketing
monthly["policy_bucket"] = np.select(
    [
        (monthly["yoy_growth_rate"] > 10),
        (monthly["yoy_growth_rate"] <= 10)
    ],
    [
        "SUPPORT / SCALE",
        "PRIORITY INTERVENTION"
    ],
    default="MONITOR"
)

#data quality
df["data_quality_score"] = 100

df.loc[df["enrolment_count"] <= 0, "data_quality_score"] -= 20
df.loc[df["pincode"].isna(), "data_quality_score"] -= 10

#save output
df.to_csv("aadhaar_enrolment_standardized.csv", index = False)