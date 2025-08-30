from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/rapidrelief")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Scenario(Base):
    __tablename__ = "scenarios"
    
    id = Column(String, primary_key=True, index=True)
    disaster_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)
    population = Column(Integer, nullable=False)
    affected_area_km2 = Column(Float, nullable=False)
    estimated_casualties = Column(Integer, nullable=False)
    infrastructure_damage = Column(Text, nullable=False)
    weather_conditions = Column(Text, nullable=False)
    available_volunteers = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    predictions = relationship("Prediction", back_populates="scenario")
    plans = relationship("Plan", back_populates="scenario")
    reports = relationship("Report", back_populates="scenario")


class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(String, primary_key=True, index=True)
    scenario_id = Column(String, ForeignKey("scenarios.id"), nullable=False)
    predicted_needs = Column(JSON, nullable=False)
    confidence_score = Column(Float, nullable=False)
    estimated_response_time_hours = Column(Integer, nullable=False)
    risk_factors = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    scenario = relationship("Scenario", back_populates="predictions")


class Plan(Base):
    __tablename__ = "plans"
    
    id = Column(String, primary_key=True, index=True)
    scenario_id = Column(String, ForeignKey("scenarios.id"), nullable=False)
    resource_allocations = Column(JSON, nullable=False)
    volunteer_assignments = Column(JSON, nullable=False)
    timeline_hours = Column(Integer, nullable=False)
    total_cost = Column(Float, nullable=False)
    efficiency_score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    scenario = relationship("Scenario", back_populates="plans")


class Report(Base):
    __tablename__ = "reports"
    
    id = Column(String, primary_key=True, index=True)
    scenario_id = Column(String, ForeignKey("scenarios.id"), nullable=False)
    prediction_id = Column(String, ForeignKey("predictions.id"), nullable=False)
    plan_id = Column(String, ForeignKey("plans.id"), nullable=False)
    narrative_summary = Column(Text, nullable=False)
    key_recommendations = Column(JSON, nullable=False)
    risk_assessment = Column(Text, nullable=False)
    cost_breakdown = Column(JSON, nullable=False)
    pdf_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    scenario = relationship("Scenario", back_populates="reports")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
