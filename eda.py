import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

plt.style.use("seaborn-v0_8")

# CREATE OUTPUT DIRECTORIES 
os.makedirs("outputs/figures/temporal", exist_ok=True)
os.makedirs("outputs/figures/geographic", exist_ok=True)
os.makedirs("outputs/figures/demographic", exist_ok=True)
os.makedirs("outputs/figures/risk_analysis", exist_ok=True)

#  LOAD DATA 
df = pd.read_csv(
    "aadhaar_enrolment_standardized.csv",
    parse_dates=["date"]
)

#DATA HEALTH 
missing_pct = df.isnull().mean() * 100
zero_enrolments = df[df["enrolment_count"] == 0].shape[0]

Q1 = df["enrolment_count"].quantile(0.25)
Q3 = df["enrolment_count"].quantile(0.75)
IQR = Q3 - Q1
outliers = df[
    (df["enrolment_count"] < Q1 - 1.5 * IQR) |
    (df["enrolment_count"] > Q3 + 1.5 * IQR)
]

# TEMPORAL ANALYSIS
yearly = df.groupby("year")["enrolment_count"].sum()

plt.figure(figsize=(8,5))
yearly.plot(marker="o")
plt.title("Year-wise Aadhaar Enrolment Trend")
plt.xlabel("Year")
plt.ylabel("Total Enrolments")
plt.savefig("outputs/figures/temporal/yearly_trend.png", dpi=300, bbox_inches="tight")
plt.close()

monthly_trend = (
    df.groupby(["year", "month"])["enrolment_count"]
      .sum()
      .reset_index()
)

plt.figure(figsize=(9,5))
sns.lineplot(
    data=monthly_trend,
    x="month",
    y="enrolment_count",
    hue="year"
)
plt.title("Monthly Enrolment Pattern (Multi-Year)")
plt.savefig("outputs/figures/temporal/monthly_pattern.png", dpi=300, bbox_inches="tight")
plt.close()

quarterly = df.groupby("quarter")["enrolment_count"].sum()

plt.figure(figsize=(6,4))
quarterly.plot(kind="bar")
plt.title("Quarter-wise Enrolment Comparison")
plt.savefig("outputs/figures/temporal/quarterly_comparison.png", dpi=300, bbox_inches="tight")
plt.close()

#GEOGRAPHIC ANALYSIS
state_enrol = (
    df.groupby("state")["enrolment_count"]
      .sum()
      .sort_values()
)

plt.figure(figsize=(7,5))
state_enrol.head(10).plot(kind="barh")
plt.title("Bottom 10 States by Enrolment")
plt.savefig("outputs/figures/geographic/bottom_10_states.png", dpi=300, bbox_inches="tight")
plt.close()

plt.figure(figsize=(7,5))
state_enrol.tail(10).plot(kind="barh")
plt.title("Top 10 States by Enrolment")
plt.savefig("outputs/figures/geographic/top_10_states.png", dpi=300, bbox_inches="tight")
plt.close()

plt.figure(figsize=(12,5))
sns.boxplot(data=df, x="state", y="enrolment_count")
plt.xticks(rotation=90)
plt.title("District Enrolment Spread within States")
plt.savefig("outputs/figures/geographic/state_district_spread.png", dpi=300, bbox_inches="tight")
plt.close()

population = df.groupby(["state", "district"], as_index=False)\
               .agg({"enrolment_count": "sum"})

population["estimated_population"] = population["enrolment_count"] * 1.2
population["esi"] = (
    population["enrolment_count"] /
    population["estimated_population"]
) * 100

population["coverage_level"] = pd.cut(
    population["esi"],
    bins=[0, 60, 85, 100],
    labels=["Low Coverage", "Medium Coverage", "High Coverage"]
)

plt.figure(figsize=(6,4))
population["coverage_level"].value_counts().plot(kind="bar")
plt.title("Coverage Level Distribution")
plt.savefig("outputs/figures/geographic/coverage_distribution.png", dpi=300, bbox_inches="tight")
plt.close()

#DEMOGRAPHIC ANALYSIS
age_state = (
    df.groupby("state")[["pct_age_0_5", "pct_age_5_17", "pct_age_18_plus"]]
      .mean()
)

plt.figure(figsize=(10,5))
age_state.plot(kind="bar", stacked=True)
plt.title("Age Composition by State")
plt.savefig("outputs/figures/demographic/age_composition_state.png", dpi=300, bbox_inches="tight")
plt.close()

age_time = df.groupby("year")[
    ["age_0_5", "age_5_17", "age_18_greater"]
].sum()

plt.figure(figsize=(8,5))
age_time.plot(kind="area", stacked=True)
plt.title("Age-wise Enrolment Trend Over Time")
plt.savefig("outputs/figures/demographic/age_trend_time.png", dpi=300, bbox_inches="tight")
plt.close()

#URBAN vs RURAL
plt.figure(figsize=(6,4))
df.groupby("pin_category")["enrolment_count"].sum().plot(kind="bar")
plt.title("Enrolment by PIN Category")
plt.savefig("outputs/figures/geographic/pin_category_enrolment.png", dpi=300, bbox_inches="tight")
plt.close()

#GROWTH & RISK ANALYSIS
monthly = (
    df.groupby(["state", "district", "year", "month"], as_index=False)
      .agg({"enrolment_count": "sum"})
)

monthly["yoy_growth_rate"] = (
    monthly.groupby(["state", "district"])["enrolment_count"]
           .pct_change(periods=12) * 100
)

plt.figure(figsize=(7,4))
sns.histplot(monthly["yoy_growth_rate"].dropna(), bins=30)
plt.title("YoY Growth Rate Distribution")
plt.savefig("outputs/figures/risk_analysis/yoy_growth_distribution.png", dpi=300, bbox_inches="tight")
plt.close()

merged = monthly.merge(
    population[["state", "district", "esi"]],
    on=["state", "district"],
    how="left"
)

plt.figure(figsize=(7,5))
sns.scatterplot(data=merged, x="esi", y="yoy_growth_rate")
plt.title("Growth vs Coverage (ESI)")
plt.savefig("outputs/figures/risk_analysis/growth_vs_coverage.png", dpi=300, bbox_inches="tight")
plt.close()

monthly["monthly_growth_rate"] = (
    monthly.groupby(["state", "district"])["enrolment_count"]
           .pct_change() * 100
)

monthly["anomaly"] = np.abs(monthly["monthly_growth_rate"]) > 50
