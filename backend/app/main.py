from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import time
import uuid
from typing import List, Optional
import os

from .models import (
    DisasterScenario, PredictionResponse, AllocationPlan, 
    ReportData, APIResponse, DisasterType, SeverityLevel
)
from .planner import DisasterResponsePlanner
from .db import init_db, get_db
from .utils.logger import setup_logging, get_logger, log_api_request, log_api_response

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="RapidRelief API",
    description="AI-Powered Disaster Response Planning System using IBM Granite and ADK",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize planner
planner = DisasterResponsePlanner()

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    request_id = str(uuid.uuid4())
    
    # Log request
    log_api_request(
        logger, 
        method=request.method, 
        path=request.url.path, 
        request_id=request_id
    )
    
    response = await call_next(request)
    
    # Calculate response time
    process_time = (time.time() - start_time) * 1000
    
    # Log response
    log_api_response(
        logger,
        method=request.method,
        path=request.url.path,
        request_id=request_id,
        status_code=response.status_code,
        response_time_ms=process_time
    )
    
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Request-ID"] = request_id
    return response


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error("Failed to initialize database", error=str(e))
        raise


@app.get("/", response_model=APIResponse)
async def root():
    """Root endpoint"""
    return APIResponse(
        success=True,
        message="RapidRelief API - AI-Powered Disaster Response Planning",
        data={
            "version": "1.0.0",
            "status": "operational",
            "features": [
                "IBM Granite AI Integration",
                "IBM Agent Development Kit Workflows",
                "Resource Prediction",
                "Allocation Planning",
                "PDF Report Generation"
            ]
        }
    )


@app.get("/health", response_model=APIResponse)
async def health_check():
    """Health check endpoint"""
    return APIResponse(
        success=True,
        message="Service is healthy",
        data={"status": "healthy", "timestamp": time.time()}
    )


@app.post("/predict", response_model=APIResponse)
async def predict_resources(scenario: DisasterScenario):
    """Predict resource needs for a disaster scenario using IBM Granite"""
    try:
        logger.info("Resource prediction request received", 
                   disaster_type=scenario.disaster_type,
                   severity=scenario.severity)
        
        # Convert Pydantic model to dict
        scenario_data = scenario.dict()
        scenario_data['id'] = str(uuid.uuid4())
        
        # Call planner for prediction
        prediction_result = await planner.predict_resources(scenario_data)
        
        return APIResponse(
            success=True,
            message="Resource prediction completed successfully",
            data=prediction_result
        )
        
    except Exception as e:
        logger.error("Resource prediction failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/plan", response_model=APIResponse)
async def generate_allocation_plan(scenario: DisasterScenario):
    """Generate optimized allocation plan using IBM Granite + ADK"""
    try:
        logger.info("Allocation plan request received", 
                   disaster_type=scenario.disaster_type,
                   severity=scenario.severity)
        
        # Convert Pydantic model to dict
        scenario_data = scenario.dict()
        scenario_data['id'] = str(uuid.uuid4())
        
        # First predict resources
        prediction_result = await planner.predict_resources(scenario_data)
        
        # Then generate allocation plan
        allocation_result = await planner.generate_allocation_plan(
            scenario_data, 
            prediction_result['predicted_needs']
        )
        
        return APIResponse(
            success=True,
            message="Allocation plan generated successfully",
            data={
                "scenario_id": scenario_data['id'],
                "prediction": prediction_result,
                "allocation": allocation_result
            }
        )
        
    except Exception as e:
        logger.error("Allocation plan generation failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Plan generation failed: {str(e)}")


