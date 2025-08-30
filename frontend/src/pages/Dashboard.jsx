import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Plus, Eye, Download, AlertTriangle, MapPin, Users, Calendar } from 'lucide-react'
import { toast } from 'react-hot-toast'
import axios from 'axios'

const Dashboard = () => {
  const [scenarios, setScenarios] = useState([])
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState({
    total: 0,
    critical: 0,
    high: 0,
    medium: 0,
    low: 0
  })

  useEffect(() => {
    fetchScenarios()
  }, [])

  const fetchScenarios = async () => {
    try {
      setLoading(true)
      const response = await axios.get('/api/scenarios')
      const scenariosData = response.data.data.scenarios || []
      setScenarios(scenariosData)
      
      // Calculate stats
      const statsData = {
        total: scenariosData.length,
        critical: scenariosData.filter(s => s.severity === 'critical').length,
        high: scenariosData.filter(s => s.severity === 'high').length,
        medium: scenariosData.filter(s => s.severity === 'medium').length,
        low: scenariosData.filter(s => s.severity === 'low').length
      }
      setStats(statsData)
    } catch (error) {
      console.error('Error fetching scenarios:', error)
      toast.error('Failed to load scenarios')
    } finally {
      setLoading(false)
    }
  }

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'badge-danger'
      case 'high': return 'badge-warning'
      case 'medium': return 'badge-info'
      case 'low': return 'badge-success'
      default: return 'badge-info'
    }
  }

  const getDisasterIcon = (type) => {
    switch (type) {
      case 'earthquake': return '🌋'
      case 'hurricane': return '🌀'
      case 'flood': return '🌊'
      case 'wildfire': return '🔥'
      case 'tornado': return '🌪️'
      case 'tsunami': return '🌊'
      default: return '⚠️'
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Disaster Response Dashboard</h1>
          <p className="text-gray-600 mt-2">AI-powered disaster response planning with IBM Granite</p>
        </div>
        <Link to="/scenario" className="btn-primary flex items-center space-x-2">
          <Plus className="h-4 w-4" />
          <span>New Scenario</span>
        </Link>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Scenarios</p>
              <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
            </div>
            <AlertTriangle className="h-8 w-8 text-gray-400" />
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Critical</p>
              <p className="text-2xl font-bold text-red-600">{stats.critical}</p>
            </div>
            <div className="h-8 w-8 bg-red-100 rounded-full flex items-center justify-center">
              <AlertTriangle className="h-4 w-4 text-red-600" />
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">High</p>
              <p className="text-2xl font-bold text-orange-600">{stats.high}</p>
            </div>
            <div className="h-8 w-8 bg-orange-100 rounded-full flex items-center justify-center">
              <AlertTriangle className="h-4 w-4 text-orange-600" />
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Medium</p>
              <p className="text-2xl font-bold text-blue-600">{stats.medium}</p>
            </div>
            <div className="h-8 w-8 bg-blue-100 rounded-full flex items-center justify-center">
              <AlertTriangle className="h-4 w-4 text-blue-600" />
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Low</p>
              <p className="text-2xl font-bold text-green-600">{stats.low}</p>
            </div>
            <div className="h-8 w-8 bg-green-100 rounded-full flex items-center justify-center">
              <AlertTriangle className="h-4 w-4 text-green-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Scenarios List */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Recent Disaster Scenarios</h2>
        </div>
        
        {scenarios.length === 0 ? (
          <div className="text-center py-12">
            <AlertTriangle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No scenarios yet</h3>
            <p className="text-gray-600 mb-4">Create your first disaster response scenario to get started.</p>
            <Link to="/scenario" className="btn-primary">
              Create Scenario
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {scenarios.map((scenario) => (
              <div key={scenario.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="text-2xl">
                      {getDisasterIcon(scenario.disaster_type)}
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900 capitalize">
                        {scenario.disaster_type} - {scenario.severity} Severity
                      </h3>
                      <div className="flex items-center space-x-4 text-sm text-gray-600 mt-1">
                        <div className="flex items-center space-x-1">
                          <MapPin className="h-4 w-4" />
                          <span>{scenario.location.city}, {scenario.location.country}</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <Users className="h-4 w-4" />
                          <span>{scenario.location.population.toLocaleString()}</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <Calendar className="h-4 w-4" />
                          <span>{new Date(scenario.created_at).toLocaleDateString()}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <span className={`badge ${getSeverityColor(scenario.severity)}`}>
                      {scenario.severity}
                    </span>
                    <Link
                      to={`/reports/${scenario.id}`}
                      className="btn-secondary flex items-center space-x-1"
                    >
                      <Eye className="h-4 w-4" />
                      <span>View</span>
                    </Link>
                  </div>
                </div>
                
                <div className="mt-3 grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  <div>
                    <span className="text-gray-600">Affected Area:</span>
                    <span className="ml-1 font-medium">{scenario.affected_area_km2} km²</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Casualties:</span>
                    <span className="ml-1 font-medium">{scenario.estimated_casualties.toLocaleString()}</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Volunteers:</span>
                    <span className="ml-1 font-medium">{scenario.available_volunteers.toLocaleString()}</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Status:</span>
                    <span className="ml-1 font-medium text-green-600">Active</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Quick Actions */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Quick Actions</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Link
            to="/scenario"
            className="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <div className="h-10 w-10 bg-primary-100 rounded-lg flex items-center justify-center">
              <Plus className="h-5 w-5 text-primary-600" />
            </div>
            <div>
              <h3 className="font-medium text-gray-900">Create New Scenario</h3>
              <p className="text-sm text-gray-600">Plan response for a new disaster</p>
            </div>
          </Link>
          
          <div className="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg bg-gray-50">
            <div className="h-10 w-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <Download className="h-5 w-5 text-blue-600" />
            </div>
            <div>
              <h3 className="font-medium text-gray-900">Download Reports</h3>
              <p className="text-sm text-gray-600">Access PDF reports and data</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg bg-gray-50">
            <div className="h-10 w-10 bg-green-100 rounded-lg flex items-center justify-center">
              <AlertTriangle className="h-5 w-5 text-green-600" />
            </div>
            <div>
              <h3 className="font-medium text-gray-900">Monitor Alerts</h3>
              <p className="text-sm text-gray-600">Real-time disaster alerts</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
