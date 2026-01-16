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


