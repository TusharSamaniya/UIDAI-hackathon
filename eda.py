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


