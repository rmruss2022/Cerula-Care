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
