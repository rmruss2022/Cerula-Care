import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import PatientList from './components/PatientList'
import PatientDetail from './components/PatientDetail'

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col">
        <header className="text-white px-8 py-4 shadow-[0_2px_4px_rgba(0,0,0,0.1)]" style={{ backgroundColor: '#2c3e50' }}>
          <h1 className="text-2xl font-semibold">Patient Care Dashboard</h1>
        </header>
        <main className="flex-1 max-w-[1400px] w-full mx-auto p-8 md:p-4">
          <Routes>
            <Route path="/" element={<PatientList />} />
            <Route path="/patients/:id" element={<PatientDetail />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
