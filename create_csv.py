import pandas as pd
from generate_data import generate_patients


patients = generate_patients(1000)

df = pd.DataFrame(patients)

df.insert(
    0,
    "patient_id",
    range(1, len(df) + 1)
)

print(len(df))
print(df.head())

df.to_csv("synthetic_patients.csv", index=False)