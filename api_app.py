from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from crewai import Crew, LLM
from trip_agents import TripAgents
from trip_tasks import TripTasks
from intelligence_agents import IntelligenceAgents
from intelligence_tasks import IntelligenceTasks
import os
from dotenv import load_dotenv
from functools import lru_cache

# Load environment variables
load_dotenv()

app = FastAPI(
    title="VacAIgent API",
    description="AI-powered travel planning API using CrewAI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TripRequest(BaseModel):
    origin: str = Field(..., 
        example="Bangalore, India",
        description="Your current location")
    destination: str = Field(..., 
        example="Krabi, Thailand",
        description="Destination city and country")
    start_date: date = Field(..., 
        example="2025-06-01",
        description="Start date of your trip")
    end_date: date = Field(..., 
        example="2025-06-10",
        description="End date of your trip")
    interests: str = Field(..., 
        example="2 adults who love swimming, dancing, hiking, shopping, local food, water sports adventures and rock climbing",
        description="Your interests and trip details")
    enable_intelligence: bool = Field(default=False,
        description="Enable AI-powered travel intelligence features")

class IntelligenceRequest(BaseModel):
    origin: str = Field(..., description="Your current location")
    destination: str = Field(..., description="Destination city and country")
    start_date: date = Field(..., description="Start date of your trip")
    end_date: date = Field(..., description="End date of your trip")
    interests: str = Field(..., description="Your interests and trip details")
    intelligence_type: str = Field(..., description="Type of intelligence analysis: risk, crowd, price, language, or all")

class TripResponse(BaseModel):
    status: str
    message: str
    itinerary: Optional[str] = None
    error: Optional[str] = None

class Settings:
    def __init__(self):
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.SERPER_API_KEY = os.getenv("SERPER_API_KEY")
        self.BROWSERLESS_API_KEY = os.getenv("BROWSERLESS_API_KEY")

@lru_cache()
def get_settings():
    return Settings()

def validate_api_keys(settings: Settings = Depends(get_settings)):
    required_keys = {
        'GEMINI_API_KEY': settings.GEMINI_API_KEY,
        'SERPER_API_KEY': settings.SERPER_API_KEY,
        'BROWSERLESS_API_KEY': settings.BROWSERLESS_API_KEY
    }
    
    missing_keys = [key for key, value in required_keys.items() if not value]
    if missing_keys:
        raise HTTPException(
            status_code=500,
            detail=f"Missing required API keys: {', '.join(missing_keys)}"
        )
    return settings

class TripCrew:
    def __init__(self, origin, destination, date_range, interests, enable_intelligence=False):
        self.destination = destination
        self.origin = origin
        self.interests = interests
        self.date_range = date_range
        self.enable_intelligence = enable_intelligence
        self.llm = LLM(model="gemini/gemini-2.0-flash")

    def run(self):
        try:
            agents = TripAgents(llm=self.llm)
            tasks = TripTasks()

            city_selector_agent = agents.city_selection_agent()
            local_expert_agent = agents.local_expert()
            travel_concierge_agent = agents.travel_concierge()

            identify_task = tasks.identify_task(
                city_selector_agent,
                self.origin,
                self.destination,
                self.interests,
                self.date_range
            )

            gather_task = tasks.gather_task(
                local_expert_agent,
                self.origin,
                self.interests,
                self.date_range
            )

            plan_task = tasks.plan_task(
                travel_concierge_agent,
                self.origin,
                self.interests,
                self.date_range
            )

            crew = Crew(
                agents=[
                    city_selector_agent, local_expert_agent, travel_concierge_agent
                ],
                tasks=[identify_task, gather_task, plan_task],
                verbose=True
            )

            result = crew.kickoff()
            # Convert CrewOutput to string and ensure it's properly formatted
            return result.raw if hasattr(result, 'raw') else str(result)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

    def run_with_intelligence(self):
        """Run trip planning with AI-powered intelligence features"""
        try:
            # Run basic trip planning
            basic_result = self.run()
            
            if not basic_result:
                return None
            
            # Initialize intelligence agents
            intel_agents = IntelligenceAgents(llm=self.llm)
            intel_tasks = IntelligenceTasks()
            
            # Run intelligence analysis
            intelligence_crew = Crew(
                agents=[
                    intel_agents.risk_assessment_agent(),
                    intel_agents.crowd_density_agent(),
                    intel_agents.price_optimization_agent(),
                    intel_agents.language_barrier_agent()
                ],
                tasks=[
                    intel_tasks.risk_assessment_task(
                        intel_agents.risk_assessment_agent(),
                        self.origin, self.destination, self.date_range, self.interests
                    ),
                    intel_tasks.crowd_density_task(
                        intel_agents.crowd_density_agent(),
                        self.destination, self.date_range, self.interests
                    ),
                    intel_tasks.price_optimization_task(
                        intel_agents.price_optimization_agent(),
                        self.origin, self.destination, self.date_range, self.interests
                    ),
                    intel_tasks.language_barrier_task(
                        intel_agents.language_barrier_agent(),
                        self.destination, self.date_range, self.interests
                    )
                ],
                verbose=True
            )
            
            intelligence_result = intelligence_crew.kickoff()
            
            # Combine results
            combined_result = f"""
{basic_result}

{intelligence_result}
            """
            
            return combined_result
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Intelligence analysis error: {str(e)}"
            )

