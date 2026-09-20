import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

df = pd.read_csv("synthetic_patients.csv")

groups = {
    "Low": {"mean": 180, "sd": 45},
    "Medium": {"mean": 270, "sd": 90},
    "High": {"mean": 360, "sd": 120}
}

for group, params in groups.items():

    data = df[df["biomarker_group"] == group]["pfs_days"]

    print(f"\n{group} group")
    print(f"Number of patients: {len(data)}")
    print(f"Expected mean: {params['mean']}")
    print(f"Generated mean: {data.mean():.2f}")
    print(f"Expected SD: {params['sd']}")
    print(f"Generated SD: {data.std():.2f}")

    # Histogram of generated patients
    plt.hist(
        data,
        bins=20,
        density=True,
        alpha=0.6,
        label="Generated PFS"
    )

    # Create x-values for expected normal curve
    x = np.linspace(
        data.min(),
        data.max(),
        200
    )

    # Expected normal distribution
    y = norm.pdf(
        x,
        loc=params["mean"],
        scale=params["sd"]
    )

    # Plot expected curve
    plt.plot(
        x,
        y,
        linewidth=2,
        label="Expected Normal Distribution"
    )

    plt.axvline(
        params["mean"],
        linestyle="--",
        label=f"Expected Mean = {params['mean']}"
    )

    plt.title(f"{group} Biomarker Group - PFS Distribution")
    plt.xlabel("PFS (days)")
    plt.ylabel("Density")
    plt.legend()

    plt.show()