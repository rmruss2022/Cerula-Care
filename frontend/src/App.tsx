import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import PatientList from './components/PatientList'
import PatientDetail from './components/PatientDetail'
import './App.css'

function App() {
  return (
    <Router>
      <div className="app">
        <header className="app-header">
          <h1>Patient Care Dashboard</h1>
        </header>
        <main className="app-main">
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
