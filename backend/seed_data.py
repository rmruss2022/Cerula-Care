"""
Seed script to populate the database with sample data.
Run this script after setting up the database to populate it with test data.
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app import models
from datetime import date, timedelta
import random

# Create tables
Base.metadata.create_all(bind=engine)


def seed_care_team_members(db: Session):
    """Seed care team members"""
    care_team_members = [
        {
            "first_name": "Sarah",
            "last_name": "Johnson",
            "email": "sarah.johnson@cerula.com",
            "phone": "555-0101",
            "role": models.CareTeamRole.HEALTH_COACH
        },
        {
            "first_name": "Michael",
            "last_name": "Chen",
            "email": "michael.chen@cerula.com",
            "phone": "555-0102",
            "role": models.CareTeamRole.HEALTH_COACH
        },
        {
            "first_name": "Emily",
            "last_name": "Rodriguez",
            "email": "emily.rodriguez@cerula.com",
            "phone": "555-0103",
            "role": models.CareTeamRole.HEALTH_COACH
        },
        {
            "first_name": "David",
            "last_name": "Williams",
            "email": "david.williams@cerula.com",
            "phone": "555-0201",
            "role": models.CareTeamRole.BHCM
        },
        {
            "first_name": "Jessica",
            "last_name": "Martinez",
            "email": "jessica.martinez@cerula.com",
            "phone": "555-0202",
            "role": models.CareTeamRole.BHCM
        },
        {
            "first_name": "Dr. Robert",
            "last_name": "Anderson",
            "email": "robert.anderson@cerula.com",
            "phone": "555-0301",
            "role": models.CareTeamRole.PSYCHIATRIST
        },
        {
            "first_name": "Dr. Lisa",
            "last_name": "Thompson",
            "email": "lisa.thompson@cerula.com",
            "phone": "555-0302",
            "role": models.CareTeamRole.PSYCHIATRIST
        },
    ]
    
    for member_data in care_team_members:
        existing = db.query(models.CareTeamMember).filter(
            models.CareTeamMember.email == member_data["email"]
        ).first()
        if not existing:
            db_member = models.CareTeamMember(**member_data)
            db.add(db_member)
    
    db.commit()
    print("✓ Seeded care team members")


def seed_patients(db: Session):
    """Seed patients"""
    patients_data = [
        {
            "first_name": "John",
            "last_name": "Smith",
            "date_of_birth": date(1985, 3, 15),
            "email": "john.smith@email.com",
            "phone": "555-1001",
            "address": "123 Main St, Anytown, ST 12345",
            "enrollment_date": date(2024, 1, 10),
            "status": models.PatientStatus.ACTIVE,
            "care_program": "Behavioral Health Program"
        },
        {
            "first_name": "Jane",
            "last_name": "Doe",
            "date_of_birth": date(1990, 7, 22),
            "email": "jane.doe@email.com",
            "phone": "555-1002",
            "address": "456 Oak Ave, Somewhere, ST 67890",
            "enrollment_date": date(2024, 2, 5),
            "status": models.PatientStatus.ACTIVE,
            "care_program": "Chronic Care Management"
        },
        {
            "first_name": "Robert",
            "last_name": "Brown",
            "date_of_birth": date(1978, 11, 8),
            "email": "robert.brown@email.com",
            "phone": "555-1003",
            "address": "789 Pine Rd, Elsewhere, ST 54321",
            "enrollment_date": date(2023, 12, 1),
            "status": models.PatientStatus.ACTIVE,
            "care_program": "Behavioral Health Program"
        },
        {
            "first_name": "Maria",
            "last_name": "Garcia",
            "date_of_birth": date(1992, 5, 30),
            "email": "maria.garcia@email.com",
            "phone": "555-1004",
            "address": "321 Elm St, Nowhere, ST 98765",
            "enrollment_date": date(2024, 3, 20),
            "status": models.PatientStatus.ACTIVE,
            "care_program": "Wellness Program"
        },
        {
            "first_name": "James",
            "last_name": "Wilson",
            "date_of_birth": date(1982, 9, 14),
            "email": "james.wilson@email.com",
            "phone": "555-1005",
            "address": "654 Maple Dr, Anywhere, ST 11111",
            "enrollment_date": date(2023, 11, 15),
            "status": models.PatientStatus.INACTIVE,
            "care_program": "Behavioral Health Program"
        },
        {
            "first_name": "Patricia",
            "last_name": "Moore",
            "date_of_birth": date(1988, 2, 28),
            "email": "patricia.moore@email.com",
            "phone": "555-1006",
            "address": "987 Cedar Ln, Someplace, ST 22222",
            "enrollment_date": date(2023, 10, 1),
            "status": models.PatientStatus.DISCHARGED,
            "care_program": "Chronic Care Management"
        },
        {
            "first_name": "William",
            "last_name": "Taylor",
            "date_of_birth": date(1975, 12, 5),
            "email": "william.taylor@email.com",
            "phone": "555-1007",
            "address": "147 Birch Way, Otherplace, ST 33333",
            "enrollment_date": date(2024, 4, 12),
            "status": models.PatientStatus.ACTIVE,
            "care_program": "Wellness Program"
        },
        {
            "first_name": "Linda",
            "last_name": "Anderson",
            "date_of_birth": date(1995, 6, 18),
            "email": "linda.anderson@email.com",
            "phone": "555-1008",
            "address": "258 Spruce Ct, Anotherplace, ST 44444",
            "enrollment_date": date(2024, 1, 25),
            "status": models.PatientStatus.ACTIVE,
            "care_program": "Behavioral Health Program"
        },
        {
            "first_name": "Richard",
            "last_name": "Thomas",
            "date_of_birth": date(1980, 4, 9),
            "email": "richard.thomas@email.com",
            "phone": "555-1009",
            "address": "369 Willow St, Yonder, ST 55555",
            "enrollment_date": date(2023, 9, 10),
            "status": models.PatientStatus.ACTIVE,
            "care_program": "Chronic Care Management"
        },
        {
            "first_name": "Barbara",
            "last_name": "Jackson",
            "date_of_birth": date(1993, 8, 25),
            "email": "barbara.jackson@email.com",
            "phone": "555-1010",
            "address": "741 Aspen Ave, Beyond, ST 66666",
            "enrollment_date": date(2024, 2, 18),
            "status": models.PatientStatus.ACTIVE,
            "care_program": "Wellness Program"
        },
        {
            "first_name": "Christopher",
            "last_name": "White",
            "date_of_birth": date(1987, 3, 12),
            "email": "christopher.white@email.com",
            "phone": "555-1011",
            "address": "852 Cherry St, Downtown, ST 77777",
            "enrollment_date": date(2024, 1, 8),
            "status": models.PatientStatus.ACTIVE,
            "care_program": "Behavioral Health Program"
        },
        {
            "first_name": "Amanda",
            "last_name": "Harris",
            "date_of_birth": date(1991, 7, 22),
            "email": "amanda.harris@email.com",
            "phone": "555-1012",
            "address": "963 Walnut Ave, Uptown, ST 88888",
            "enrollment_date": date(2023, 12, 15),
            "status": models.PatientStatus.ACTIVE,
            "care_program": "Chronic Care Management"
        },
        {
            "first_name": "Daniel",
            "last_name": "Martin",
            "date_of_birth": date(1984, 11, 5),
            "email": "daniel.martin@email.com",
            "phone": "555-1013",
            "address": "147 Oakwood Dr, Midtown, ST 99999",
            "enrollment_date": date(2024, 3, 5),
            "status": models.PatientStatus.ACTIVE,
            "care_program": "Wellness Program"
        },
        {
            "first_name": "Jennifer",
            "last_name": "Thompson",
            "date_of_birth": date(1989, 4, 18),
            "email": "jennifer.thompson@email.com",
            "phone": "555-1014",
            "address": "258 Riverside Blvd, Waterfront, ST 10101",
            "enrollment_date": date(2024, 2, 22),
            "status": models.PatientStatus.INACTIVE,
            "care_program": "Behavioral Health Program"
        },
        {
            "first_name": "Michael",
            "last_name": "Garcia",
            "date_of_birth": date(1979, 9, 30),
            "email": "michael.garcia@email.com",
            "phone": "555-1015",
            "address": "369 Parkview Ln, Greenway, ST 20202",
            "enrollment_date": date(2023, 11, 20),
            "status": models.PatientStatus.ACTIVE,
            "care_program": "Chronic Care Management"
        },
        {
            "first_name": "Sarah",
            "last_name": "Martinez",
            "date_of_birth": date(1994, 1, 14),
            "email": "sarah.martinez@email.com",
            "phone": "555-1016",
            "address": "741 Hillcrest Rd, Highlands, ST 30303",
            "enrollment_date": date(2024, 4, 1),
            "status": models.PatientStatus.ACTIVE,
            "care_program": "Wellness Program"
        },
        {
            "first_name": "David",
            "last_name": "Robinson",
            "date_of_birth": date(1986, 6, 28),
            "email": "david.robinson@email.com",
            "phone": "555-1017",
            "address": "852 Valley View Ct, Hillside, ST 40404",
            "enrollment_date": date(2023, 10, 10),
            "status": models.PatientStatus.ACTIVE,
            "care_program": "Behavioral Health Program"
        },
        {
            "first_name": "Emily",
            "last_name": "Clark",
            "date_of_birth": date(1992, 12, 8),
            "email": "emily.clark@email.com",
            "phone": "555-1018",
            "address": "963 Sunset Blvd, Westside, ST 50505",
            "enrollment_date": date(2024, 1, 30),
            "status": models.PatientStatus.ACTIVE,
            "care_program": "Chronic Care Management"
        },
        {
            "first_name": "James",
            "last_name": "Rodriguez",
            "date_of_birth": date(1981, 5, 19),
            "email": "james.rodriguez@email.com",
            "phone": "555-1019",
            "address": "147 Mountain View Dr, Northside, ST 60606",
            "enrollment_date": date(2023, 9, 25),
            "status": models.PatientStatus.DISCHARGED,
            "care_program": "Behavioral Health Program"
        },
        {
            "first_name": "Jessica",
            "last_name": "Lewis",
            "date_of_birth": date(1988, 8, 3),
            "email": "jessica.lewis@email.com",
            "phone": "555-1020",
            "address": "258 Lakeview Ave, Lakeside, ST 70707",
            "enrollment_date": date(2024, 2, 14),
            "status": models.PatientStatus.ACTIVE,
            "care_program": "Wellness Program"
        },
        {
            "first_name": "Matthew",
            "last_name": "Lee",
            "date_of_birth": date(1983, 2, 25),
            "email": "matthew.lee@email.com",
            "phone": "555-1021",
            "address": "369 Forest Park Way, Woodland, ST 80808",
            "enrollment_date": date(2024, 3, 28),
            "status": models.PatientStatus.ACTIVE,
            "care_program": "Chronic Care Management"
        },
        {
            "first_name": "Ashley",
            "last_name": "Walker",
            "date_of_birth": date(1990, 10, 11),
            "email": "ashley.walker@email.com",
            "phone": "555-1022",
            "address": "741 Meadowbrook Ln, Meadowlands, ST 90909",
            "enrollment_date": date(2023, 12, 5),
            "status": models.PatientStatus.ACTIVE,
            "care_program": "Behavioral Health Program"
        },
        {
            "first_name": "Andrew",
            "last_name": "Hall",
            "date_of_birth": date(1985, 7, 17),
            "email": "andrew.hall@email.com",
            "phone": "555-1023",
            "address": "852 Spring Garden St, Gardenview, ST 01010",
            "enrollment_date": date(2024, 4, 10),
            "status": models.PatientStatus.ACTIVE,
            "care_program": "Wellness Program"
        },
        {
            "first_name": "Lauren",
            "last_name": "Allen",
            "date_of_birth": date(1993, 3, 29),
            "email": "lauren.allen@email.com",
            "phone": "555-1024",
            "address": "963 Brookside Dr, Brookside, ST 11111",
            "enrollment_date": date(2024, 1, 18),
            "status": models.PatientStatus.INACTIVE,
            "care_program": "Chronic Care Management"
        },
        {
            "first_name": "Ryan",
            "last_name": "Young",
            "date_of_birth": date(1987, 9, 6),
            "email": "ryan.young@email.com",
            "phone": "555-1025",
            "address": "147 Countryside Rd, Countryside, ST 12121",
            "enrollment_date": date(2023, 11, 12),
            "status": models.PatientStatus.ACTIVE,
            "care_program": "Behavioral Health Program"
        },
        {
            "first_name": "Nicole",
            "last_name": "King",
            "date_of_birth": date(1991, 1, 23),
            "email": "nicole.king@email.com",
            "phone": "555-1026",
            "address": "258 Fairview Ave, Fairview, ST 13131",
            "enrollment_date": date(2024, 2, 28),
            "status": models.PatientStatus.ACTIVE,
            "care_program": "Wellness Program"
        },
        {
            "first_name": "Kevin",
            "last_name": "Wright",
            "date_of_birth": date(1982, 6, 15),
            "email": "kevin.wright@email.com",
            "phone": "555-1027",
            "address": "369 Bridgewater St, Bridgewater, ST 14141",
            "enrollment_date": date(2024, 3, 15),
            "status": models.PatientStatus.ACTIVE,
            "care_program": "Chronic Care Management"
        },
        {
            "first_name": "Michelle",
            "last_name": "Lopez",
            "date_of_birth": date(1989, 11, 2),
            "email": "michelle.lopez@email.com",
            "phone": "555-1028",
            "address": "741 Stonebridge Way, Stonebridge, ST 15151",
            "enrollment_date": date(2023, 10, 28),
            "status": models.PatientStatus.ACTIVE,
            "care_program": "Behavioral Health Program"
        },
        {
            "first_name": "Brandon",
            "last_name": "Hill",
            "date_of_birth": date(1984, 4, 9),
            "email": "brandon.hill@email.com",
            "phone": "555-1029",
            "address": "852 Windmill Dr, Windmill, ST 16161",
            "enrollment_date": date(2024, 1, 5),
            "status": models.PatientStatus.DISCHARGED,
            "care_program": "Wellness Program"
        },
    ]
    
    patients = []
    for patient_data in patients_data:
        existing = db.query(models.Patient).filter(
            models.Patient.email == patient_data["email"]
        ).first()
        if not existing:
            db_patient = models.Patient(**patient_data)
            db.add(db_patient)
            db.flush()
            patients.append(db_patient)
    
    db.commit()
    print(f"✓ Seeded {len(patients)} patients")
    return patients


def seed_care_team_assignments(db: Session, patients: list, care_team_members: list):
    """Seed care team assignments"""
    # Get all care team members
    all_members = db.query(models.CareTeamMember).all()
    
    # Assign care team members to patients
    assignments = [
        # Patient 1 (John Smith) - Active
        {"patient_id": 1, "member_email": "sarah.johnson@cerula.com"},
        {"patient_id": 1, "member_email": "david.williams@cerula.com"},
        {"patient_id": 1, "member_email": "robert.anderson@cerula.com"},
        
        # Patient 2 (Jane Doe) - Active
        {"patient_id": 2, "member_email": "michael.chen@cerula.com"},
        {"patient_id": 2, "member_email": "jessica.martinez@cerula.com"},
        
        # Patient 3 (Robert Brown) - Active
        {"patient_id": 3, "member_email": "emily.rodriguez@cerula.com"},
        {"patient_id": 3, "member_email": "david.williams@cerula.com"},
        
        # Patient 4 (Maria Garcia) - Active
        {"patient_id": 4, "member_email": "sarah.johnson@cerula.com"},
        
        # Patient 5 (James Wilson) - Inactive
        {"patient_id": 5, "member_email": "michael.chen@cerula.com"},
        
        # Patient 7 (William Taylor) - Active
        {"patient_id": 7, "member_email": "emily.rodriguez@cerula.com"},
        {"patient_id": 7, "member_email": "jessica.martinez@cerula.com"},
        {"patient_id": 7, "member_email": "lisa.thompson@cerula.com"},
        
        # Patient 8 (Linda Anderson) - Active
        {"patient_id": 8, "member_email": "sarah.johnson@cerula.com"},
        {"patient_id": 8, "member_email": "robert.anderson@cerula.com"},
        
        # Patient 9 (Richard Thomas) - Active
        {"patient_id": 9, "member_email": "michael.chen@cerula.com"},
        {"patient_id": 9, "member_email": "david.williams@cerula.com"},
        
        # Patient 10 (Barbara Jackson) - Active
        {"patient_id": 10, "member_email": "emily.rodriguez@cerula.com"},
        
        # Patient 11 (Christopher White) - Active
        {"patient_id": 11, "member_email": "sarah.johnson@cerula.com"},
        {"patient_id": 11, "member_email": "david.williams@cerula.com"},
        
        # Patient 12 (Amanda Harris) - Active
        {"patient_id": 12, "member_email": "michael.chen@cerula.com"},
        
        # Patient 13 (Daniel Martin) - Active
        {"patient_id": 13, "member_email": "emily.rodriguez@cerula.com"},
        {"patient_id": 13, "member_email": "jessica.martinez@cerula.com"},
        
        # Patient 15 (Michael Garcia) - Active
        {"patient_id": 15, "member_email": "sarah.johnson@cerula.com"},
        {"patient_id": 15, "member_email": "robert.anderson@cerula.com"},
        
        # Patient 16 (Sarah Martinez) - Active
        {"patient_id": 16, "member_email": "michael.chen@cerula.com"},
        {"patient_id": 16, "member_email": "david.williams@cerula.com"},
        
        # Patient 17 (David Robinson) - Active
        {"patient_id": 17, "member_email": "emily.rodriguez@cerula.com"},
        
        # Patient 18 (Emily Clark) - Active
        {"patient_id": 18, "member_email": "sarah.johnson@cerula.com"},
        {"patient_id": 18, "member_email": "lisa.thompson@cerula.com"},
        
        # Patient 20 (Jessica Lewis) - Active
        {"patient_id": 20, "member_email": "michael.chen@cerula.com"},
        
        # Patient 21 (Matthew Lee) - Active
        {"patient_id": 21, "member_email": "david.williams@cerula.com"},
        {"patient_id": 21, "member_email": "jessica.martinez@cerula.com"},
        
        # Patient 22 (Ashley Walker) - Active
        {"patient_id": 22, "member_email": "sarah.johnson@cerula.com"},
        
        # Patient 23 (Andrew Hall) - Active
        {"patient_id": 23, "member_email": "emily.rodriguez@cerula.com"},
        {"patient_id": 23, "member_email": "robert.anderson@cerula.com"},
        
        # Patient 25 (Ryan Young) - Active
        {"patient_id": 25, "member_email": "michael.chen@cerula.com"},
        {"patient_id": 25, "member_email": "david.williams@cerula.com"},
        
        # Patient 26 (Nicole King) - Active
        {"patient_id": 26, "member_email": "sarah.johnson@cerula.com"},
        
        # Patient 27 (Kevin Wright) - Active
        {"patient_id": 27, "member_email": "emily.rodriguez@cerula.com"},
        
        # Patient 28 (Michelle Lopez) - Active
        {"patient_id": 28, "member_email": "jessica.martinez@cerula.com"},
        {"patient_id": 28, "member_email": "lisa.thompson@cerula.com"},
    ]
    
    for assignment_data in assignments:
        member = next((m for m in all_members if m.email == assignment_data["member_email"]), None)
        if member:
            existing = db.query(models.CareTeamAssignment).filter(
                models.CareTeamAssignment.patient_id == assignment_data["patient_id"],
                models.CareTeamAssignment.care_team_member_id == member.id
            ).first()
            if not existing:
                db_assignment = models.CareTeamAssignment(
                    patient_id=assignment_data["patient_id"],
                    care_team_member_id=member.id,
                    assigned_date=date.today() - timedelta(days=random.randint(1, 90))
                )
                db.add(db_assignment)
    
    db.commit()
    print("✓ Seeded care team assignments")


def seed_health_screenings(db: Session, patients: list):
    """Seed health screenings for the last 6 months for each patient"""
    if not patients:
        print("⚠️  No patients available, skipping health screenings")
        return
    
    today = date.today()
    screenings_added = 0
    
    for patient in patients:
        # Generate screenings for the last 6 months (one per month)
        for month_offset in range(6):
            # Calculate screening date (approximately one month apart)
            screening_date = today - timedelta(days=30 * (5 - month_offset))
            
            # Generate a realistic score trend (generally improving over time)
            # Start with higher scores and gradually improve
            base_score = 7.0 - (month_offset * 0.5) + random.uniform(-1.0, 1.0)
            score = max(0.0, min(10.0, base_score))
            
            # Check if screening already exists
            existing = db.query(models.HealthScreening).filter(
                models.HealthScreening.patient_id == patient.id,
                models.HealthScreening.screening_date == screening_date
            ).first()
            
            if not existing:
                db_screening = models.HealthScreening(
                    patient_id=patient.id,
                    screening_date=screening_date,
                    score=round(score, 1)
                )
                db.add(db_screening)
                screenings_added += 1
    
    db.commit()
    print(f"✓ Seeded {screenings_added} health screenings (6 months per patient)")


def main():
    """Main seeding function - Safe and idempotent, never deletes existing data"""
    db = SessionLocal()
    try:
        # Ensure tables exist
        Base.metadata.create_all(bind=engine)
        
        print("Starting database seeding...")
        print("Note: This script is safe to run multiple times - it only adds missing data.")
        
        # Check existing data counts before seeding
        existing_patients = db.query(models.Patient).count()
        existing_members = db.query(models.CareTeamMember).count()
        existing_assignments = db.query(models.CareTeamAssignment).count()
        existing_screenings = db.query(models.HealthScreening).count()
        
        print(f"\nCurrent database state:")
        print(f"  - Care team members: {existing_members}")
        print(f"  - Patients: {existing_patients}")
        print(f"  - Assignments: {existing_assignments}")
        print(f"  - Screenings: {existing_screenings}")
        
        # Seed in order due to foreign key dependencies
        # These functions check for existing data and skip if already present
        seed_care_team_members(db)
        care_team_members = db.query(models.CareTeamMember).all()
        
        patients = seed_patients(db)
        if not patients:
            # If patients already exist, fetch them
            patients = db.query(models.Patient).all()
        
        # Only seed assignments and screenings if we have patients
        if patients:
            seed_care_team_assignments(db, patients, care_team_members)
            seed_health_screenings(db, patients)
        
        # Final counts
        final_patients = db.query(models.Patient).count()
        final_members = db.query(models.CareTeamMember).count()
        final_assignments = db.query(models.CareTeamAssignment).count()
        final_screenings = db.query(models.HealthScreening).count()
        
        print("\n✓ Database seeding completed successfully!")
        print(f"\nFinal database state:")
        print(f"  - {final_members} care team members")
        print(f"  - {final_patients} patients")
        print(f"  - {final_assignments} care team assignments")
        print(f"  - {final_screenings} health screenings")
        
        if final_patients == 0:
            print("\n⚠️  WARNING: No patients found after seeding. Check database connection.")
        
    except Exception as e:
        print(f"\n✗ Error seeding database: {e}")
        import traceback
        print(traceback.format_exc())
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
