import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getPatients, deletePatient } from '../api/patients'
import { Patient, PatientStatus } from '../types'

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
    const baseClasses = 'inline-block rounded-xl text-sm font-medium capitalize'
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

  return (
    <div className="w-full">
      <div className="flex justify-between items-center mb-8">
        <h2 className="text-[2rem] text-[#2c3e50]">Patients</h2>
        <button 
          className="px-4 py-2 bg-[#007bff] text-white rounded border-none text-base cursor-pointer transition-colors duration-200 hover:bg-[#0056b3] disabled:opacity-50 disabled:cursor-not-allowed" 
          onClick={() => navigate('/patients/new')}
        >
          + Add Patient
        </button>
      </div>

      <div className="flex gap-4 mb-6 items-center">
        <div className="flex-1">
          <input
            type="text"
            placeholder="Search by name, email, or phone..."
            value={search}
            onChange={handleSearchChange}
            className="w-full rounded border border-[#ddd] text-base p-3"
          />
        </div>
        <div className="min-w-[200px]">
          <select
            value={statusFilter}
            onChange={handleStatusFilterChange}
            className="w-full rounded border border-[#ddd] bg-white text-base p-3"
          >
            <option value="">All Statuses</option>
            <option value={PatientStatus.ACTIVE}>Active</option>
            <option value={PatientStatus.INACTIVE}>Inactive</option>
            <option value={PatientStatus.DISCHARGED}>Discharged</option>
          </select>
        </div>
      </div>

      {error && (
        <div className="rounded p-4 mb-4 border text-[#dc3545] bg-[#f8d7da] border-[#f5c6cb]">
          {error}
        </div>
      )}

      {loading ? (
        <div className="text-center py-12 text-[#6c757d]">Loading patients...</div>
      ) : patients.length === 0 ? (
        <div className="text-center py-12 text-[#6c757d]">No patients found</div>
      ) : (
        <>
          <div className="overflow-x-auto bg-white rounded-lg shadow-[0_2px_4px_rgba(0,0,0,0.1)]">
            <table className="w-full border-collapse">
              <thead className="bg-[#f8f9fa]">
                <tr>
                  <th className="p-4 text-left font-semibold text-[#495057] border-b-2 border-[#dee2e6]">Name</th>
                  <th className="p-4 text-left font-semibold text-[#495057] border-b-2 border-[#dee2e6]">Email</th>
                  <th className="p-4 text-left font-semibold text-[#495057] border-b-2 border-[#dee2e6]">Phone</th>
                  <th className="p-4 text-left font-semibold text-[#495057] border-b-2 border-[#dee2e6]">Status</th>
                  <th className="p-4 text-left font-semibold text-[#495057] border-b-2 border-[#dee2e6]">Enrollment Date</th>
                  <th className="p-4 text-left font-semibold text-[#495057] border-b-2 border-[#dee2e6]">Care Program</th>
                  <th className="p-4 text-left font-semibold text-[#495057] border-b-2 border-[#dee2e6]">Actions</th>
                </tr>
              </thead>
              <tbody>
                {patients.map((patient) => (
                  <tr
                    key={patient.id}
                    onClick={() => navigate(`/patients/${patient.id}`)}
                    className="cursor-pointer transition-colors duration-200 border-b border-[#dee2e6] hover:bg-[#f8f9fa]"
                  >
                    <td className="p-4">
                      {patient.first_name} {patient.last_name}
                    </td>
                    <td className="p-4">{patient.email}</td>
                    <td className="p-4">{patient.phone || '—'}</td>
                    <td className="p-4">
                      <span className={getStatusBadgeClass(patient.status)}>
                        {patient.status}
                      </span>
                    </td>
                    <td className="p-4">{new Date(patient.enrollment_date).toLocaleDateString()}</td>
                    <td className="p-4">{patient.care_program || '—'}</td>
                    <td className="p-4" onClick={(e) => e.stopPropagation()}>
                      <button
                        className="px-2 py-1 bg-[#dc3545] text-white rounded border-none text-sm cursor-pointer transition-colors duration-200 hover:bg-[#c82333] disabled:opacity-50 disabled:cursor-not-allowed"
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
            <div className="flex justify-center items-center gap-4 mt-8">
              <button
                className="px-4 py-2 bg-[#6c757d] text-white rounded border-none text-base cursor-pointer transition-colors duration-200 hover:bg-[#5a6268] disabled:opacity-50 disabled:cursor-not-allowed"
                onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                disabled={currentPage === 1}
              >
                Previous
              </button>
              <span className="text-sm text-[#6c757d]">
                Page {currentPage} of {totalPages} ({totalPatients} total)
              </span>
              <button
                className="px-4 py-2 bg-[#6c757d] text-white rounded border-none text-base cursor-pointer transition-colors duration-200 hover:bg-[#5a6268] disabled:opacity-50 disabled:cursor-not-allowed"
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
