-- RapidRelief Database Initialization Script
-- This script creates sample disaster scenarios for testing

-- Create sample disaster scenarios
INSERT INTO scenarios (id, disaster_type, severity, latitude, longitude, city, state, country, population, affected_area_km2, estimated_casualties, infrastructure_damage, weather_conditions, available_volunteers, description, created_at) VALUES
(
    'sample-earthquake-001',
    'earthquake',
    'high',
    34.0522,
    -118.2437,
    'Los Angeles',
    'California',
    'United States',
    3979576,
    150.5,
    2500,
    'Significant damage to buildings and roads, power outages affecting 30% of the city',
    'Clear skies, moderate temperatures, no precipitation expected',
    1500,
    'A 7.2 magnitude earthquake has struck the Los Angeles metropolitan area, causing widespread damage to infrastructure and buildings. The epicenter was located in the San Fernando Valley, affecting multiple neighborhoods.',
    NOW() - INTERVAL '2 days'
),
(
    'sample-hurricane-002',
    'hurricane',
    'critical',
    25.7617,
    -80.1918,
    'Miami',
    'Florida',
    'United States',
    454279,
    200.0,
    5000,
    'Extensive flooding, destroyed homes, downed power lines, blocked roads',
    'Heavy rainfall, strong winds up to 120 mph, storm surge expected',
    800,
    'Hurricane Maria has made landfall in Miami with Category 4 strength, bringing catastrophic winds and storm surge. The hurricane has caused massive flooding and destruction across the coastal areas.',
    NOW() - INTERVAL '1 day'
),
(
    'sample-flood-003',
    'flood',
    'medium',
    40.7128,
    -74.0060,
    'New York',
    'New York',
    'United States',
    8336817,
    75.2,
    1200,
    'Subway system flooded, roads impassable, basement apartments affected',
    'Heavy rainfall for 48 hours, rivers overflowing, flash flood warnings',
    2000,
    'Heavy rainfall has caused severe flooding across New York City, particularly affecting low-lying areas and the subway system. Multiple neighborhoods are experiencing water damage.',
    NOW() - INTERVAL '6 hours'
);

-- Create sample predictions
INSERT INTO predictions (id, scenario_id, predicted_needs, confidence_score, estimated_response_time_hours, risk_factors, created_at) VALUES
(
    'pred-earthquake-001',
    'sample-earthquake-001',
    '[
        {"resource_type": "medical_supplies", "quantity": 500, "priority": "high", "estimated_cost": 25000.0, "delivery_time_hours": 6},
        {"resource_type": "water", "quantity": 1000, "priority": "critical", "estimated_cost": 5000.0, "delivery_time_hours": 2},
        {"resource_type": "shelter", "quantity": 200, "priority": "high", "estimated_cost": 40000.0, "delivery_time_hours": 12},
        {"resource_type": "food", "quantity": 800, "priority": "medium", "estimated_cost": 8000.0, "delivery_time_hours": 8}
    ]',
    0.85,
    24,
    '["aftershocks", "building_collapse", "power_outage"]',
    NOW() - INTERVAL '2 days'
),
(
    'pred-hurricane-002',
    'sample-hurricane-002',
    '[
        {"resource_type": "water", "quantity": 2000, "priority": "critical", "estimated_cost": 10000.0, "delivery_time_hours": 4},
        {"resource_type": "medical_supplies", "quantity": 1000, "priority": "critical", "estimated_cost": 50000.0, "delivery_time_hours": 8},
        {"resource_type": "shelter", "quantity": 500, "priority": "high", "estimated_cost": 100000.0, "delivery_time_hours": 16},
        {"resource_type": "generators", "quantity": 50, "priority": "high", "estimated_cost": 75000.0, "delivery_time_hours": 12}
    ]',
    0.92,
    36,
    '["storm_surge", "flooding", "power_outage", "communication_disruption"]',
    NOW() - INTERVAL '1 day'
),
(
    'pred-flood-003',
    'sample-flood-003',
    '[
        {"resource_type": "water", "quantity": 500, "priority": "medium", "estimated_cost": 2500.0, "delivery_time_hours": 3},
        {"resource_type": "medical_supplies", "quantity": 200, "priority": "medium", "estimated_cost": 10000.0, "delivery_time_hours": 4},
        {"resource_type": "pumps", "quantity": 25, "priority": "high", "estimated_cost": 12500.0, "delivery_time_hours": 6}
    ]',
    0.78,
    18,
    '["continued_rainfall", "sewer_backup", "transportation_disruption"]',
    NOW() - INTERVAL '6 hours'
);

