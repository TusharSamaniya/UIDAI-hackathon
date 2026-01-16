import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use("seaborn-v0_8")

df = pd.read_csv(
    "aadhaar_enrolment_standardized.csv",
    parse_date=["date"]
)

#data health and coverage analysis
#missing values
missing_pct = df.isnull().mean*100
missing_pct.sort_values(ascending= False)

#zero enrolment
zero_enrolments = df[df["enrolment_count"] == 0].shape[0]
zero_enrolments

#outlier detection
Q1 = df["enrolment_count"].quantile(0.25)
Q3 = df["enrolment_count"].quantile(0.75)
IQR = Q3 - Q1

outliers = df[
    (df["enrolment_count"] < Q1 - 1.5 * IQR) |
    (df["enrolment_count"] > Q3 + 1.5 * IQR)
]

outliers.shape

#temporal analysis
yearly = df.groupby("year")["enrolment_count"].sum()
plt.title("Year-wise Aadhar Enrolment Trend")
plt.ylabel("Totla Enrolment")
plt.xlabel("Year")
plt.show()

#monthly thrend
monthly_trend = (
    df.groupby(["year", "month"])["enrolment_count"]
    .sum()
    .reset_index()
)
sns.lineplot(
    date=month_trend,
    x = "month",
    y = "enrolment_count",
    hue = "year"
)
plt.title("Monthly enrolment plattern (Multi-year)")
plt.show()

#Quarter wise comparsion
quarterly = df.groupby("quarter")["enrolment_count"].sum()

quarterly.plot(lind = "bar")
plt.title("Quarter-wise Enrolment Comparison")
plt.show()

#Financial year growth
fy = df.groupby("financial_year")["enrolment_count"].sum()
fy_growth = fy.pct_change() * 100

fy_growth

#geographic analysis
#top 10 and bottom 10 states
state_enrol = (
    df.groupby("state")["enrolment_count"]
    .sum()
    .sort_values()
)
bottom_10 = state_enrol.head(10)
top_10 = state_enrol.tail(10)

top_10.plot(kind = "barh", title = "Top 10 states by Enrolment")
plt.show()

bottom_10.plot(kind = "barh", title = "Bottom 10 states by Enrolment")
plt.show()

sns.boxplot(
    date = df,
    x = "state",
    y = "enrolment_count"
)
plt.xtickxlabel("State")
plt.title("District Enrolment Spread within States")
plt.xticks(rotation = 90)
plt.show()

#coverage level distribution
population["coverage_level"].value_counts().plot(kind="bar")
plt.title("Coverage Level Distribution")
plt.show()

#Demographic analysis -- age wise
age_state = (
    df.groupby("state")[["pct_age_0_5", "pct_age_5_17", "pct_age_18_plus"]]
    .mean()
)
age_state.plot(kind = "bar", stacked = True)
plt.title("Age Composition by State")
plt.show()

#age trends over time
age_time = df.groupby("year")[
    ["age_0_5", "age_5_17", "age_18_greater"]
].sum()

age_time.plot(kind = "area", stacked = True)
plt.title("Age-wise Enrolment Trend Over Time")
plt.show()
