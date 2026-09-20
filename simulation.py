import pandas as pd

df = pd.read_csv("synthetic_patients.csv")

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

    if len(available_pfs) > 0:

        group_stats = (
            available_pfs
            .groupby("biomarker_group")["pfs_days"]
            .agg(["count", "mean", "std"])
        )

        group_stats["lower_boundary"] = (
            group_stats["mean"] - 2 * group_stats["std"]
        )

        group_stats["upper_boundary"] = (
            group_stats["mean"] + 2 * group_stats["std"]
        )

        for group, stats in group_stats.iterrows():

            simulation_records.append({
                "simulation_day": current_day,
                "patients_treated": len(treated_patients),
                "total_pfs_available": len(available_pfs),
                "biomarker_group": group,
                "group_pfs_count": stats["count"],
                "mean_pfs": stats["mean"],
                "pfs_sd": stats["std"],
                "lower_boundary": stats["lower_boundary"],
                "upper_boundary": stats["upper_boundary"]
            })


# OUTSIDE the loop
simulation_df = pd.DataFrame(simulation_records)

simulation_df.to_csv(
    "simulation_history.csv",
    index=False
)

print(simulation_df.head())

print("\nSimulation history saved.")