import apiClient from './client'
import { Patient, PatientDetail, PatientStatus } from '../types'

export interface PatientsResponse {
  patients: Patient[]
  total: number
}

export const getPatients = async (
  skip: number = 0,
  limit: number = 20,
  search?: string,
  status?: PatientStatus
): Promise<PatientsResponse> => {
  const params: any = { skip, limit }
  if (search) params.search = search
  if (status) params.status = status

  const [patientsResponse, countResponse] = await Promise.all([
    apiClient.get<Patient[]>('/api/patients', { params }),
    apiClient.get<{ count: number }>('/api/patients/count', { params: { search, status } }),
  ])

  return {
    patients: patientsResponse.data,
    total: countResponse.data.count,
  }
}

export const getPatient = async (id: number): Promise<PatientDetail> => {
  const response = await apiClient.get<PatientDetail>(`/api/patients/${id}`)
  return response.data
}

export const createPatient = async (patient: Partial<Patient>): Promise<Patient> => {
  const response = await apiClient.post<Patient>('/api/patients', patient)
  return response.data
}

export const updatePatient = async (id: number, patient: Partial<Patient>): Promise<Patient> => {
  const response = await apiClient.put<Patient>(`/api/patients/${id}`, patient)
  return response.data
}

export const deletePatient = async (id: number): Promise<void> => {
  await apiClient.delete(`/api/patients/${id}`)
}
