import pandas as pd
import numpy as np
import os

# Create output folders automatically (very useful!)
os.makedirs('insights', exist_ok=True)

print("Current working directory:", os.getcwd())

file_path = "../working_with_csv/aadhaar_enrolment_standardized.csv"
print("Trying to load:", os.path.abspath(file_path))

df = pd.read_csv(file_path)

print("Origin shape: ", df.shape)
print(df.columns)

#Aggregate to district level
district_level = df.groupby(['state', 'district'], as_index=False).agg({
    'enrolment_count':          'sum',
    'age_0_5':                  'sum',
    'age_5_17':                 'sum',
    'age_18_greater':           'sum',
    'year':                     'max',           
    'pin_category':             lambda x: x.mode()[0] if not x.mode().empty else 'UNKNOWN',  
})

#quick percentage calculations
district_level['pct_child'] = district_level['age_0_5'] / district_level['enrolment_count'].replace(0, np.nan) * 100
district_level['pct_child'] = district_level['pct_child'].fillna(0)

# Estimated Saturation Index (ESI) 
district_level['estimated_population'] = district_level['enrolment_count'] * 1.15  
district_level['esi'] = district_level['enrolment_count'] / district_level['estimated_population'] * 100
district_level['esi'] = district_level['esi'].clip(0, 100)

#calcute the invidual risk composition
#Coverage Risk ── (higher = worse)
# Low ESI → high risk
district_level['low_coverage_score'] = 1 - (district_level['esi'] / 100)
district_level['low_coverage_score'] = district_level['low_coverage_score'].clip(0, 1)

# Growth Risk 
# We need recent growth → let's take last 12 months if possible

# First: monthly enrolments per district
monthly = df.groupby(['state', 'district', 'year', 'month'], as_index=False)['enrolment_count'].sum()

# Latest 12 months growth (approximation)
latest = monthly.sort_values(['state','district','year','month']).groupby(['state','district']).tail(12)
growth_12m = latest.groupby(['state','district'])['enrolment_count'].sum()

# Previous 12 months
prev = monthly.sort_values(['state','district','year','month']).groupby(['state','district']).tail(24).head(12)
growth_prev = prev.groupby(['state','district'])['enrolment_count'].sum()

yoy_growth = (growth_12m / growth_prev.replace(0, np.nan) - 1) * 100
yoy_growth = yoy_growth.replace([np.inf, -np.inf], np.nan).fillna(0)

district_level = district_level.merge(yoy_growth.rename('yoy_growth_pct'), on=['state','district'], how='left')

# Growth risk: negative or very low growth = bad
district_level['growth_risk_score'] = np.where(
    district_level['yoy_growth_pct'] <= 0, 1.0,
    np.where(district_level['yoy_growth_pct'] <= 5, 0.7,
             np.where(district_level['yoy_growth_pct'] <= 15, 0.4, 0.1))
)

# Child % risk 
# Too low = future risk
district_level['child_gap_score'] = np.where(
    district_level['pct_child'] >= 12, 0.0,
    np.where(district_level['pct_child'] >= 8,  0.3,
             np.where(district_level['pct_child'] >= 4,  0.7, 1.0))
)

# Months with zero enrolment in recent period
recent_months = monthly[monthly['year'] >= monthly['year'].max() - 2]
zero_months = recent_months[recent_months['enrolment_count'] == 0].groupby(['state','district']).size()

district_level = district_level.merge(zero_months.rename('zero_months_count'), on=['state','district'], how='left')
district_level['zero_months_count'] = district_level['zero_months_count'].fillna(0)

# Infra risk - more zero months = higher risk
district_level['infra_risk_score'] = np.clip(district_level['zero_months_count'] / 6, 0, 1)

district_level['risk_score'] = (
    0.40 * district_level['low_coverage_score'] +
    0.30 * district_level['growth_risk_score'] +
    0.20 * district_level['child_gap_score'] +
    0.10 * district_level['infra_risk_score']
)

# Round for readability
district_level['risk_score'] = district_level['risk_score'].round(3)

# Categorize
district_level['risk_level'] = pd.cut(
    district_level['risk_score'],
    bins=[-0.001, 0.40, 0.70, 1.001],
    labels=['Low Risk', 'Medium Risk', 'High Risk']
)

# ── Save results ──
district_level.to_csv('insights/district_risk_scores.csv', index=False)

# Top 20 most risky districts
top_risky = district_level.sort_values('risk_score', ascending=False).head(20)
top_risky.to_csv('insights/top_20_high_risk_districts.csv', index=False)

print("\nTop 10 highest risk districts:")
print(top_risky[['state', 'district', 'risk_score', 'risk_level', 'esi', 'pct_child', 'yoy_growth_pct']].to_string(index=False))