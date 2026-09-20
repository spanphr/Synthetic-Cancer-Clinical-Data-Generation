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
        a,
        b,
        loc=mean,
        scale=sd
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

    pfs = round(np.random.normal(
        loc=pfs_mean,
        scale=pfs_sd
    ),0)

    return {
    "biomarker_a": round(biomarker_a, 4),
    "biomarker_group": biomarker_group,
    "pfs_days": pfs
    }

def generate_patients(n=1000):
    patients = []

    for i in range(n):
        patient = generate_patient()
        patients.append(patient)

    return patients