@app.get("/")
async def root():
    return {
        "message": "Welcome to VacAIgent API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

@app.post("/api/v1/plan-trip", response_model=TripResponse)
async def plan_trip(
    trip_request: TripRequest,
    settings: Settings = Depends(validate_api_keys)
):
    # Validate dates
    if trip_request.end_date <= trip_request.start_date:
        raise HTTPException(
            status_code=400,
            detail="End date must be after start date"
        )

    # Format date range
    date_range = f"{trip_request.start_date} to {trip_request.end_date}"

    try:
        trip_crew = TripCrew(
            trip_request.origin,
            trip_request.destination,
            date_range,
            trip_request.interests,
            enable_intelligence=trip_request.enable_intelligence
        )
        
        if trip_request.enable_intelligence:
            itinerary = trip_crew.run_with_intelligence()
        else:
            itinerary = trip_crew.run()
        
        # Ensure itinerary is a string
        if not isinstance(itinerary, str):
            itinerary = str(itinerary)
            
        return TripResponse(
            status="success",
            message="Trip plan generated successfully",
            itinerary=itinerary
        )
    
    except Exception as e:
        return TripResponse(
            status="error",
            message="Failed to generate trip plan",
            error=str(e)
        )

@app.post("/api/v1/intelligence-analysis", response_model=TripResponse)
async def intelligence_analysis(
    intel_request: IntelligenceRequest,
    settings: Settings = Depends(validate_api_keys)
):
    """Run specific intelligence analysis"""
    # Validate dates
    if intel_request.end_date <= intel_request.start_date:
        raise HTTPException(
            status_code=400,
            detail="End date must be after start date"
        )

    # Format date range
    date_range = f"{intel_request.start_date} to {intel_request.end_date}"

    try:
        intel_agents = IntelligenceAgents()
        intel_tasks = IntelligenceTasks()
        
        # Select agent and task based on intelligence type
        if intel_request.intelligence_type == "risk":
            agent = intel_agents.risk_assessment_agent()
            task = intel_tasks.risk_assessment_task(
                agent, intel_request.origin, intel_request.destination, 
                date_range, intel_request.interests
            )
        elif intel_request.intelligence_type == "crowd":
            agent = intel_agents.crowd_density_agent()
            task = intel_tasks.crowd_density_task(
                agent, intel_request.destination, date_range, intel_request.interests
            )
        elif intel_request.intelligence_type == "price":
            agent = intel_agents.price_optimization_agent()
            task = intel_tasks.price_optimization_task(
                agent, intel_request.origin, intel_request.destination, 
                date_range, intel_request.interests
            )
        elif intel_request.intelligence_type == "language":
            agent = intel_agents.language_barrier_agent()
            task = intel_tasks.language_barrier_task(
                agent, intel_request.destination, date_range, intel_request.interests
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid intelligence type. Use: risk, crowd, price, language"
            )
        
        crew = Crew(agents=[agent], tasks=[task], verbose=True)
        result = crew.kickoff()
        
        return TripResponse(
            status="success",
            message=f"{intel_request.intelligence_type.title()} analysis completed",
            itinerary=str(result)
        )
    
    except Exception as e:
        return TripResponse(
            status="error",
            message="Failed to run intelligence analysis",
            error=str(e)
        )

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
