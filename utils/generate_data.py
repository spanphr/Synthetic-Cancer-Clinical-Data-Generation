from scipy.stats import truncnorm
import numpy as np

def generate_patient():
    mean = 0.55
    sd = 0.25
    lower = 0.1
    upper = 1.0

    a = (lower - mean) / sd
    b = (upper - mean) / sd

    biomarker_a = truncnorm.rvs(
        a, b, loc=mean, scale=sd
    )

    if biomarker_a < 0.4:
        biomarker_group = "Low"
    elif biomarker_a < 0.7:
        biomarker_group = "Medium"
    else:
        biomarker_group = "High"

    if biomarker_group == "Low":
        pfs_mean = 180
        pfs_sd = 45
    elif biomarker_group == "Medium":
        pfs_mean = 270
        pfs_sd = 90
    else:
        pfs_mean = 360
        pfs_sd = 120

    pfs = round(
        np.random.normal(
            loc=pfs_mean,
            scale=pfs_sd
        )
    )

    return {
        "biomarker_a": round(biomarker_a, 4),
        "biomarker_group": biomarker_group,
        "pfs_days": pfs
    }


def generate_patients(batch_id, n=1000):

    np.random.seed( 22 + batch_id)

    patients = []

    for i in range(n):

        patient = generate_patient()

        patient_id = f"B{batch_id:03d}P{i + 1:04d}"
        treatment_day = i + 1

        pfs_available_day = (
            treatment_day + patient["pfs_days"]
        )

        patient["patient_id"] = patient_id
        patient["treatment_day"] = treatment_day
        patient["pfs_available_day"] = pfs_available_day

        patients.append(patient)

    return patients