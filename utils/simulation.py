import pandas as pd

# --------------------------------------------------
# 1. Select which synthetic batch to simulate
# --------------------------------------------------

batch_id = 1

df = pd.read_csv(
    f"data/synthetic_patients/synthetic_patients_batch_{batch_id}.csv"
)


# --------------------------------------------------
# 2. Determine how long the simulation must run
# --------------------------------------------------
# Treatment happens for 1,000 days, but some patients'
# PFS outcomes become available after Day 1000.
# Therefore, we continue until the final PFS has elapsed.

final_day = int(df["pfs_available_day"].max())


# --------------------------------------------------
# 3. Store the dashboard state for every simulation day
# --------------------------------------------------

simulation_records = []

groups = ["Low", "Medium", "High"]


# --------------------------------------------------
# 4. Simulate one day at a time
# --------------------------------------------------

for current_day in range(1, final_day + 1):

    # All patients who have been treated by this day
    treated_patients = df[
        df["treatment_day"] <= current_day
    ]

    # Only patients whose PFS period has elapsed
    # Their PFS is now allowed to appear on the dashboard
    available_pfs = df[
        df["pfs_available_day"] <= current_day
    ]

    print(
        "\nDay:", current_day,
        "| Patients treated:", len(treated_patients),
        "| PFS available:", len(available_pfs)
    )


    # --------------------------------------------------
    # 5. Calculate statistics for each Biomarker-A group
    # --------------------------------------------------

    for group in groups:

        # Number of treated patients belonging to this group
        group_treated = treated_patients[
            treated_patients["biomarker_group"] == group
        ]

        group_patients_treated = len(group_treated)


        # PFS outcomes that are AVAILABLE for this group
        group_data = available_pfs[
            available_pfs["biomarker_group"] == group
        ]["pfs_days"]

        group_pfs_count = len(group_data)


        # Mean PFS
        if group_pfs_count > 0:
            mean = group_data.mean()
        else:
            mean = None


        # Standard deviation and ±2 SD boundaries
        # We need at least 2 observations to calculate sample SD.
        if group_pfs_count > 1:
            sd = group_data.std()

            lower_boundary = mean - 2 * sd
            upper_boundary = mean + 2 * sd

        else:
            sd = None
            lower_boundary = None
            upper_boundary = None


        # --------------------------------------------------
        # 6. Save this group's state for the current day
        # --------------------------------------------------

        simulation_records.append({
            "simulation_day": current_day,

            # Overall monitoring statistics
            "patients_treated": len(treated_patients),
            "total_pfs_available": len(available_pfs),

            # Biomarker group
            "biomarker_group": group,

            # Group-specific monitoring statistics
            "group_patients_treated": group_patients_treated,
            "group_pfs_count": group_pfs_count,

            # PFS statistics using ONLY available outcomes
            "mean_pfs": mean,
            "pfs_sd": sd,
            "lower_boundary": lower_boundary,
            "upper_boundary": upper_boundary
        })


# --------------------------------------------------
# 7. Convert simulation history to DataFrame
# --------------------------------------------------

simulation_df = pd.DataFrame(simulation_records)


# --------------------------------------------------
# 8. Save simulation history
# --------------------------------------------------

output_path = (
    f"data/simulation_history/"
    f"simulation_history_batch_{batch_id}.csv"
)

simulation_df.to_csv(
    output_path,
    index=False
)


# --------------------------------------------------
# 9. Quick validation
# --------------------------------------------------

print("\nFirst 15 rows:")
print(simulation_df.head(15))

print("\nFinal simulation day:", final_day)

print(
    "Final patients treated:",
    simulation_df["patients_treated"].max()
)

print(
    "Final PFS outcomes available:",
    simulation_df["total_pfs_available"].max()
)

print("\nSimulation history saved to:")
print(output_path)