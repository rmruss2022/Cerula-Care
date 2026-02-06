import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getPatient, updatePatient, createPatient } from '../api/patients'
import { getPatientCareTeamAssignments, assignCareTeamMember, unassignCareTeamMember } from '../api/careTeam'
import { getCareTeamMembers } from '../api/careTeam'
import { getPatientHealthScreenings } from '../api/healthScreenings'
import { PatientDetail as PatientDetailType, CareTeamMember, CareTeamAssignment, HealthScreening, PatientStatus, CareTeamRole } from '../types'
import HealthScreeningChart from './HealthScreeningChart'
import './PatientDetail.css'

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

  if (loading) {
    return <div className="loading">Loading patient details...</div>
  }

  return (
    <div className="patient-detail">
      <div className="patient-detail-header">
        <button className="btn btn-secondary" onClick={() => navigate('/')}>
          ← Back to Patients
        </button>
        {!isNew && !isEditing && (
          <button className="btn btn-primary" onClick={() => setIsEditing(true)}>
            Edit Patient
          </button>
        )}
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="patient-detail-content">
        <div className="patient-info-card">
          <h2>{isNew ? 'New Patient' : `${patient.first_name} ${patient.last_name}`}</h2>
          
          {isEditing ? (
            <div className="patient-form">
              <div className="form-row">
                <div className="form-group">
                  <label>First Name *</label>
                  <input
                    type="text"
                    value={patient.first_name || ''}
                    onChange={(e) => setPatient({ ...patient, first_name: e.target.value })}
                  />
                </div>
                <div className="form-group">
                  <label>Last Name *</label>
                  <input
                    type="text"
                    value={patient.last_name || ''}
                    onChange={(e) => setPatient({ ...patient, last_name: e.target.value })}
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Email *</label>
                  <input
                    type="email"
                    value={patient.email || ''}
                    onChange={(e) => setPatient({ ...patient, email: e.target.value })}
                  />
                </div>
                <div className="form-group">
                  <label>Phone</label>
                  <input
                    type="tel"
                    value={patient.phone || ''}
                    onChange={(e) => setPatient({ ...patient, phone: e.target.value })}
                  />
                </div>
              </div>

              <div className="form-group">
                <label>Address</label>
                <input
                  type="text"
                  value={patient.address || ''}
                  onChange={(e) => setPatient({ ...patient, address: e.target.value })}
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Date of Birth *</label>
                  <input
                    type="date"
                    value={patient.date_of_birth || ''}
                    onChange={(e) => setPatient({ ...patient, date_of_birth: e.target.value })}
                  />
                </div>
                <div className="form-group">
                  <label>Enrollment Date *</label>
                  <input
                    type="date"
                    value={patient.enrollment_date || ''}
                    onChange={(e) => setPatient({ ...patient, enrollment_date: e.target.value })}
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Status *</label>
                  <select
                    value={patient.status || PatientStatus.ACTIVE}
                    onChange={(e) => setPatient({ ...patient, status: e.target.value as PatientStatus })}
                  >
                    <option value={PatientStatus.ACTIVE}>Active</option>
                    <option value={PatientStatus.INACTIVE}>Inactive</option>
                    <option value={PatientStatus.DISCHARGED}>Discharged</option>
                  </select>
                </div>
                <div className="form-group">
                  <label>Care Program</label>
                  <input
                    type="text"
                    value={patient.care_program || ''}
                    onChange={(e) => setPatient({ ...patient, care_program: e.target.value })}
                  />
                </div>
              </div>

              <div className="form-actions">
                <button className="btn btn-primary" onClick={handleSave} disabled={saving}>
                  {saving ? 'Saving...' : isNew ? 'Create Patient' : 'Save Changes'}
                </button>
                {!isNew && (
                  <button className="btn btn-secondary" onClick={() => {
                    setIsEditing(false)
                    loadPatientData()
                  }}>
                    Cancel
                  </button>
                )}
              </div>
            </div>
          ) : (
            <div className="patient-info">
              <div className="info-row">
                <span className="info-label">Email:</span>
                <span>{patient.email}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Phone:</span>
                <span>{patient.phone || '—'}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Address:</span>
                <span>{patient.address || '—'}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Date of Birth:</span>
                <span>{patient.date_of_birth ? new Date(patient.date_of_birth).toLocaleDateString() : '—'}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Enrollment Date:</span>
                <span>{patient.enrollment_date ? new Date(patient.enrollment_date).toLocaleDateString() : '—'}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Status:</span>
                <span className={`status-badge ${patient.status}`}>{patient.status}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Care Program:</span>
                <span>{patient.care_program || '—'}</span>
              </div>
            </div>
          )}
        </div>

        {!isNew && (
          <>
            <div className="care-team-card">
              <div className="card-header">
                <h3>Care Team</h3>
                <button className="btn btn-primary btn-sm" onClick={() => setShowAssignModal(true)}>
                  + Assign Member
                </button>
              </div>
              {careTeamAssignments.length === 0 ? (
                <div className="empty-state">No care team members assigned</div>
              ) : (
                <div className="care-team-list">
                  {careTeamAssignments.map((assignment) => (
                    <div key={assignment.id} className="care-team-item">
                      <div>
                        <strong>{assignment.care_team_member.first_name} {assignment.care_team_member.last_name}</strong>
                        <span className="role-badge">{assignment.care_team_member.role}</span>
                      </div>
                      <div className="care-team-meta">
                        <span>Assigned: {new Date(assignment.assigned_date).toLocaleDateString()}</span>
                        <button
                          className="btn btn-danger btn-sm"
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

            <div className="health-screenings-card">
              <h3>Health Screening Trends</h3>
              {healthScreenings.length === 0 ? (
                <div className="empty-state">No health screening data available</div>
              ) : (
                <>
                  <HealthScreeningChart screenings={healthScreenings} />
                  <div className="screenings-table">
                    <table>
                      <thead>
                        <tr>
                          <th>Date</th>
                          <th>Score</th>
                        </tr>
                      </thead>
                      <tbody>
                        {healthScreenings.map((screening) => (
                          <tr key={screening.id}>
                            <td>{new Date(screening.screening_date).toLocaleDateString()}</td>
                            <td className={screening.score >= 7 ? 'score-high' : screening.score >= 4 ? 'score-medium' : 'score-low'}>
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
        <div className="modal-overlay" onClick={() => setShowAssignModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>Assign Care Team Member</h3>
            <div className="form-group">
              <label>Select Member</label>
              <select
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
              <p className="text-muted">All available members are already assigned</p>
            )}
            <div className="modal-actions">
              <button className="btn btn-primary" onClick={handleAssign} disabled={!selectedMemberId}>
                Assign
              </button>
              <button className="btn btn-secondary" onClick={() => setShowAssignModal(false)}>
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
