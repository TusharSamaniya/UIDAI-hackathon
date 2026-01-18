import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

input_path = os.path.join(BASE_DIR, "working_with_csv", "aadhaar_enrolment_standardized.csv")
insights_dir = os.path.join(BASE_DIR, "insights")

os.makedirs(insights_dir, exist_ok=True)

df = pd.read_csv(input_path)

district_level = df.groupby(['state','district'], as_index=False).agg({
    'enrolment_count':'sum',
    'age_0_5':'sum',
    'age_5_17':'sum',
    'age_18_greater':'sum'
})

district_level['pct_child'] = district_level['age_0_5'] / district_level['enrolment_count'] * 100
district_level['estimated_population'] = district_level['enrolment_count'] * 1.15
district_level['esi'] = district_level['enrolment_count'] / district_level['estimated_population'] * 100

district_level['risk_score'] = 1 - (district_level['esi'] / 100)
district_level['risk_score'] = district_level['risk_score'].clip(0,1)

district_level.to_csv(os.path.join(insights_dir, "district_risk_scores.csv"), index=False)

top_20 = district_level.sort_values("risk_score", ascending=False).head(20)
top_20.to_csv(os.path.join(insights_dir, "top_20_high_risk_districts.csv"), index=False)

print("✅ Risk scoring completed")
