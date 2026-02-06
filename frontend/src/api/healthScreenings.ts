import apiClient from './client'
import { HealthScreening } from '../types'

export const getPatientHealthScreenings = async (patientId: number): Promise<HealthScreening[]> => {
  const response = await apiClient.get<HealthScreening[]>(
    `/api/patients/${patientId}/health-screenings`
  )
  return response.data
}
