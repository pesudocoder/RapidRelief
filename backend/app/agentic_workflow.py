import structlog
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid
import json
from .granite_client import GraniteClient
from .db import SessionLocal, Scenario, Prediction, Plan, Report
from .utils.report import ReportGenerator

logger = structlog.get_logger(__name__)

# TODO(API_KEY): Import IBM Agent Development Kit when available
# from ibm_adk import Agent, Workflow, Node
# For now, we'll create a mock ADK workflow structure


class AgentNode:
    """Mock ADK Agent Node for development"""
    def __init__(self, name: str, function):
        self.name = name
        self.function = function
        self.status = "pending"
        self.result = None
        self.error = None
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        try:
            logger.info(f"Executing agent node: {self.name}")
            self.status = "running"
            self.result = self.function(context)
            self.status = "completed"
            logger.info(f"Agent node completed: {self.name}")
            return self.result
        except Exception as e:
            self.status = "failed"
            self.error = str(e)
            logger.error(f"Agent node failed: {self.name}", error=str(e))
            raise


class AgenticWorkflow:
    """IBM ADK-inspired workflow orchestration for disaster response"""
    
    def __init__(self):
        self.granite_client = GraniteClient()
        self.report_generator = ReportGenerator()
        self.workflow_id = None
        
    def create_workflow(self) -> str:
        """Create a new workflow instance"""
        self.workflow_id = str(uuid.uuid4())
        logger.info("Created new agentic workflow", workflow_id=self.workflow_id)
        return self.workflow_id
    
    def ingest_scenario_node(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Agent Node 1: Ingest and validate disaster scenario"""
        scenario_data = context.get('scenario_data')
        if not scenario_data:
            raise ValueError("No scenario data provided")
        
        # Validate scenario data
        required_fields = ['disaster_type', 'severity', 'location', 'affected_area_km2']
        for field in required_fields:
            if field not in scenario_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Generate scenario ID
        scenario_id = str(uuid.uuid4())
        
        # Save to database
        db = SessionLocal()
        try:
            scenario = Scenario(
                id=scenario_id,
                disaster_type=scenario_data['disaster_type'],
                severity=scenario_data['severity'],
                latitude=scenario_data['location']['latitude'],
                longitude=scenario_data['location']['longitude'],
                city=scenario_data['location']['city'],
                state=scenario_data['location']['state'],
                country=scenario_data['location']['country'],
                population=scenario_data['location']['population'],
                affected_area_km2=scenario_data['affected_area_km2'],
                estimated_casualties=scenario_data['estimated_casualties'],
                infrastructure_damage=scenario_data['infrastructure_damage'],
                weather_conditions=scenario_data['weather_conditions'],
                available_volunteers=scenario_data['available_volunteers'],
                description=scenario_data['description']
            )
            db.add(scenario)
            db.commit()
            
            logger.info("Scenario ingested successfully", scenario_id=scenario_id)
            return {
                'scenario_id': scenario_id,
                'scenario_data': scenario_data,
                'status': 'ingested'
            }
        finally:
            db.close()
    
    def predict_resources_node(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Agent Node 2: Use Granite to predict resource needs"""
        scenario_id = context.get('scenario_id')
        scenario_data = context.get('scenario_data')
        
        if not scenario_id or not scenario_data:
            raise ValueError("Missing scenario information")
        
        # Call Granite for resource prediction
        prediction_result = self.granite_client.predict_resources(scenario_data)
        
        # Save prediction to database
        db = SessionLocal()
        try:
            prediction = Prediction(
                id=str(uuid.uuid4()),
                scenario_id=scenario_id,
                predicted_needs=prediction_result['predicted_needs'],
                confidence_score=prediction_result['confidence_score'],
                estimated_response_time_hours=prediction_result['estimated_response_time_hours'],
                risk_factors=prediction_result['risk_factors']
            )
            db.add(prediction)
            db.commit()
            
            logger.info("Resource prediction completed", 
                       scenario_id=scenario_id, 
                       prediction_id=prediction.id,
                       confidence=prediction_result['confidence_score'])
            
            return {
                'prediction_id': prediction.id,
                'prediction_result': prediction_result,
                'status': 'predicted'
            }
        finally:
            db.close()
    
    def generate_allocation_node(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Agent Node 3: Use Granite to generate optimized allocation plan"""
        scenario_id = context.get('scenario_id')
        scenario_data = context.get('scenario_data')
        predicted_needs = context.get('prediction_result', {}).get('predicted_needs', [])
        
        if not scenario_id or not scenario_data or not predicted_needs:
            raise ValueError("Missing required context for allocation planning")
        
        # Call Granite for allocation planning
        allocation_result = self.granite_client.generate_allocation_plan(scenario_data, predicted_needs)
        
        # Save plan to database
        db = SessionLocal()
        try:
            plan = Plan(
                id=str(uuid.uuid4()),
                scenario_id=scenario_id,
                resource_allocations=allocation_result['resource_allocations'],
                volunteer_assignments=allocation_result['volunteer_assignments'],
                timeline_hours=allocation_result['timeline_hours'],
                total_cost=allocation_result['total_cost'],
                efficiency_score=allocation_result['efficiency_score']
            )
            db.add(plan)
            db.commit()
            
            logger.info("Allocation plan generated", 
                       scenario_id=scenario_id, 
                       plan_id=plan.id,
                       efficiency=allocation_result['efficiency_score'])
            
            return {
                'plan_id': plan.id,
                'allocation_result': allocation_result,
                'status': 'allocated'
            }
        finally:
            db.close()
    
    def save_to_database_node(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Agent Node 4: Save all results to database (already done in previous nodes)"""
        scenario_id = context.get('scenario_id')
        prediction_id = context.get('prediction_id')
        plan_id = context.get('plan_id')
        
        logger.info("Database save completed", 
                   scenario_id=scenario_id,
                   prediction_id=prediction_id,
                   plan_id=plan_id)
        
        return {
            'status': 'saved',
            'message': 'All data successfully saved to database'
        }
    
    def generate_report_node(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Agent Node 5: Generate comprehensive report using Granite narrative"""
        scenario_id = context.get('scenario_id')
        prediction_result = context.get('prediction_result')
        allocation_result = context.get('allocation_result')
        scenario_data = context.get('scenario_data')
        
        if not all([scenario_id, prediction_result, allocation_result, scenario_data]):
            raise ValueError("Missing required context for report generation")
        
        # Generate narrative using Granite
        narrative = self.granite_client.generate_narrative_report(
            scenario_data, prediction_result, allocation_result
        )
        
        # Generate PDF report
        pdf_path = self.report_generator.generate_report(
            scenario_data, prediction_result, allocation_result, narrative
        )
        
        # Save report to database
        db = SessionLocal()
        try:
            report = Report(
                id=str(uuid.uuid4()),
                scenario_id=scenario_id,
                prediction_id=context.get('prediction_id'),
                plan_id=context.get('plan_id'),
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
                       scenario_id=scenario_id, 
                       report_id=report.id,
                       pdf_path=pdf_path)
            
            return {
                'report_id': report.id,
                'pdf_path': pdf_path,
                'narrative': narrative,
                'status': 'reported'
            }
        finally:
            db.close()
    
    def execute_workflow(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the complete agentic workflow"""
        workflow_id = self.create_workflow()
        context = {'scenario_data': scenario_data}
        
        # Define workflow nodes
        nodes = [
            AgentNode("ingest_scenario", self.ingest_scenario_node),
            AgentNode("predict_resources", self.predict_resources_node),
            AgentNode("generate_allocation", self.generate_allocation_node),
            AgentNode("save_to_database", self.save_to_database_node),
            AgentNode("generate_report", self.generate_report_node)
        ]
        
        # Execute workflow sequentially
        workflow_results = {}
        
        for node in nodes:
            try:
                result = node.execute(context)
                workflow_results[node.name] = result
                context.update(result)  # Pass results to next node
                
                logger.info(f"Workflow step completed: {node.name}", 
                           workflow_id=workflow_id,
                           status=node.status)
                
            except Exception as e:
                logger.error(f"Workflow step failed: {node.name}", 
                           workflow_id=workflow_id,
                           error=str(e))
                raise
        
        # Compile final results
        final_result = {
            'workflow_id': workflow_id,
            'status': 'completed',
            'scenario_id': context.get('scenario_id'),
            'prediction_id': context.get('prediction_id'),
            'plan_id': context.get('plan_id'),
            'report_id': context.get('report_id'),
            'pdf_path': context.get('pdf_path'),
            'summary': {
                'confidence_score': context.get('prediction_result', {}).get('confidence_score'),
                'efficiency_score': context.get('allocation_result', {}).get('efficiency_score'),
                'total_cost': context.get('allocation_result', {}).get('total_cost'),
                'timeline_hours': context.get('allocation_result', {}).get('timeline_hours')
            }
        }
        
        logger.info("Agentic workflow completed successfully", 
                   workflow_id=workflow_id,
                   final_status=final_result['status'])
        
        return final_result
