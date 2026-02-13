import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getPatient, updatePatient, createPatient } from '../api/patients'
import { getPatientCareTeamAssignments, assignCareTeamMember, unassignCareTeamMember } from '../api/careTeam'
import { getCareTeamMembers } from '../api/careTeam'
import { getPatientHealthScreenings } from '../api/healthScreenings'
import { PatientDetail as PatientDetailType, CareTeamMember, CareTeamAssignment, HealthScreening, PatientStatus } from '../types'
import HealthScreeningChart from './HealthScreeningChart'

const PatientDetail = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const isNew = id === 'new'
  
  const [patient, setPatient] = useState<Partial<PatientDetailType>>({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    address: '',
    date_of_birth: '',
    enrollment_date: new Date().toISOString().split('T')[0],
    status: PatientStatus.ACTIVE,
    care_program: '',
  })
  const [careTeamAssignments, setCareTeamAssignments] = useState<CareTeamAssignment[]>([])
  const [healthScreenings, setHealthScreenings] = useState<HealthScreening[]>([])
  const [availableMembers, setAvailableMembers] = useState<CareTeamMember[]>([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isEditing, setIsEditing] = useState(isNew)
  const [showAssignModal, setShowAssignModal] = useState(false)
  const [selectedMemberId, setSelectedMemberId] = useState<number | ''>('')

  useEffect(() => {
    if (!isNew) {
      loadPatientData()
    } else {
      setLoading(false)
    }
    loadCareTeamMembers()
  }, [id])

  const loadPatientData = async () => {
    if (!id || isNew) return
    
    try {
      setLoading(true)
      setError(null)
      const [patientData, assignments, screenings] = await Promise.all([
        getPatient(parseInt(id)),
        getPatientCareTeamAssignments(parseInt(id)),
        getPatientHealthScreenings(parseInt(id)),
      ])
      setPatient(patientData)
      setCareTeamAssignments(assignments)
      setHealthScreenings(screenings)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load patient data')
    } finally {
      setLoading(false)
    }
  }

  const loadCareTeamMembers = async () => {
    try {
      const members = await getCareTeamMembers()
      setAvailableMembers(members)
    } catch (err) {
      console.error('Failed to load care team members', err)
    }
  }

  const handleSave = async () => {
    try {
      setSaving(true)
      setError(null)
      
      if (isNew) {
        const newPatient = await createPatient(patient)
        navigate(`/patients/${newPatient.id}`)
      } else {
        await updatePatient(parseInt(id!), patient)
        setIsEditing(false)
        await loadPatientData()
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save patient')
    } finally {
      setSaving(false)
    }
  }

  const handleAssign = async () => {
    if (!selectedMemberId || !id || isNew) return

    try {
      await assignCareTeamMember(parseInt(id), selectedMemberId as number)
      setShowAssignModal(false)
      setSelectedMemberId('')
      await loadPatientData()
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to assign care team member')
    }
  }

  const handleUnassign = async (assignmentId: number) => {
    if (!id || isNew) return

    if (!window.confirm('Are you sure you want to unassign this care team member?')) {
      return
    }

    try {
      await unassignCareTeamMember(parseInt(id), assignmentId)
      await loadPatientData()
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to unassign care team member')
    }
  }

  const getAvailableMembersForAssignment = () => {
    const assignedIds = new Set(careTeamAssignments.map(a => a.care_team_member_id))
    return availableMembers.filter(m => !assignedIds.has(m.id))
  }

  const getStatusBadgeClass = (status?: PatientStatus) => {
    const baseClasses = 'inline-block px-3 py-1 rounded-xl text-sm font-medium capitalize'
    switch (status) {
      case PatientStatus.ACTIVE:
        return `${baseClasses} status-badge-active`
      case PatientStatus.INACTIVE:
        return `${baseClasses} status-badge-inactive`
      case PatientStatus.DISCHARGED:
        return `${baseClasses} status-badge-discharged`
      default:
        return baseClasses
    }
  }

  const getScoreClass = (score: number) => {
    if (score >= 7) return 'text-[#dc3545] font-semibold'
    if (score >= 4) return 'text-[#ffc107] font-semibold'
    return 'text-[#28a745] font-semibold'
  }

  if (loading) {
    return <div className="text-center py-12 text-[#6c757d]">Loading patient details...</div>
  }

  return (
    <div className="w-full">
      <div className="flex justify-between items-center mb-8">
        <button 
          className="px-4 py-2 bg-[#6c757d] text-white rounded border-none text-base cursor-pointer transition-colors duration-200 hover:bg-[#5a6268]" 
          onClick={() => navigate('/')}
        >
          ← Back to Patients
        </button>
        {!isNew && !isEditing && (
          <button 
            className="px-4 py-2 bg-[#007bff] text-white rounded border-none text-base cursor-pointer transition-colors duration-200 hover:bg-[#0056b3]" 
            onClick={() => setIsEditing(true)}
          >
            Edit Patient
          </button>
        )}
      </div>

      {error && (
        <div className="text-[#dc3545] bg-[#f8d7da] border border-[#f5c6cb] rounded p-4 mb-4">
          {error}
        </div>
      )}

      <div className="flex flex-col gap-8">
        <div className="bg-white rounded-lg p-8 shadow-[0_2px_4px_rgba(0,0,0,0.1)]">
          <h2 className="mb-6 text-[#2c3e50]">{isNew ? 'New Patient' : `${patient.first_name} ${patient.last_name}`}</h2>
          
          {isEditing ? (
            <div className="flex flex-col gap-4">
              <div className="grid grid-cols-2 gap-4 md:grid-cols-1">
                <div className="flex flex-col gap-2">
                  <label className="font-medium text-[#495057]">First Name *</label>
                  <input
                    type="text"
                    className="border border-[#ddd] rounded text-base p-3"
                    value={patient.first_name || ''}
                    onChange={(e) => setPatient({ ...patient, first_name: e.target.value })}
                  />
                </div>
                <div className="flex flex-col gap-2">
                  <label className="font-medium text-[#495057]">Last Name *</label>
                  <input
                    type="text"
                    className="border border-[#ddd] rounded text-base p-3"
                    value={patient.last_name || ''}
                    onChange={(e) => setPatient({ ...patient, last_name: e.target.value })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 md:grid-cols-1">
                <div className="flex flex-col gap-2">
                  <label className="font-medium text-[#495057]">Email *</label>
                  <input
                    type="email"
                    className="border border-[#ddd] rounded text-base p-3"
                    value={patient.email || ''}
                    onChange={(e) => setPatient({ ...patient, email: e.target.value })}
                  />
                </div>
                <div className="flex flex-col gap-2">
                  <label className="font-medium text-[#495057]">Phone</label>
                  <input
                    type="tel"
                    className="border border-[#ddd] rounded text-base p-3"
                    value={patient.phone || ''}
                    onChange={(e) => setPatient({ ...patient, phone: e.target.value })}
                  />
                </div>
              </div>

              <div className="flex flex-col gap-2">
                <label className="font-medium text-[#495057]">Address</label>
                <input
                  type="text"
                  className="border border-[#ddd] rounded text-base p-3"
                  value={patient.address || ''}
                  onChange={(e) => setPatient({ ...patient, address: e.target.value })}
                />
              </div>

              <div className="grid grid-cols-2 gap-4 md:grid-cols-1">
                <div className="flex flex-col gap-2">
                  <label className="font-medium text-[#495057]">Date of Birth *</label>
                  <input
                    type="date"
                    className="border border-[#ddd] rounded text-base p-3"
                    value={patient.date_of_birth || ''}
                    onChange={(e) => setPatient({ ...patient, date_of_birth: e.target.value })}
                  />
                </div>
                <div className="flex flex-col gap-2">
                  <label className="font-medium text-[#495057]">Enrollment Date *</label>
                  <input
                    type="date"
                    className="border border-[#ddd] rounded text-base p-3"
                    value={patient.enrollment_date || ''}
                    onChange={(e) => setPatient({ ...patient, enrollment_date: e.target.value })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 md:grid-cols-1">
                <div className="flex flex-col gap-2">
                  <label className="font-medium text-[#495057]">Status *</label>
                  <select
                    className="border border-[#ddd] rounded text-base p-3"
                    value={patient.status || PatientStatus.ACTIVE}
                    onChange={(e) => setPatient({ ...patient, status: e.target.value as PatientStatus })}
                  >
                    <option value={PatientStatus.ACTIVE}>Active</option>
                    <option value={PatientStatus.INACTIVE}>Inactive</option>
                    <option value={PatientStatus.DISCHARGED}>Discharged</option>
                  </select>
                </div>
                <div className="flex flex-col gap-2">
                  <label className="font-medium text-[#495057]">Care Program</label>
                  <input
                    type="text"
                    className="border border-[#ddd] rounded text-base p-3"
                    value={patient.care_program || ''}
                    onChange={(e) => setPatient({ ...patient, care_program: e.target.value })}
                  />
                </div>
              </div>

              <div className="flex gap-4 mt-4">
                <button 
                  className="px-4 py-2 bg-[#007bff] text-white rounded border-none text-base cursor-pointer transition-colors duration-200 hover:bg-[#0056b3] disabled:opacity-50 disabled:cursor-not-allowed" 
                  onClick={handleSave} 
                  disabled={saving}
                >
                  {saving ? 'Saving...' : isNew ? 'Create Patient' : 'Save Changes'}
                </button>
                {!isNew && (
                  <button 
                    className="px-4 py-2 bg-[#6c757d] text-white rounded border-none text-base cursor-pointer transition-colors duration-200 hover:bg-[#5a6268]" 
                    onClick={() => {
                      setIsEditing(false)
                      loadPatientData()
                    }}
                  >
                    Cancel
                  </button>
                )}
              </div>
            </div>
          ) : (
            <div className="flex flex-col gap-4">
              <div className="grid grid-cols-[150px_1fr] gap-4 border-b border-[#f0f0f0] md:grid-cols-1" style={{ padding: '0.5rem 0' }}>
                <span className="font-medium text-[#6c757d]">Email:</span>
                <span>{patient.email}</span>
              </div>
              <div className="grid grid-cols-[150px_1fr] gap-4 border-b border-[#f0f0f0] md:grid-cols-1" style={{ padding: '0.5rem 0' }}>
                <span className="font-medium text-[#6c757d]">Phone:</span>
                <span>{patient.phone || '—'}</span>
              </div>
              <div className="grid grid-cols-[150px_1fr] gap-4 border-b border-[#f0f0f0] md:grid-cols-1" style={{ padding: '0.5rem 0' }}>
                <span className="font-medium text-[#6c757d]">Address:</span>
                <span>{patient.address || '—'}</span>
              </div>
              <div className="grid grid-cols-[150px_1fr] gap-4 border-b border-[#f0f0f0] md:grid-cols-1" style={{ padding: '0.5rem 0' }}>
                <span className="font-medium text-[#6c757d]">Date of Birth:</span>
                <span>{patient.date_of_birth ? new Date(patient.date_of_birth).toLocaleDateString() : '—'}</span>
              </div>
              <div className="grid grid-cols-[150px_1fr] gap-4 border-b border-[#f0f0f0] md:grid-cols-1" style={{ padding: '0.5rem 0' }}>
                <span className="font-medium text-[#6c757d]">Enrollment Date:</span>
                <span>{patient.enrollment_date ? new Date(patient.enrollment_date).toLocaleDateString() : '—'}</span>
              </div>
              <div className="grid grid-cols-[150px_1fr] gap-4 border-b border-[#f0f0f0] md:grid-cols-1" style={{ padding: '0.5rem 0' }}>
                <span className="font-medium text-[#6c757d]">Status:</span>
                <span className={getStatusBadgeClass(patient.status)}>{patient.status}</span>
              </div>
              <div className="grid grid-cols-[150px_1fr] gap-4 border-b border-[#f0f0f0] md:grid-cols-1" style={{ padding: '0.5rem 0' }}>
                <span className="font-medium text-[#6c757d]">Care Program:</span>
                <span>{patient.care_program || '—'}</span>
              </div>
            </div>
          )}
        </div>

        {!isNew && (
          <>
            <div className="bg-white rounded-lg p-8 shadow-[0_2px_4px_rgba(0,0,0,0.1)]">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-[#2c3e50]">Care Team</h3>
                <button 
                  className="px-2 py-1 bg-[#007bff] text-white rounded border-none text-sm cursor-pointer transition-colors duration-200 hover:bg-[#0056b3]" 
                  onClick={() => setShowAssignModal(true)}
                >
                  + Assign Member
                </button>
              </div>
              {careTeamAssignments.length === 0 ? (
                <div className="text-center py-8 text-[#6c757d]">No care team members assigned</div>
              ) : (
                <div className="flex flex-col gap-4">
                  {careTeamAssignments.map((assignment) => (
                    <div key={assignment.id} className="p-4 border border-[#e0e0e0] rounded flex justify-between items-center md:flex-col md:items-start md:gap-4">
                      <div className="flex items-center gap-3">
                        <strong>{assignment.care_team_member.first_name} {assignment.care_team_member.last_name}</strong>
                        <span className="px-2 py-1 bg-[#e9ecef] rounded text-sm text-[#495057]">{assignment.care_team_member.role}</span>
                      </div>
                      <div className="flex items-center gap-4">
                        <span>Assigned: {new Date(assignment.assigned_date).toLocaleDateString()}</span>
                        <button
                          className="px-2 py-1 bg-[#dc3545] text-white rounded border-none text-sm cursor-pointer transition-colors duration-200 hover:bg-[#c82333]"
                          onClick={() => handleUnassign(assignment.id)}
                        >
                          Unassign
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="bg-white rounded-lg p-8 shadow-[0_2px_4px_rgba(0,0,0,0.1)]">
              <h3 className="text-[#2c3e50]">Health Screening Trends</h3>
              {healthScreenings.length === 0 ? (
                <div className="text-center py-8 text-[#6c757d]">No health screening data available</div>
              ) : (
                <>
                  <HealthScreeningChart screenings={healthScreenings} />
                  <div className="mt-8">
                    <table className="w-full border-collapse">
                      <thead>
                        <tr>
                          <th className="p-3 text-left border-b border-[#e0e0e0] bg-[#f8f9fa] font-semibold">Date</th>
                          <th className="p-3 text-left border-b border-[#e0e0e0] bg-[#f8f9fa] font-semibold">Score</th>
                        </tr>
                      </thead>
                      <tbody>
                        {healthScreenings.map((screening) => (
                          <tr key={screening.id}>
                            <td className="p-3 text-left border-b border-[#e0e0e0]">{new Date(screening.screening_date).toLocaleDateString()}</td>
                            <td className={`p-3 text-left border-b border-[#e0e0e0] ${getScoreClass(screening.score)}`}>
                              {screening.score.toFixed(1)}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </>
              )}
            </div>
          </>
        )}
      </div>

      {showAssignModal && (
        <div 
          className="fixed inset-0 flex justify-center items-center z-[1000]" 
          style={{ backgroundColor: 'rgba(0, 0, 0, 0.5)' }}
          onClick={() => setShowAssignModal(false)}
        >
          <div 
            className="bg-white p-8 rounded-lg max-w-[500px] w-[90%] max-h-[90vh] overflow-y-auto" 
            onClick={(e) => e.stopPropagation()}
          >
            <h3 className="mb-6 text-[#2c3e50]">Assign Care Team Member</h3>
            <div className="flex flex-col gap-2">
              <label className="font-medium text-[#495057]">Select Member</label>
              <select
                className="border border-[#ddd] rounded text-base p-3"
                value={selectedMemberId}
                onChange={(e) => setSelectedMemberId(e.target.value ? parseInt(e.target.value) : '')}
              >
                <option value="">Select a member...</option>
                {getAvailableMembersForAssignment().map((member) => (
                  <option key={member.id} value={member.id}>
                    {member.first_name} {member.last_name} - {member.role}
                  </option>
                ))}
              </select>
            </div>
            {getAvailableMembersForAssignment().length === 0 && (
              <p className="text-[#6c757d] text-sm mt-2">All available members are already assigned</p>
            )}
            <div className="flex gap-4 mt-6 justify-end">
              <button 
                className="px-4 py-2 bg-[#007bff] text-white rounded border-none text-base cursor-pointer transition-colors duration-200 hover:bg-[#0056b3] disabled:opacity-50 disabled:cursor-not-allowed" 
                onClick={handleAssign} 
                disabled={!selectedMemberId}
              >
                Assign
              </button>
              <button 
                className="px-4 py-2 bg-[#6c757d] text-white rounded border-none text-base cursor-pointer transition-colors duration-200 hover:bg-[#5a6268]" 
                onClick={() => setShowAssignModal(false)}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default PatientDetail
