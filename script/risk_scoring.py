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

