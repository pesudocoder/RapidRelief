from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class DisasterType(str, Enum):
    EARTHQUAKE = "earthquake"
    HURRICANE = "hurricane"
    FLOOD = "flood"
    WILDFIRE = "wildfire"
    TORNADO = "tornado"
    TSUNAMI = "tsunami"


class SeverityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Location(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    city: str
    state: str
    country: str
    population: int = Field(..., gt=0)


class DisasterScenario(BaseModel):
    disaster_type: DisasterType
    severity: SeverityLevel
    location: Location
    affected_area_km2: float = Field(..., gt=0)
    estimated_casualties: int = Field(..., ge=0)
    infrastructure_damage: str
    weather_conditions: str
    available_volunteers: int = Field(..., ge=0)
    description: str


class ResourceNeed(BaseModel):
    resource_type: str
    quantity: int
    priority: str
    estimated_cost: float
    delivery_time_hours: int


class PredictionResponse(BaseModel):
    scenario_id: str
    predicted_needs: List[ResourceNeed]
    confidence_score: float = Field(..., ge=0, le=1)
    estimated_response_time_hours: int
    risk_factors: List[str]
    generated_at: datetime


class AllocationPlan(BaseModel):
    plan_id: str
    scenario_id: str
    resource_allocations: List[ResourceNeed]
    volunteer_assignments: Dict[str, List[str]]
    timeline_hours: int
    total_cost: float
    efficiency_score: float = Field(..., ge=0, le=1)
    generated_at: datetime


class ReportData(BaseModel):
    report_id: str
    scenario_id: str
    prediction_id: str
    plan_id: str
    narrative_summary: str
    key_recommendations: List[str]
    risk_assessment: str
    cost_breakdown: Dict[str, float]
    generated_at: datetime


class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
