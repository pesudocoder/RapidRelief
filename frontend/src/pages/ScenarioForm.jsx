import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { Save, AlertTriangle, MapPin, Users, Calendar, FileText } from 'lucide-react'
import { toast } from 'react-hot-toast'
import axios from 'axios'

const ScenarioForm = () => {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [disasterTypes, setDisasterTypes] = useState([])
  const [severityLevels, setSeverityLevels] = useState([])
  const [actionType, setActionType] = useState('predict') // predict, plan, report

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
    setValue,
    reset
  } = useForm()

  useEffect(() => {
    fetchFormOptions()
  }, [])

  const fetchFormOptions = async () => {
    try {
      const [typesResponse, severityResponse] = await Promise.all([
        axios.get('/api/disaster-types'),
        axios.get('/api/severity-levels')
      ])
      
      setDisasterTypes(typesResponse.data.data.disaster_types || [])
      setSeverityLevels(severityResponse.data.data.severity_levels || [])
    } catch (error) {
      console.error('Error fetching form options:', error)
      toast.error('Failed to load form options')
    }
  }

  const onSubmit = async (data) => {
    try {
      setLoading(true)
      
      // Prepare scenario data
      const scenarioData = {
        disaster_type: data.disaster_type,
        severity: data.severity,
        location: {
          latitude: parseFloat(data.latitude),
          longitude: parseFloat(data.longitude),
          city: data.city,
          state: data.state,
          country: data.country,
          population: parseInt(data.population)
        },
        affected_area_km2: parseFloat(data.affected_area_km2),
        estimated_casualties: parseInt(data.estimated_casualties),
        infrastructure_damage: data.infrastructure_damage,
        weather_conditions: data.weather_conditions,
        available_volunteers: parseInt(data.available_volunteers),
        description: data.description
      }

      let response
      switch (actionType) {
        case 'predict':
          response = await axios.post('/api/predict', scenarioData)
          toast.success('Resource prediction completed!')
          break
        case 'plan':
          response = await axios.post('/api/plan', scenarioData)
          toast.success('Allocation plan generated!')
          break
        case 'report':
          response = await axios.post('/api/report', scenarioData)
          toast.success('Comprehensive report generated!')
          // Navigate to report viewer
          if (response.data.data?.report_id) {
            navigate(`/reports/${response.data.data.report_id}`)
            return
          }
          break
        default:
          response = await axios.post('/api/predict', scenarioData)
          toast.success('Resource prediction completed!')
      }

      // Reset form
      reset()
      toast.success('Scenario submitted successfully!')
      
    } catch (error) {
      console.error('Error submitting scenario:', error)
      toast.error(error.response?.data?.detail || 'Failed to submit scenario')
    } finally {
      setLoading(false)
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

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'text-red-600'
      case 'high': return 'text-orange-600'
      case 'medium': return 'text-blue-600'
      case 'low': return 'text-green-600'
      default: return 'text-gray-600'
    }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900">Create Disaster Response Scenario</h1>
        <p className="text-gray-600 mt-2">AI-powered planning with IBM Granite and Agent Development Kit</p>
      </div>

      {/* Action Type Selector */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Select Action Type</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[
            { value: 'predict', label: 'Resource Prediction', icon: AlertTriangle, description: 'Predict resource needs' },
            { value: 'plan', label: 'Allocation Plan', icon: MapPin, description: 'Generate optimized plan' },
            { value: 'report', label: 'Full Report', icon: FileText, description: 'Complete analysis & PDF' }
          ].map((action) => (
            <button
              key={action.value}
              onClick={() => setActionType(action.value)}
              className={`p-4 border rounded-lg text-left transition-colors ${
                actionType === action.value
                  ? 'border-primary-500 bg-primary-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center space-x-3">
                <div className={`h-10 w-10 rounded-lg flex items-center justify-center ${
                  actionType === action.value ? 'bg-primary-100' : 'bg-gray-100'
                }`}>
                  <action.icon className={`h-5 w-5 ${
                    actionType === action.value ? 'text-primary-600' : 'text-gray-600'
                  }`} />
                </div>
                <div>
                  <h3 className={`font-medium ${
                    actionType === action.value ? 'text-primary-900' : 'text-gray-900'
                  }`}>
                    {action.label}
                  </h3>
                  <p className="text-sm text-gray-600">{action.description}</p>
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Scenario Form */}
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Disaster Information */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Disaster Information</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Disaster Type *
              </label>
              <select
                {...register('disaster_type', { required: 'Disaster type is required' })}
                className="input-field"
              >
                <option value="">Select disaster type</option>
                {disasterTypes.map((type) => (
                  <option key={type} value={type}>
                    {getDisasterIcon(type)} {type.charAt(0).toUpperCase() + type.slice(1)}
                  </option>
                ))}
              </select>
              {errors.disaster_type && (
                <p className="text-red-600 text-sm mt-1">{errors.disaster_type.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Severity Level *
              </label>
              <select
                {...register('severity', { required: 'Severity level is required' })}
                className="input-field"
              >
                <option value="">Select severity level</option>
                {severityLevels.map((level) => (
                  <option key={level} value={level}>
                    <span className={getSeverityColor(level)}>
                      {level.charAt(0).toUpperCase() + level.slice(1)}
                    </span>
                  </option>
                ))}
              </select>
              {errors.severity && (
                <p className="text-red-600 text-sm mt-1">{errors.severity.message}</p>
              )}
            </div>
          </div>
        </div>

        {/* Location Information */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Location Information</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                City *
              </label>
              <input
                type="text"
                {...register('city', { required: 'City is required' })}
                className="input-field"
                placeholder="Enter city name"
              />
              {errors.city && (
                <p className="text-red-600 text-sm mt-1">{errors.city.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                State/Province *
              </label>
              <input
                type="text"
                {...register('state', { required: 'State/Province is required' })}
                className="input-field"
                placeholder="Enter state or province"
              />
              {errors.state && (
                <p className="text-red-600 text-sm mt-1">{errors.state.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Country *
              </label>
              <input
                type="text"
                {...register('country', { required: 'Country is required' })}
                className="input-field"
                placeholder="Enter country name"
              />
              {errors.country && (
                <p className="text-red-600 text-sm mt-1">{errors.country.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Population *
              </label>
              <input
                type="number"
                {...register('population', { 
                  required: 'Population is required',
                  min: { value: 1, message: 'Population must be greater than 0' }
                })}
                className="input-field"
                placeholder="Enter population"
              />
              {errors.population && (
                <p className="text-red-600 text-sm mt-1">{errors.population.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Latitude *
              </label>
              <input
                type="number"
                step="any"
                {...register('latitude', { 
                  required: 'Latitude is required',
                  min: { value: -90, message: 'Latitude must be between -90 and 90' },
                  max: { value: 90, message: 'Latitude must be between -90 and 90' }
                })}
                className="input-field"
                placeholder="Enter latitude (-90 to 90)"
              />
              {errors.latitude && (
                <p className="text-red-600 text-sm mt-1">{errors.latitude.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Longitude *
              </label>
              <input
                type="number"
                step="any"
                {...register('longitude', { 
                  required: 'Longitude is required',
                  min: { value: -180, message: 'Longitude must be between -180 and 180' },
                  max: { value: 180, message: 'Longitude must be between -180 and 180' }
                })}
                className="input-field"
                placeholder="Enter longitude (-180 to 180)"
              />
              {errors.longitude && (
                <p className="text-red-600 text-sm mt-1">{errors.longitude.message}</p>
              )}
            </div>
          </div>
        </div>

        {/* Impact Assessment */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Impact Assessment</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Affected Area (km²) *
              </label>
              <input
                type="number"
                step="0.1"
                {...register('affected_area_km2', { 
                  required: 'Affected area is required',
                  min: { value: 0.1, message: 'Affected area must be greater than 0' }
                })}
                className="input-field"
                placeholder="Enter affected area in km²"
              />
              {errors.affected_area_km2 && (
                <p className="text-red-600 text-sm mt-1">{errors.affected_area_km2.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Estimated Casualties *
              </label>
              <input
                type="number"
                {...register('estimated_casualties', { 
                  required: 'Estimated casualties is required',
                  min: { value: 0, message: 'Casualties cannot be negative' }
                })}
                className="input-field"
                placeholder="Enter estimated casualties"
              />
              {errors.estimated_casualties && (
                <p className="text-red-600 text-sm mt-1">{errors.estimated_casualties.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Available Volunteers *
              </label>
              <input
                type="number"
                {...register('available_volunteers', { 
                  required: 'Available volunteers is required',
                  min: { value: 0, message: 'Volunteers cannot be negative' }
                })}
                className="input-field"
                placeholder="Enter number of available volunteers"
              />
              {errors.available_volunteers && (
                <p className="text-red-600 text-sm mt-1">{errors.available_volunteers.message}</p>
              )}
            </div>
          </div>

          <div className="mt-6 space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Infrastructure Damage *
              </label>
              <textarea
                {...register('infrastructure_damage', { required: 'Infrastructure damage description is required' })}
                className="input-field"
                rows="3"
                placeholder="Describe the extent of infrastructure damage..."
              />
              {errors.infrastructure_damage && (
                <p className="text-red-600 text-sm mt-1">{errors.infrastructure_damage.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Weather Conditions *
              </label>
              <textarea
                {...register('weather_conditions', { required: 'Weather conditions description is required' })}
                className="input-field"
                rows="3"
                placeholder="Describe current weather conditions..."
              />
              {errors.weather_conditions && (
                <p className="text-red-600 text-sm mt-1">{errors.weather_conditions.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Scenario Description *
              </label>
              <textarea
                {...register('description', { required: 'Scenario description is required' })}
                className="input-field"
                rows="4"
                placeholder="Provide a detailed description of the disaster scenario..."
              />
              {errors.description && (
                <p className="text-red-600 text-sm mt-1">{errors.description.message}</p>
              )}
            </div>
          </div>
        </div>

        {/* Submit Button */}
        <div className="flex justify-end space-x-4">
          <button
            type="button"
            onClick={() => navigate('/')}
            className="btn-secondary"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={loading}
            className="btn-primary flex items-center space-x-2"
          >
            {loading ? (
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
            ) : (
              <Save className="h-4 w-4" />
            )}
            <span>
              {loading ? 'Processing...' : 
               actionType === 'predict' ? 'Predict Resources' :
               actionType === 'plan' ? 'Generate Plan' : 'Generate Report'
              }
            </span>
          </button>
        </div>
      </form>
    </div>
  )
}

export default ScenarioForm
