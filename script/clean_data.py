import pandas as pd

files = [
    "api_data_aadhar_enrolment/api_data_aadhar_enrolment_0_500000.csv",
    "api_data_aadhar_enrolment/api_data_aadhar_enrolment_500000_1000000.csv",
    "api_data_aadhar_enrolment/api_data_aadhar_enrolment_1000000_1006029.csv"
]

df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
df.to_csv("combined.csv", index=False)

print("Combined CSV created successfully!")
