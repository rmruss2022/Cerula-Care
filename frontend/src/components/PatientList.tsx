import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getPatients, deletePatient } from '../api/patients'
import { Patient, PatientStatus } from '../types'
import './PatientList.css'

const PatientList = () => {
  const navigate = useNavigate()
  const [patients, setPatients] = useState<Patient[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState<PatientStatus | ''>('')
  const [currentPage, setCurrentPage] = useState(1)
  const [totalPatients, setTotalPatients] = useState(0)
  const [deletingId, setDeletingId] = useState<number | null>(null)

  const patientsPerPage = 20

  useEffect(() => {
    loadPatients()
  }, [currentPage, search, statusFilter])

  const loadPatients = async () => {
    try {
      setLoading(true)
      setError(null)
      const skip = (currentPage - 1) * patientsPerPage
      const result = await getPatients(
        skip,
        patientsPerPage,
        search || undefined,
        statusFilter || undefined
      )
      setPatients(result.patients)
      setTotalPatients(result.total)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load patients')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id: number, e: React.MouseEvent) => {
    e.stopPropagation()
    if (!window.confirm('Are you sure you want to delete this patient?')) {
      return
    }

    try {
      setDeletingId(id)
      await deletePatient(id)
      await loadPatients()
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to delete patient')
    } finally {
      setDeletingId(null)
    }
  }

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(e.target.value)
    setCurrentPage(1)
  }

  const handleStatusFilterChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setStatusFilter(e.target.value as PatientStatus | '')
    setCurrentPage(1)
  }

  const totalPages = Math.ceil(totalPatients / patientsPerPage)

  const getStatusBadgeClass = (status: PatientStatus) => {
    switch (status) {
      case PatientStatus.ACTIVE:
        return 'status-badge active'
      case PatientStatus.INACTIVE:
        return 'status-badge inactive'
      case PatientStatus.DISCHARGED:
        return 'status-badge discharged'
      default:
        return 'status-badge'
    }
  }

  return (
    <div className="patient-list">
      <div className="patient-list-header">
        <h2>Patients</h2>
        <button className="btn btn-primary" onClick={() => navigate('/patients/new')}>
          + Add Patient
        </button>
      </div>

      <div className="patient-list-filters">
        <div className="search-box">
          <input
            type="text"
            placeholder="Search by name, email, or phone..."
            value={search}
            onChange={handleSearchChange}
            className="search-input"
          />
        </div>
        <div className="filter-box">
          <select
            value={statusFilter}
            onChange={handleStatusFilterChange}
            className="filter-select"
          >
            <option value="">All Statuses</option>
            <option value={PatientStatus.ACTIVE}>Active</option>
            <option value={PatientStatus.INACTIVE}>Inactive</option>
            <option value={PatientStatus.DISCHARGED}>Discharged</option>
          </select>
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      {loading ? (
        <div className="loading">Loading patients...</div>
      ) : patients.length === 0 ? (
        <div className="empty-state">No patients found</div>
      ) : (
        <>
          <div className="patient-table-container">
            <table className="patient-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Phone</th>
                  <th>Status</th>
                  <th>Enrollment Date</th>
                  <th>Care Program</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {patients.map((patient) => (
                  <tr
                    key={patient.id}
                    onClick={() => navigate(`/patients/${patient.id}`)}
                    className="patient-row"
                  >
                    <td>
                      {patient.first_name} {patient.last_name}
                    </td>
                    <td>{patient.email}</td>
                    <td>{patient.phone || '—'}</td>
                    <td>
                      <span className={getStatusBadgeClass(patient.status)}>
                        {patient.status}
                      </span>
                    </td>
                    <td>{new Date(patient.enrollment_date).toLocaleDateString()}</td>
                    <td>{patient.care_program || '—'}</td>
                    <td onClick={(e) => e.stopPropagation()}>
                      <button
                        className="btn btn-danger btn-sm"
                        onClick={(e) => handleDelete(patient.id, e)}
                        disabled={deletingId === patient.id}
                      >
                        {deletingId === patient.id ? 'Deleting...' : 'Delete'}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {totalPages > 1 && (
            <div className="pagination">
              <button
                className="btn btn-secondary"
                onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                disabled={currentPage === 1}
              >
                Previous
              </button>
              <span className="pagination-info">
                Page {currentPage} of {totalPages} ({totalPatients} total)
              </span>
              <button
                className="btn btn-secondary"
                onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
                disabled={currentPage === totalPages}
              >
                Next
              </button>
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default PatientList
