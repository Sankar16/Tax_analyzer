from faker import Faker
import random
import json
import os

fake = Faker()
os.makedirs("../data/synthetic_json/linked", exist_ok=True)

def generate_linked_w2_1040(i):
    name = fake.name()
    ssn = fake.ssn()
    address = fake.address().replace("\n", ", ")

    # Income + withholding
    wages = round(random.uniform(40000, 150000), 2)
    federal_tax = round(wages * random.uniform(0.10, 0.20), 2)
    ss_wages = wages
    ss_tax = round(ss_wages * 0.062, 2)
    medicare_tax = round(wages * 0.0145, 2)
    state_wages = round(wages * 0.95, 2)
    state_tax = round(state_wages * 0.05, 2)

    # 1040-related values
    adjustments = round(random.uniform(0, 10000), 2)
    std_deduction = 14600  # single filer
    taxable_income = max(0, wages - adjustments - std_deduction)
    tax = round(taxable_income * 0.12, 2)  # simple 12% estimate
    refund = max(federal_tax - tax, 0)

    # Shared user fields
    user = {
        "name": name,
        "ssn": ssn,
        "address": address
    }

    # W-2 structure
    w2 = {
        **user,
        "employer_name": fake.company(),
        "employer_ein": f"{random.randint(10, 99)}-{random.randint(1000000, 9999999)}",
        "employer_address": fake.address().replace("\n", ", "),
        "wages": wages,
        "federal_tax": federal_tax,
        "ss_wages": ss_wages,
        "ss_tax": ss_tax,
        "medicare_tax": medicare_tax,
        "state": fake.state_abbr(),
        "state_wages": state_wages,
        "state_tax": state_tax,
        "year": 2023
    }

    # 1040 structure
    form_1040 = {
        **user,
        "filing_status": "Single",
        "gross_income": wages,
        "adjustments": adjustments,
        "taxable_income": taxable_income,
        "tax": tax,
        "withholding": federal_tax,
        "refund": refund,
        "year": 2023
    }

    # Save to disk
    with open(f"../data/synthetic_json/linked/w2_{i}.json", "w") as f:
        json.dump(w2, f, indent=2)

    with open(f"../data/synthetic_json/linked/1040_{i}.json", "w") as f:
        json.dump(form_1040, f, indent=2)

# Generate 100 linked records
for i in range(100):
    generate_linked_w2_1040(i)