import random
from datetime import date, timedelta
import pandas as pd

random.seed(42)

OUTPUT_DIR = "data"

# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def random_date(start_year=2020, end_year=2026):
    start = date(start_year, 1, 1)
    end = date(end_year, 8, 21)
    days = (end - start).days
    return start + timedelta(days=random.randint(0, days))


# --------------------------------------------------
# 1. MEMBERS
# --------------------------------------------------

first_names = [
    "Ravi", "Anita", "Rajesh", "Priya", "Suresh",
    "Kiran", "Arun", "Meena", "John", "David",
    "Sarah", "Michael", "Neha", "Rahul", "Sneha"
]

last_names = [
    "Kumar", "Sharma", "Reddy", "Patel", "Smith",
    "Williams", "Johnson", "Rao", "Verma", "Singh"
]

cities_states = [
    ("Hyderabad", "TS"),
    ("Warangal", "TS"),
    ("Karimnagar", "TS"),
    ("Vijayawada", "AP"),
    ("Visakhapatnam", "AP"),
    ("Bangalore", "KA"),
    ("Chennai", "TN"),
    ("Dallas", "TX"),
    ("Houston", "TX"),
    ("Chicago", "IL")
]

members = []

for i in range(1, 10001):
    member_id = f"M{i:06d}"

    first = random.choice(first_names)
    last = random.choice(last_names)

    city, state = random.choice(cities_states)

    dob = random_date(1950, 2002)
    effective_date = random_date(2022, 2026)

    status = random.choices(
        ["ACTIVE", "TERMINATED"],
        weights=[85, 15]
    )[0]

    termination_date = None

    if status == "TERMINATED":
        termination_date = effective_date + timedelta(
            days=random.randint(100, 1000)
        )

    members.append({
        "member_id": member_id,
        "member_name": f"{first} {last}",
        "date_of_birth": dob,
        "gender": random.choice(["M", "F"]),
        "city": city,
        "state": state,
        "member_status": status,
        "effective_date": effective_date,
        "termination_date": termination_date
    })

members_df = pd.DataFrame(members)


# --------------------------------------------------
# Inject bad member records
# --------------------------------------------------

# Null member ID
members_df.loc[10, "member_id"] = None

# Duplicate member ID
members_df.loc[20, "member_id"] = members_df.loc[21, "member_id"]

# Invalid status
members_df.loc[30, "member_status"] = "UNKNOWN"


# --------------------------------------------------
# 2. PROVIDERS
# --------------------------------------------------

providers = []

provider_types = [
    "HOSPITAL",
    "CLINIC",
    "PHYSICIAN",
    "PHARMACY"
]

specialties = [
    "CARDIOLOGY",
    "ORTHOPEDICS",
    "PEDIATRICS",
    "GENERAL_MEDICINE",
    "NEUROLOGY",
    "ONCOLOGY"
]

for i in range(1, 1001):
    provider_id = f"P{i:05d}"

    city, state = random.choice(cities_states)

    providers.append({
        "provider_id": provider_id,
        "provider_name": f"Provider_{i}",
        "provider_type": random.choice(provider_types),
        "specialty": random.choice(specialties),
        "city": city,
        "state": state
    })

providers_df = pd.DataFrame(providers)


# --------------------------------------------------
# 3. ENROLLMENT
# --------------------------------------------------

enrollments = []

coverage_types = [
    "INDIVIDUAL",
    "FAMILY",
    "SPOUSE",
    "CHILD"
]

for i in range(1, 15001):

    member_id = f"M{random.randint(1, 10000):06d}"

    effective_date = random_date(2023, 2026)

    status = random.choices(
        ["ACTIVE", "TERMINATED"],
        weights=[80, 20]
    )[0]

    termination_date = None

    if status == "TERMINATED":
        termination_date = effective_date + timedelta(
            days=random.randint(30, 800)
        )

    enrollments.append({
        "enrollment_id": f"E{i:06d}",
        "member_id": member_id,
        "plan_id": f"PLAN{random.randint(1, 10):03d}",
        "coverage_type": random.choice(coverage_types),
        "effective_date": effective_date,
        "termination_date": termination_date,
        "status": status
    })

enrollment_df = pd.DataFrame(enrollments)


# --------------------------------------------------
# 4. CLAIMS
# --------------------------------------------------

claims = []

claim_statuses = [
    "APPROVED",
    "PENDING",
    "REJECTED"
]

for i in range(1, 50001):

    member_id = f"M{random.randint(1, 10000):06d}"
    provider_id = f"P{random.randint(1, 1000):05d}"

    claims.append({
        "claim_id": f"C{i:07d}",
        "member_id": member_id,
        "provider_id": provider_id,
        "service_date": random_date(2024, 2026),
        "claim_amount": round(random.uniform(50, 10000), 2),
        "claim_status": random.choice(claim_statuses)
    })

claims_df = pd.DataFrame(claims)


# --------------------------------------------------
# Inject bad claims
# --------------------------------------------------

# Invalid claim amount
claims_df.loc[100, "claim_amount"] = "INVALID"

# Missing member
claims_df.loc[200, "member_id"] = None

# Duplicate claim
claims_df.loc[300, "claim_id"] = claims_df.loc[301, "claim_id"]


# --------------------------------------------------
# Write files
# --------------------------------------------------

import os

os.makedirs(OUTPUT_DIR, exist_ok=True)

members_df.to_csv(
    f"{OUTPUT_DIR}/members.csv",
    index=False
)

enrollment_df.to_csv(
    f"{OUTPUT_DIR}/enrollment.csv",
    index=False
)

providers_df.to_csv(
    f"{OUTPUT_DIR}/providers.csv",
    index=False
)

claims_df.to_csv(
    f"{OUTPUT_DIR}/claims.csv",
    index=False
)


# --------------------------------------------------
# Summary
# --------------------------------------------------

print("Healthcare source data generated successfully.")
print()

print(f"Members     : {len(members_df):,}")
print(f"Enrollment  : {len(enrollment_df):,}")
print(f"Providers   : {len(providers_df):,}")
print(f"Claims      : {len(claims_df):,}")

print()
print("Files created in ./data/")
