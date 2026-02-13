"""
Script to add more patients via API to demonstrate pagination.
This can be run locally and will add patients directly to the Railway database.
"""
import requests
from datetime import date, timedelta
import random

API_URL = "https://cerula-care-production.up.railway.app"

# Additional patients to add (beyond the existing 10)
additional_patients = [
    {
        "first_name": "Christopher",
        "last_name": "White",
        "date_of_birth": "1987-03-12",
        "email": "christopher.white@email.com",
        "phone": "555-1011",
        "address": "852 Cherry St, Downtown, ST 77777",
        "enrollment_date": "2024-01-08",
        "status": "active",
        "care_program": "Behavioral Health Program"
    },
    {
        "first_name": "Amanda",
        "last_name": "Harris",
        "date_of_birth": "1991-07-22",
        "email": "amanda.harris@email.com",
        "phone": "555-1012",
        "address": "963 Walnut Ave, Uptown, ST 88888",
        "enrollment_date": "2023-12-15",
        "status": "active",
        "care_program": "Chronic Care Management"
    },
    {
        "first_name": "Daniel",
        "last_name": "Martin",
        "date_of_birth": "1984-11-05",
        "email": "daniel.martin@email.com",
        "phone": "555-1013",
        "address": "147 Oakwood Dr, Midtown, ST 99999",
        "enrollment_date": "2024-03-05",
        "status": "active",
        "care_program": "Wellness Program"
    },
    {
        "first_name": "Jennifer",
        "last_name": "Thompson",
        "date_of_birth": "1989-04-18",
        "email": "jennifer.thompson@email.com",
        "phone": "555-1014",
        "address": "258 Riverside Blvd, Waterfront, ST 10101",
        "enrollment_date": "2024-02-22",
        "status": "inactive",
        "care_program": "Behavioral Health Program"
    },
    {
        "first_name": "Michael",
        "last_name": "Garcia",
        "date_of_birth": "1979-09-30",
        "email": "michael.garcia@email.com",
        "phone": "555-1015",
        "address": "369 Parkview Ln, Greenway, ST 20202",
        "enrollment_date": "2023-11-20",
        "status": "active",
        "care_program": "Chronic Care Management"
    },
    {
        "first_name": "Sarah",
        "last_name": "Martinez",
        "date_of_birth": "1994-01-14",
        "email": "sarah.martinez@email.com",
        "phone": "555-1016",
        "address": "741 Hillcrest Rd, Highlands, ST 30303",
        "enrollment_date": "2024-04-01",
        "status": "active",
        "care_program": "Wellness Program"
    },
    {
        "first_name": "David",
        "last_name": "Robinson",
        "date_of_birth": "1986-06-28",
        "email": "david.robinson@email.com",
        "phone": "555-1017",
        "address": "852 Valley View Ct, Hillside, ST 40404",
        "enrollment_date": "2023-10-10",
        "status": "active",
        "care_program": "Behavioral Health Program"
    },
    {
        "first_name": "Emily",
        "last_name": "Clark",
        "date_of_birth": "1992-12-08",
        "email": "emily.clark@email.com",
        "phone": "555-1018",
        "address": "963 Sunset Blvd, Westside, ST 50505",
        "enrollment_date": "2024-01-30",
        "status": "active",
        "care_program": "Chronic Care Management"
    },
    {
        "first_name": "James",
        "last_name": "Rodriguez",
        "date_of_birth": "1981-05-19",
        "email": "james.rodriguez@email.com",
        "phone": "555-1019",
        "address": "147 Mountain View Dr, Northside, ST 60606",
        "enrollment_date": "2023-09-25",
        "status": "discharged",
        "care_program": "Behavioral Health Program"
    },
    {
        "first_name": "Jessica",
        "last_name": "Lewis",
        "date_of_birth": "1988-08-03",
        "email": "jessica.lewis@email.com",
        "phone": "555-1020",
        "address": "258 Lakeview Ave, Lakeside, ST 70707",
        "enrollment_date": "2024-02-14",
        "status": "active",
        "care_program": "Wellness Program"
    },
    {
        "first_name": "Matthew",
        "last_name": "Lee",
        "date_of_birth": "1983-02-25",
        "email": "matthew.lee@email.com",
        "phone": "555-1021",
        "address": "369 Forest Park Way, Woodland, ST 80808",
        "enrollment_date": "2024-03-28",
        "status": "active",
        "care_program": "Chronic Care Management"
    },
    {
        "first_name": "Ashley",
        "last_name": "Walker",
        "date_of_birth": "1990-10-11",
        "email": "ashley.walker@email.com",
        "phone": "555-1022",
        "address": "741 Meadowbrook Ln, Meadowlands, ST 90909",
        "enrollment_date": "2023-12-05",
        "status": "active",
        "care_program": "Behavioral Health Program"
    },
    {
        "first_name": "Andrew",
        "last_name": "Hall",
        "date_of_birth": "1985-07-17",
        "email": "andrew.hall@email.com",
        "phone": "555-1023",
        "address": "852 Spring Garden St, Gardenview, ST 01010",
        "enrollment_date": "2024-04-10",
        "status": "active",
        "care_program": "Wellness Program"
    },
    {
        "first_name": "Lauren",
        "last_name": "Allen",
        "date_of_birth": "1993-03-29",
        "email": "lauren.allen@email.com",
        "phone": "555-1024",
        "address": "963 Brookside Dr, Brookside, ST 11111",
        "enrollment_date": "2024-01-18",
        "status": "inactive",
        "care_program": "Chronic Care Management"
    },
    {
        "first_name": "Ryan",
        "last_name": "Young",
        "date_of_birth": "1987-09-06",
        "email": "ryan.young@email.com",
        "phone": "555-1025",
        "address": "147 Countryside Rd, Countryside, ST 12121",
        "enrollment_date": "2023-11-12",
        "status": "active",
        "care_program": "Behavioral Health Program"
    },
    {
        "first_name": "Nicole",
        "last_name": "King",
        "date_of_birth": "1991-01-23",
        "email": "nicole.king@email.com",
        "phone": "555-1026",
        "address": "258 Fairview Ave, Fairview, ST 13131",
        "enrollment_date": "2024-02-28",
        "status": "active",
        "care_program": "Wellness Program"
    },
    {
        "first_name": "Kevin",
        "last_name": "Wright",
        "date_of_birth": "1982-06-15",
        "email": "kevin.wright@email.com",
        "phone": "555-1027",
        "address": "369 Bridgewater St, Bridgewater, ST 14141",
        "enrollment_date": "2024-03-15",
        "status": "active",
        "care_program": "Chronic Care Management"
    },
    {
        "first_name": "Michelle",
        "last_name": "Lopez",
        "date_of_birth": "1989-11-02",
        "email": "michelle.lopez@email.com",
        "phone": "555-1028",
        "address": "741 Stonebridge Way, Stonebridge, ST 15151",
        "enrollment_date": "2023-10-28",
        "status": "active",
        "care_program": "Behavioral Health Program"
    },
    {
        "first_name": "Brandon",
        "last_name": "Hill",
        "date_of_birth": "1984-04-09",
        "email": "brandon.hill@email.com",
        "phone": "555-1029",
        "address": "852 Windmill Dr, Windmill, ST 16161",
        "enrollment_date": "2024-01-05",
        "status": "discharged",
        "care_program": "Wellness Program"
    },
]

def add_patients():
    """Add patients via API"""
    added = 0
    skipped = 0
    
    for patient_data in additional_patients:
        try:
            response = requests.post(f"{API_URL}/api/patients", json=patient_data)
            if response.status_code == 201:
                added += 1
                print(f"✓ Added {patient_data['first_name']} {patient_data['last_name']}")
            elif response.status_code == 400 and "already registered" in response.text:
                skipped += 1
                print(f"⊘ Skipped {patient_data['first_name']} {patient_data['last_name']} (already exists)")
            else:
                print(f"✗ Failed to add {patient_data['first_name']} {patient_data['last_name']}: {response.status_code} - {response.text[:100]}")
        except Exception as e:
            print(f"✗ Error adding {patient_data['first_name']} {patient_data['last_name']}: {e}")
    
    print(f"\n✓ Added {added} patients, skipped {skipped} (already exist)")
    
    # Check final count
    count_response = requests.get(f"{API_URL}/api/patients/count")
    if count_response.status_code == 200:
        total = count_response.json()["count"]
        print(f"✓ Total patients in database: {total}")

if __name__ == "__main__":
    add_patients()
