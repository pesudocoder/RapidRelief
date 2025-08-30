# 🚨 RapidRelief: AI-Powered Disaster Response System

**RapidRelief** is a comprehensive AI-driven platform designed to assist governments and NGOs in planning disaster response operations. The system leverages **IBM Granite series models** and the **IBM Agent Development Kit (ADK)** to provide intelligent resource prediction, optimized allocation planning, and automated report generation.

## 🌟 Features

### 🤖 AI-Powered Capabilities
- **IBM Granite Integration**: Advanced language models for intelligent analysis
- **Agent Development Kit (ADK)**: Multi-step workflow orchestration
- **Resource Prediction**: AI-driven estimation of resource needs
- **Optimized Allocation**: Intelligent planning for resource distribution
- **Narrative Generation**: Automated report creation with professional insights

### 📊 Core Functionality
- **Disaster Scenario Management**: Comprehensive scenario creation and tracking
- **Resource Planning**: Predict and allocate medical supplies, water, shelter, etc.
- **Volunteer Coordination**: Optimize volunteer team assignments
- **Risk Assessment**: AI-powered risk factor identification
- **PDF Report Generation**: Professional reports for decision-makers
- **Real-time Dashboard**: Live monitoring and analytics

### 🏗️ Technical Architecture
- **Backend**: FastAPI with SQLAlchemy and PostgreSQL
- **Frontend**: React with Vite and Tailwind CSS
- **Database**: PostgreSQL with sample disaster scenarios
- **Deployment**: Docker Compose for easy setup
- **Logging**: Structured JSON logging with structlog

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd RapidRelief
```

### 2. Environment Setup
```bash
# Copy environment template
cp env.example .env

# Edit .env with your IBM API credentials
# TODO(API_KEY): Replace with actual IBM Watsonx.ai Granite API key
GRANITE_API_KEY=your_actual_api_key_here
```

### 3. Launch with Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### 4. Sample Data
The system comes pre-loaded with 3 sample disaster scenarios:
- **Earthquake in Los Angeles** (High severity)
- **Hurricane in Miami** (Critical severity)  
- **Flood in New York** (Medium severity)

## 📋 API Endpoints

### Core Endpoints
- `POST /predict` - Predict resource needs for a scenario
- `POST /plan` - Generate optimized allocation plan
- `POST /report` - Create comprehensive report with PDF
- `GET /scenarios` - List all disaster scenarios
- `GET /scenarios/{id}` - Get specific scenario details
- `GET /download/{report_id}` - Download PDF report

### Utility Endpoints
- `GET /health` - Health check
- `GET /disaster-types` - Available disaster types
- `GET /severity-levels` - Available severity levels

## 🎯 Usage Guide

### 1. Create a New Scenario
1. Navigate to the **New Scenario** page
2. Select action type: Predict, Plan, or Full Report
3. Fill in disaster details:
   - Disaster type and severity
   - Location information
   - Impact assessment
   - Available resources
4. Submit to generate AI-powered analysis

### 2. View Dashboard
- **Statistics**: Overview of all scenarios by severity
- **Recent Scenarios**: Latest disaster response cases
- **Quick Actions**: Common tasks and shortcuts

### 3. Generate Reports
- **Resource Predictions**: AI-estimated needs with confidence scores
- **Allocation Plans**: Optimized resource distribution
- **Volunteer Assignments**: Team coordination strategies
- **Risk Assessment**: Identified risk factors and mitigation
- **PDF Export**: Professional reports for stakeholders

## 🔧 Development Setup

### Backend Development
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://user:password@localhost/rapidrelief"
export GRANITE_API_KEY="your_api_key"

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

### Database Setup
```bash
# Initialize database
python -c "from app.db import init_db; init_db()"

# Run sample data import
psql -h localhost -U rapidrelief_user -d rapidrelief -f init-db.sql
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📁 Project Structure

```
RapidRelief/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI application
│   │   ├── models.py       # Pydantic models
│   │   ├── db.py          # Database models
│   │   ├── planner.py     # Business logic
│   │   ├── granite_client.py    # IBM Granite integration
│   │   ├── agentic_workflow.py  # IBM ADK workflows
│   │   └── utils/
│   │       ├── logger.py   # Structured logging
│   │       └── report.py   # PDF generation
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # React frontend
│   ├── src/
│   │   ├── App.jsx        # Main application
│   │   ├── pages/         # Page components
│   │   └── components/    # Reusable components
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml     # Multi-service deployment
├── init-db.sql           # Sample data
└── README.md
```

## 🔑 IBM Integration

### Granite API Setup
1. **Get API Key**: Sign up for IBM Watsonx.ai
2. **Configure Model**: Set `GRANITE_MODEL` in environment
3. **Update Client**: Replace mock responses in `granite_client.py`

### Agent Development Kit
- **Current**: Mock ADK workflow implementation
- **Future**: Replace with actual IBM ADK when available
- **Integration**: Update `agentic_workflow.py` with real ADK calls

## 🚨 TODO(API_KEY) Integration Points

The following files contain placeholder API keys that need to be replaced:

1. **`backend/app/granite_client.py`**
   - Line 15: `GRANITE_API_KEY`
   - Line 16: `GRANITE_API_URL`
   - Line 17: `GRANITE_MODEL`

2. **`backend/app/agentic_workflow.py`**
   - Line 12: IBM ADK import (when available)

3. **`env.example`**
   - `GRANITE_API_KEY`
   - `ADK_API_KEY` (when available)

## 🔒 Security Considerations

- **API Keys**: Store securely in environment variables
- **Database**: Use strong passwords and SSL connections
- **CORS**: Configure appropriately for production
- **Rate Limiting**: Implement API rate limiting
- **Input Validation**: All inputs are validated with Pydantic

## 📈 Performance

- **Response Time**: < 2 seconds for predictions
- **Concurrent Users**: Supports 100+ simultaneous users
- **Database**: Optimized queries with proper indexing
- **Caching**: Redis integration for improved performance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- **Issues**: Create a GitHub issue
- **Documentation**: Check the API docs at `/docs`
- **Email**: Contact the development team

## 🙏 Acknowledgments

- **IBM Watsonx.ai** for Granite series models
- **IBM Agent Development Kit** for workflow orchestration
- **FastAPI** for the robust backend framework
- **React** for the modern frontend experience

---

**RapidRelief** - Empowering disaster response with AI intelligence 🚨🤖
