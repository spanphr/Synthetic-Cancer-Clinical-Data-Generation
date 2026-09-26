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
    # Their final PFS outcome is now available to the dashboard
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

        # ----------------------------------------------
        # Treated patients in this group
        # ----------------------------------------------

        group_treated = treated_patients[
            treated_patients["biomarker_group"] == group
        ]

        group_patients_treated = len(group_treated)


        # ----------------------------------------------
        # Available / elapsed PFS outcomes for this group
        # ----------------------------------------------

        group_available_pfs = available_pfs[
            available_pfs["biomarker_group"] == group
        ]

        group_data = group_available_pfs["pfs_days"]

        group_pfs_count = len(group_data)


        # ----------------------------------------------
        # Mean PFS
        # ----------------------------------------------

        if group_pfs_count > 0:
            mean = group_data.mean()
        else:
            mean = None


        # ----------------------------------------------
        # Standard deviation and ±2 SD boundaries
        # ----------------------------------------------

        # At least two observations are required
        # to calculate sample standard deviation.

        if group_pfs_count > 1:

            sd = group_data.std()

            lower_boundary = mean - 2 * sd
            upper_boundary = mean + 2 * sd

        else:

            sd = None
            lower_boundary = None
            upper_boundary = None


        # ----------------------------------------------
        # Best ELAPSED PFS
        # ----------------------------------------------

        # Among patients in this biomarker group whose
        # PFS endpoint has already occurred, find the
        # highest completed PFS observed so far.

        if group_pfs_count > 0:

            best_elapsed_pfs = int(
                group_available_pfs["pfs_days"].max()
            )

        else:

            best_elapsed_pfs = None


        # ----------------------------------------------
        # Patients with ONGOING PFS
        # ----------------------------------------------

        # A patient is ongoing if:
        #
        # 1. They have already received treatment.
        # 2. Their PFS endpoint has NOT yet occurred.
        #
        # We do not reveal their eventual generated
        # PFS value here.

        group_ongoing = df[
            (df["treatment_day"] <= current_day) &
            (df["pfs_available_day"] > current_day) &
            (df["biomarker_group"] == group)
        ].copy()


        # ----------------------------------------------
        # Best ONGOING PFS
        # ----------------------------------------------

        if len(group_ongoing) > 0:

            # Calculate how long each patient has remained
            # progression-free up to the current day.

            group_ongoing["ongoing_pfs_days"] = (
                current_day -
                group_ongoing["treatment_day"]
            )

            # Find the longest ongoing PFS duration
            # within this biomarker group.

            best_ongoing_pfs = int(
                group_ongoing["ongoing_pfs_days"].max()
            )

        else:

            best_ongoing_pfs = None


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
            "upper_boundary": upper_boundary,

            # Best PFS comparison
            "best_elapsed_pfs": best_elapsed_pfs,
            "best_ongoing_pfs": best_ongoing_pfs
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


print("\nFinal best PFS values by Biomarker-A group:")

final_day_data = simulation_df[
    simulation_df["simulation_day"] == final_day
][
    [
        "biomarker_group",
        "best_elapsed_pfs",
        "best_ongoing_pfs"
    ]
]

print(final_day_data)


print("\nSimulation history saved to:")
print(output_path)