import requests
import json
import structlog
from typing import Dict, List, Any, Optional
from datetime import datetime
import os

logger = structlog.get_logger(__name__)

# TODO(API_KEY): Replace with actual IBM Watsonx.ai Granite API credentials
GRANITE_API_KEY = os.getenv("GRANITE_API_KEY", "TODO_REPLACE_WITH_ACTUAL_API_KEY")
GRANITE_API_URL = os.getenv("GRANITE_API_URL", "https://api.watsonx.ai/v1/text/generation")
GRANITE_MODEL = os.getenv("GRANITE_MODEL", "ibm/granite-13b-instruct-v2")


class GraniteClient:
    def __init__(self):
        self.api_key = GRANITE_API_KEY
        self.api_url = GRANITE_API_URL
        self.model = GRANITE_MODEL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, prompt: str, max_tokens: int = 2048, temperature: float = 0.7) -> Dict[str, Any]:
        """Make a request to IBM Granite API"""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 0.9,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        }
        
        try:
            # TODO(API_KEY): Uncomment when API key is available
            # response = requests.post(self.api_url, headers=self.headers, json=payload)
            # response.raise_for_status()
            # return response.json()

            # Mock response for development
            logger.info("Using mock Granite response - replace with actual API call")
            return self._mock_response(prompt)

        except Exception as e:
            logger.error("Granite API request failed", error=str(e))
            raise
    
    def _mock_response(self, prompt: str) -> Dict[str, Any]:
        """Generate mock responses for development"""
        if "resource prediction" in prompt.lower():
            return {
                "choices": [{
                    "text": json.dumps({
                        "predicted_needs": [
                            {
                                "resource_type": "medical_supplies",
                                "quantity": 1500,
                                "priority": "high",
                                "estimated_cost": 75000.0,
                                "delivery_time_hours": 6
                            },
                            {
                                "resource_type": "water",
                                "quantity": 5000,
                                "priority": "critical",
                                "estimated_cost": 25000.0,
                                "delivery_time_hours": 2
                            },
                            {
                                "resource_type": "shelter",
                                "quantity": 200,
                                "priority": "high",
                                "estimated_cost": 100000.0,
                                "delivery_time_hours": 8
                            }
                        ],
                        "confidence_score": 0.87,
                        "estimated_response_time_hours": 12,
                        "risk_factors": ["infrastructure_damage", "limited_access", "weather_conditions"]
                    })
                }]
            }
        elif "allocation plan" in prompt.lower():
            return {
                "choices": [{
                    "text": json.dumps({
                        "resource_allocations": [
                            {
                                "resource_type": "medical_supplies",
                                "quantity": 1500,
                                "priority": "high",
                                "estimated_cost": 75000.0,
                                "delivery_time_hours": 6,
                                "allocation_strategy": "distributed_centers"
                            },
                            {
                                "resource_type": "water",
                                "quantity": 5000,
                                "priority": "critical",
                                "estimated_cost": 25000.0,
                                "delivery_time_hours": 2,
                                "allocation_strategy": "immediate_deployment"
                            }
                        ],
                        "volunteer_assignments": {
                            "medical_response": ["Team Alpha", "Team Beta"],
                            "logistics": ["Team Gamma"],
                            "coordination": ["Team Delta"]
                        },
                        "timeline_hours": 24,
                        "total_cost": 200000.0,
                        "efficiency_score": 0.92
                    })
                }]
            }
        else:
            return {
                "choices": [{
                    "text": "This is a comprehensive disaster response analysis generated by IBM Granite AI. The system has analyzed the scenario and provided detailed recommendations for resource allocation, volunteer coordination, and risk mitigation strategies."
                }]
            }
    
    def predict_resources(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict resource needs for a disaster scenario"""
        prompt = f"""
        Analyze the following disaster scenario and predict resource needs:
        
        Disaster Type: {scenario_data.get('disaster_type')}
        Severity: {scenario_data.get('severity')}
        Location: {scenario_data.get('location', {}).get('city')}, {scenario_data.get('location', {}).get('country')}
        Affected Area: {scenario_data.get('affected_area_km2')} km²
        Population: {scenario_data.get('location', {}).get('population')}
        Estimated Casualties: {scenario_data.get('estimated_casualties')}
        Available Volunteers: {scenario_data.get('available_volunteers')}
        
        Please provide a JSON response with:
        - predicted_needs: List of resources with type, quantity, priority, cost, delivery time
        - confidence_score: Prediction confidence (0-1)
        - estimated_response_time_hours: Estimated time to respond
        - risk_factors: List of key risk factors
        """
        
        response = self._make_request(prompt)
        result_text = response['choices'][0]['text']
        
        try:
            # Try to parse JSON from response
            if result_text.strip().startswith('{'):
                return json.loads(result_text)
            else:
                # Fallback to mock data if response is not JSON
                return {
                    "predicted_needs": [
                        {
                            "resource_type": "medical_supplies",
                            "quantity": 1500,
                            "priority": "high",
                            "estimated_cost": 75000.0,
                            "delivery_time_hours": 6
                        }
                    ],
                    "confidence_score": 0.87,
                    "estimated_response_time_hours": 12,
                    "risk_factors": ["infrastructure_damage", "limited_access"]
                }
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON response, using fallback data")
            return {
                "predicted_needs": [
                    {
                        "resource_type": "medical_supplies",
                        "quantity": 1500,
                        "priority": "high",
                        "estimated_cost": 75000.0,
                        "delivery_time_hours": 6
                    }
                ],
                "confidence_score": 0.87,
                "estimated_response_time_hours": 12,
                "risk_factors": ["infrastructure_damage", "limited_access"]
            }
    
    def generate_allocation_plan(self, scenario_data: Dict[str, Any], predicted_needs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate optimized allocation plan"""
        prompt = f"""
        Generate an optimized resource allocation plan for the following disaster scenario:
        
        Disaster Type: {scenario_data.get('disaster_type')}
        Severity: {scenario_data.get('severity')}
        Location: {scenario_data.get('location', {}).get('city')}, {scenario_data.get('location', {}).get('country')}
        Available Volunteers: {scenario_data.get('available_volunteers')}
        
        Predicted Resource Needs:
        {json.dumps(predicted_needs, indent=2)}
        
        Please provide a JSON response with:
        - resource_allocations: Optimized allocation of resources
        - volunteer_assignments: Team assignments for different tasks
        - timeline_hours: Estimated timeline for deployment
        - total_cost: Total estimated cost
        - efficiency_score: Plan efficiency score (0-1)
        """
        
        response = self._make_request(prompt)
        result_text = response['choices'][0]['text']
        
        try:
            # Try to parse JSON from response
            if result_text.strip().startswith('{'):
                return json.loads(result_text)
            else:
                # Fallback to mock data if response is not JSON
                return {
                    "resource_allocations": [
                        {
                            "resource_type": "medical_supplies",
                            "quantity": 1500,
                            "priority": "high",
                            "estimated_cost": 75000.0,
                            "delivery_time_hours": 6,
                            "allocation_strategy": "distributed_centers"
                        }
                    ],
                    "volunteer_assignments": {
                        "medical_response": ["Team Alpha", "Team Beta"],
                        "logistics": ["Team Gamma"]
                    },
                    "timeline_hours": 24,
                    "total_cost": 200000.0,
                    "efficiency_score": 0.92
                }
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON response, using fallback data")
            return {
                "resource_allocations": [
                    {
                        "resource_type": "medical_supplies",
                        "quantity": 1500,
                        "priority": "high",
                        "estimated_cost": 75000.0,
                        "delivery_time_hours": 6,
                        "allocation_strategy": "distributed_centers"
                    }
                ],
                "volunteer_assignments": {
                    "medical_response": ["Team Alpha", "Team Beta"],
                    "logistics": ["Team Gamma"]
                },
                "timeline_hours": 24,
                "total_cost": 200000.0,
                "efficiency_score": 0.92
            }
    
    def generate_narrative_report(self, scenario_data: Dict[str, Any], prediction_result: Dict[str, Any], allocation_result: Dict[str, Any]) -> str:
        """Generate narrative report"""
        prompt = f"""
        Generate a comprehensive narrative report for the disaster response scenario:
        
        Scenario: {scenario_data.get('disaster_type')} - {scenario_data.get('severity')} severity in {scenario_data.get('location', {}).get('city')}, {scenario_data.get('location', {}).get('country')}
        
        Prediction Results:
        - Confidence: {prediction_result.get('confidence_score', 0):.1%}
        - Response Time: {prediction_result.get('estimated_response_time_hours', 0)} hours
        - Risk Factors: {', '.join(prediction_result.get('risk_factors', []))}
        
        Allocation Plan:
        - Efficiency: {allocation_result.get('efficiency_score', 0):.1%}
        - Total Cost: ${allocation_result.get('total_cost', 0):,.2f}
        - Timeline: {allocation_result.get('timeline_hours', 0)} hours
        
        Please provide a professional narrative analysis suitable for decision-makers.
        """
        
        response = self._make_request(prompt)
        return response['choices'][0]['text']
