# fitness_insights_with_pii.py
import random
import uuid
from datetime import date, timedelta

TODAY = date(2025, 8, 30)

FIRST_NAMES = [
    "Alex","Jordan","Taylor","Morgan","Casey","Riley","Sam","Avery","Jamie","Drew",
    "Cameron","Reese","Peyton","Quinn","Rowan","Logan","Harper","Skyler","Elliot","Blake"
]
LAST_NAMES = [
    "Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Martinez","Hernandez",
    "Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin","Lee"
]
STREET_NAMES = [
    "Oak","Maple","Pine","Cedar","Elm","Washington","Lake","Hill","Sunset","Riverview",
    "Cherry","Willow","Highland","Forest","Meadow"
]
STREET_TYPES = ["St","Ave","Blvd","Rd","Ln","Ct","Pl","Dr","Ter","Way"]
CITIES = [
    "Aurora","Boulder","Denver","Fort Collins","Provo","Salt Lake City","Boise","Phoenix",
    "Albuquerque","Las Vegas","Cheyenne","Idaho Falls","St. George","Missoula","Billings"
]
US_STATES = ["CO","UT","ID","AZ","NM","NV","WY","MT"]
EMAIL_DOMAINS = ["example.com","mail.com","demo.org","student.edu","sample.net"]

def _random_birthdate_for_age(age: int) -> date:
    # Pick a random birthday within the 12 months window that yields the given age as of TODAY.
    years_ago = TODAY.replace(year=TODAY.year - age)
    # Choose an offset from -364 to +0 days so that DOB stays within the last year window.
    offset_days = random.randint(-364, 0)
    return years_ago + timedelta(days=offset_days)

def _random_phone() -> str:
    # Simple NANP-like format; avoid 0/1 starts in area/exchange
    area = random.randint(201, 989)
    exch = random.randint(200, 999)
    line = random.randint(0, 9999)
    return f"({area}) {exch:03d}-{line:04d}"

def _random_zip() -> str:
    return f"{random.randint(80001, 99950)}"  # US 5-digit range; skewed high to avoid real mapping

def _make_email(first: str, last: str) -> str:
    token = "".join(c for c in (first + last) if c.isalpha()).lower()
    num = random.randint(1, 9999)
    domain = random.choice(EMAIL_DOMAINS)
    return f"{token}{num}@{domain}"

def _synthetic_pii(age: int):
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    email = _make_email(first, last)
    phone = _random_phone()
    street = f"{random.randint(100, 9899)} {random.choice(STREET_NAMES)} {random.choice(STREET_TYPES)}"
    city = random.choice(CITIES)
    state = random.choice(US_STATES)
    zip_code = _random_zip()
    birthdate = _random_birthdate_for_age(age)
    return {
        "respondent_id": str(uuid.uuid4()),
        "first_name": first,
        "last_name": last,
        "email": email,
        "phone": phone,
        "street_address": street,
        "city": city,
        "state": state,
        "zip": zip_code,
        "birthdate": birthdate.isoformat(),
    }

def generate_fitness_survey_data(n: int, seed: int | None = None):
    """
    Generate n rows of synthetic fitness insights survey data with PII.
    Returns (header, rows) where rows are lists aligned with the header.
    """
    if seed is not None:
        random.seed(seed)

    genders = ["Male", "Female"]
    workout_types = ["Cardio", "Strength", "Yoga", "Mixed"]
    injury_types = ["None", "Knee", "Back", "Shoulder", "Ankle"]

    header = [
        # PII
        "respondent_id","first_name","last_name","email","phone",
        "street_address","city","state","zip","birthdate",
        # Fitness fields
        "age","gender","weekly_workouts","preferred_workout",
        "past_injury","injury_type","joint_pain"
    ]
    rows = []

    for _ in range(n):
        age = random.randint(18, 65)
        gender = random.choice(genders)
        workouts = random.randint(0, 7)
        preferred = random.choice(workout_types)
        past_injury = random.choice([True, False])
        injury_type = random.choice(injury_types[1:]) if past_injury else "None"

        # Joint pain heuristic
        if age > 50 or workouts >= 6:
            joint_pain = (random.random() < 0.7)
        elif age < 30 and workouts <= 1:
            joint_pain = (random.random() < 0.2)
        else:
            joint_pain = (random.random() < 0.4)

        pii = _synthetic_pii(age)
        row = [
            pii["respondent_id"], pii["first_name"], pii["last_name"], pii["email"], pii["phone"],
            pii["street_address"], pii["city"], pii["state"], pii["zip"], pii["birthdate"],
            age, gender, workouts, preferred, past_injury, injury_type, joint_pain
        ]
        rows.append(row)

    return header, rows

if __name__ == "__main__":
    import csv

    hdr, data = generate_fitness_survey_data(100000, seed=42)
    output_file = "fitness_survey_data.csv"
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(hdr)
        writer.writerows(data)
    print(f"Wrote {len(data)} rows to {output_file}")
