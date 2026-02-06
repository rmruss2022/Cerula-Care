export enum PatientStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  DISCHARGED = 'discharged',
}

export enum CareTeamRole {
  HEALTH_COACH = 'Health Coach',
  BHCM = 'Behavioral Health Care Manager',
  PSYCHIATRIST = 'Psychiatrist',
}

export interface Patient {
  id: number
  first_name: string
  last_name: string
  date_of_birth: string
  email: string
  phone?: string
  address?: string
  enrollment_date: string
  status: PatientStatus
  care_program?: string
}

export interface PatientDetail extends Patient {
  care_team_assignments: CareTeamAssignment[]
  health_screenings: HealthScreening[]
}

export interface CareTeamMember {
  id: number
  first_name: string
  last_name: string
  email: string
  phone?: string
  role: CareTeamRole
}

export interface CareTeamAssignment {
  id: number
  patient_id: number
  care_team_member_id: number
  assigned_date: string
  care_team_member: CareTeamMember
}

export interface HealthScreening {
  id: number
  patient_id: number
  screening_date: string
  score: number
}
