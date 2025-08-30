import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { Shield, BarChart3, FileText, Home } from 'lucide-react'
import Dashboard from './pages/Dashboard'
import ScenarioForm from './pages/ScenarioForm'
import ReportViewer from './pages/ReportViewer'
import Navigation from './components/Navigation'

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      <main className="container mx-auto px-4 py-8">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/scenario" element={<ScenarioForm />} />
          <Route path="/reports/:reportId" element={<ReportViewer />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
