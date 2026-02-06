from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import date
import enum
from app.database import Base


class PatientStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISCHARGED = "discharged"


class CareTeamRole(str, enum.Enum):
    HEALTH_COACH = "Health Coach"
    BHCM = "Behavioral Health Care Manager"
    PSYCHIATRIST = "Psychiatrist"


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    address = Column(String)
    enrollment_date = Column(Date, nullable=False)
    status = Column(SQLEnum(PatientStatus), default=PatientStatus.ACTIVE, nullable=False)
    care_program = Column(String)

    # Relationships
    care_team_assignments = relationship("CareTeamAssignment", back_populates="patient", cascade="all, delete-orphan")
    health_screenings = relationship("HealthScreening", back_populates="patient", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Patient {self.first_name} {self.last_name}>"


class CareTeamMember(Base):
    __tablename__ = "care_team_members"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    role = Column(SQLEnum(CareTeamRole), nullable=False)

    # Relationships
    assignments = relationship("CareTeamAssignment", back_populates="care_team_member", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<CareTeamMember {self.first_name} {self.last_name} ({self.role.value})>"


class CareTeamAssignment(Base):
    __tablename__ = "care_team_assignments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    care_team_member_id = Column(Integer, ForeignKey("care_team_members.id"), nullable=False)
    assigned_date = Column(Date, nullable=False, default=date.today)

    # Relationships
    patient = relationship("Patient", back_populates="care_team_assignments")
    care_team_member = relationship("CareTeamMember", back_populates="assignments")

    def __repr__(self):
        return f"<CareTeamAssignment Patient {self.patient_id} - Member {self.care_team_member_id}>"


class HealthScreening(Base):
    __tablename__ = "health_screenings"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    screening_date = Column(Date, nullable=False)
    score = Column(Float, nullable=False)  # 0-10 scale

    # Relationships
    patient = relationship("Patient", back_populates="health_screenings")

    def __repr__(self):
        return f"<HealthScreening Patient {self.patient_id} - Score {self.score} on {self.screening_date}>"