@app.post("/report", response_model=APIResponse)
async def generate_report(scenario: DisasterScenario):
    """Generate comprehensive report with narrative and PDF"""
    try:
        logger.info("Report generation request received", 
                   disaster_type=scenario.disaster_type,
                   severity=scenario.severity)
        
        # Convert Pydantic model to dict
        scenario_data = scenario.dict()
        scenario_data['id'] = str(uuid.uuid4())
        
        # Execute full workflow
        workflow_result = await planner.execute_full_workflow(scenario_data)
        
        return APIResponse(
            success=True,
            message="Comprehensive report generated successfully",
            data=workflow_result
        )
        
    except Exception as e:
        logger.error("Report generation failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")


@app.get("/scenarios", response_model=APIResponse)
async def get_scenarios():
    """Get all disaster scenarios"""
    try:
        scenarios = await planner.get_all_scenarios()
        return APIResponse(
            success=True,
            message=f"Retrieved {len(scenarios)} scenarios",
            data={"scenarios": scenarios}
        )
    except Exception as e:
        logger.error("Failed to retrieve scenarios", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to retrieve scenarios: {str(e)}")


@app.get("/scenarios/{scenario_id}", response_model=APIResponse)
async def get_scenario(scenario_id: str):
    """Get specific scenario by ID"""
    try:
        scenario = await planner.get_scenario_by_id(scenario_id)
        if not scenario:
            raise HTTPException(status_code=404, detail="Scenario not found")
        
        return APIResponse(
            success=True,
            message="Scenario retrieved successfully",
            data={"scenario": scenario}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to retrieve scenario", error=str(e), scenario_id=scenario_id)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve scenario: {str(e)}")


@app.get("/predictions/{prediction_id}", response_model=APIResponse)
async def get_prediction(prediction_id: str):
    """Get specific prediction by ID"""
    try:
        prediction = await planner.get_prediction_by_id(prediction_id)
        if not prediction:
            raise HTTPException(status_code=404, detail="Prediction not found")
        
        return APIResponse(
            success=True,
            message="Prediction retrieved successfully",
            data={"prediction": prediction}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to retrieve prediction", error=str(e), prediction_id=prediction_id)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve prediction: {str(e)}")


@app.get("/plans/{plan_id}", response_model=APIResponse)
async def get_plan(plan_id: str):
    """Get specific plan by ID"""
    try:
        plan = await planner.get_plan_by_id(plan_id)
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        
        return APIResponse(
            success=True,
            message="Plan retrieved successfully",
            data={"plan": plan}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to retrieve plan", error=str(e), plan_id=plan_id)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve plan: {str(e)}")


@app.get("/reports/{report_id}", response_model=APIResponse)
async def get_report(report_id: str):
    """Get specific report by ID"""
    try:
        report = await planner.get_report_by_id(report_id)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        return APIResponse(
            success=True,
            message="Report retrieved successfully",
            data={"report": report}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to retrieve report", error=str(e), report_id=report_id)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve report: {str(e)}")


@app.get("/download/{report_id}")
async def download_report(report_id: str):
    """Download PDF report"""
    try:
        report = await planner.get_report_by_id(report_id)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        pdf_path = report['pdf_path']
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=404, detail="PDF file not found")
        
        return FileResponse(
            pdf_path,
            media_type='application/pdf',
            filename=f"disaster_response_report_{report_id}.pdf"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to download report", error=str(e), report_id=report_id)
        raise HTTPException(status_code=500, detail=f"Failed to download report: {str(e)}")


@app.get("/disaster-types", response_model=APIResponse)
async def get_disaster_types():
    """Get available disaster types"""
    return APIResponse(
        success=True,
        message="Disaster types retrieved successfully",
        data={"disaster_types": [dt.value for dt in DisasterType]}
    )


@app.get("/severity-levels", response_model=APIResponse)
async def get_severity_levels():
    """Get available severity levels"""
    return APIResponse(
        success=True,
        message="Severity levels retrieved successfully",
        data={"severity_levels": [sl.value for sl in SeverityLevel]}
    )


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return APIResponse(
        success=False,
        message="Resource not found",
        error="The requested resource was not found"
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return APIResponse(
        success=False,
        message="Internal server error",
        error="An unexpected error occurred"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
