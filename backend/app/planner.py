import structlog
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid
from .granite_client import GraniteClient
from .agentic_workflow import AgenticWorkflow
from .db import SessionLocal, Scenario, Prediction, Plan, Report
from .utils.logger import log_workflow_step, log_error

logger = structlog.get_logger(__name__)


class DisasterResponsePlanner:
    """Main planning coordinator for disaster response scenarios"""
    
    def __init__(self):
        self.granite_client = GraniteClient()
        self.workflow = AgenticWorkflow()
    
    async def predict_resources(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict resource needs for a disaster scenario"""
        try:
            logger.info("Starting resource prediction", scenario_type=scenario_data.get('disaster_type'))
            
            # Call Granite for resource prediction
            prediction_result = self.granite_client.predict_resources(scenario_data)
            
            # Save prediction to database
            prediction_id = str(uuid.uuid4())
            db = SessionLocal()
            try:
                prediction = Prediction(
                    id=prediction_id,
                    scenario_id=scenario_data.get('id'),
                    predicted_needs=prediction_result['predicted_needs'],
                    confidence_score=prediction_result['confidence_score'],
                    estimated_response_time_hours=prediction_result['estimated_response_time_hours'],
                    risk_factors=prediction_result['risk_factors']
                )
                db.add(prediction)
                db.commit()
                
                logger.info("Resource prediction completed", 
                           prediction_id=prediction_id,
                           confidence=prediction_result['confidence_score'])
                
                return {
                    'prediction_id': prediction_id,
                    'predicted_needs': prediction_result['predicted_needs'],
                    'confidence_score': prediction_result['confidence_score'],
                    'estimated_response_time_hours': prediction_result['estimated_response_time_hours'],
                    'risk_factors': prediction_result['risk_factors'],
                    'generated_at': datetime.utcnow().isoformat()
                }
                
            finally:
                db.close()
                
        except Exception as e:
            log_error(logger, e, context={'operation': 'predict_resources'})
            raise
    
    async def generate_allocation_plan(self, scenario_data: Dict[str, Any], 
                                     predicted_needs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate optimized allocation plan"""
        try:
            logger.info("Starting allocation plan generation", scenario_type=scenario_data.get('disaster_type'))
            
            # Call Granite for allocation planning
            allocation_result = self.granite_client.generate_allocation_plan(scenario_data, predicted_needs)
            
            # Save plan to database
            plan_id = str(uuid.uuid4())
            db = SessionLocal()
            try:
                plan = Plan(
                    id=plan_id,
                    scenario_id=scenario_data.get('id'),
                    resource_allocations=allocation_result['resource_allocations'],
                    volunteer_assignments=allocation_result['volunteer_assignments'],
                    timeline_hours=allocation_result['timeline_hours'],
                    total_cost=allocation_result['total_cost'],
                    efficiency_score=allocation_result['efficiency_score']
                )
                db.add(plan)
                db.commit()
                
                logger.info("Allocation plan generated", 
                           plan_id=plan_id,
                           efficiency=allocation_result['efficiency_score'])
                
                return {
                    'plan_id': plan_id,
                    'resource_allocations': allocation_result['resource_allocations'],
                    'volunteer_assignments': allocation_result['volunteer_assignments'],
                    'timeline_hours': allocation_result['timeline_hours'],
                    'total_cost': allocation_result['total_cost'],
                    'efficiency_score': allocation_result['efficiency_score'],
                    'generated_at': datetime.utcnow().isoformat()
                }
                
            finally:
                db.close()
                
        except Exception as e:
            log_error(logger, e, context={'operation': 'generate_allocation_plan'})
            raise
    
    async def generate_report(self, scenario_data: Dict[str, Any], 
                            prediction_result: Dict[str, Any], 
                            allocation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive report"""
        try:
            logger.info("Starting report generation", scenario_type=scenario_data.get('disaster_type'))
            
            # Generate narrative using Granite
            narrative = self.granite_client.generate_narrative_report(
                scenario_data, prediction_result, allocation_result
            )
            
            # Generate PDF report
            from .utils.report import ReportGenerator
            report_generator = ReportGenerator()
            pdf_path = report_generator.generate_report(
                scenario_data, prediction_result, allocation_result, narrative
            )
            
            # Save report to database
            report_id = str(uuid.uuid4())
            db = SessionLocal()
            try:
                report = Report(
                    id=report_id,
                    scenario_id=scenario_data.get('id'),
                    prediction_id=prediction_result.get('prediction_id'),
                    plan_id=allocation_result.get('plan_id'),
                    narrative_summary=narrative,
                    key_recommendations=[
                        "Immediate medical response deployment",
                        "Establish emergency communication channels",
                        "Coordinate with local authorities",
                        "Monitor weather conditions"
                    ],
                    risk_assessment="High risk due to infrastructure damage and limited access",
                    cost_breakdown={
                        "medical_supplies": prediction_result.get('predicted_needs', [{}])[0].get('estimated_cost', 0),
                        "logistics": allocation_result.get('total_cost', 0) * 0.3,
                        "coordination": allocation_result.get('total_cost', 0) * 0.2
                    },
                    pdf_path=pdf_path
                )
                db.add(report)
                db.commit()
                
                logger.info("Report generated successfully", 
                           report_id=report_id,
                           pdf_path=pdf_path)
                
                return {
                    'report_id': report_id,
                    'pdf_path': pdf_path,
                    'narrative_summary': narrative,
                    'key_recommendations': report.key_recommendations,
                    'risk_assessment': report.risk_assessment,
                    'cost_breakdown': report.cost_breakdown,
                    'generated_at': datetime.utcnow().isoformat()
                }
                
            finally:
                db.close()
                
        except Exception as e:
            log_error(logger, e, context={'operation': 'generate_report'})
            raise
    
    async def execute_full_workflow(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the complete agentic workflow for disaster response planning"""
        try:
            logger.info("Starting full agentic workflow", scenario_type=scenario_data.get('disaster_type'))
            
            # Execute the complete workflow using IBM ADK
            workflow_result = self.workflow.execute_workflow(scenario_data)
            
            logger.info("Full workflow completed successfully", 
                       workflow_id=workflow_result['workflow_id'],
                       scenario_id=workflow_result['scenario_id'])
            
            return workflow_result
            
        except Exception as e:
            log_error(logger, e, context={'operation': 'execute_full_workflow'})
            raise
    
    async def get_scenario_by_id(self, scenario_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve scenario by ID"""
        try:
            db = SessionLocal()
            try:
                scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
                if scenario:
                    return {
                        'id': scenario.id,
                        'disaster_type': scenario.disaster_type,
                        'severity': scenario.severity,
                        'location': {
                            'latitude': scenario.latitude,
                            'longitude': scenario.longitude,
                            'city': scenario.city,
                            'state': scenario.state,
                            'country': scenario.country,
                            'population': scenario.population
                        },
                        'affected_area_km2': scenario.affected_area_km2,
                        'estimated_casualties': scenario.estimated_casualties,
                        'infrastructure_damage': scenario.infrastructure_damage,
                        'weather_conditions': scenario.weather_conditions,
                        'available_volunteers': scenario.available_volunteers,
                        'description': scenario.description,
                        'created_at': scenario.created_at.isoformat()
                    }
                return None
            finally:
                db.close()
        except Exception as e:
            log_error(logger, e, context={'operation': 'get_scenario_by_id', 'scenario_id': scenario_id})
            raise
    
    async def get_all_scenarios(self) -> List[Dict[str, Any]]:
        """Retrieve all scenarios"""
        try:
            db = SessionLocal()
            try:
                scenarios = db.query(Scenario).order_by(Scenario.created_at.desc()).all()
                return [
                    {
                        'id': scenario.id,
                        'disaster_type': scenario.disaster_type,
                        'severity': scenario.severity,
                        'location': {
                            'city': scenario.city,
                            'state': scenario.state,
                            'country': scenario.country,
                            'population': scenario.population
                        },
                        'affected_area_km2': scenario.affected_area_km2,
                        'estimated_casualties': scenario.estimated_casualties,
                        'created_at': scenario.created_at.isoformat()
                    }
                    for scenario in scenarios
                ]
            finally:
                db.close()
        except Exception as e:
            log_error(logger, e, context={'operation': 'get_all_scenarios'})
            raise
    
    async def get_prediction_by_id(self, prediction_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve prediction by ID"""
        try:
            db = SessionLocal()
            try:
                prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
                if prediction:
                    return {
                        'id': prediction.id,
                        'scenario_id': prediction.scenario_id,
                        'predicted_needs': prediction.predicted_needs,
                        'confidence_score': prediction.confidence_score,
                        'estimated_response_time_hours': prediction.estimated_response_time_hours,
                        'risk_factors': prediction.risk_factors,
                        'created_at': prediction.created_at.isoformat()
                    }
                return None
            finally:
                db.close()
        except Exception as e:
            log_error(logger, e, context={'operation': 'get_prediction_by_id', 'prediction_id': prediction_id})
            raise
    
    async def get_plan_by_id(self, plan_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve plan by ID"""
        try:
            db = SessionLocal()
            try:
                plan = db.query(Plan).filter(Plan.id == plan_id).first()
                if plan:
                    return {
                        'id': plan.id,
                        'scenario_id': plan.scenario_id,
                        'resource_allocations': plan.resource_allocations,
                        'volunteer_assignments': plan.volunteer_assignments,
                        'timeline_hours': plan.timeline_hours,
                        'total_cost': plan.total_cost,
                        'efficiency_score': plan.efficiency_score,
                        'created_at': plan.created_at.isoformat()
                    }
                return None
            finally:
                db.close()
        except Exception as e:
            log_error(logger, e, context={'operation': 'get_plan_by_id', 'plan_id': plan_id})
            raise
    
    async def get_report_by_id(self, report_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve report by ID"""
        try:
            db = SessionLocal()
            try:
                report = db.query(Report).filter(Report.id == report_id).first()
                if report:
                    return {
                        'id': report.id,
                        'scenario_id': report.scenario_id,
                        'prediction_id': report.prediction_id,
                        'plan_id': report.plan_id,
                        'narrative_summary': report.narrative_summary,
                        'key_recommendations': report.key_recommendations,
                        'risk_assessment': report.risk_assessment,
                        'cost_breakdown': report.cost_breakdown,
                        'pdf_path': report.pdf_path,
                        'created_at': report.created_at.isoformat()
                    }
                return None
            finally:
                db.close()
        except Exception as e:
            log_error(logger, e, context={'operation': 'get_report_by_id', 'report_id': report_id})
            raise
