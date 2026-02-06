import apiClient from './client'
import { CareTeamMember, CareTeamAssignment, CareTeamRole } from '../types'

export const getCareTeamMembers = async (role?: CareTeamRole): Promise<CareTeamMember[]> => {
  const params = role ? { role } : {}
  const response = await apiClient.get<CareTeamMember[]>('/api/care-team-members', { params })
  return response.data
}

export const getPatientCareTeamAssignments = async (patientId: number): Promise<CareTeamAssignment[]> => {
  const response = await apiClient.get<CareTeamAssignment[]>(
    `/api/patients/${patientId}/care-team-assignments`
  )
  return response.data
}

export const assignCareTeamMember = async (
  patientId: number,
  careTeamMemberId: number
): Promise<CareTeamAssignment> => {
  const response = await apiClient.post<CareTeamAssignment>(
    `/api/patients/${patientId}/care-team-assignments`,
    { care_team_member_id: careTeamMemberId }
  )
  return response.data
}

export const unassignCareTeamMember = async (patientId: number, assignmentId: number): Promise<void> => {
  await apiClient.delete(`/api/patients/${patientId}/care-team-assignments/${assignmentId}`)
}
