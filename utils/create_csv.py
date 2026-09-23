import pandas as pd
from generate_data import generate_patients

batch_id = 1

patients = generate_patients( batch_id=batch_id, n=1000)

df = pd.DataFrame(patients)

# Arrange columns
df = df[
    [
        "patient_id",
        "biomarker_a",
        "biomarker_group",
        "pfs_days",
        "treatment_day",
        "pfs_available_day"
    ]
]

print(len(df))
print(df.head())

df.to_csv(f"data/synthetic_patients/synthetic_patients_batch_{batch_id}.csv", index=False)
