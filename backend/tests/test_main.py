import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "RapidRelief API" in data["message"]


def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "healthy"


def test_disaster_types_endpoint():
    """Test the disaster types endpoint"""
    response = client.get("/disaster-types")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "disaster_types" in data["data"]
    assert len(data["data"]["disaster_types"]) > 0


def test_severity_levels_endpoint():
    """Test the severity levels endpoint"""
    response = client.get("/severity-levels")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "severity_levels" in data["data"]
    assert len(data["data"]["severity_levels"]) > 0


def test_scenarios_endpoint():
    """Test the scenarios endpoint"""
    response = client.get("/scenarios")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "scenarios" in data["data"]


def test_predict_endpoint():
    """Test the predict endpoint with sample data"""
    sample_scenario = {
        "disaster_type": "earthquake",
        "severity": "high",
        "location": {
            "latitude": 34.0522,
            "longitude": -118.2437,
            "city": "Los Angeles",
            "state": "California",
            "country": "United States",
            "population": 3979576
        },
        "affected_area_km2": 150.5,
        "estimated_casualties": 2500,
        "infrastructure_damage": "Significant damage to buildings and roads",
        "weather_conditions": "Clear skies, moderate temperatures",
        "available_volunteers": 1500,
        "description": "A 7.2 magnitude earthquake has struck Los Angeles"
    }
    
    response = client.post("/predict", json=sample_scenario)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "prediction_id" in data["data"]


def test_plan_endpoint():
    """Test the plan endpoint with sample data"""
    sample_scenario = {
        "disaster_type": "hurricane",
        "severity": "critical",
        "location": {
            "latitude": 25.7617,
            "longitude": -80.1918,
            "city": "Miami",
            "state": "Florida",
            "country": "United States",
            "population": 454279
        },
        "affected_area_km2": 200.0,
        "estimated_casualties": 5000,
        "infrastructure_damage": "Extensive flooding, destroyed homes",
        "weather_conditions": "Heavy rainfall, strong winds",
        "available_volunteers": 800,
        "description": "Hurricane Maria has made landfall in Miami"
    }
    
    response = client.post("/plan", json=sample_scenario)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "scenario_id" in data["data"]


def test_report_endpoint():
    """Test the report endpoint with sample data"""
    sample_scenario = {
        "disaster_type": "flood",
        "severity": "medium",
        "location": {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "city": "New York",
            "state": "New York",
            "country": "United States",
            "population": 8336817
        },
        "affected_area_km2": 75.2,
        "estimated_casualties": 1200,
        "infrastructure_damage": "Subway system flooded, roads impassable",
        "weather_conditions": "Heavy rainfall for 48 hours",
        "available_volunteers": 2000,
        "description": "Heavy rainfall has caused severe flooding"
    }
    
    response = client.post("/report", json=sample_scenario)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "workflow_id" in data["data"]


def test_invalid_scenario_data():
    """Test endpoint with invalid data"""
    invalid_scenario = {
        "disaster_type": "invalid_type",
        "severity": "invalid_severity",
        "location": {
            "latitude": 999,  # Invalid latitude
            "longitude": -118.2437,
            "city": "",
            "state": "",
            "country": "",
            "population": -1  # Invalid population
        },
        "affected_area_km2": -1,
        "estimated_casualties": -1,
        "infrastructure_damage": "",
        "weather_conditions": "",
        "available_volunteers": -1,
        "description": ""
    }
    
    response = client.post("/predict", json=invalid_scenario)
    assert response.status_code == 422  # Validation error


def test_missing_required_fields():
    """Test endpoint with missing required fields"""
    incomplete_scenario = {
        "disaster_type": "earthquake",
        "severity": "high"
        # Missing location and other required fields
    }
    
    response = client.post("/predict", json=incomplete_scenario)
    assert response.status_code == 422  # Validation error


def test_nonexistent_scenario():
    """Test getting a non-existent scenario"""
    response = client.get("/scenarios/nonexistent-id")
    assert response.status_code == 404


def test_nonexistent_prediction():
    """Test getting a non-existent prediction"""
    response = client.get("/predictions/nonexistent-id")
    assert response.status_code == 404


def test_nonexistent_plan():
    """Test getting a non-existent plan"""
    response = client.get("/plans/nonexistent-id")
    assert response.status_code == 404


def test_nonexistent_report():
    """Test getting a non-existent report"""
    response = client.get("/reports/nonexistent-id")
    assert response.status_code == 404


def test_download_nonexistent_report():
    """Test downloading a non-existent report"""
    response = client.get("/download/nonexistent-id")
    assert response.status_code == 404
