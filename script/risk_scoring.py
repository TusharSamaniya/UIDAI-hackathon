import pandas as pd
import numpy as np

#load the processing data
df = pd.read_csv("aadhaar_enrolment_standardized.csv")

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

