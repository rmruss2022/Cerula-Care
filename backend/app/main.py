from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import List, Optional
from datetime import date, timedelta
import os
from app.database import get_db, engine, Base
from app import models, schemas

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Patient Care Dashboard API",
    description="API for managing patients, care teams, and health screenings",
    version="1.0.0"
)

# CORS middleware
# Get allowed origins from environment variable or use defaults
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:5173"
).split(",")

# Add Vercel frontend URL if provided
vercel_url = os.getenv("VERCEL_FRONTEND_URL")
if vercel_url:
    allowed_origins.append(vercel_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Patient endpoints
@app.get("/api/patients", response_model=List[schemas.PatientResponse])
def get_patients(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    status: Optional[schemas.PatientStatus] = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of patients with pagination, search, and filtering"""
    query = db.query(models.Patient)
    
    if search:
        search_filter = or_(
            models.Patient.first_name.ilike(f"%{search}%"),
            models.Patient.last_name.ilike(f"%{search}%"),
            models.Patient.email.ilike(f"%{search}%"),
            models.Patient.phone.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    if status:
        query = query.filter(models.Patient.status == status)
    
    patients = query.order_by(models.Patient.last_name, models.Patient.first_name).offset(skip).limit(limit).all()
    return patients


@app.get("/api/patients/count")
def get_patients_count(
    search: Optional[str] = Query(None),
    status: Optional[schemas.PatientStatus] = Query(None),
    db: Session = Depends(get_db)
):
    """Get total count of patients matching filters"""
    query = db.query(models.Patient)
    
    if search:
        search_filter = or_(
            models.Patient.first_name.ilike(f"%{search}%"),
            models.Patient.last_name.ilike(f"%{search}%"),
            models.Patient.email.ilike(f"%{search}%"),
            models.Patient.phone.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    if status:
        query = query.filter(models.Patient.status == status)
    
    return {"count": query.count()}


@app.get("/api/patients/{patient_id}", response_model=schemas.PatientDetailResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    """Get detailed patient information"""
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@app.post("/api/patients", response_model=schemas.PatientResponse, status_code=201)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    """Create a new patient"""
    # Check if email already exists
    existing = db.query(models.Patient).filter(models.Patient.email == patient.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


@app.put("/api/patients/{patient_id}", response_model=schemas.PatientResponse)
def update_patient(patient_id: int, patient_update: schemas.PatientUpdate, db: Session = Depends(get_db)):
    """Update patient information"""
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    update_data = patient_update.dict(exclude_unset=True)
    
    # Check email uniqueness if being updated
    if "email" in update_data:
        existing = db.query(models.Patient).filter(
            models.Patient.email == update_data["email"],
            models.Patient.id != patient_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    for field, value in update_data.items():
        setattr(db_patient, field, value)
    
    db.commit()
    db.refresh(db_patient)
    return db_patient


@app.delete("/api/patients/{patient_id}", status_code=204)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    """Delete a patient"""
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    db.delete(db_patient)
    db.commit()
    return None


# Care Team Member endpoints
@app.get("/api/care-team-members", response_model=List[schemas.CareTeamMemberResponse])
def get_care_team_members(
    role: Optional[schemas.CareTeamRole] = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of care team members"""
    query = db.query(models.CareTeamMember)
    
    if role:
        query = query.filter(models.CareTeamMember.role == role)
    
    return query.order_by(models.CareTeamMember.last_name, models.CareTeamMember.first_name).all()


@app.get("/api/care-team-members/{member_id}", response_model=schemas.CareTeamMemberResponse)
def get_care_team_member(member_id: int, db: Session = Depends(get_db)):
    """Get care team member details"""
    member = db.query(models.CareTeamMember).filter(models.CareTeamMember.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Care team member not found")
    return member


# Care Team Assignment endpoints
@app.get("/api/patients/{patient_id}/care-team-assignments", response_model=List[schemas.CareTeamAssignmentResponse])
def get_patient_care_team_assignments(patient_id: int, db: Session = Depends(get_db)):
    """Get care team assignments for a patient"""
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return patient.care_team_assignments


@app.post("/api/patients/{patient_id}/care-team-assignments", response_model=schemas.CareTeamAssignmentResponse, status_code=201)
def assign_care_team_member(
    patient_id: int,
    assignment: schemas.CareTeamAssignmentCreate,
    db: Session = Depends(get_db)
):
    """Assign a care team member to a patient"""
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    member = db.query(models.CareTeamMember).filter(models.CareTeamMember.id == assignment.care_team_member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Care team member not found")
    
    # Check if assignment already exists
    existing = db.query(models.CareTeamAssignment).filter(
        models.CareTeamAssignment.patient_id == patient_id,
        models.CareTeamAssignment.care_team_member_id == assignment.care_team_member_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Care team member already assigned to this patient")
    
    assigned_date = assignment.assigned_date or date.today()
    db_assignment = models.CareTeamAssignment(
        patient_id=patient_id,
        care_team_member_id=assignment.care_team_member_id,
        assigned_date=assigned_date
    )
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment


@app.delete("/api/patients/{patient_id}/care-team-assignments/{assignment_id}", status_code=204)
def unassign_care_team_member(patient_id: int, assignment_id: int, db: Session = Depends(get_db)):
    """Unassign a care team member from a patient"""
    assignment = db.query(models.CareTeamAssignment).filter(
        models.CareTeamAssignment.id == assignment_id,
        models.CareTeamAssignment.patient_id == patient_id
    ).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    db.delete(assignment)
    db.commit()
    return None


# Health Screening endpoints
@app.get("/api/patients/{patient_id}/health-screenings", response_model=List[schemas.HealthScreeningResponse])
def get_patient_health_screenings(patient_id: int, db: Session = Depends(get_db)):
    """Get health screening history for a patient"""
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    screenings = db.query(models.HealthScreening).filter(
        models.HealthScreening.patient_id == patient_id
    ).order_by(models.HealthScreening.screening_date.desc()).all()
    
    return screenings


@app.get("/api/health-screenings/{screening_id}", response_model=schemas.HealthScreeningResponse)
def get_health_screening(screening_id: int, db: Session = Depends(get_db)):
    """Get a specific health screening"""
    screening = db.query(models.HealthScreening).filter(models.HealthScreening.id == screening_id).first()
    if not screening:
        raise HTTPException(status_code=404, detail="Health screening not found")
    return screening


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
