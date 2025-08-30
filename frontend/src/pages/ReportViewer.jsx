import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { Download, ArrowLeft, FileText, AlertTriangle, MapPin, Users, Calendar, DollarSign, Clock } from 'lucide-react'
import { toast } from 'react-hot-toast'
import axios from 'axios'

const ReportViewer = () => {
  const { reportId } = useParams()
  const [report, setReport] = useState(null)
  const [scenario, setScenario] = useState(null)
  const [prediction, setPrediction] = useState(null)
  const [plan, setPlan] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchReportData()
  }, [reportId])

  const fetchReportData = async () => {
    try {
      setLoading(true)
      
      // Fetch report data
      const reportResponse = await axios.get(`/api/reports/${reportId}`)
      const reportData = reportResponse.data.data.report
      setReport(reportData)

      // Fetch related data
      const [scenarioResponse, predictionResponse, planResponse] = await Promise.all([
        axios.get(`/api/scenarios/${reportData.scenario_id}`),
        axios.get(`/api/predictions/${reportData.prediction_id}`),
        axios.get(`/api/plans/${reportData.plan_id}`)
      ])

      setScenario(scenarioResponse.data.data.scenario)
      setPrediction(predictionResponse.data.data.prediction)
      setPlan(planResponse.data.data.plan)

    } catch (error) {
      console.error('Error fetching report data:', error)
      toast.error('Failed to load report data')
    } finally {
      setLoading(false)
    }
  }

  const downloadReport = async () => {
    try {
      const response = await axios.get(`/api/download/${reportId}`, {
        responseType: 'blob'
      })
      
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `disaster_response_report_${reportId}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
      
      toast.success('Report downloaded successfully!')
    } catch (error) {
      console.error('Error downloading report:', error)
      toast.error('Failed to download report')
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

  if (!report || !scenario) {
    return (
      <div className="text-center py-12">
        <AlertTriangle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">Report not found</h3>
        <p className="text-gray-600 mb-4">The requested report could not be found.</p>
        <Link to="/" className="btn-primary">
          Return to Dashboard
        </Link>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Link to="/" className="btn-secondary flex items-center space-x-2">
            <ArrowLeft className="h-4 w-4" />
            <span>Back to Dashboard</span>
          </Link>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Disaster Response Report</h1>
            <p className="text-gray-600 mt-1">AI-generated analysis and recommendations</p>
          </div>
        </div>
        <button
          onClick={downloadReport}
          className="btn-primary flex items-center space-x-2"
        >
          <Download className="h-4 w-4" />
          <span>Download PDF</span>
        </button>
      </div>

      {/* Report Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Scenario Summary */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Scenario Summary</h2>
          </div>
          <div className="space-y-4">
            <div className="flex items-center space-x-3">
              <div className="text-3xl">
                {getDisasterIcon(scenario.disaster_type)}
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 capitalize">
                  {scenario.disaster_type}
                </h3>
                <span className={`badge ${getSeverityColor(scenario.severity)}`}>
                  {scenario.severity} severity
                </span>
              </div>
            </div>
            
            <div className="space-y-2 text-sm">
              <div className="flex items-center space-x-2">
                <MapPin className="h-4 w-4 text-gray-500" />
                <span>{scenario.location.city}, {scenario.location.country}</span>
              </div>
              <div className="flex items-center space-x-2">
                <Users className="h-4 w-4 text-gray-500" />
                <span>{scenario.location.population.toLocaleString()} population</span>
              </div>
              <div className="flex items-center space-x-2">
                <Calendar className="h-4 w-4 text-gray-500" />
                <span>{new Date(scenario.created_at).toLocaleDateString()}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Prediction Summary */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">AI Predictions</h2>
          </div>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Confidence Score</span>
              <span className="font-semibold text-gray-900">
                {(prediction.confidence_score * 100).toFixed(1)}%
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Response Time</span>
              <span className="font-semibold text-gray-900">
                {prediction.estimated_response_time_hours} hours
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Resource Types</span>
              <span className="font-semibold text-gray-900">
                {prediction.predicted_needs.length}
              </span>
            </div>
            <div>
              <span className="text-sm text-gray-600">Risk Factors</span>
              <div className="mt-1 space-y-1">
                {prediction.risk_factors.map((risk, index) => (
                  <div key={index} className="text-xs bg-red-50 text-red-700 px-2 py-1 rounded">
                    {risk}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Plan Summary */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Allocation Plan</h2>
          </div>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Efficiency Score</span>
              <span className="font-semibold text-gray-900">
                {(plan.efficiency_score * 100).toFixed(1)}%
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Total Cost</span>
              <span className="font-semibold text-gray-900">
                ${plan.total_cost.toLocaleString()}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Timeline</span>
              <span className="font-semibold text-gray-900">
                {plan.timeline_hours} hours
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Volunteer Teams</span>
              <span className="font-semibold text-gray-900">
                {Object.keys(plan.volunteer_assignments).length}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Detailed Sections */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Resource Predictions */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Predicted Resource Needs</h2>
          </div>
          <div className="space-y-3">
            {prediction.predicted_needs.map((need, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-medium text-gray-900 capitalize">
                    {need.resource_type.replace('_', ' ')}
                  </h4>
                  <span className={`badge ${
                    need.priority === 'critical' ? 'badge-danger' :
                    need.priority === 'high' ? 'badge-warning' :
                    need.priority === 'medium' ? 'badge-info' : 'badge-success'
                  }`}>
                    {need.priority}
                  </span>
                </div>
                <div className="grid grid-cols-3 gap-4 text-sm">
                  <div>
                    <span className="text-gray-600">Quantity:</span>
                    <span className="ml-1 font-medium">{need.quantity.toLocaleString()}</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Cost:</span>
                    <span className="ml-1 font-medium">${need.estimated_cost.toLocaleString()}</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Delivery:</span>
                    <span className="ml-1 font-medium">{need.delivery_time_hours}h</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Allocation Plan */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Resource Allocations</h2>
          </div>
          <div className="space-y-3">
            {plan.resource_allocations.map((allocation, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-medium text-gray-900 capitalize">
                    {allocation.resource_type.replace('_', ' ')}
                  </h4>
                  <span className={`badge ${
                    allocation.priority === 'critical' ? 'badge-danger' :
                    allocation.priority === 'high' ? 'badge-warning' :
                    allocation.priority === 'medium' ? 'badge-info' : 'badge-success'
                  }`}>
                    {allocation.priority}
                  </span>
                </div>
                <div className="grid grid-cols-3 gap-4 text-sm">
                  <div>
                    <span className="text-gray-600">Quantity:</span>
                    <span className="ml-1 font-medium">{allocation.quantity.toLocaleString()}</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Cost:</span>
                    <span className="ml-1 font-medium">${allocation.estimated_cost.toLocaleString()}</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Delivery:</span>
                    <span className="ml-1 font-medium">{allocation.delivery_time_hours}h</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Volunteer Assignments */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Volunteer Team Assignments</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {Object.entries(plan.volunteer_assignments).map(([task, teams]) => (
            <div key={task} className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-medium text-gray-900 mb-2 capitalize">
                {task.replace('_', ' ')}
              </h4>
              <div className="space-y-1">
                {teams.map((team, index) => (
                  <div key={index} className="text-sm bg-blue-50 text-blue-700 px-2 py-1 rounded">
                    {team}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Narrative Analysis */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">AI-Generated Narrative Analysis</h2>
        </div>
        <div className="prose max-w-none">
          <p className="text-gray-700 leading-relaxed">
            {report.narrative_summary}
          </p>
        </div>
      </div>

      {/* Key Recommendations */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Key Recommendations</h2>
        </div>
        <div className="space-y-3">
          {report.key_recommendations.map((recommendation, index) => (
            <div key={index} className="flex items-start space-x-3">
              <div className="flex-shrink-0 w-6 h-6 bg-primary-100 rounded-full flex items-center justify-center">
                <span className="text-primary-600 text-sm font-medium">{index + 1}</span>
              </div>
              <p className="text-gray-700">{recommendation}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Cost Breakdown */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Cost Breakdown</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {Object.entries(report.cost_breakdown).map(([category, cost]) => (
            <div key={category} className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-medium text-gray-900 capitalize mb-2">
                {category.replace('_', ' ')}
              </h4>
              <p className="text-2xl font-bold text-primary-600">
                ${cost.toLocaleString()}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Risk Assessment */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Risk Assessment</h2>
        </div>
        <div className="prose max-w-none">
          <p className="text-gray-700 leading-relaxed">
            {report.risk_assessment}
          </p>
        </div>
      </div>
    </div>
  )
}

export default ReportViewer
