Aadhaar Enrolment Analytics & Risk Assessment
UIDAI Data Hackathon 2026
Despite widespread Aadhaar adoption across India, enrolment coverage and growth patterns vary significantly across regions and demographic groups. Certain states and districts continue to show slow growth, low child enrolment, or early saturation, which may lead to future identity coverage gaps.
UIDAI requires a data-driven, scalable approach to identify such regions early and support targeted policy interventions.

Objective
The primary objectives of this project are to:
Analyze Aadhaar enrolment patterns across time, geography, and age groups
Identify regions with slowing enrolment growth or low coverage
Develop a risk-based prioritization framework for states and districts
Provide actionable insights and policy recommendations to support UIDAI decision-making

Dataset Description
Source: UIDAI Aadhaar Enrolment Dataset (data.gov.in)
The dataset contains aggregated Aadhaar enrolment information with the following key attributes:

Methodology
The project follows a structured analytics workflow:
1. Data Cleaning & Standardization
2. Feature Engineering
3. Exploratory Data Analysis (EDA)
4. Advanced Analytics:
(i). Estimated coverage calculation
(ii). Enrolment momentum analysis
(iii). Composite risk scoring for districts
5.Validation & Robustness Checks
6.Key Insights
(i). Several districts exhibit low enrolment coverage combined with declining growth, indicating high future risk
(ii). Child (0–5 years) enrolment shows significant regional disparity, potentially impacting long-term inclusion
(ii). Urban regions demonstrate near saturation, while rural and semi-urban regions retain substantial enrolment potential
(iv). A relatively small subset of districts contributes disproportionately to enrolment stagnation risk

7.Enrolment Risk Scoring
Districts were categorized into High Risk, Medium Risk, and Low Risk groups to support targeted interventions and efficient resource allocation.

8.Policy Recommendations

Validation & Limitations

Validation:
Risk rankings align with observed enrolment and coverage patterns
Sensitivity analysis confirms stability of high-risk region identification

Limitations:
Population coverage is estimated due to lack of official denominators
Aggregated data limits household-level inference
Long-term forecasting accuracy may reduce without additional variables

9.Expected Impact

(i). If adopted, this solution can help UIDAI:
(ii). Proactively identify enrolment gaps
(iii). Optimize deployment of enrolment infrastructure
(iv). Improve inclusion outcomes
(v). Enable data-driven policy planning at district and state levels

📁 Project Structure
project/
│── data/
│   ├── raw/
│   ├── cleaned/
│── analysis/
│── notebooks/
│── outputs/
│   ├── charts/
│── README.md

How to Run (Optional)
Install required Python dependencies
Run the data processing script
Execute the EDA and analytics scripts