-- Create sample plans
INSERT INTO plans (id, scenario_id, resource_allocations, volunteer_assignments, timeline_hours, total_cost, efficiency_score, created_at) VALUES
(
    'plan-earthquake-001',
    'sample-earthquake-001',
    '[
        {"resource_type": "medical_supplies", "quantity": 500, "priority": "high", "estimated_cost": 25000.0, "delivery_time_hours": 6},
        {"resource_type": "water", "quantity": 1000, "priority": "critical", "estimated_cost": 5000.0, "delivery_time_hours": 2}
    ]',
    '{
        "medical_teams": ["team_alpha", "team_beta"],
        "logistics": ["team_gamma"],
        "coordination": ["team_delta"]
    }',
    24,
    78000.0,
    0.92,
    NOW() - INTERVAL '2 days'
),
(
    'plan-hurricane-002',
    'sample-hurricane-002',
    '[
        {"resource_type": "water", "quantity": 2000, "priority": "critical", "estimated_cost": 10000.0, "delivery_time_hours": 4},
        {"resource_type": "medical_supplies", "quantity": 1000, "priority": "critical", "estimated_cost": 50000.0, "delivery_time_hours": 8}
    ]',
    '{
        "emergency_response": ["team_echo", "team_foxtrot"],
        "evacuation": ["team_golf"],
        "medical": ["team_hotel", "team_india"]
    }',
    36,
    235000.0,
    0.88,
    NOW() - INTERVAL '1 day'
),
(
    'plan-flood-003',
    'sample-flood-003',
    '[
        {"resource_type": "water", "quantity": 500, "priority": "medium", "estimated_cost": 2500.0, "delivery_time_hours": 3},
        {"resource_type": "pumps", "quantity": 25, "priority": "high", "estimated_cost": 12500.0, "delivery_time_hours": 6}
    ]',
    '{
        "water_management": ["team_juliet"],
        "medical": ["team_kilo"],
        "coordination": ["team_lima"]
    }',
    18,
    25000.0,
    0.85,
    NOW() - INTERVAL '6 hours'
);

-- Create sample reports
INSERT INTO reports (id, scenario_id, prediction_id, plan_id, narrative_summary, key_recommendations, risk_assessment, cost_breakdown, pdf_path, created_at) VALUES
(
    'report-earthquake-001',
    'sample-earthquake-001',
    'pred-earthquake-001',
    'plan-earthquake-001',
    'The 7.2 magnitude earthquake in Los Angeles has caused significant damage to infrastructure and buildings across the metropolitan area. Our AI analysis indicates a high-priority response is required with immediate deployment of medical supplies and water resources. The optimized allocation plan achieves 92% efficiency with a total cost of $78,000 and a 24-hour response timeline.',
    '[
        "Immediate medical response deployment to affected areas",
        "Establish emergency communication channels",
        "Coordinate with local authorities and emergency services",
        "Monitor aftershock activity and adjust plans accordingly"
    ]',
    'High risk due to potential aftershocks, building collapse hazards, and power outages affecting emergency response capabilities.',
    '{
        "medical_supplies": 25000.0,
        "logistics": 23400.0,
        "coordination": 15600.0
    }',
    '/app/reports/disaster_response_report_earthquake_001.pdf',
    NOW() - INTERVAL '2 days'
),
(
    'report-hurricane-002',
    'sample-hurricane-002',
    'pred-hurricane-002',
    'plan-hurricane-002',
    'Hurricane Maria has made catastrophic landfall in Miami with Category 4 strength, causing extensive flooding and destruction. The AI-powered analysis shows critical resource needs with 92% prediction confidence. The allocation plan achieves 88% efficiency with a total cost of $235,000 and a 36-hour response timeline.',
    '[
        "Immediate evacuation coordination for affected areas",
        "Deploy emergency medical teams and supplies",
        "Establish water distribution networks",
        "Coordinate with FEMA and federal agencies"
    ]',
    'Critical risk due to storm surge, continued flooding, power outages, and communication disruptions.',
    '{
        "medical_supplies": 50000.0,
        "logistics": 70500.0,
        "coordination": 47000.0
    }',
    '/app/reports/disaster_response_report_hurricane_002.pdf',
    NOW() - INTERVAL '1 day'
),
(
    'report-flood-003',
    'sample-flood-003',
    'pred-flood-003',
    'plan-flood-003',
    'Heavy rainfall has caused severe flooding across New York City, particularly affecting the subway system and low-lying areas. The AI analysis indicates moderate resource needs with 78% confidence. The optimized plan achieves 85% efficiency with a total cost of $25,000 and an 18-hour response timeline.',
    '[
        "Deploy water pumps to affected areas",
        "Coordinate with MTA for subway system recovery",
        "Establish emergency shelters for displaced residents",
        "Monitor weather conditions for continued rainfall"
    ]',
    'Medium risk due to continued rainfall, sewer backup, and transportation system disruption.',
    '{
        "water_management": 12500.0,
        "logistics": 7500.0,
        "coordination": 5000.0
    }',
    '/app/reports/disaster_response_report_flood_003.pdf',
    NOW() - INTERVAL '6 hours'
);
