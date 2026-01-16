import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use("seaborn-v0_8")

# Load data
df = pd.read_csv(
    "aadhaar_enrolment_standardized.csv",
    parse_dates=["date"]
)


# 1. DATA HEALTH

missing_pct = df.isnull().mean() * 100

zero_enrolments = df[df["enrolment_count"] == 0].shape[0]

Q1 = df["enrolment_count"].quantile(0.25)
Q3 = df["enrolment_count"].quantile(0.75)
IQR = Q3 - Q1
outliers = df[
    (df["enrolment_count"] < Q1 - 1.5 * IQR) |
    (df["enrolment_count"] > Q3 + 1.5 * IQR)
]


# 2. TEMPORAL ANALYSIS

yearly = df.groupby("year")["enrolment_count"].sum()
yearly.plot(marker="o")
plt.title("Year-wise Aadhaar Enrolment Trend")
plt.show()

monthly_trend = (
    df.groupby(["year", "month"])["enrolment_count"]
    .sum()
    .reset_index()
)

sns.lineplot(
    data=monthly_trend,
    x="month",
    y="enrolment_count",
    hue="year"
)
plt.title("Monthly Enrolment Pattern (Multi-Year)")
plt.show()

quarterly = df.groupby("quarter")["enrolment_count"].sum()
quarterly.plot(kind="bar")
plt.title("Quarter-wise Enrolment Comparison")
plt.show()

fy = df.groupby("financial_year")["enrolment_count"].sum()
fy_growth = fy.pct_change() * 100


# 3. GEOGRAPHIC ANALYSIS

state_enrol = (
    df.groupby("state")["enrolment_count"]
    .sum()
    .sort_values()
)

state_enrol.head(10).plot(kind="barh", title="Bottom 10 States")
plt.show()

state_enrol.tail(10).plot(kind="barh", title="Top 10 States")
plt.show()

sns.boxplot(data=df, x="state", y="enrolment_count")
plt.xticks(rotation=90)
plt.title("District Enrolment Spread within States")
plt.show()

population = df.groupby(["state", "district"], as_index=False)\
               .agg({"enrolment_count": "sum"})

population["estimated_population"] = population["enrolment_count"] * 1.2
population["esi"] = (population["enrolment_count"] /
                     population["estimated_population"]) * 100

population["coverage_level"] = pd.cut(
    population["esi"],
    bins=[0, 60, 85, 100],
    labels=["Low Coverage", "Medium Coverage", "High Coverage"]
)

population["coverage_level"].value_counts().plot(kind="bar")
plt.title("Coverage Level Distribution")
plt.show()


# 4. DEMOGRAPHIC ANALYSIS

age_state = (
    df.groupby("state")[["pct_age_0_5", "pct_age_5_17", "pct_age_18_plus"]]
    .mean()
)
age_state.plot(kind="bar", stacked=True)
plt.title("Age Composition by State")
plt.show()

age_time = df.groupby("year")[
    ["age_0_5", "age_5_17", "age_18_greater"]
].sum()

age_time.plot(kind="area", stacked=True)
plt.title("Age-wise Enrolment Trend Over Time")
plt.show()


# 5. URBAN vs RURAL

df.groupby("pin_category")["enrolment_count"].sum().plot(kind="bar")
plt.title("Enrolment by PIN Category")
plt.show()


# 6. GROWTH & RISK

monthly = (
    df.groupby(["state", "district", "year", "month"], as_index=False)
    .agg({"enrolment_count": "sum"})
)

monthly["yoy_growth_rate"] = (
    monthly.groupby(["state", "district"])["enrolment_count"]
    .pct_change(periods=12) * 100
)

sns.histplot(monthly["yoy_growth_rate"], bins=30)
plt.title("YoY Growth Rate Distribution")
plt.show()

merged = monthly.merge(
    population[["state", "district", "esi"]],
    on=["state", "district"],
    how="left"
)

sns.scatterplot(data=merged, x="esi", y="yoy_growth_rate")
plt.title("Growth vs Coverage")
plt.show()

monthly["monthly_growth_rate"] = (
    monthly.groupby(["state", "district"])["enrolment_count"]
    .pct_change() * 100
)

monthly["anomaly"] = np.abs(monthly["monthly_growth_rate"]) > 50
