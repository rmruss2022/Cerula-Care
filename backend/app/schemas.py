from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional, List
from app.models import PatientStatus, CareTeamRole


# Patient Schemas
class PatientBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: date
    status: PatientStatus = PatientStatus.ACTIVE
    care_program: Optional[str] = None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[date] = None
    status: Optional[PatientStatus] = None
    care_program: Optional[str] = None


class PatientResponse(PatientBase):
    id: int

    class Config:
        from_attributes = True


class PatientDetailResponse(PatientResponse):
    care_team_assignments: List["CareTeamAssignmentResponse"] = []
    health_screenings: List["HealthScreeningResponse"] = []


# Care Team Member Schemas
class CareTeamMemberBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    role: CareTeamRole


class CareTeamMemberCreate(CareTeamMemberBase):
    pass


class CareTeamMemberResponse(CareTeamMemberBase):
    id: int

    class Config:
        from_attributes = True


# Care Team Assignment Schemas
class CareTeamAssignmentBase(BaseModel):
    patient_id: int
    care_team_member_id: int
    assigned_date: date


class CareTeamAssignmentCreate(BaseModel):
    care_team_member_id: int
    assigned_date: Optional[date] = None


class CareTeamAssignmentResponse(BaseModel):
    id: int
    patient_id: int
    care_team_member_id: int
    assigned_date: date
    care_team_member: CareTeamMemberResponse

    class Config:
        from_attributes = True


# Health Screening Schemas
class HealthScreeningBase(BaseModel):
    patient_id: int
    screening_date: date
    score: float = Field(ge=0, le=10)


class HealthScreeningCreate(HealthScreeningBase):
    pass


class HealthScreeningResponse(HealthScreeningBase):
    id: int

    class Config:
        from_attributes = True


# Update forward references
PatientDetailResponse.model_rebuild()
CareTeamAssignmentResponse.model_rebuild()
