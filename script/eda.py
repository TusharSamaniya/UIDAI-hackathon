import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

data_path = os.path.join(BASE_DIR, "working_with_csv", "aadhaar_enrolment_standardized.csv")
output_dir = os.path.join(BASE_DIR, "outputs", "figures")

os.makedirs(os.path.join(output_dir, "temporal"), exist_ok=True)
os.makedirs(os.path.join(output_dir, "geographic"), exist_ok=True)
os.makedirs(os.path.join(output_dir, "demographic"), exist_ok=True)
os.makedirs(os.path.join(output_dir, "risk_analysis"), exist_ok=True)

df = pd.read_csv(data_path, parse_dates=["date"])

yearly = df.groupby("year")["enrolment_count"].sum()

plt.figure(figsize=(8,5))
yearly.plot(marker="o")
plt.title("Year-wise Aadhaar Enrolment Trend")
plt.savefig(os.path.join(output_dir, "temporal", "yearly_trend.png"), dpi=300)
plt.close()
