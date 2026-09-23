import pandas as pd

batch_id = 1

df = pd.read_csv(
    f"data/synthetic_patients/synthetic_patients_batch_{batch_id}.csv"
)

final_day = df["pfs_available_day"].max()

simulation_records = []

for current_day in range(1, final_day + 1):

    treated_patients = df[
        df["treatment_day"] <= current_day
    ]

    available_pfs = df[
        df["pfs_available_day"] <= current_day
    ]

    print(
        "\nDay:", current_day,
        "| Patients treated:", len(treated_patients),
        "| PFS available:", len(available_pfs)
    )

    groups = ["Low", "Medium", "High"]

    for group in groups:

        group_data = available_pfs[
            available_pfs["biomarker_group"] == group
        ]["pfs_days"]

        count = len(group_data)

        if count > 0:
            mean = group_data.mean()
        else:
            mean = None

        if count > 1:
            sd = group_data.std()
            lower_boundary = mean - 2 * sd
            upper_boundary = mean + 2 * sd
        else:
            sd = None
            lower_boundary = None
            upper_boundary = None

        simulation_records.append({
            "simulation_day": current_day,
            "patients_treated": len(treated_patients),
            "total_pfs_available": len(available_pfs),
            "biomarker_group": group,
            "group_pfs_count": count,
            "mean_pfs": mean,
            "pfs_sd": sd,
            "lower_boundary": lower_boundary,
            "upper_boundary": upper_boundary
        })


simulation_df = pd.DataFrame(simulation_records)

simulation_df.to_csv(
    f"data/simulation_history/simulation_history_batch_{batch_id}.csv",
    index=False
)

print(simulation_df.head(15))
print("\nSimulation history saved.")